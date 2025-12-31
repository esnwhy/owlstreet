# OwlStreet MVP (Nasdaq 100 × 日本語) — Windows + GitHub ひな形

これは **Nasdaq 100の銘柄一覧** と **SEC EDGAR (提出書類・XBRL)** を使って、Peragaru風の「米国株DB」サイトを作るための最小構成です。

> ✅ まずはAPIだけ動かすMVP（フロントは後で）  
> ✅ Windowsで迷いにくいPowerShellスクリプト付き  
> ✅ GitHubにそのまま上げられる構成（.gitignore同梱）

---

## 0) 事前準備
- Windows 10/11
- Python 3.11+ 推奨
- Git（GitHub DesktopでもOK）

---

## 1) セットアップ（最短）
PowerShellでこのフォルダに移動して実行:

```powershell
./setup_windows.ps1
```

---

## 2) データ更新（Nasdaq100 + SEC ticker→CIK）
```powershell
./update_data.ps1
```

生成されるファイル:
- `data/nasdaq100.json`
- `data/sec_ticker_cik.json`

---

## 3) API起動
```powershell
./run_api.ps1
```

### 動作確認URL
- Nasdaq100一覧: http://127.0.0.1:8000/api/universe/nasdaq100
- 例: AAPL詳細: http://127.0.0.1:8000/api/ticker/AAPL

---

## 4) SEC User-Agent（重要）
SECは User-Agent の明記を推奨しています（連絡先メールなど）。  
`.env.example` を `.env` にコピーして、自分のメールに書き換えてください。

例:
```
SEC_USER_AGENT=OwlStreet/0.1 (contact: your_email@example.com)
```

---

## GitHubに上げる（コマンド派）
```powershell
git init
git add .
git commit -m "Initial OwlStreet MVP (Nasdaq100 + SEC API)"
```

GitHubで新規Repoを作ってから:
```powershell
git branch -M main
git remote add origin https://github.com/<yourname>/owlstreet.git
git push -u origin main
```

---

## 次に作るもの（フロント）
- `/tickers`（検索・絞り込み）
- `/ticker/[symbol]`（会社情報・提出書類・財務ハイライト）

必要なら、Next.jsのフロント一式もこのテンプレに追加して渡します。
