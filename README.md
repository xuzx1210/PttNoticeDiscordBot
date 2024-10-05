設定：

-   `touch .env`
-   把機器人 `TOKEN` 填入 `.env`
-   把目標 DC 頻道 ID 填入 `channels.txt`
-   調整 `arguments.py` 的看板、分類、間隔時間

python 虛擬環境：

-   `python -m venv .venv`
-   `source .venv/bin/activate`
-   `pip install -r requirements.txt`

執行：

-   `python notice.py`
