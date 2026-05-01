# ─────────────────────────────────────────────────────────────────
#  CLV + RFM Intelligence Dashboard  ·  Streamlit app
#  Reads:  clv_rfm_output.csv  (produced by CELL 9A)
# ─────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="CLV Intelligence Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLORS = {
    "Champions": "#4CAF50", "Loyal": "#2196F3",
    "Potential Loyal": "#03A9F4", "At Risk": "#FF9800",
    "Hibernating": "#F44336", "Lost": "#9E9E9E", "New": "#9C27B0"
}

# ── Load data ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = "clv_rfm_output.csv"
    if not os.path.exists(csv_path):
        st.error(f"❌  {csv_path} not found.  Run CELL 9A first to generate it.")
        st.stop()
    df = pd.read_csv(csv_path)
    return df

df = load_data()

# ── Sidebar filters ──────────────────────────────────────────────
st.sidebar.title("🔍 Filters")
all_segs = sorted(df["segment"].unique().tolist())
selected_segs = st.sidebar.multiselect("Segment", all_segs, default=all_segs)

all_channels = sorted(df["acquisition_channel"].dropna().unique().tolist())
selected_channels = st.sidebar.multiselect("Acquisition Channel", all_channels, default=all_channels)

all_products = sorted(df["product_type"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect("Product Type", all_products, default=all_products)

clv_min, clv_max = float(df["clv_365d"].min()), float(df["clv_365d"].max())
clv_range = st.sidebar.slider("CLV 365d range (₹)", clv_min, clv_max, (clv_min, clv_max))

filtered = df[
    (df["segment"].isin(selected_segs)) &
    (df["acquisition_channel"].isin(selected_channels)) &
    (df["product_type"].isin(selected_products)) &
    (df["clv_365d"] >= clv_range[0]) &
    (df["clv_365d"] <= clv_range[1])
]

# ── Top KPIs ─────────────────────────────────────────────────────
st.title("💳 CLV + RFM Intelligence Dashboard")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Customers",   f"{len(filtered):,}")
k2.metric("Avg CLV (365d)",    f"₹{filtered['clv_365d'].mean():,.0f}")
k3.metric("Avg CLV (90d)",     f"₹{filtered['clv_90d'].mean():,.0f}")
k4.metric("Avg Prob Alive",    f"{filtered['prob_alive'].mean():.1%}")
k5.metric("Champions",         f"{(filtered['segment']=='Champions').sum():,}")

st.divider()

# ── Row 1 ─────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    seg_counts = filtered["segment"].value_counts().reset_index()
    seg_counts.columns = ["segment", "count"]
    fig = px.bar(
        seg_counts, x="count", y="segment", orientation="h",
        color="segment", color_discrete_map=COLORS,
        title="Customer Segment Distribution",
        labels={"count": "Customers", "segment": ""}
    )
    fig.update_layout(showlegend=False, plot_bgcolor="white",
                      paper_bgcolor="white",
                      yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    pie_df = filtered["segment"].value_counts().reset_index()
    pie_df.columns = ["segment", "count"]
    fig2 = px.pie(
        pie_df, names="segment", values="count",
        color="segment", color_discrete_map=COLORS,
        title="Segment Share (%)",
        hole=0.4
    )
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(showlegend=False, paper_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2 ─────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    box_df = filtered[filtered["clv_365d"] > 0]
    fig3 = px.box(
        box_df, x="segment", y="clv_365d",
        color="segment", color_discrete_map=COLORS,
        title="CLV (365d) Distribution by Segment",
        labels={"clv_365d": "Predicted CLV ₹ (1 yr)"}
    )
    fig3.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    scatter_df = filtered.nlargest(1000, "clv_365d")
    fig4 = px.scatter(
        scatter_df,
        x="frequency", y="monetary",
        color="segment", color_discrete_map=COLORS,
        size="clv_365d", size_max=20,
        hover_data=["customer_id", "clv_365d", "prob_alive"],
        title="Frequency vs Avg Spend (bubble = CLV)",
        labels={"frequency": "Repeat Purchases",
                "monetary": "Avg Spend per Txn ₹"},
        opacity=0.75
    )
    fig4.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3 — Heatmap + Top 20 ──────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    hmap = filtered.groupby(
        ["acquisition_channel", "product_type"])["clv_365d"].mean().round(0).unstack(fill_value=0)
    fig5 = px.imshow(
        hmap, text_auto=True, color_continuous_scale="Blues",
        title="Avg CLV (₹) — Channel × Product",
        labels=dict(x="Product Type", y="Channel", color="Avg CLV ₹")
    )
    fig5.update_layout(paper_bgcolor="white")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    top20 = filtered.nlargest(20, "clv_365d")[
        ["customer_id", "segment", "clv_365d", "prob_alive"]
    ].reset_index(drop=True)
    fig6 = px.bar(
        top20, x="customer_id", y="clv_365d",
        color="segment", color_discrete_map=COLORS,
        title="Top 20 Customers by CLV (1yr)",
        labels={"clv_365d": "CLV ₹", "customer_id": "Customer"}
    )
    fig6.update_xaxes(tickangle=45)
    fig6.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig6, use_container_width=True)

# ── Row 4 — Recency histogram + Prob-alive distribution ───────────
col7, col8 = st.columns(2)

with col7:
    fig7 = px.histogram(
        filtered, x="recency", nbins=40,
        color="segment", color_discrete_map=COLORS,
        title="Recency Distribution by Segment",
        labels={"recency": "Days Since Last Purchase"},
        barmode="overlay", opacity=0.7
    )
    fig7.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    fig8 = px.histogram(
        filtered, x="prob_alive", nbins=30,
        color="segment", color_discrete_map=COLORS,
        title="Probability Still Active — by Segment",
        labels={"prob_alive": "P(Alive)"},
        barmode="overlay", opacity=0.7
    )
    fig8.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig8, use_container_width=True)

# ── Customer Explorer ─────────────────────────────────────────────
st.divider()
st.subheader("🔎 Customer Explorer")

search_id = st.text_input("Search Customer ID (e.g. CUST_00001)", "")
show_df = filtered[filtered["customer_id"].str.contains(search_id, case=False, na=False)] \
          if search_id else filtered

cols_show = ["customer_id", "segment", "recency", "frequency", "monetary",
             "prob_alive", "clv_90d", "clv_180d", "clv_365d",
             "acquisition_channel", "product_type"]
cols_show = [c for c in cols_show if c in show_df.columns]

st.dataframe(
    show_df[cols_show].sort_values("clv_365d", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=350
)

# ── LLM Explain (optional — requires GROQ key) ───────────────────
st.divider()
st.subheader("🤖 AI Customer Explanation (optional)")

groq_key = st.text_input("Groq API Key (leave blank to skip)", type="password")

if groq_key:
    cust_ids = filtered["customer_id"].tolist()
    chosen_id = st.selectbox("Pick a customer to explain", cust_ids)
    if st.button("Generate AI Explanation"):
        row = filtered[filtered["customer_id"] == chosen_id].iloc[0]
        try:
            from langchain_groq import ChatGroq
            from langchain.prompts import PromptTemplate
            llm = ChatGroq(model="llama-3.3-70b-versatile",
                           temperature=0.3, api_key=groq_key)
            template = (
                "You are a senior data scientist at a fintech company.\n"
                "Analyse this customer's CLV + RFM profile and give 3-4 sentence business insight.\n\n"
                "Segment: {segment} | Recency: {recency:.0f}d | Frequency: {frequency:.0f} repeats\n"
                "Avg spend: ₹{monetary:.0f} | P(alive): {prob_alive:.0%}\n"
                "CLV 90d: ₹{clv_90d:.0f} | CLV 365d: ₹{clv_365d:.0f}\n"
                "Product: {product_type} | Channel: {acquisition_channel}\n\n"
                "Write a concise, actionable business summary."
            )
            prompt = PromptTemplate(
                input_variables=["segment","recency","frequency","monetary",
                                 "prob_alive","clv_90d","clv_365d",
                                 "product_type","acquisition_channel"],
                template=template
            )
            chain = prompt | llm
            with st.spinner("Generating AI explanation..."):
                result = chain.invoke(row.to_dict())
            st.info(result.content)
        except Exception as e:
            st.error(f"LLM error: {e}")
else:
    st.caption("Enter your Groq API key above to enable AI explanations.")
