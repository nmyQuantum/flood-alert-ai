from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class Report(BaseModel):
    text: str

@app.post("/analyze")
def analyze(report: Report):
    prompt = f"""Bạn là hệ thống phân tích rủi ro ngập lụt. Đọc báo cáo sau và trả về CHÍNH XÁC định dạng JSON, không thêm chữ nào khác:
{{"risk": "Thấp/Trung bình/Cao", "advice": "1-2 câu khuyến nghị hành động cụ thể bằng tiếng Việt"}}

Báo cáo: {report.text}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    result = json.loads(message.content[0].text)
    return result