import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import math
import os

# =========================
# 網頁基本設定
# =========================
st.set_page_config(page_title="股票加碼策略儀表板", layout="wide")

st.title("📈 股票加碼策略儀表板")
st.write("自動判斷 0050、00662 的加碼條件，並根據本月投入狀況與年底完成目標，給出下一步建議。")


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
# 操作紀錄功能
# =========================
LOG_FILE = "investment_log.csv"


def load_investment_log():
    """
    讀取歷史輸入紀錄。
    如果還沒有紀錄檔，就建立一個空的表格。
    """
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    else:
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


def save_investment_log(df):
    """
    儲存歷史輸入紀錄到 CSV 檔案。
    """
    df.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")


def add_investment_record(
    purchased_0050,
    purchased_00662,
    monthly_0050,
    monthly_00662,
    note
):
    """
    新增一筆輸入紀錄。
    """
    log_df = load_investment_log()

    new_record = {
        "時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "0050已購入總金額": purchased_0050,
        "00662已購入總金額": purchased_00662,
        "0050本月已投入金額": monthly_0050,
        "00662本月已投入金額": monthly_00662,
        "備註": note
    }

    log_df = pd.concat(
        [log_df, pd.DataFrame([new_record])],
        ignore_index=True
    )

    save_investment_log(log_df)


def delete_investment_record(index_to_delete):
    """
    刪除指定的一筆紀錄。
    """
    log_df = load_investment_log()

    if 0 <= index_to_delete < len(log_df):
        log_df = log_df.drop(index=index_to_delete).reset_index(drop=True)
        save_investment_log(log_df)
        return True

    return False


# =========================
# 股票資料下載
# =========================
@st.cache_data
def load_stock_data(symbol, start, end):
    data = yf.download(
        symbol,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()
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
# 側邊欄輸入
# =========================
st.sidebar.header("資金設定")

st.sidebar.write("總計畫資金：105 萬")
st.sidebar.write("0050：40 萬")
st.sidebar.write("00662：65 萬")

purchased_0050 = st.sidebar.number_input(
    "0050 已購入總金額",
    min_value=0,
    max_value=400000,
    value=0,
    step=10000
)

purchased_00662 = st.sidebar.number_input(
    "00662 已購入總金額",
    min_value=0,
    max_value=650000,
    value=0,
    step=10000
)

st.sidebar.write("---")
st.sidebar.subheader("本月投入狀態")

monthly_0050 = st.sidebar.number_input(
    "0050 本月已投入金額",
    min_value=0,
    max_value=400000,
    value=0,
    step=10000
)

monthly_00662 = st.sidebar.number_input(
    "00662 本月已投入金額",
    min_value=0,
    max_value=650000,
    value=0,
    step=10000
)

st.sidebar.write("---")
st.sidebar.subheader("紀錄本次輸入")

record_note = st.sidebar.text_input(
    "備註",
    value="",
    placeholder="例如：5月定期定額、修正金額、下跌加碼"
)

if st.sidebar.button("儲存本次輸入紀錄"):
    add_investment_record(
        purchased_0050,
        purchased_00662,
        monthly_0050,
        monthly_00662,
        record_note
    )

    st.sidebar.success("已儲存本次輸入紀錄")

chart_type = st.sidebar.radio(
    "圖表類型",
    ["K 線圖", "折線圖"]
)

st.sidebar.write("---")
st.sidebar.write("說明：")
st.sidebar.write("已購入總金額：代表這檔今年計畫中，你目前總共已經買多少。")
st.sidebar.write("本月已投入金額：用來判斷這個月是否已經完成定期投入。")


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
total_purchased = purchased_0050 + purchased_00662
total_remaining = total_budget - total_purchased

st.subheader("資金總覽")

col_a, col_b, col_c, col_d = st.columns(4)

col_a.metric("總計畫資金", f"{total_budget:,.0f} 元")
col_b.metric("已購入金額", f"{total_purchased:,.0f} 元")
col_c.metric("剩餘資金", f"{total_remaining:,.0f} 元")
col_d.metric("今年剩餘月份", f"{months_left} 個月")

st.write("---")


# =========================
# 今日建議總覽
# =========================
st.subheader("今日建議操作總覽")

summary_rows = []


# =========================
# 個股分析
# =========================
for symbol, info in strategy.items():

    if symbol == "0050.TW":
        purchased_amount = purchased_0050
        monthly_invested = monthly_0050
    else:
        purchased_amount = purchased_00662
        monthly_invested = monthly_00662

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

        latest_close = float(data["Close"].iloc[-1])
        period_high = float(data["High"].max())

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

        summary_rows.append({
            "標的": f"{symbol} {info['name']}",
            "目前價格": round(latest_close, 2),
            "距離高點跌幅": f"{drawdown_pct:.2f}%",
            "已購入": f"{purchased_amount:,.0f} 元",
            "剩餘可投入": f"{remaining_budget:,.0f} 元",
            "本月已投入": f"{monthly_invested:,.0f} 元",
            "本月建議投入": f"{total_suggestion:,.0f} 元",
            "約可買股數": f"{estimated_shares:,} 股",
            "建議操作": action_text
        })

    except Exception as e:
        st.error(f"{symbol} 發生錯誤：{e}")


summary_df = pd.DataFrame(summary_rows)
st.dataframe(summary_df, width="stretch")

st.write("---")


# =========================
# 詳細個股區塊
# =========================
for symbol, info in strategy.items():

    st.header(f"{symbol}｜{info['name']}")

    if symbol == "0050.TW":
        purchased_amount = purchased_0050
        monthly_invested = monthly_0050
    else:
        purchased_amount = purchased_00662
        monthly_invested = monthly_00662

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

        latest_close = float(data["Close"].iloc[-1])
        period_high = float(data["High"].max())
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
        # 重點數據
        # =========================
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("目前價格", f"{latest_close:.2f}")
        col2.metric("近一年高點", f"{period_high:.2f}")
        col3.metric("距離高點跌幅", f"{drawdown_pct:.2f}%")
        col4.metric("剩餘可投入", f"{remaining_budget:,.0f} 元")

        col5, col6, col7, col8 = st.columns(4)

        col5.metric("基本月投入", f"{basic_monthly_dca:,.0f} 元")
        col6.metric("年底完成所需月投入", f"{required_monthly_by_year_end:,.0f} 元")
        col7.metric("本月已投入", f"{monthly_invested:,.0f} 元")
        col8.metric("本月建議再投入", f"{total_suggestion:,.0f} 元")

        # =========================
        # 今日建議
        # =========================
        st.subheader("今日建議操作")

        if remaining_budget <= 0:
            st.success("這檔股票已完成今年預計投入金額。")

        else:
            if monthly_invested < basic_monthly_dca:
                st.warning(
                    f"本月尚未完成基本定期定額。"
                    f"基本定期定額還差 {basic_remaining_this_month:,.0f} 元。"
                )
            else:
                st.info("本月基本定期定額已完成。")

            if required_monthly_by_year_end > basic_monthly_dca:
                st.warning(
                    f"因為你希望年底前完成投入，"
                    f"目前每月平均需要投入約 {required_monthly_by_year_end:,.0f} 元，"
                    f"高於原本基本定期定額 {basic_monthly_dca:,.0f} 元。"
                )
            else:
                st.info("目前進度足以用原本定期定額節奏完成。")

            if triggered_rule is not None:
                st.error(
                    f"目前已觸發 {triggered_level}% 下跌加碼條件，"
                    f"額外下跌加碼建議為 {dip_suggestion:,.0f} 元。"
                )
            else:
                st.info("目前尚未觸發下跌加碼條件。")

            st.success(
                f"本次總建議投入：{total_suggestion:,.0f} 元，"
                f"以目前價格估算約可買 {estimated_shares:,} 股。"
            )

        # =========================
        # 下一步觀察點
        # =========================
        st.subheader("下一步觀察點")

        if next_rule is not None:
            next_level, next_amount = next_rule
            next_price = period_high * (1 + next_level / 100)

            st.write(
                f"下一個下跌加碼觀察點：{next_level}% ，"
                f"約等於價格 {next_price:.2f} 元。"
            )

            st.write(
                f"如果跌到這個位置，原定下跌加碼金額為 {next_amount:,.0f} 元。"
            )
        else:
            st.write("目前已經跌破所有設定的下跌加碼條件，應避免一次把剩餘資金全部打完。")

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
                "跌幅條件": f"{level}%",
                "觸發價格約": round(trigger_price, 2),
                "原定加碼金額": f"{amount:,.0f} 元",
                "目前狀態": status
            })

        rule_df = pd.DataFrame(rule_rows)
        st.dataframe(rule_df, width="stretch")

        # =========================
        # 股價圖表
        # =========================
        st.subheader("股價走勢圖")

        fig = go.Figure()

        if chart_type == "K 線圖":
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
        else:
            fig.add_trace(
                go.Scatter(
                    x=data["Date"],
                    y=data["Close"],
                    mode="lines",
                    name="收盤價"
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
            title=f"{symbol} 股價走勢",
            xaxis_title="日期",
            yaxis_title="價格",
            height=500,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, width="stretch")


        st.write("---")

    except Exception as e:
        st.error(f"{symbol} 發生錯誤：{e}")
        

# =========================
# 歷史輸入紀錄
# =========================
st.header("歷史輸入紀錄")

log_df = load_investment_log()

if log_df.empty:
    st.info("目前還沒有任何輸入紀錄。")
else:
    # 讓最新紀錄顯示在最上面
    display_log_df = log_df.copy()
    display_log_df.insert(0, "紀錄編號", display_log_df.index)

    st.dataframe(
        display_log_df.sort_values("時間", ascending=False),
        width="stretch"
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