# liveaboard-work（工作檔分支）

這個 `work` 分支是「斯米蘭船宿＋曼谷」比價頁的完整工作檔。網站本身在 `main` 分支（GitHub Pages：https://c10213133.github.io/test/）。
完整流程請看 **MANUAL.md**。

## 目錄
- `work/`：Python 腳本、資料 JSON、`RUN_NOTES.txt`（最新狀態與規則）、`rt_batch.json` / `flight_batches.json`（原本的瀏覽器批次指令，可當作要抓哪些頁面的清單）
- `tpl3/`：最終版型（`finish.py` 使用）
- `backup_before_rebuild.html`：`assemble.py` 的底稿
- `thailand-liveaboard-plan.html`：最近一次產出的頁面

## 放到 server 上（腳本寫死 /home/claude 路徑）
```bash
git clone -b work https://github.com/c10213133/test.git ~/liveaboard-work
sudo mkdir -p /home/claude && sudo chown $USER /home/claude
cp -r ~/liveaboard-work/* /home/claude/
git clone -b main https://github.com/c10213133/test.git /home/claude/test     # 推網站用
mkdir -p /home/claude/liveaboard-site && cp /home/claude/tpl3/liveaboard-site/* -r /home/claude/liveaboard-site/ 2>/dev/null
pip install playwright && playwright install --with-deps chromium
gh auth login     # 或設定 git credential，讓 /home/claude/test 能 push
```
（不想用 /home/claude，也可以用 `grep -rl /home/claude work | xargs sed -i "s#/home/claude#$HOME/lb#g"` 改路徑。）

## server 上要重寫的部分（原本靠 Mac 的 Claude 瀏覽器 localStorage 小工具）
用 Playwright（headless Chromium，locale zh-TW）實作，輸出格式跟原本相同：

1. **船位 `cabins`** → 寫入 `work/updates.json` 的 `cabins`：`{"tab|船名":[每人NT$價格, "FULL"|"N"]}`
   - 方法：開 `https://www.liveaboard.com/BookingStep1?tourid=<tourid>&boatid=<boatid>`（幣別 TWD），讀頁面文字，
     用正規式 `([A-Z][A-Za-z0-9/ -]{2,40}?) (\d) People (.{0,70}?) (?:Save \d+% NT\$ [\d,]+ )?NT\$ ([\d,]+) / Person (FULL|only (\d) spaces? left!|Select)` 找到對應房型（`cabinname` 關鍵字）。
   - tourid/boatid：原本存在 Mac 瀏覽器的 `CABL`，這裡沒有；可從 `https://www.liveaboard.com/diving/thailand/<slug>` 的出發日按鈕連結取得（slug 見 `work/data.py`）。
2. **國內線單程 `flights`** → `updates.json` 的 `flights`：`{"FROM|TO|YYYY-MM-DD|HH:MM": 價格}`
   - 頁面：`https://www.google.com/travel/flights?q=Flights%20from%20BKK%20to%20HKT%20on%20<date>%20one%20way&curr=TWD&hl=zh-TW&gl=TW`
   - 讀每個結果 `li` 的 `aria-label`（含「新台幣起」、航空公司、起降時間），取指定出發時刻的價格。要抓哪些：看 `work/flight_batches.json`，或跑 `python3 work/gen_batches.py`。
   - 也可改用 `pip install fast-flights`。
3. **國際線來回** → 產生 `/tmp/rtres.json`：`{"<key>": 來回起價}`，key = `前綴|去程日|回程日|航空中文名|HH:MM`（見 `work/rt_*.json` 的 `k`），再跑 `python3 work/rt_apply.py`。
   - 注意：Google 的來回「起價」可能混搭航空，所以每列有 `adj` 校正值。cur 列變動 >500 時，要點進去去程，讀回程 aria-label 的「來回總價」確認同一家航空的實價。

## 每次執行
見 MANUAL.md 第 5 節（組頁：`cp work/*.py work/*.json work/*.html /tmp && cd /tmp && python3 assemble.py && python3 finish.py`，再複製到 `/home/claude/test/index.html` 並 push）。
