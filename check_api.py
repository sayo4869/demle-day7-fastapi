"""起動中のAPIにリクエストを送って、期待どおりの答えが返るかを確かめるスクリプト（標準ライブラリだけで動く）。

使い方（別のターミナルでサーバーを起動しておく）:
    python check_api.py main  http://127.0.0.1:8080
    python check_api.py main2 http://127.0.0.1:8080
    python check_api.py main3 http://ec2-XX-XX-XX-XX.ap-northeast-1.compute.amazonaws.com:8080
"""
import json
import sys
import urllib.error
import urllib.request

CASES = {
    "main": [("/", 200, {"message": "Hello World"}), ("/calculate?x=3.5", 200, {"result": 40.0}),
             ("/calculate?x=abc", 422, None)],
    "main2": [("/os_version", 200, None), ("/python_version", 200, None)],
    "main3": [("/calculate?x=3.5", 200, {"result": 24.25}), ("/calculate?x=-1", 200, {"result": 4.0}),
              ("/calculate?x=abc", 422, None)],
}


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())
    except urllib.error.URLError as e:
        print(f"つながりません: {url}\n  → サーバーが起動しているか、URL・ポート・セキュリティグループ（EC2）を確認してください（{e.reason}）")
        sys.exit(2)


def main():
    app, base = sys.argv[1], sys.argv[2].rstrip("/")
    ok = True
    for path, want_status, want_body in CASES[app]:
        status, body = get(base + path)
        good = status == want_status and (want_body is None or body == want_body)
        ok &= good
        print(f"{'OK ' if good else 'NG '} {status} GET {path} -> {json.dumps(body, ensure_ascii=False)[:120]}")
    print("すべてOK" if ok else "期待と違う結果があります")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
