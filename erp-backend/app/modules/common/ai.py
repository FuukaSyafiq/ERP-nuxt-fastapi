import os
import re
import json
from typing import List, Dict, Any, Optional
import openai


class AiService:
    def __init__(self):
        api_key = os.getenv("KOLOSAL_API_KEY")
        base_url = os.getenv("KOLOSAL_BASE_URL")

        if not api_key or not base_url:
            raise ValueError("KOLOSAL_API_KEY and KOLOSAL_BASE_URL must be configured")

        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = "qwen/qwen3-vl-30b-a3b-instruct"

    async def generate_completion(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        content = response.choices[0].message.content or ""
        return content

    async def normalize_ocr_data(self, raw_text: str) -> dict:
        escaped_text = raw_text.replace("{", "{{").replace("}", "}}")
        prompt = f'''You are an expert receipt parser. Extract item details from the following raw text from an OCR scan of a receipt.
The text is from an Indonesian receipt.

Raw Text:
"""
{escaped_text}
"""

You MUST respond with ONLY a valid JSON object in the following format. Do not include any other text, explanations, or markdown.
The JSON object should contain 'items' (an array of objects with 'name', 'qty', and 'price') and 'total' (a number).
- "name" should be a string.
- "qty" should be a number.
- "price" should be the total price for that line item as a number, not the unit price.
- "total" should be the grand total of the receipt. If not found, calculate it from the sum of item prices.

Example response:
{{
  "items": [
    {{ "name": "PRO MIE INSTAN", "qty": 3, "price": 7500 }},
    {{ "name": "BIMOLI MINYAK", "qty": 1, "price": 25000 }}
  ],
  "total": 32500
}}
'''
        result = await self.generate_completion(prompt, 1000, 0.2)
        cleaned = result.strip().replace("```json", "").replace("```", "")

        match = re.search(r'\{[\s\S]*?\}', cleaned)
        if match:
            parsed = json.loads(match.group())
            if "items" in parsed and "total" in parsed:
                return {"items": parsed["items"], "total": parsed["total"], "rawText": raw_text}

        return {"items": [], "total": 0, "rawText": raw_text}

    async def generate_pricing_recommendation(
        self, item_name: str, current_price: float, sales_data: dict, target_margin: float
    ) -> dict:
        price_formatted = f"{current_price:,.0f}"
        revenue_formatted = f"{sales_data.get('total_revenue', 0):,.0f}"
        total_qty = sales_data.get('total_qty', 0)
        frequency = sales_data.get('frequency', 0)

        prompt = f'''You are a pricing expert for Indonesian MSMEs (small businesses/warungs).

Item: {item_name}
Current Average Price: Rp {price_formatted}
Sales Data:
- Total Quantity Sold: {total_qty} units
- Total Revenue: Rp {revenue_formatted}
- Number of Transactions: {frequency}
Target Profit Margin: {target_margin}%

IMPORTANT: You MUST respond with ONLY a valid JSON object, nothing else. No explanations before or after.

Provide a recommended selling price and reasoning in this EXACT JSON format:
{{
  "recommended_price": 15000,
  "reasoning": "Your reasoning here"
}}

Do not include any text before or after the JSON object.'''

        response = await self.generate_completion(prompt, 500, 0.3)
        cleaned = response.strip().replace("```json", "").replace("```", "")

        first_brace = cleaned.find("{")
        last_brace = cleaned.rfind("}")

        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_str = cleaned[first_brace : last_brace + 1]
            parsed = json.loads(json_str)
            if "recommended_price" in parsed and "reasoning" in parsed:
                return {
                    "recommended_price": round(parsed["recommended_price"]),
                    "reasoning": parsed["reasoning"],
                }

        fallback_price = round(current_price * (1 + target_margin / 100))
        return {
            "recommended_price": fallback_price,
            "reasoning": f"Fallback calculation: {target_margin}% markup on current price of Rp {price_formatted}",
        }

    async def analyze_receipt(self, raw_text: str, items: List[Dict[str, Any]]) -> dict:
        items_parts = []
        for item in items:
            name = item.get('name', 'Unknown')
            qty = item.get('qty', 0)
            price = item.get('price', 0)
            price_fmt = f"{price:,.0f}"
            items_parts.append(f"- {name}: {qty}x @ Rp {price_fmt}")

        items_str = "\n".join(items_parts)
        prompt = f'''You are an AI assistant for Indonesian warung (small shop) owners.

Analyze this receipt:
Raw Text: {raw_text}

Parsed Items:
{items_str}

IMPORTANT: You MUST respond with ONLY a valid JSON object, nothing else.

Provide business insights and suggestions in this EXACT JSON format:
{{
  "insights": "Your insights here",
  "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}}

Do not include any text before or after the JSON object.'''

        response = await self.generate_completion(prompt, 800, 0.7)
        return {"insights": response[:500], "suggestions": []}

    async def generate_market_insights(self, top_items: List[Dict[str, Any]], sales_summary: dict) -> str:
        items_parts = []
        for i, item in enumerate(top_items[:5]):
            name = item.get('name', 'Unknown')
            total_qty = item.get('total_qty', 0)
            revenue = item.get('total_revenue', 0)
            frequency = item.get('frequency', 0)
            revenue_fmt = f"{revenue:,.0f}"
            items_parts.append(f"{i+1}. {name} - {total_qty} units, Rp {revenue_fmt} revenue, {frequency} transactions")

        items_str = "\n".join(items_parts)

        total_sales = sales_summary.get('total_sales', 0)
        total_profit = sales_summary.get('total_profit', 0)
        avg_margin = sales_summary.get('avg_profit_margin', 0)
        tx_count = sales_summary.get('transaction_count', 0)

        sales_fmt = f"{total_sales:,.0f}"
        profit_fmt = f"{total_profit:,.0f}"

        prompt = f'''You are a business analyst for Indonesian MSMEs.

Sales Summary:
- Total Sales: Rp {sales_fmt}
- Total Profit: Rp {profit_fmt}
- Average Profit Margin: {avg_margin}%
- Total Transactions: {tx_count}

Top Selling Items:
{items_str}

Provide comprehensive market insights and strategic recommendations for this warung owner in Indonesian context. Focus on:
1. Sales performance analysis
2. Product mix optimization
3. Pricing strategy
4. Growth opportunities

Keep it concise and actionable (max 300 words).'''

        return await self.generate_completion(prompt, 1000, 0.7)