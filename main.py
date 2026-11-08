"""一次関数 y = 10x + 5 を計算して返す Web API（Day7 一緒にやってみよう）。

起動:  python -m uvicorn main:app --reload --port 8080
確認:  http://127.0.0.1:8080/calculate?x=3.5  ->  {"result":40.0}
"""
from fastapi import FastAPI

app = FastAPI(title="一次関数API")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/calculate")
async def calculate_y(x: float):
    # x: float と型を書くだけで、数値に変換できない値（?x=abc）や x なしは
    # FastAPI が関数を呼ぶ前に 422 エラーで弾いてくれる（自分で isinstance を書く必要はない）
    y = 10 * x + 5
    return {"result": y}
