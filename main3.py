"""二次関数 y = x^2 + 2x + 5 を計算して返す Web API（Day7 宿題・穴あき）。

起動:  python -m uvicorn main3:app --reload --port 8080
確認:  http://127.0.0.1:8080/calculate?x=3.5  ->  {"result":24.25}
"""
from fastapi import FastAPI

app = FastAPI(title="二次関数API")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/calculate")
async def calculate_y(x: float):
    # 数値以外は FastAPI が 422 で返す（main.py と同じ）

    # TODO: 二次関数 y = x^2 + 2x + 5 を計算する式を書く（宿題）
    #       書けたら python check_api.py main3 http://127.0.0.1:8080 で答え合わせ
    y = None
    return {"result": y}
