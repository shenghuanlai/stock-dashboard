# =========================
# 🚀 How to Run (本機執行方式)
# =========================
# cd Desktop\stock_app
# streamlit run app.py
#
# 💡 開發小提醒：
# - 修改程式後按 Ctrl + S 會自動刷新
# - 若沒有刷新，按 R 或重新整理頁面
# - 若出錯，Ctrl + C 停止後重新執行
# =========================

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import math
import os
import gspread
from google.oauth2.service_account import Credentials

# =========================
# 網頁基本設定
# =========================
st.set_page_config(
    page_title="股票加碼計畫",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =========================
# CSS：黑底 iOS Health 風格
# =========================
st.markdown(
    """
<style>
.stApp {
    background: #000000;
    color: #F5F5F7;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    max-width: 760px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

.top-title {
    font-size: 2.3rem;
    font-weight: 900;
    color: #F5F5F7;
    margin-bottom: 0.2rem;
}

.top-subtitle {
    font-size: 0.95rem;
    color: #8E8E93;
    margin-bottom: 1.4rem;
}

.section-title {
    font-size: 1.55rem;
    font-weight: 850;
    color: #F5F5F7;
    margin-top: 1.4rem;
    margin-bottom: 0.8rem;
}

.summary-card {
    background: #1C1C1E;
    border-radius: 24px;
    padding: 18px;
    margin-bottom: 24px;
    border: 1px solid rgba(255,255,255,0.06);
}

.mini-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.mini-item {
    background: #2C2C2E;
    border-radius: 18px;
    padding: 14px;
}

.mini-label {
    font-size: 0.88rem;
    margin-bottom: 0.35rem;
    font-weight: 800;
}

.label-blue { color: #0A84FF; }
.label-green { color: #30D158; }
.label-orange { color: #FF9F0A; }
.label-pink { color: #FF2D55; }

.mini-value {
    color: #F5F5F7;
    font-size: 1.75rem;
    font-weight: 900;
    line-height: 1.2;
}

.card {
    background: #1C1C1E;
    border-radius: 24px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.card-title {
    font-size: 1.15rem;
    font-weight: 850;
    color: #F5F5F7;
}

.card-time {
    font-size: 0.9rem;
    color: #8E8E93;
}

.badge-blue {
    color: #0A84FF;
    font-weight: 850;
    font-size: 1rem;
    margin-bottom: 8px;
}

.big-value {
    font-size: 2rem;
    font-weight: 900;
    color: #F5F5F7;
    line-height: 1.15;
}

.subtext {
    font-size: 0.95rem;
    color: #8E8E93;
    margin-top: 4px;
}

.two-col {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 11px;
    margin-top: 14px;
}

.metric-box {
    background: #2C2C2E;
    border-radius: 16px;
    padding: 12px;
}

.metric-label {
    font-size: 0.82rem;
    color: #8E8E93;
    margin-bottom: 4px;
}

.metric-value {
    font-size: 1.35rem;
    font-weight: 850;
    color: #F5F5F7;
}

.status-box {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 16px;
    font-size: 0.95rem;
    font-weight: 650;
}

.status-good {
    background: rgba(48, 209, 88, 0.12);
    color: #30D158;
    border: 1px solid rgba(48, 209, 88, 0.18);
}

.stock-hero-card {
    background: #1C1C1E;
    border-radius: 26px;
    padding: 22px;
    margin-bottom: 22px;
    border: 1px solid rgba(255,255,255,0.08);
}

.stock-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}

.stock-name {
    font-size: 1.55rem;
    font-weight: 900;
    color: #F5F5F7;
}

.status-pill {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 850;
}

.pill-good {
    background: rgba(48, 209, 88, 0.14);
    color: #30D158;
}

.pill-warn {
    background: rgba(255, 159, 10, 0.14);
    color: #FF9F0A;
}

.pill-danger {
    background: rgba(255, 69, 58, 0.14);
    color: #FF453A;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 14px;
    margin-bottom: 16px;
}

.hero-main {
    background: #2C2C2E;
    border-radius: 20px;
    padding: 18px;
}

.hero-label {
    color: #8E8E93;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.hero-price {
    font-size: 3rem;
    font-weight: 900;
    color: #F5F5F7;
    line-height: 1;
}

.hero-change {
    font-size: 1.25rem;
    font-weight: 850;
    margin-top: 10px;
}

.price-up {
    color: #FF453A;
}

.price-down {
    color: #30D158;
}

.price-flat {
    color: #8E8E93;
}

.hero-suggestion {
    background: rgba(10, 132, 255, 0.14);
    border: 1px solid rgba(10, 132, 255, 0.25);
    border-radius: 20px;
    padding: 18px;
}

.suggestion-value {
    font-size: 2.15rem;
    font-weight: 900;
    color: #0A84FF;
    line-height: 1.1;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.info-tile {
    background: #2C2C2E;
    border-radius: 16px;
    padding: 12px;
}

.info-label {
    color: #8E8E93;
    font-size: 0.8rem;
    margin-bottom: 5px;
}

.info-value {
    color: #F5F5F7;
    font-size: 1.25rem;
    font-weight: 850;
}

@media (max-width: 640px) {
    .top-title {
        font-size: 1.9rem;
    }

    .section-title {
        font-size: 1.35rem;
    }

    .mini-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .two-col,
    .hero-grid {
        grid-template-columns: 1fr;
    }

    .info-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .mini-value {
        font-size: 1.55rem;
    }

    .hero-price {
        font-size: 2.4rem;
    }

    .stock-name {
        font-size: 1.3rem;
    }
}
/* =========================
   表格黑色風格
========================= */

/* st.dataframe 外框 */
[data-testid="stDataFrame"] {
    background-color: #111111 !important;
    border-radius: 18px !important;
    overflow: hidden !important;
}

/* 表格內部 */
[data-testid="stDataFrame"] div {
    color: #f5f5f7 !important;
}

/* 表頭 */
[data-testid="stDataFrame"] th {
    background-color: #1c1c1e !important;
    color: #f5f5f7 !important;
}

/* 儲存格 */
[data-testid="stDataFrame"] td {
    background-color: #111111 !important;
    color: #f5f5f7 !important;
}

/* st.table 用 */
[data-testid="stTable"] {
    background-color: #111111 !important;
    color: #f5f5f7 !important;
}

[data-testid="stTable"] table {
    background-color: #111111 !important;
    color: #f5f5f7 !important;
}

[data-testid="stTable"] th,
[data-testid="stTable"] td {
    background-color: #111111 !important;
    color: #f5f5f7 !important;
    border-color: #2c2c2e !important;
}
.input-card {
    background: linear-gradient(180deg, #1C1C1E 0%, #111113 100%);
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="top-title">📈 股票加碼計畫</div>
    <div class="top-subtitle">0050・00662 投資進度儀表板｜自動判斷本月建議操作</div>
    """,
    unsafe_allow_html=True
)


# =========================
# 股票策略設定
# =========================
strategy = {
    "0050.TW": {
        "name": "元大台灣50",
        "total_budget": 400000,
        "basic_monthly_dca": 30000,
        "dip_rules": {
            -5: 30000,
            -10: 40000,
            -15: 40000,
            -20: 50000
        }
    },
    "00662.TW": {
        "name": "富邦NASDAQ-100",
        "total_budget": 650000,
        "basic_monthly_dca": 45000,
        "dip_rules": {
            -5: 50000,
            -10: 70000,
            -15: 80000,
            -20: 90000
        }
    }
}

# =========================
# Google Sheets 紀錄功能
# =========================

def get_google_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet_id = st.secrets["google_sheet"]["spreadsheet_id"]
    worksheet_name = st.secrets["google_sheet"]["worksheet_name"]

    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(worksheet_name)

    return worksheet


def load_investment_log():
    worksheet = get_google_sheet()
    records = worksheet.get_all_records()

    if len(records) == 0:
        return pd.DataFrame(
            columns=[
                "時間",
                "0050已購入總金額",
                "00662已購入總金額",
                "0050本月已投入金額",
                "00662本月已投入金額",
                "備註"
            ]
        )

    return pd.DataFrame(records)


def add_investment_record(
    purchased_0050,
    purchased_00662,
    monthly_0050,
    monthly_00662,
    note
):
    worksheet = get_google_sheet()

    new_row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        purchased_0050,
        purchased_00662,
        monthly_0050,
        monthly_00662,
        note
    ]

    worksheet.append_row(new_row)


def delete_investment_record(index_to_delete):
    worksheet = get_google_sheet()

    # Google Sheet 第 1 列是標題，所以資料從第 2 列開始
    sheet_row_number = index_to_delete + 2

    all_values = worksheet.get_all_values()

    if sheet_row_number <= len(all_values):
        worksheet.delete_rows(sheet_row_number)
        return True

    return False


# =========================
# 股票資料下載
# =========================
@st.cache_data(ttl=300)
def load_stock_data(symbol, start, end):
    """
    下載股票資料。
    使用 yfinance 抓近一年資料。
    如果第一次抓不到，會改用 Ticker.history() 再試一次。
    ttl=300 代表快取 5 分鐘，避免錯誤資料被記太久。
    """

    data = pd.DataFrame()

    # 方法一：使用 yf.download()
    try:
        data = yf.download(
            symbol,
            period="1y",
            interval="1d",
            progress=False,
            auto_adjust=False,
            repair=True,
            threads=False
        )
    except Exception:
        data = pd.DataFrame()

    # 方法二：如果方法一失敗，改用 yf.Ticker().history()
    if data.empty:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(
                period="1y",
                interval="1d",
                auto_adjust=False
            )
        except Exception:
            data = pd.DataFrame()

    # 如果還是沒有資料，直接回傳空表
    if data.empty:
        return pd.DataFrame()

    # 如果 yfinance 回傳多層欄位，轉成一般欄位
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 把日期索引變成 Date 欄位
    data = data.reset_index()

    # 有些情況欄位叫 Datetime，統一改成 Date
    if "Datetime" in data.columns and "Date" not in data.columns:
        data = data.rename(columns={"Datetime": "Date"})

    # 確認必要欄位存在
    required_cols = ["Date", "Open", "High", "Low", "Close"]
    for col in required_cols:
        if col not in data.columns:
            return pd.DataFrame()

    # 數字欄位轉型
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # 刪掉 Close 是空值的資料
    data = data.dropna(subset=["Close"])

    if data.empty:
        return pd.DataFrame()

    return data


# =========================
# 加碼條件判斷
# =========================
def get_triggered_rule(drawdown_pct, dip_rules):
    triggered = []

    for level, amount in dip_rules.items():
        if drawdown_pct <= level:
            triggered.append((level, amount))

    if len(triggered) == 0:
        return None

    triggered = sorted(triggered, key=lambda x: x[0])
    return triggered[0]


def get_next_rule(drawdown_pct, dip_rules):
    untriggered = []

    for level, amount in dip_rules.items():
        if drawdown_pct > level:
            untriggered.append((level, amount))

    if len(untriggered) == 0:
        return None

    untriggered = sorted(untriggered, key=lambda x: abs(x[0]))
    return untriggered[0]


# =========================
# 計算今年剩餘月份
# =========================
def get_months_left_in_year():
    today = date.today()
    return 12 - today.month + 1


# =========================
# 金額進位
# =========================
def round_up_to_thousand(amount):
    return math.ceil(amount / 1000) * 1000


# =========================
# 主畫面輸入區
# =========================

# 初始化 session_state
if "purchased_0050" not in st.session_state:
    st.session_state.purchased_0050 = 0

if "purchased_00662" not in st.session_state:
    st.session_state.purchased_00662 = 0

if "monthly_0050" not in st.session_state:
    st.session_state.monthly_0050 = 0

if "monthly_00662" not in st.session_state:
    st.session_state.monthly_00662 = 0


show_input = st.toggle("＋ 更新投入金額", value=False)

if show_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    st.markdown("### 資金設定")

    st.session_state.purchased_0050 = st.number_input(
        "0050 已購入總金額",
        min_value=0,
        max_value=400000,
        value=st.session_state.purchased_0050,
        step=10000
    )

    st.session_state.purchased_00662 = st.number_input(
        "00662 已購入總金額",
        min_value=0,
        max_value=650000,
        value=st.session_state.purchased_00662,
        step=10000
    )

    st.markdown("### 本月投入狀態")

    st.session_state.monthly_0050 = st.number_input(
        "0050 本月已投入金額",
        min_value=0,
        max_value=400000,
        value=st.session_state.monthly_0050,
        step=10000
    )

    st.session_state.monthly_00662 = st.number_input(
        "00662 本月已投入金額",
        min_value=0,
        max_value=650000,
        value=st.session_state.monthly_00662,
        step=10000
    )

    st.markdown("### 紀錄本次輸入")

    record_note = st.text_input(
        "備註",
        value="",
        placeholder="例如：5月定期定額、修正金額、下跌加碼"
    )

    if st.button("儲存本次輸入紀錄"):
        add_investment_record(
            st.session_state.purchased_0050,
            st.session_state.purchased_00662,
            st.session_state.monthly_0050,
            st.session_state.monthly_00662,
            record_note
        )

        st.success("已儲存本次輸入紀錄")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 日期設定
# =========================
today = date.today()
start_date = today - timedelta(days=365)
end_date = today + timedelta(days=1)
months_left = get_months_left_in_year()


# =========================
# 整體總覽
# =========================
total_budget = 1050000
total_purchased = (
    st.session_state.purchased_0050 +
    st.session_state.purchased_00662
)
total_remaining = total_budget - total_purchased

st.markdown('<div class="section-title">資金總覽</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="summary-card">
        <div class="mini-grid">
            <div class="mini-item">
                <div class="mini-label label-blue">總計畫資金</div>
                <div class="mini-value">{total_budget:,.0f} 元</div>
            </div>
            <div class="mini-item">
                <div class="mini-label label-green">已購入金額</div>
                <div class="mini-value">{total_purchased:,.0f} 元</div>
            </div>
            <div class="mini-item">
                <div class="mini-label label-orange">剩餘資金</div>
                <div class="mini-value">{total_remaining:,.0f} 元</div>
            </div>
            <div class="mini-item">
                <div class="mini-label label-pink">今年剩餘月份</div>
                <div class="mini-value">{months_left} 個月</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")



# =========================
# 個股分析
# =========================
for symbol, info in strategy.items():

    if symbol == "0050.TW":
        purchased_amount = st.session_state.purchased_0050
        monthly_invested = st.session_state.monthly_0050
    else:
        purchased_amount = st.session_state.purchased_00662
        monthly_invested = st.session_state.monthly_00662

    remaining_budget = info["total_budget"] - purchased_amount

    try:
        data = load_stock_data(symbol, start_date, end_date)

        if data.empty:
            st.error(f"{symbol} 查無資料")
            continue

        data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
        data["Open"] = pd.to_numeric(data["Open"], errors="coerce")
        data["High"] = pd.to_numeric(data["High"], errors="coerce")
        data["Low"] = pd.to_numeric(data["Low"], errors="coerce")

        data["MA5"] = data["Close"].rolling(window=5).mean()
        data["MA20"] = data["Close"].rolling(window=20).mean()

        latest_close = float(data["Close"].dropna().iloc[-1])
        period_high = float(data["High"].dropna().max())

        drawdown_pct = (latest_close - period_high) / period_high * 100

        triggered_rule = get_triggered_rule(drawdown_pct, info["dip_rules"])
        next_rule = get_next_rule(drawdown_pct, info["dip_rules"])

        # =========================
        # 年底完成所需投入
        # =========================
        if remaining_budget > 0:
            required_monthly_by_year_end = round_up_to_thousand(remaining_budget / months_left)
        else:
            required_monthly_by_year_end = 0

        basic_monthly_dca = info["basic_monthly_dca"]

        basic_remaining_this_month = max(basic_monthly_dca - monthly_invested, 0)

        year_end_remaining_this_month = max(required_monthly_by_year_end - monthly_invested, 0)

        # 本月進度投入建議：
        # 取「基本定期定額剩餘」與「年底完成所需剩餘」兩者較高
        progress_suggestion = max(
            basic_remaining_this_month,
            year_end_remaining_this_month
        )

        progress_suggestion = min(progress_suggestion, remaining_budget)

        # =========================
        # 下跌加碼建議
        # =========================
        if triggered_rule is not None and remaining_budget > 0:
            triggered_level, triggered_amount = triggered_rule
            dip_suggestion = min(triggered_amount, max(remaining_budget - progress_suggestion, 0))
        else:
            triggered_level = None
            dip_suggestion = 0

        total_suggestion = min(progress_suggestion + dip_suggestion, remaining_budget)

        estimated_shares = int(total_suggestion // latest_close) if latest_close > 0 else 0

        if remaining_budget <= 0:
            action_text = "已完成投入"
        elif total_suggestion <= 0:
            action_text = "本月已達進度，暫時等待"
        elif triggered_rule is not None:
            action_text = f"建議投入 {total_suggestion:,.0f} 元，包含進度投入與 {triggered_level}% 下跌加碼"
        else:
            action_text = f"建議投入 {total_suggestion:,.0f} 元，以符合年底完成進度"


    except Exception as e:
        st.error(f"{symbol} 發生錯誤：{e}")



# =========================
# 詳細個股區塊
# =========================
for symbol, info in strategy.items():

    with st.expander(f"{symbol}｜{info['name']}", expanded=False):

        if symbol == "0050.TW":
            purchased_amount = st.session_state.purchased_0050
            monthly_invested = st.session_state.monthly_0050
        else:
            purchased_amount = st.session_state.purchased_00662
            monthly_invested = st.session_state.monthly_00662

        remaining_budget = info["total_budget"] - purchased_amount

        try:
            data = load_stock_data(symbol, start_date, end_date)

            if data.empty:
                st.error(f"{symbol} 查無資料")
                continue

            data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
            data["Open"] = pd.to_numeric(data["Open"], errors="coerce")
            data["High"] = pd.to_numeric(data["High"], errors="coerce")
            data["Low"] = pd.to_numeric(data["Low"], errors="coerce")

            data["MA5"] = data["Close"].rolling(window=5).mean()
            data["MA20"] = data["Close"].rolling(window=20).mean()

            latest_close = float(data["Close"].dropna().iloc[-1])
            period_high = float(data["High"].dropna().max())
            drawdown_pct = (latest_close - period_high) / period_high * 100

            triggered_rule = get_triggered_rule(drawdown_pct, info["dip_rules"])
            next_rule = get_next_rule(drawdown_pct, info["dip_rules"])

            if remaining_budget > 0:
                required_monthly_by_year_end = round_up_to_thousand(remaining_budget / months_left)
            else:
                required_monthly_by_year_end = 0

            basic_monthly_dca = info["basic_monthly_dca"]

            basic_remaining_this_month = max(basic_monthly_dca - monthly_invested, 0)
            year_end_remaining_this_month = max(required_monthly_by_year_end - monthly_invested, 0)

            progress_suggestion = max(
                basic_remaining_this_month,
                year_end_remaining_this_month
            )

            progress_suggestion = min(progress_suggestion, remaining_budget)

            if triggered_rule is not None and remaining_budget > 0:
                triggered_level, triggered_amount = triggered_rule
                dip_suggestion = min(triggered_amount, max(remaining_budget - progress_suggestion, 0))
            else:
                triggered_level = None
                dip_suggestion = 0

            total_suggestion = min(progress_suggestion + dip_suggestion, remaining_budget)
            estimated_shares = int(total_suggestion // latest_close) if latest_close > 0 else 0

            # =========================
            # 股票主卡片
            # =========================

            # 計算今日漲跌幅
            if len(data) >= 2:
                previous_close = float(data["Close"].dropna().iloc[-2])
                daily_change_pct = (latest_close - previous_close) / previous_close * 100
            else:
                daily_change_pct = 0

            # 加碼狀態標籤
            if triggered_rule is not None:
                pill_text = "已觸發加碼"
                pill_class = "pill-danger"
            elif drawdown_pct <= -3:
                pill_text = "接近觀察區"
                pill_class = "pill-warn"
            else:
                pill_text = "尚未觸發加碼"
                pill_class = "pill-good"

            # 台股習慣：紅色代表漲，綠色代表跌
            if daily_change_pct > 0:
                change_class = "price-up"
                change_text = f"今日上漲 +{daily_change_pct:.2f}%"
            elif daily_change_pct < 0:
                change_class = "price-down"
                change_text = f"今日下跌 {daily_change_pct:.2f}%"
            else:
                change_class = "price-flat"
                change_text = "今日持平 0.00%"

            st.markdown(
                f"""
            <div class="stock-hero-card">
            <div class="stock-header-row">
            <div class="stock-name">{symbol}｜{info["name"]}</div>
            <div class="status-pill {pill_class}">{pill_text}</div>
            </div>

            <div class="hero-grid">
            <div class="hero-main">
            <div class="hero-label">目前價格</div>
            <div class="hero-price">{latest_close:.2f}</div>
            <div class="hero-change {change_class}">{change_text}</div>
            </div>

            <div class="hero-suggestion">
            <div class="hero-label">本月建議投入</div>
            <div class="suggestion-value">{total_suggestion / 10000:.1f} 萬</div>
            <div class="subtext">約可買 {estimated_shares:,} 股</div>
            </div>
            </div>

            <div class="info-grid">
            <div class="info-tile">
            <div class="info-label">近一年高點</div>
            <div class="info-value">{period_high:.2f}</div>
            </div>

            <div class="info-tile">
            <div class="info-label">剩餘可投入</div>
            <div class="info-value">{remaining_budget / 10000:.1f} 萬</div>
            </div>

            <div class="info-tile">
            <div class="info-label">距高點跌幅</div>
            <div class="info-value">{drawdown_pct:.2f}%</div>
            </div>

            <div class="info-tile">
            <div class="info-label">基本月投入</div>
            <div class="info-value">{basic_monthly_dca / 10000:.1f} 萬</div>
            </div>

            <div class="info-tile">
            <div class="info-label">年度所需月投入</div>
            <div class="info-value">{required_monthly_by_year_end / 10000:.1f} 萬</div>
            </div>

            <div class="info-tile">
            <div class="info-label">本月已投入</div>
            <div class="info-value">{monthly_invested / 10000:.1f} 萬</div>
            </div>
            </div>
            </div>
            """,
                unsafe_allow_html=True
            )

            # =========================
            # 今日建議
            # =========================
            st.subheader("今日建議操作")

            suggestion_points = []

            if remaining_budget <= 0:
                suggestion_points.append("這檔股票已完成今年預計投入金額。")

            else:
                # 第 1 點：整合本月進度、年底完成需求、本次建議投入
                if monthly_invested < basic_monthly_dca:
                    monthly_status_text = (
                        f"本月尚未完成基本定期定額，還差 {basic_remaining_this_month:,.0f} 元"
                    )
                else:
                    monthly_status_text = "本月基本定期定額已完成"

                if required_monthly_by_year_end > basic_monthly_dca:
                    year_end_text = (
                        f"為了年底前完成投入，目前每月平均需要投入約 "
                        f"{required_monthly_by_year_end:,.0f} 元，"
                        f"高於原本基本定期定額 {basic_monthly_dca:,.0f} 元"
                    )
                else:
                    year_end_text = "目前進度足以用原本定期定額節奏完成"

                suggestion_points.append(
                    f"{monthly_status_text}；{year_end_text}。"
                    f"本次總建議投入 "
                    f"<span style='color:#30D158;font-weight:800;'>{total_suggestion:,.0f} 元</span>，"
                    f"以目前價格估算約可買 "
                    f"<span style='color:#30D158;font-weight:800;'>{estimated_shares:,} 股</span>。"
                )

                # 第 2 點：整合目前加碼狀態、下一個觀察點
                if triggered_rule is not None:
                    dip_status_text = (
                        f"目前已觸發 {triggered_level}% 下跌加碼條件，"
                        f"額外下跌加碼建議為 {dip_suggestion:,.0f} 元"
                    )
                else:
                    dip_status_text = "目前尚未觸發下跌加碼條件"

                if next_rule is not None:
                    next_level, next_amount = next_rule
                    next_price = period_high * (1 + next_level / 100)

                    next_point_text = (
                        f"下一個觀察點為 {next_level}% 跌幅，約等於價格 "
                        f"<span style='color:#0A84FF;font-weight:800;'>{next_price:.2f} 元</span>，"
                        f"若觸發則原定加碼 {next_amount / 10000:.1f} 萬"
                    )
                else:
                    next_point_text = (
                        "目前已跌破所有設定的下跌加碼條件，建議避免一次投入全部剩餘資金"
                    )

                suggestion_points.append(
                    f"{dip_status_text}；{next_point_text}。"
                )

            suggestion_html = "".join([f"<li>{point}</li>" for point in suggestion_points])

            st.markdown(
                f"""
                <div class="card">
                    <ul style="
                        margin-top: 0;
                        margin-bottom: 0;
                        padding-left: 22px;
                        line-height: 1.9;
                        color: #F5F5F7;
                        font-size: 1rem;
                    ">
                        {suggestion_html}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )


            # =========================
            # 加碼條件表
            # =========================
            st.subheader("加碼條件表")

            rule_rows = []

            for level, amount in info["dip_rules"].items():
                trigger_price = period_high * (1 + level / 100)

                if drawdown_pct <= level:
                    status = "已觸發"
                else:
                    status = "尚未觸發"

                rule_rows.append({
                    "跌幅": f"{level}%",
                    "價格": f"{trigger_price:.2f}",
                    "金額": f"{amount / 10000:.1f} 萬",
                    "狀態": status
                })

            rule_df = pd.DataFrame(rule_rows)

            styled_rule_df = rule_df.style.set_properties(
                **{
                    "text-align": "center"
                }
            ).set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [
                        ("text-align", "center")
                        ]
                    },
                    {
                        "selector": "td",
                        "props": [
                            ("text-align", "center")
                        ]       
                    }
                ]
            )

            st.dataframe(
                styled_rule_df,
                width="stretch",
                hide_index=True,
                column_config={
                    "跌幅": st.column_config.TextColumn("跌幅", width="small"),
                    "價格": st.column_config.TextColumn("價格", width="small"),
                    "金額": st.column_config.TextColumn("金額", width="small"),
                    "狀態": st.column_config.TextColumn("狀態", width="small"),
                }
            )

            # =========================
            # 股價圖表
            # =========================
            st.subheader("股價走勢圖")

            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=data["Date"],
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"],
                    name="K 線"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=data["Date"],
                    y=data["MA5"],
                    mode="lines",
                    name="MA5"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=data["Date"],
                    y=data["MA20"],
                    mode="lines",
                    name="MA20"
                )
            )

            fig.update_layout(
                title=f"{symbol} 近一年 K 線圖",
                xaxis_title="日期",
                yaxis_title="價格",
                height=400,
                xaxis_rangeslider_visible=False,
                dragmode=False
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "scrollZoom": False
                }
            )

            st.write("---")

        except Exception as e:
            st.error(f"{symbol} 發生錯誤：{e}")


# =========================
# 策略回測績效模組
# 放在 00662 區塊下方、歷史輸入紀錄上方
# =========================

def calculate_max_drawdown(equity_series):
    """
    計算最大回撤
    """
    rolling_max = equity_series.cummax()
    drawdown = (equity_series - rolling_max) / rolling_max
    return drawdown.min()


def run_dca_backtest(symbol, start_date, end_date, monthly_amount):
    """
    定期定額回測
    每月第一個交易日投入固定金額
    """

    data = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        return None

    data = data[["Close"]].dropna()
    data.index = pd.to_datetime(data.index)

    # 取每個月第一個交易日價格
    monthly_data = data.resample("MS").first().dropna()

    shares = 0
    total_invested = 0
    records = []

    for date, row in monthly_data.iterrows():
        price = row["Close"]

        if hasattr(price, "iloc"):
            price = price.iloc[0]

        price = float(price)

        buy_shares = monthly_amount / price
        shares += buy_shares
        total_invested += monthly_amount

        asset_value = shares * price
        total_return = (asset_value - total_invested) / total_invested

        records.append({
            "日期": date,
            "價格": price,
            "本月投入": monthly_amount,
            "累積投入": total_invested,
            "持有股數": shares,
            "資產價值": asset_value,
            "累積報酬率": total_return
        })

    result_df = pd.DataFrame(records)

    summary = {
        "期末資產": result_df["資產價值"].iloc[-1],
        "累積投入": result_df["累積投入"].iloc[-1],
        "累積報酬率": result_df["累積報酬率"].iloc[-1],
        "最大回撤": calculate_max_drawdown(result_df["資產價值"])
    }

    return result_df, summary


def plot_equity_curve(result_df):
    """
    畫資產曲線
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=result_df["日期"],
        y=result_df["資產價值"],
        mode="lines",
        name="資產價值",
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=result_df["日期"],
        y=result_df["累積投入"],
        mode="lines",
        name="累積投入",
        line=dict(width=2, dash="dash")
    ))

    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),
        xaxis=dict(
            showgrid=False,
            color="white"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)",
            color="white"
        )
    )

    return fig


# =========================
# 策略回測績效 UI
# =========================

with st.expander("策略回測績效", expanded=False):

    st.markdown("回測標的：0050.TW｜定期定額策略")

    current_year = pd.Timestamp.today().year
    current_month = pd.Timestamp.today().month

    col1, col2 = st.columns(2)

    with col1:
        start_year = st.selectbox(
            "開始年份",
            list(range(2015, current_year + 1)),
            index=5,
            key="backtest_start_year"
        )

    with col2:
        start_month = st.selectbox(
            "開始月份",
            list(range(1, 13)),
            index=0,
            format_func=lambda x: f"{x:02d} 月",
            key="backtest_start_month"
        )

    col3, col4 = st.columns(2)

    with col3:
        end_year = st.selectbox(
            "結束年份",
            list(range(2015, current_year + 1)),
            index=len(list(range(2015, current_year + 1))) - 1,
            key="backtest_end_year"
        )

    with col4:
        end_month = st.selectbox(
            "結束月份",
            list(range(1, 13)),
            index=current_month - 1,
            format_func=lambda x: f"{x:02d} 月",
            key="backtest_end_month"
        )

    monthly_amount = st.number_input(
        "每月投入金額",
        min_value=1000,
        max_value=500000,
        value=10000,
        step=1000,
        key="backtest_monthly_amount"
    )

    run_backtest = st.button(
        "開始回測",
        key="run_backtest_button",
        use_container_width=True
    )

    if run_backtest:

        backtest_start_date = pd.Timestamp(start_year, start_month, 1)
        backtest_end_date = pd.Timestamp(end_year, end_month, 1) + pd.offsets.MonthEnd(1)

        if backtest_end_date <= backtest_start_date:
            st.warning("結束年月必須晚於開始年月。")

        else:
            backtest_result = run_dca_backtest(
                symbol="0050.TW",
                start_date=backtest_start_date,
                end_date=backtest_end_date,
                monthly_amount=monthly_amount
            )

            if backtest_result is None:
                st.warning("抓不到回測資料，請確認日期區間。")

            else:
                result_df, summary = backtest_result

                final_asset = summary["期末資產"]
                total_invested = summary["累積投入"]
                total_return = summary["累積報酬率"]
                max_drawdown = summary["最大回撤"]

                st.markdown(
                    f"""
                    <div class="summary-card">
                        <div class="mini-grid">
                            <div class="mini-item">
                                <div class="mini-label label-blue">期末資產</div>
                                <div class="mini-value">{final_asset:,.0f} 元</div>
                            </div>
                            <div class="mini-item">
                                <div class="mini-label label-green">累積投入</div>
                                <div class="mini-value">{total_invested:,.0f} 元</div>
                            </div>
                            <div class="mini-item">
                                <div class="mini-label label-red">累積報酬率</div>
                                <div class="mini-value">{total_return:.2%}</div>
                            </div>
                            <div class="mini-item">
                                <div class="mini-label label-orange">最大回撤</div>
                                <div class="mini-value">{max_drawdown:.2%}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("#### 資產曲線")
                fig = plot_equity_curve(result_df)
                st.plotly_chart(fig, width="stretch")

                with st.expander("查看回測明細", expanded=False):
                    display_df = result_df.copy()

                    display_df["日期"] = display_df["日期"].dt.strftime("%Y-%m")
                    display_df["價格"] = display_df["價格"].map(lambda x: f"{x:,.2f}")
                    display_df["本月投入"] = display_df["本月投入"].map(lambda x: f"{x:,.0f}")
                    display_df["累積投入"] = display_df["累積投入"].map(lambda x: f"{x:,.0f}")
                    display_df["持有股數"] = display_df["持有股數"].map(lambda x: f"{x:,.4f}")
                    display_df["資產價值"] = display_df["資產價值"].map(lambda x: f"{x:,.0f}")
                    display_df["累積報酬率"] = display_df["累積報酬率"].map(lambda x: f"{x:.2%}")

                    st.dataframe(
                        display_df,
                        width="stretch",
                        hide_index=True
                    )


# =========================
# 歷史輸入紀錄
# =========================
with st.expander("歷史輸入紀錄", expanded=False):

    log_df = load_investment_log()

    if log_df.empty:
        st.info("目前還沒有任何輸入紀錄。")
    else:
        display_log_df = log_df.copy()

        # 加入紀錄編號，方便刪除
        display_log_df.insert(0, "編號", display_log_df.index)

        # 時間縮短
        if "時間" in display_log_df.columns:
            display_log_df["時間"] = pd.to_datetime(
                display_log_df["時間"],
                errors="coerce"
            )

        display_log_df["時間"] = display_log_df["時間"].dt.strftime("%m/%d %H:%M")
        display_log_df["時間"] = display_log_df["時間"].fillna("時間錯誤")

        # 金額欄位改成「萬」
        money_cols = [
            "0050已購入總金額",
            "00662已購入總金額",
            "0050本月已投入金額",
            "00662本月已投入金額"
        ]

        for col in money_cols:
            if col in display_log_df.columns:
                display_log_df[col] = pd.to_numeric(
                    display_log_df[col],
                    errors="coerce"
                ).fillna(0)
                display_log_df[col] = display_log_df[col].apply(
                    lambda x: f"{x / 10000:.1f}萬"
                )

        # 欄位名稱縮短
        display_log_df = display_log_df.rename(
            columns={
                "0050已購入總金額": "0050總",
                "00662已購入總金額": "00662總",
                "0050本月已投入金額": "0050月",
                "00662本月已投入金額": "00662月"
            }
        )

        # 最新紀錄放最上面
        display_log_df = display_log_df.sort_values("時間", ascending=False)

        styled_log_df = display_log_df.style.set_properties(
            **{
                "text-align": "center"
            }
        ).set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("text-align", "center")
                    ]
                }
            ]
        )

        st.dataframe(
            styled_log_df,
            width="stretch",
            hide_index=True
        )

        st.subheader("取消 / 刪除錯誤紀錄")

        delete_index = st.number_input(
            "請輸入要刪除的紀錄編號",
            min_value=0,
            max_value=max(len(log_df) - 1, 0),
            value=0,
            step=1
        )

        if st.button("刪除這筆紀錄"):
            success = delete_investment_record(delete_index)

            if success:
                st.success(f"已刪除紀錄編號 {delete_index}。請重新整理頁面查看結果。")
            else:
                st.error("刪除失敗，請確認紀錄編號是否正確。")

        st.warning("刪除後無法復原，請確認紀錄編號再刪除。")
