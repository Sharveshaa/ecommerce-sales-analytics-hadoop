
import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="E-Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM THEME
# =====================================================

st.markdown("""
<style>
.stApp {
    background: #0e1117;
}
[data-testid="stMetric"] {
    background: #1c2333;
    border: 1px solid #30394b;
    padding: 20px;
    border-radius: 12px;
}
[data-testid="stMetricLabel"] {
    color: #aab4c5;
}
[data-testid="stMetricValue"] {
    color: white;
}
h1, h2, h3 {
    color: #f0f3f8;
}
.subtitle {
    color: #9ca9bb;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("📊 E-Commerce Intelligence")
st.markdown(
    '<p class="subtitle">Executive Sales Analytics | '
    'Apache Hadoop 3.5.0 | Python MapReduce</p>',
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# LOAD MAPREDUCE OUTPUT
# =====================================================

FILE_PATH = "analytics_results.txt"

@st.cache_data
def load_results():
    records = []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if "|" not in line:
                continue

            dimension, details = line.split("|", 1)

            match = re.search(
                r"Revenue:\s*([\d.]+)\s+"
                r"Quantity:\s*(\d+)\s+"
                r"Records:\s*(\d+)",
                details
            )

            if not match:
                continue

            name = details[:match.start()].strip()

            records.append({
                "Dimension": dimension.strip(),
                "Name": name,
                "Revenue": float(match.group(1)),
                "Quantity": int(match.group(2)),
                "Records": int(match.group(3))
            })

    return pd.DataFrame(records)


try:
    data = load_results()
except FileNotFoundError:
    st.error("analytics_results.txt not found.")
    st.stop()

if data.empty:
    st.error("No valid Hadoop output found.")
    st.stop()

# =====================================================
# SEPARATE DIMENSIONS
# =====================================================

products = data[data.Dimension == "PRODUCT"].copy()
regions = data[data.Dimension == "REGION"].copy()
categories = data[data.Dimension == "CATEGORY"].copy()
monthly = data[data.Dimension == "MONTH"].copy()
payments = data[data.Dimension == "PAYMENT"].copy()

if any(x.empty for x in [
    products, regions, categories, monthly, payments
]):
    st.error("One or more analytics dimensions are missing.")
    st.stop()

monthly["Name"] = pd.to_datetime(
    monthly["Name"],
    format="%Y-%m",
    errors="coerce"
)
monthly = monthly.dropna(subset=["Name"]).sort_values("Name")

# =====================================================
# HELPERS
# =====================================================

def inr(value):
    return f"₹{value:,.0f}"

def crore(value):
    return f"₹{value / 10000000:.2f} Cr"

def style_chart(fig, ax):
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#171d29")
    ax.tick_params(colors="#d7dfeb")
    ax.xaxis.label.set_color("#d7dfeb")
    ax.yaxis.label.set_color("#d7dfeb")
    ax.title.set_color("#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#394354")
    ax.grid(axis="x", alpha=0.18)

def bar_chart(frame, title, label, horizontal=True):
    frame = frame.sort_values("Revenue", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    style_chart(fig, ax)

    if horizontal:
        bars = ax.barh(
            frame["Name"],
            frame["Revenue"] / 10000000
        )
        ax.set_xlabel("Revenue (₹ Crore)")
        ax.set_ylabel("")
        for bar in bars:
            ax.text(
                bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                f"  {bar.get_width():.2f}",
                va="center",
                color="white",
                fontsize=8
            )
    else:
        bars = ax.bar(
            frame["Name"],
            frame["Revenue"] / 10000000
        )
        ax.set_ylabel("Revenue (₹ Crore)")
        ax.tick_params(axis="x", rotation=25)

    ax.set_title(title, fontsize=14, pad=15)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.caption("Filter individual analytics sections")

selected_products = st.sidebar.multiselect(
    "Products",
    sorted(products["Name"].unique()),
    default=sorted(products["Name"].unique())
)

selected_regions = st.sidebar.multiselect(
    "Regions",
    sorted(regions["Name"].unique()),
    default=sorted(regions["Name"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Categories",
    sorted(categories["Name"].unique()),
    default=sorted(categories["Name"].unique())
)

# Independent dimension filters
p = products[products.Name.isin(selected_products)]
r = regions[regions.Name.isin(selected_regions)]
c = categories[categories.Name.isin(selected_categories)]

st.sidebar.divider()
st.sidebar.caption("Source: Hadoop MapReduce output")
st.sidebar.caption("Dataset: 10,000 synthetic transactions")

# =====================================================
# KPI OVERVIEW
# =====================================================

# KPIs use the complete dataset and remain independent
# of the individual chart filters.

total_revenue = categories["Revenue"].sum()
total_orders = int(categories["Records"].sum())
total_units = int(categories["Quantity"].sum())
average_order = total_revenue / total_orders

st.subheader("Business Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Revenue", crore(total_revenue))
k2.metric("Transactions", f"{total_orders:,}")
k3.metric("Units Sold", f"{total_units:,}")
k4.metric("Average Order Value", inr(average_order))

st.caption("KPIs represent the complete dataset.")
st.divider()

# =====================================================
# PRODUCT PERFORMANCE
# =====================================================

st.subheader("🏆 Product Intelligence")

left, right = st.columns([1.4, 1])

with left:
    bar_chart(p, "Revenue by Product", "Product")

with right:
    st.markdown("#### Top 5 Products")
    top = p.sort_values("Revenue", ascending=False).head(5)

    st.dataframe(
        top[["Name", "Revenue", "Quantity", "Records"]]
        .rename(columns={
            "Name": "Product",
            "Revenue": "Revenue (₹)",
            "Quantity": "Units",
            "Records": "Orders"
        }),
        hide_index=True,
        use_container_width=True
    )

    if not p.empty:
        best = p.loc[p["Revenue"].idxmax()]
        st.success(
            f"Revenue leader: {best['Name']} "
            f"({crore(best['Revenue'])})"
        )

st.divider()

# =====================================================
# MONTHLY SALES TREND
# =====================================================

st.subheader("📅 Monthly Revenue Trend")

fig, ax = plt.subplots(figsize=(12, 4))
style_chart(fig, ax)

ax.plot(
    monthly["Name"],
    monthly["Revenue"] / 10000000,
    marker="o",
    linewidth=2.5,
    markersize=7
)

ax.fill_between(
    monthly["Name"],
    monthly["Revenue"] / 10000000,
    alpha=0.15
)

ax.set_ylabel("Revenue (₹ Crore)")
ax.set_xlabel("Month")
ax.set_title("Monthly Sales Performance", fontsize=14)
ax.tick_params(axis="x", rotation=30)

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

best_month = monthly.loc[monthly["Revenue"].idxmax()]
worst_month = monthly.loc[monthly["Revenue"].idxmin()]

m1, m2 = st.columns(2)
m1.success(
    f"Best month: {best_month['Name'].strftime('%B %Y')} "
    f"| {crore(best_month['Revenue'])}"
)
m2.warning(
    f"Lowest month: {worst_month['Name'].strftime('%B %Y')} "
    f"| {crore(worst_month['Revenue'])}"
)

st.divider()

# =====================================================
# REGIONAL ANALYSIS
# =====================================================

st.subheader("🌍 Regional Intelligence")

left, right = st.columns([1.3, 1])

with left:
    bar_chart(r, "Revenue by Region", "Region")

with right:
    st.markdown("#### Regional Summary")
    st.dataframe(
        r.sort_values("Revenue", ascending=False)
        .rename(columns={
            "Name": "Region",
            "Revenue": "Revenue (₹)",
            "Quantity": "Units",
            "Records": "Orders"
        }),
        hide_index=True,
        use_container_width=True
    )

st.divider()

# =====================================================
# CATEGORY ANALYSIS
# =====================================================

st.subheader("🛍️ Category Contribution")

left, right = st.columns(2)

with left:
    category_data = c.sort_values("Revenue", ascending=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    ax.pie(
        category_data["Revenue"],
        labels=category_data["Name"],
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.75,
        textprops={"color": "white"},
        wedgeprops={"width": 0.42, "edgecolor": "#0e1117"}
    )

    ax.set_title(
        "Revenue Share by Category",
        color="white",
        fontsize=14
    )

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.markdown("#### Category Summary")

    st.dataframe(
        category_data.rename(columns={
            "Name": "Category",
            "Revenue": "Revenue (₹)",
            "Quantity": "Units",
            "Records": "Orders"
        }),
        hide_index=True,
        use_container_width=True
    )

st.divider()

# =====================================================
# PAYMENT ANALYSIS
# =====================================================

st.subheader("💳 Payment Method Intelligence")

left, right = st.columns(2)

with left:
    payment_data = payments.sort_values(
        "Revenue", ascending=False
    )

    bar_chart(
        payment_data,
        "Revenue by Payment Method",
        "Payment"
    )

with right:
    st.markdown("#### Payment Distribution")

    st.dataframe(
        payment_data.rename(columns={
            "Name": "Payment",
            "Revenue": "Revenue (₹)",
            "Quantity": "Units",
            "Records": "Transactions"
        }),
        hide_index=True,
        use_container_width=True
    )

    best_payment = payment_data.iloc[0]
    st.success(
        f"Leading payment method: {best_payment['Name']}"
    )

st.divider()

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("💡 Executive Insights")

best_product = products.loc[products["Revenue"].idxmax()]
best_region = regions.loc[regions["Revenue"].idxmax()]
best_category = categories.loc[categories["Revenue"].idxmax()]
best_payment = payments.loc[payments["Revenue"].idxmax()]

i1, i2 = st.columns(2)

with i1:
    st.info(
        f"🏆 **Product leader:** {best_product['Name']} "
        f"generated {crore(best_product['Revenue'])}."
    )
    st.info(
        f"🌍 **Regional leader:** {best_region['Name']} "
        f"generated {crore(best_region['Revenue'])}."
    )

with i2:
    st.info(
        f"🛍️ **Category leader:** {best_category['Name']} "
        f"generated {crore(best_category['Revenue'])}."
    )
    st.info(
        f"💳 **Payment leader:** {best_payment['Name']} "
        f"generated {crore(best_payment['Revenue'])}."
    )

# =====================================================
# DOWNLOAD ANALYTICS
# =====================================================

st.divider()
st.subheader("📥 Export Analytics")

csv_data = data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Analytics CSV",
    data=csv_data,
    file_name="hadoop_sales_analytics.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#8995a8;">
        <b>E-Commerce Intelligence Dashboard</b><br>
        Apache Hadoop 3.5.0 | HDFS | YARN |
        Python Hadoop Streaming | MapReduce | Streamlit<br><br>
        10,000 Synthetic Transactions |
        January–December 2025
    </div>
    """,
    unsafe_allow_html=True
)
