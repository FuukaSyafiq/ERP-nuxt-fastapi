from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.dto.ocr import OcrProcessResponse
from app.modules.ocr.service import OcrService
from app.modules.common.jwt import jwt_bearer
from app.modules.common.error import UnauthorizedError, BadRequestError
from app.core.response import BaseResponse

router = APIRouter()


@router.post("/", response_model=BaseResponse)
async def parse_ocr(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    try:
        user_id = None
        if hasattr(request.state, "user") and request.state.user:
            user_id = request.state.user.get("id")

        file_data = await file.read()
        service = OcrService(db)
        result = await service.process_ocr(file_data, file.filename, user_id)

        return BaseResponse.success_response(
            data=result.model_dump(),
            message="OCR process successful",
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.message)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))