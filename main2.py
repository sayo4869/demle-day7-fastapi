"""サーバーのOSとPythonのバージョンを返す Web API（Day7 EC2でAPIを動かす）。

手元:  python -m uvicorn main2:app --reload --port 8080
EC2 :  python3 -m uvicorn main2:app --host 0.0.0.0 --port 8080
確認:  /os_version  /python_version
"""
import platform
import sys

from fastapi import FastAPI

app = FastAPI(title="バージョン確認API")


@app.get("/os_version")
async def get_os_version():
    return {"os_version": platform.platform()}


@app.get("/python_version")
async def get_python_version():
    v = sys.version_info
    return {"python_version": f"{v.major}.{v.minor}.{v.micro}"}
