import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="Amazon Price Tracker",
    page_icon="📈",
    layout="wide"
)

# =========================
# カスタム CSS（見た目を一気に良くする）
# =========================
st.markdown("""
<style>
/* タイトル中央寄せ */
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

/* カード UI */
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* 商品名 */
.product-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 8px;
}

/* 価格 */
.price-text {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB 読み込み
# =========================
def load_data():
    conn = sqlite3.connect("db/prices.db")
    df = pd.read_sql_query("SELECT * FROM prices ORDER BY datetime ASC", conn)
    conn.close()
    return df

df = load_data()

# =========================
# UI：タイトル
# =========================
st.markdown('<div class="main-title">Amazon Price Tracker（複数商品対応）</div>', unsafe_allow_html=True)

# =========================
# サイドバー
# =========================
st.sidebar.header("🔧 操作メニュー")

product_list = df["title"].unique().tolist()

# メイン商品（カード表示用）
selected_product = st.sidebar.selectbox("メイン商品を選択", product_list)

# 複数商品比較
compare_products = st.sidebar.multiselect(
    "比較したい商品を選択（複数選択可）",
    product_list,
    default=[selected_product]
)

st.sidebar.markdown("---")
st.sidebar.write("📦 GitHub（公開用リンク）を後で追加できます")

# =========================
# メイン商品のデータ抽出
# =========================
product_df = df[df["title"] == selected_product]

current_price = product_df["price"].iloc[-1]
min_price = product_df["price"].min()
max_price = product_df["price"].max()
last_update = product_df["datetime"].iloc[-1]

# =========================
# 商品情報カード
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="product-title">{selected_product}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="price-text">¥{current_price:,}</div>', unsafe_allow_html=True)
st.write(f"📉 最安値: ¥{min_price:,}")
st.write(f"📈 最高値: ¥{max_price:,}")
st.write(f"⏱ 最終更新: {last_update}")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 複数商品比較データ
# =========================
compare_df = df[df["title"].isin(compare_products)]

# =========================
# 複数商品の比較グラフ
# =========================
compare_chart = (
    alt.Chart(compare_df)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X("datetime:T", title="日時"),
        y=alt.Y("price:Q", title="価格（円）"),
        color=alt.Color("title:N", title="商品名"),
        tooltip=["title", "datetime", "price"]
    )
    .properties(height=450)
)

st.altair_chart(compare_chart, use_container_width=True)
