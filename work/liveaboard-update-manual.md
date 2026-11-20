# 斯米蘭船宿＋曼谷行程頁 — 自動更新工作手冊

版本：2026-11-20　｜　適用：Richelieu / Similan 船宿比價頁（2 人、雙人房、Nitrox、每人 TWD 價格）

---

## 0. 一句話總覽

每 6 小時（台北時間 02:00 / 08:00 / 14:00 / 20:00）跑一次：

1. 用瀏覽器抓**船位與船價**（liveaboard.com）
2. 用瀏覽器抓**國內線單程票價**（Google Flights，曼谷⇄普吉）
3. 用瀏覽器抓**國際線來回票價**（Google Flights，台北⇄曼谷）
4. 把數字寫進 JSON → 用 Python 重建 HTML
5. 推到 **GitHub Pages** 和 **Claude artifact**
6. 用中文訊息**推播報告給你**，並**預約下一次執行**

---

## 1. 成品放在哪裡

| 成品 | 位置 |
|---|---|
| 公開網站 | https://c10213133.github.io/test/ （repo：`c10213133/test`，檔案 `index.html`） |
| Claude artifact | slug `80b36b68-1926-439d-b9b8-d517ff60322d`（Richelieu Liveaboard + Bangkok） |
| 離線打包 | `/home/claude/liveaboard-site.zip` |
| 最終 HTML | `/home/claude/thailand-liveaboard-plan.html` |

---

## 2. 執行環境（三個部分）

1. **雲端工作區**（Linux，`/home/claude/`）：放 Python 腳本、JSON 資料、git repo，負責組 HTML、推送。
2. **你電腦上的 Claude 桌面 App 內建瀏覽器**（透過 device bridge 連線）：負責真的去開網頁抓價格。
   - 分頁 `seed` = liveaboard.com（抓船位）
   - 分頁 `tab-1` = Google Flights（抓機票）
   - ⚠️ **電腦睡眠／App 關閉時，瀏覽器工具就消失，那一次更新只能跳過**（例如 11/20 08:00 那次）。
3. **排程**：用 `send_later` 一次只排「下一次」，每次跑完再排下一次（鏈式排程）。

---

## 3. 檔案清單（`/home/claude/work/`）

| 檔案 | 用途 |
|---|---|
| `RUN_NOTES.txt` | **每次執行必讀**的操作備忘與覆寫規則、最新 artifact 版本號 |
| `updates.json` | 本次抓到的資料：`flights`（單程票價）、`cabins`（船價/剩餘床位）、`remove`（已滿要下架的船）。它的修改時間 = 網頁右上角「Updated」時間 |
| `data.py` | 原始行程資料（每艘船的日期、船價、國內線、時間軸） |
| `patch.py`～`patch4.py` | 歷史修補（保留不動） |
| `patch_auto.py` | 把 `updates.json` 的票價／船價套進資料、移除 FULL 的船 |
| `patch_ny.py` | 新年檔＋聖誕檔：國際線取 `rt_ny.json`／`rt_xmas.json` 的 cur 列；國內線班次、時間軸、下水後小時數 |
| `patch_dj.py` | 12 月檔＋1 月檔：國際線取 `rt_dec.json`／`rt_jan.json` 的 cur 列；國內線班次 |
| `gen.py` | 產生每個分頁的船卡片、比較表（含 `BUILT` 下水/翻新年份） |
| `rtny.py` | 產生每個分頁的「國際線來回比價表」（⭐標最便宜的全服務航空） |
| `assemble.py` | 組裝四個分頁 + 「也查過但已滿」表格（`add_rows`） |
| `finish.py` | 套上最終版型（hero 圖、相簿、右上角更新時間）→ 寫出最終 HTML |
| `gen_batches.py` | 依目前頁面實際使用的國內線，自動產生 `flight_batches.json` |
| `flight_batches.json` | 國內線抓價的瀏覽器批次指令（目前 2 批、9 頁） |
| `rt_batch.json` | 國際線來回抓價的瀏覽器批次指令（41 個動作） |
| `rt_ny/xmas/dec/jan.json` | 各分頁國際線候選列：`k`(查價 key)、`air`、`out`、`ret`、`price`、`adj`(校正值)、`ok`(可用)、`cur`(目前採用) |
| `rt_apply.py` | 把抓到的來回價套進四個 rt 檔，自動挑最便宜的 ok 列當 cur |

---

## 4. 瀏覽器端的小工具（存在 Google / liveaboard 的 localStorage）

這些 JS 小函式事先存在瀏覽器 localStorage，每次用 `eval(localStorage.XXX)` 呼叫：

| 名稱 | 所在網域 | 作用 |
|---|---|---|
| `CABL` | liveaboard.com | 要查的船清單：`[tab, 船名, boatid, tourid, 房型關鍵字]` |
| `CABRUN` | liveaboard.com | 逐一 fetch `/BookingStep1?tourid=…&boatid=…`，用正規表示式找房型列：`房型 N People … NT$ 價格 / Person (FULL / only N spaces left! / Select)`，結果放 `window._CJ`，完成時 `window._ckd=true`。每艘間隔 1.3 秒避免被擋 |
| `CK2(from,to,date,[出發時刻])` | google.com | 在已打開的 Google Flights 單程頁，讀指定出發時刻的票價，寫入 `localStorage.FRES`，並回報當天最便宜班次 |
| `OW` | google.com | 列出整頁單程班次（航空、起降時間、價格），用來找替代班機 |
| `RTJ(key)` | google.com | 在 Google Flights 來回頁讀每家航空每個去程時刻的「來回總價起」，寫入 `localStorage.RTRES`，key 格式 `前綴|日期|日期|航空|HH:MM` |

> 注意：Google 的來回「起價」是**任何回程**的最低價，可能是混搭航空。所以每個 rt 列有 `adj` 校正值（同一家航空來回的實價 − 起價），透過「點進去去程、讀回程的 aria-label『來回總價 …』」驗證得到。

---

## 5. 每次執行的標準步驟

### 步驟 1：開始抓船位（背景執行）
在 `seed` 分頁執行：
```js
window._ckd=false; eval(localStorage.CABRUN)
```

### 步驟 2：國內線單程（tab-1）
1. `localStorage.FRES='{}'` 清空
2. 跑完 `flight_batches.json` 裡**所有**批次（每頁：navigate → 等 4 秒 → `CK2(...)`）
3. 最後讀出 FRES（過濾掉 `MIN` 開頭的 key），存成 `/tmp/fres.json`，合併進 `updates.json` 的 `flights`

**漲價處理規則**（見第 7 節航班規則）：使用中的班次大漲時，用 `OW` 列出當天所有班次，找「時間可行、且比較便宜」的替代班次 → 修改 `patch_ny.py` / `patch_dj.py` 對應那一行 → 執行 `python3 gen_batches.py`。

### 步驟 3：國際線來回（tab-1）
1. `localStorage.RTRES='{}'`
2. `rt_batch.json` 分 4 次呼叫執行：`[0:13]`、`[13:25]`、`[25:37]`、`[37:41]`（瀏覽器批次有 50 秒上限，一次最多約 4 個來回頁）
3. 最後一個動作回傳過濾後的 RTRES JSON → 存 `/tmp/rtres.json`
4. `python3 rt_apply.py`
   - 印出 `RT ... 舊價 -> 新價`
   - 若最便宜可用列換人，印出 `SWITCH from ... to ...`
5. **任何分頁 cur 列變動 > 500 元 → 必須點進去驗證**同航空來回實價，修正 `adj`（或把新候選設 `ok:true`）後再跑一次 `rt_apply.py`
   - 點擊技巧：截圖是 800×600，但網頁 CSS 是 1024×768，要用**截圖座標**點

### 步驟 4：船位結果
讀 `window._CJ`（`_ckd` 為 true 才算完成），整包寫入 `updates.json` 的 `cabins`。
- 新出現 **FULL** → 加進 `updates.json` 的 `remove`（格式 `tab|船名`），並在 `assemble.py` 對應的 `add_rows(...)` 加一列「已滿（日期）」
  - 分頁對應：`also4`=12月、`also`=聖誕、`also2`=新年、`also3`=1月
- 可疑情況（例如一次全部房型 FULL）→ 再單獨 fetch 一次確認

### 步驟 5：重建 HTML
```bash
cd /home/claude/work && cp *.py *.json *.html /tmp/
cd /tmp && python3 assemble.py && python3 finish.py
grep -c tagline /home/claude/thailand-liveaboard-plan.html   # 要 >0
```
⚠️ **finish.py 一定最後跑**；跑完不要再跑 assemble.py（會蓋掉最終版型）。
assemble 會印出每個分頁的每人總價，報告用得到。

### 步驟 6：發佈
```bash
cd /home/claude
cp thailand-liveaboard-plan.html test/index.html
cp thailand-liveaboard-plan.html liveaboard-site/index.html
cp thailand-liveaboard-plan.html artifact/index.html
rm -f liveaboard-site.zip && zip -qr liveaboard-site.zip liveaboard-site
cd test && git add -A && \
git -c user.name=c10213133 -c user.email=noreply@users.noreply.github.com \
  commit -qm "Auto-update <日期 時間>

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01MPefaRscBk9HS82iGK5obW" && \
git -c push.negotiate=true push
```
Artifact：`publish_files`（slug 如上、`base_version` = RUN_NOTES 裡記的最新版號、檔案 `/home/claude/artifact/index.html` as `index.html`），成功後把新版號寫回 `RUN_NOTES.txt`。

### 步驟 7：推播給你
用 **SendUserMessage**（會推到你手機的 Claude App）送一則繁體中文短報告，內容固定包含：
- 新滿房的船
- 價格變動 > 100 元的項目
- 換了哪些班機（原因）
- 各分頁每人總價

### 步驟 8：預約下一次
`send_later`，時間 = 本次 + 6 小時（例：`2026-11-20T14:00:00[Asia/Taipei]`），訊息內容 = 同一段排程指令（日期往後推）。
- 若瀏覽器連不上：跳過抓價、通知你、**照樣排下一次**。

---

## 6. 目前各分頁採用的方案（2026-11-20 02:00）

| 分頁 | 國際線（同一家航空來回） | 國內線重點 |
|---|---|---|
| 12月（12/18–12/28） | 華航 12/18 22:30 去、12/28 02:35 回 | Bavaria：VJ 12/19 06:50 去、VJ 12/23 21:30 回 |
| 聖誕（12/24–1/4） | 華航 12/24 22:30 去、1/4 02:35 回（19,457） | Bunmee 4：VJ 12/25 19:20 去、VJ 1/3 19:40 回 |
| 新年（12/31–1/11） | 華航 12/31 10:05 去、1/11 回（13,969） | VJ 12/31 18:45 去、AA 1/9 22:20 回 |
| 1月（1/8–1/18） | 華航 1/8 22:30 去、1/18 02:35 回（9,935） | AA 1/9 或 1/10 07:45 去、AA 1/16 14:30 回 |

已下架（滿房）：Dolphin Queen（12月、聖誕全部房型）、MQ2/Gentle Giant（12月）、Sawasdee Fasai（聖誕）、MQ8/Pawara（新年）、Pawara（1月）。

---

## 7. 選班機規則（你訂的）

**國際線**
- 一定要**同一家航空來回**；優先選長榮／華航裡最便宜、時間符合的
- 去程只能「前一天晚上或當天早上」：
  - 12月：12/18 晚或 12/19 早
  - 聖誕：12/24 晚或 12/25 早
  - 新年：12/30 晚或 12/31 早，**不能 12/31 下午之後起飛（不要跨年在飛機上）**
  - 1月：1/8 晚或 1/9 早
- 回程要趕得上週一上班；紅眼班機可以

**國內線（曼谷⇄普吉）**
- 選時間可行中最便宜的
- 最後一潛到起飛 **≥ 24 小時**
- 在普吉多待幾天沒關係
- 分開買單程若比較便宜就分開買（實測 LCC 來回價 = 兩張單程相加）
- 回程落地轉國際線至少要留約 3 小時（太趕的不換）

---

## 8. 常見狀況排除

| 狀況 | 處理 |
|---|---|
| 瀏覽器工具不見 | 電腦睡眠／App 關閉 → 本次跳過、通知、照排下一次 |
| 瀏覽器分頁被關 | `navigate https://www.liveaboard.com/`（開出 seed）→ `tabs_create`（開出 tab-1）；localStorage 小工具會保留 |
| browser_batch 逾時 | 拆小批，每批 ≤ 4 個來回頁 |
| 來回價突然跳很多 | 可能是 Google 暫時性報價，點進去驗證後修 `adj` |
| `NOPATCH` / `unused` 警告 | 舊 patch 找不到舊班次，已由 patch_ny/patch_dj 覆寫，可忽略 |
| artifact 發佈衝突 | 用 `get_artifact` 取最新版號再發佈 |

---

## 9. 若要搬到別的環境自己跑

1. 複製 `/home/claude/work/`、`/home/claude/test/`（git repo）、`/home/claude/tpl3/`（版型）、`backup_before_rebuild.html`
2. 準備一個能執行 JS 的瀏覽器自動化（Playwright 等），把第 4 節的 localStorage 小工具改寫成腳本
3. 用 cron 每 6 小時跑第 5 節步驟 1–6
4. 推播可改用 LINE Notify／Email／Telegram bot 取代 SendUserMessage
