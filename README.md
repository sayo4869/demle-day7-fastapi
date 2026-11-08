# demle-day7-fastapi

**FastAPI で小さな Web API を作り、手元のPCと Amazon EC2 の両方で動かす**練習用のコードです。
データミックス DEMLE Day7「クラウドサーバーを使った API 作成入門」の復習用に、自分で書き直しました。

| ファイル | 中身 | 確認するURL | 返ってくる値 |
|---|---|---|---|
| `main.py` | 一次関数 y = 10x + 5 | `/calculate?x=3.5` | `{"result":40.0}` |
| `main2.py` | サーバーのOSとPythonのバージョン | `/os_version`、`/python_version` | `{"os_version":"Linux-6.1…"}` など |
| `main3.py` | 二次関数 y = x² + 2x + 5（宿題・**穴あき**。`y = None` の所に式を書く） | `/calculate?x=3.5` | `{"result":24.25}` |
| `check_api.py` | 起動中のAPIに自動でリクエストして答え合わせ | — | `すべてOK` |

数値以外（`?x=abc`）や `x` なしで呼ぶと、FastAPI が自動で **422** エラーを返します（型ヒント `x: float` の効果）。

---

## 公開してよい情報 / 公開してはいけない情報

このレポジトリは **public** です。

| 区分 | 中身 | このレポジトリ |
|---|---|---|
| ✅ 公開OK | 自分で書き直したコード、README、`requirements.txt`、`.gitignore` | 入れている |
| ✅ 公開OK | 一般的なコマンド（git / ssh / pip / uvicorn） | README に記載 |
| ❌ 公開NG | **EC2のキーペア（`.pem`）** | 入れない（`.gitignore` で除外） |
| ❌ 公開NG | **GitHubのトークン（`ghp_…`）、AWSのアクセスキー、パスワード、`.env`** | 入れない |
| ❌ 公開NG | **自分のEC2のパブリックIPv4 DNS / IP** | README では `ec2-XX-XX-XX-XX…` と伏せ字 |
| ❌ 公開NG | **講座の配布物**（スライド、配布コードそのもの、講義のまとめノート）。「無断複製・転載・配布禁止」 | 入れない |
| ⚠️ 注意 | ポート 8080 を `0.0.0.0/0` に開けると世界中からアクセスできる | 使い終わったらSGのルールを消す |

---

## 1. 手元のPCで動かす

### 1-1. clone と仮想環境

OSでコマンドが違うのは **「仮想環境を有効にする」行**と **python / python3** だけです。

**Mac（ターミナル）**

```bash
cd ~
git clone https://github.com/sayo4869/demle-day7-fastapi.git
cd demle-day7-fastapi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows（Git Bash）**

```bash
cd ~
git clone https://github.com/sayo4869/demle-day7-fastapi.git
cd demle-day7-fastapi
python -m venv .venv
source .venv/Scripts/activate       # Mac と違って Scripts
pip install -r requirements.txt
```

**Windows（PowerShell）**

```powershell
cd ~
git clone https://github.com/sayo4869/demle-day7-fastapi.git
cd demle-day7-fastapi
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> PowerShell で「このシステムではスクリプトの実行が無効になっている」と出たら、一度だけ
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` を実行してから、もう一度 `Activate.ps1`。

有効になるとプロンプトの先頭に `(.venv)` が付きます。仮想環境を有効にしたあとは、**どのOSでも `python` で動きます**。

### 1-2. サーバーを起動する（3つのOS共通）

```bash
python -m uvicorn main:app --reload --port 8080
```

`Uvicorn running on http://127.0.0.1:8080` と出たら起動成功。止めるときは `Ctrl + C`。
`main` を `main2`、`main3` に変えれば、それぞれのAPIが起動します。

### 1-3. 確認する

ブラウザで `http://127.0.0.1:8080/calculate?x=3.5` を開くか、**別のターミナル**で：

**Mac（ターミナル）／ Windows（Git Bash）**

```bash
curl "http://127.0.0.1:8080/calculate?x=3.5"
python check_api.py main http://127.0.0.1:8080     # 自動で答え合わせ（仮想環境を有効にしたターミナルで）
```

**Windows（PowerShell）**

```powershell
Invoke-RestMethod "http://127.0.0.1:8080/calculate?x=3.5"   # PowerShell の curl は別物なので curl.exe か これを使う
python check_api.py main http://127.0.0.1:8080
```

`check_api.py` の出力例：

```
OK  200 GET / -> {"message": "Hello World"}
OK  200 GET /calculate?x=3.5 -> {"result": 40.0}
OK  422 GET /calculate?x=abc -> {"detail": [{"type": "float_parsing", ...
すべてOK
```

`http://127.0.0.1:8080/docs` を開くと、API の説明と「Try it out」で試せる画面が自動でできています。

---

## 2. EC2で動かす

### 2-1. 事前準備（AWS画面）

- EC2（Amazon Linux 2023）を起動し、「パブリック IPv4 DNS」をメモ
- セキュリティグループのインバウンドルールに **カスタムTCP / ポート 8080 / ソース：マイIP**（授業では Anywhere-IPv4）を追加

### 2-2. ログイン

**Mac（ターミナル）／ Windows（Git Bash）**

```bash
cd ~
chmod 400 "First Key pair.pem"
ssh -i "First Key pair.pem" ec2-user@ec2-XX-XX-XX-XX.ap-northeast-1.compute.amazonaws.com
```

**Windows（PowerShell）**

```powershell
cd ~
icacls "First Key pair.pem" /inheritance:r
icacls "First Key pair.pem" /grant:r "$($env:USERNAME):(R)"
ssh -i "First Key pair.pem" ec2-user@ec2-XX-XX-XX-XX.ap-northeast-1.compute.amazonaws.com
```

### 2-3. セットアップと起動（ここから先はEC2の中。OS共通）

```bash
sudo dnf install -y git python3-pip          # 講座の yum install と同じ
cd ~
git clone https://github.com/sayo4869/demle-day7-fastapi.git
cd demle-day7-fastapi
python3 -m pip install --user -r requirements.txt
python3 -m uvicorn main2:app --host 0.0.0.0 --port 8080
```

**`--host 0.0.0.0` を必ず付けます。** 付けないと EC2 自身（127.0.0.1）からしか受け付けず、手元のブラウザからは開けません。

### 2-4. 手元のPCから確認する

ブラウザで `http://ec2-XX-XX-XX-XX.ap-northeast-1.compute.amazonaws.com:8080/os_version` を開きます。
`"os_version":"Linux-…amzn2023…"` と出れば、EC2 で動いています。

手元のターミナルからまとめて確認するなら（`https` ではなく `http`）：

```bash
python check_api.py main2 http://ec2-XX-XX-XX-XX.ap-northeast-1.compute.amazonaws.com:8080
```

### 2-5. コードを直したら（手元 → GitHub → EC2）

```bash
# 手元のPC（Mac / Git Bash / PowerShell 共通）
git add main3.py
git commit -m "update main3"
git push origin main

# EC2（uvicorn を Ctrl+C で止めてから）
cd ~/demle-day7-fastapi
git pull
python3 -m uvicorn main3:app --host 0.0.0.0 --port 8080
```

### 2-6. SSHを閉じても動かし続ける（任意）

```bash
nohup python3 -m uvicorn main3:app --host 0.0.0.0 --port 8080 > uvicorn.log 2>&1 &
pkill -f uvicorn        # 止めるとき
```

### 2-7. 片付け

- EC2：`Ctrl + C` で止める → `exit`
- AWS画面：セキュリティグループから 8080 のルールを削除 → インスタンスを「停止」または「終了」

---

## つまずきポイント

| 症状 | 原因と対処 |
|---|---|
| `Error loading ASGI app. Could not import module "main"` | `main.py` のあるフォルダで起動していない（`ls` で確認） |
| `ModuleNotFoundError: No module named 'fastapi'` | 仮想環境を有効にしていない／`pip install -r requirements.txt` をしていない |
| `[Errno 48] Address already in use` | 8080 を別のプロセスが使っている。前のサーバーを `Ctrl + C` で止めるか `--port 8081` |
| 手元のブラウザからEC2が開けない（タイムアウト） | SGに 8080 がない／`--host 0.0.0.0` を付けていない／URLが `https://` になっている |
| `{"detail":"Not Found"}` | サーバーには届いている。パスの打ち間違い |
| `/os_version/`（末尾 `/` あり）で開いた | FastAPI が 307 で `/os_version` に転送するので、ブラウザでは同じ結果になる |
| PowerShell の `curl` で変な表示 | PowerShell の `curl` は `Invoke-WebRequest` の別名。`curl.exe` か `Invoke-RestMethod` を使う |

---

## 参考

- [FastAPI（日本語）](https://fastapi.tiangolo.com/ja/) ／ [クエリパラメータ](https://fastapi.tiangolo.com/ja/tutorial/query-params/)
- [Uvicorn の設定](https://www.uvicorn.org/settings/)（`--host` `--port` `--reload`）
- [venv（Python 公式）](https://docs.python.org/ja/3/library/venv.html)
