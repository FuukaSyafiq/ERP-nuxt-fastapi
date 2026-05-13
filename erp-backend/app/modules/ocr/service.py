from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Optional
import os
import requests
from io import BytesIO
from decimal import Decimal

from app.models.models import Session as SessionModel, Item, Sale
from app.dto.ocr import OcrProcessResponse, OcrItemResponse
from app.modules.common.error import AppError, BadRequestError, InternalServerError, UnauthorizedError


class OcrService:
    def __init__(self, db: Session):
        self.db = db
        self.AI_API_KEY = os.getenv("AI_API_KEY")
        self.AI_API_URL = os.getenv("AI_API_URL")

        if not self.AI_API_KEY:
            raise UnauthorizedError("AI_API_KEY is not configured.")
        if not self.AI_API_URL:
            raise UnauthorizedError("AI_API_URL is not configured.")

    async def process_ocr(self, file_data: bytes, filename: str, user_id: Optional[str] = None) -> OcrProcessResponse:
        if not file_data:
            raise BadRequestError("No file provided for OCR.")

        from app.modules.common.ai import AiService

        try:
            files = {"image": (filename, file_data)}
            data = {"invoice": "false", "language": "auto"}

            response = requests.post(
                self.kolosal_api_url,
                files=files,
                data=data,
                headers={"Authorization": f"Bearer {self.AI_API_KEY}"},
                timeout=30,
            )
            response.raise_for_status()
            ocr_result = response.json()

        except requests.RequestException as e:
            raise InternalServerError(f"Failed to process OCR request: {str(e)}")

        raw_text = self._extract_text(ocr_result)

        from app.modules.common.ai import AiService
        ai_service = AiService()

        try:
            parsed_nota = await ai_service.normalize_ocr_data(raw_text)
            if not parsed_nota.get("items") or len(parsed_nota["items"]) == 0:
                parsed_nota = self._parse_with_regex(raw_text)
        except Exception:
            parsed_nota = self._parse_with_regex(raw_text)

        if not parsed_nota.get("items") or len(parsed_nota["items"]) == 0:
            raise BadRequestError("No items found in the receipt.")

        if not parsed_nota.get("total") or parsed_nota["total"] <= 0:
            raise BadRequestError("Invalid total amount in the receipt.")

        total = parsed_nota["total"]
        profit = total * 0.2
        profit_margin = (profit / total) * 100 if total > 0 else 0

        session_model = SessionModel(
            userId=user_id,
            rawText=parsed_nota.get("rawText", raw_text),
        )
        self.db.add(session_model)
        self.db.flush()

        items = []
        for item_data in parsed_nota["items"]:
            qty = item_data.get("qty", 1)
            price = item_data.get("price", 0)
            unit_price = price / qty if qty > 0 else price

            item = Item(
                sessionId=session_model.id,
                name=item_data.get("name", "Unknown"),
                qty=qty,
                unitPrice=Decimal(str(unit_price)),
                subtotal=Decimal(str(price)),
            )
            self.db.add(item)
            items.append(item)

        sale = Sale(
            sessionId=session_model.id,
            totalAmount=Decimal(str(total)),
            profit=Decimal(str(profit)),
            profitMargin=Decimal(str(profit_margin)),
        )
        self.db.add(sale)
        self.db.flush()

        self.db.commit()

        try:
            insights_result = await ai_service.analyze_receipt(
                raw_text,
                [{"name": item.name, "qty": item.qty, "price": float(item.subtotal)} for item in items],
            )
        except Exception:
            insights_result = {"insights": "", "suggestions": []}

        return OcrProcessResponse(
            items=[
                OcrItemResponse(name=item.name, qty=item.qty, price=float(item.subtotal))
                for item in items
            ],
            total=float(total),
            profit=float(profit),
            summary={
                "insights": insights_result.get("insights", ""),
                "suggestions": insights_result.get("suggestions", []),
            },
        )

    def _parse_with_regex(self, text: str) -> dict:
        import re
        lines = text.split("\n")
        items = []
        total = 0

        item_regex = r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*([^|]+?)\s*\|\s*([\d.,]+)\s*\/[^|]+\|\s*Rp([\d.,]+)"

        for line in lines:
            match = re.match(item_regex, line)
            if match:
                name = match.group(2).strip()
                qty = int(match.group(3).strip())
                total_price = float(match.group(6).replace(".", "").replace(",", ""))

                if not name or "nama" in name.lower() or name == "---":
                    continue

                items.append({"name": name, "qty": qty, "price": total_price})
            elif "jumlah" in line.lower() or "total" in line.lower():
                total_match = re.search(r"Rp([\d.,]+)", line)
                if total_match:
                    extracted_total = float(total_match.group(1).replace(".", "").replace(",", ""))
                    if extracted_total > 0:
                        total = max(total, extracted_total)

        if total == 0 and len(items) > 0:
            total = sum(item["price"] for item in items)

        return {"items": items, "total": total, "rawText": text}

    def _extract_text(self, ocr_result) -> str:
        if isinstance(ocr_result, str):
            return ocr_result
        if isinstance(ocr_result, dict):
            if "extracted_text" in ocr_result:
                return ocr_result["extracted_text"]
            if "data" in ocr_result and isinstance(ocr_result["data"], dict):
                if "text" in ocr_result["data"]:
                    return ocr_result["data"]["text"]
            if "text" in ocr_result:
                return ocr_result["text"]
        if isinstance(ocr_result, list):
            return "\n".join([self._extract_text(item) for item in ocr_result if isinstance(item, dict) and "text" in item])
        return ""