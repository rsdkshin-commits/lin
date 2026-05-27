# 遠端互動通知系統

功能：
- 發送方 / 接收方選擇身分組
- 發送方按需求按鈕
- 多位接收方即時收到通知
- 接收方可回覆狀態
- 雙方收到訊息會有語音通知
- 支援瀏覽器通知 / 手機 PWA 加入主畫面

## 本機啟動

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

打開：

```text
http://127.0.0.1:8000
```

## Render 部署

Start Command：

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Build Command：

```bash
pip install -r requirements.txt
```

## 使用方式

1. 發送方手機或電腦打開網址，選「我是發送方」
2. 接收方多人打開同一個網址，選「我是接收方」
3. 每個人先按一次「開啟通知」
4. 發送方按按鈕，接收方即時收到
5. 接收方按回覆，發送方即時收到
