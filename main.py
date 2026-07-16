from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class Report(BaseModel):
    text: str

@app.post("/analyze")
def analyze(report: Report):
    prompt = f"""Bạn là hệ thống phân tích rủi ro ngập lụt. Đọc báo cáo sau và trả về CHÍNH XÁC định dạng JSON, không thêm chữ nào khác:
{{"risk": "Thấp/Trung bình/Cao", "advice": "1-2 câu khuyến nghị hành động cụ thể bằng tiếng Việt"}}

Báo cáo: {report.text}"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    result = json.loads(completion.choices[0].message.content)
    return result