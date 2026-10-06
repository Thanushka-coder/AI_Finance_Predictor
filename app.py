import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

from utils.database import add_expense, get_expenses


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    font-weight: 700;
}

.metric-card {
    background: linear-gradient(135deg, #161b22, #21262d);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363d;
}

.insight-box {
    background: #161b22;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #00c896;
    margin-bottom: 15px;
}

.warning-box {
    background: #161b22;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #ffb000;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATABASE
# ============================================================

def load_expenses():

    data = get_expenses()

    if not data:
        return pd.DataFrame(
            columns=[
                "Date",
                "Category",
                "Amount",
                "Description"
            ]
        )

    df = pd.DataFrame(data)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


expenses = load_expenses()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("💰 FinSight AI")

st.sidebar.caption(
    "AI-Powered Personal Finance Intelligence"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Command Center",
        "➕ Add Expense",
        "📊 Spending Intelligence",
        "🤖 AI Prediction",
        "🧠 Financial Health",
        "🎯 What-If Simulator",
        "🚨 Risk Detection"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "FinSight AI transforms your spending data "
    "into predictions, insights and financial warnings."
)


# ============================================================
# COMMAND CENTER
# ============================================================

if page == "🏠 Command Center":

    st.title("💰 FinSight AI")
    st.subheader("Your Personal Financial Intelligence System")

    if expenses.empty:

        st.info(
            "No expenses yet. Go to **➕ Add Expense** "
            "to start building your financial dataset."
        )

    else:

        total_spending = expenses["Amount"].sum()

        current_month = pd.Timestamp.today().month
        current_year = pd.Timestamp.today().year

        monthly_data = expenses[
            (expenses["Date"].dt.month == current_month)
            &
            (expenses["Date"].dt.year == current_year)
        ]

        monthly_spending = monthly_data["Amount"].sum()

        monthly_budget = 40000

        remaining = monthly_budget - monthly_spending

        if monthly_spending > 0:

            savings_rate = max(
                0,
                ((monthly_budget - monthly_spending)
                 / monthly_budget) * 100
            )

        else:

            savings_rate = 100

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Spending",
                f"₹{total_spending:,.0f}"
            )

        with col2:

            st.metric(
                "This Month",
                f"₹{monthly_spending:,.0f}"
            )

        with col3:

            st.metric(
                "Budget Remaining",
                f"₹{remaining:,.0f}"
            )

        with col4:

            st.metric(
                "Savings Rate",
                f"{savings_rate:.1f}%"
            )

        st.divider()

        # ----------------------------------------------------
        # CATEGORY ANALYSIS
        # ----------------------------------------------------

        st.subheader("📊 Spending Breakdown")

        category_data = (
            expenses
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.bar_chart(category_data)

        with col2:

            st.dataframe(
                category_data.rename("Total Amount"),
                use_container_width=True
            )

        # ----------------------------------------------------
        # TIMELINE
        # ----------------------------------------------------

        st.subheader("📈 Spending Timeline")

        timeline = (
            expenses
            .groupby("Date")["Amount"]
            .sum()
        )

        st.line_chart(timeline)

        # ----------------------------------------------------
        # AI SNAPSHOT
        # ----------------------------------------------------

        st.subheader("🧠 AI Financial Snapshot")

        highest_category = category_data.index[0]

        highest_amount = category_data.iloc[0]

        avg_daily = expenses.groupby(
            "Date"
        )["Amount"].sum().mean()

        st.markdown(
            f"""
            <div class="insight-box">
            <b>AI Insight</b><br><br>
            Your highest spending category is
            <b>{highest_category}</b> with
            <b>₹{highest_amount:,.0f}</b> spent.<br><br>

            Your average daily spending is approximately
            <b>₹{avg_daily:,.0f}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ADD EXPENSE
# ============================================================

elif page == "➕ Add Expense":

    st.title("➕ Add New Expense")

    st.write(
        "Every expense you add becomes part of your personal "
        "financial dataset."
    )

    st.divider()

    with st.form("expense_form"):

        expense_date = st.date_input(
            "📅 Date",
            value=date.today()
        )

        category = st.selectbox(
            "🏷️ Category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Health",
                "Education",
                "Travel",
                "Other"
            ]
        )

        amount = st.number_input(
            "💰 Amount (₹)",
            min_value=0.0,
            step=50.0
        )

        description = st.text_input(
            "📝 Description",
            placeholder="Example: Lunch at college"
        )

        submitted = st.form_submit_button(
            "💾 Save Expense",
            use_container_width=True
        )

        if submitted:

            if amount <= 0:

                st.error(
                    "Please enter an amount greater than ₹0."
                )

            else:

                add_expense(
                    expense_date,
                    category,
                    amount,
                    description
                )

                st.success(
                    "✅ Expense saved successfully!"
                )

                st.rerun()


# ============================================================
# SPENDING INTELLIGENCE
# ============================================================

elif page == "📊 Spending Intelligence":

    st.title("📊 Spending Intelligence")

    if expenses.empty:

        st.warning(
            "Add some expenses first to generate analytics."
        )

    else:

        category_data = (
            expenses
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("Category Spending")

        st.bar_chart(category_data)

        st.subheader("Expense History")

        display_df = expenses.sort_values(
            "Date",
            ascending=False
        )

        st.dataframe(
            display_df,
            use_container_width=True
        )

        st.subheader("📈 Daily Spending")

        daily = (
            expenses
            .groupby("Date")["Amount"]
            .sum()
        )

        st.line_chart(daily)


# ============================================================
# AI PREDICTION
# ============================================================

elif page == "🤖 AI Prediction":

    st.title("🤖 AI Expense Prediction")

    st.write(
        "FinSight estimates your future spending based "
        "on your historical expense behavior."
    )

    if len(expenses) < 5:

        st.warning(
            "⚠️ Add at least 5 expenses before generating "
            "a meaningful prediction."
        )

    else:

        daily_spending = (
            expenses
            .groupby("Date")["Amount"]
            .sum()
            .sort_index()
        )

        average_daily = daily_spending.mean()

        predicted_30_days = average_daily * 30

        predicted_7_days = average_daily * 7

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Predicted Next 7 Days",
                f"₹{predicted_7_days:,.0f}"
            )

        with col2:

            st.metric(
                "Predicted Next 30 Days",
                f"₹{predicted_30_days:,.0f}"
            )

        st.divider()

        st.subheader("Historical Spending Pattern")

        st.line_chart(daily_spending)

        st.markdown(
            f"""
            <div class="insight-box">
            <b>🤖 Prediction Insight</b><br><br>
            Based on your current spending pattern,
            FinSight estimates approximately
            <b>₹{predicted_30_days:,.0f}</b> of spending
            over the next 30 days.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "As more real expense data is collected, "
            "this module can be upgraded to a trained ML "
            "forecasting model such as XGBoost."
        )


# ============================================================
# FINANCIAL HEALTH
# ============================================================

elif page == "🧠 Financial Health":

    st.title("🧠 Financial Health Score")

    if expenses.empty:

        st.warning(
            "Add expenses to calculate your financial health."
        )

    else:

        total = expenses["Amount"].sum()

        daily = (
            expenses
            .groupby("Date")["Amount"]
            .sum()
        )

        avg_daily = daily.mean()

        monthly_estimate = avg_daily * 30

        budget = 40000

        utilization = monthly_estimate / budget

        if utilization < 0.50:

            score = 90

        elif utilization < 0.70:

            score = 80

        elif utilization < 0.85:

            score = 70

        elif utilization < 1.00:

            score = 55

        else:

            score = 35

        st.metric(
            "Financial Health Score",
            f"{score}/100"
        )

        st.progress(score / 100)

        if score >= 80:

            st.success(
                "🟢 Your projected spending is comfortably "
                "within the budget."
            )

        elif score >= 60:

            st.warning(
                "🟡 Your spending is approaching the "
                "recommended budget range."
            )

        else:

            st.error(
                "🔴 Your projected spending may exceed "
                "your monthly budget."
            )

        st.subheader("Health Factors")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Estimated Monthly Spending",
                f"₹{monthly_estimate:,.0f}"
            )

        with col2:

            st.metric(
                "Monthly Budget",
                f"₹{budget:,.0f}"
            )

        with col3:

            st.metric(
                "Budget Usage",
                f"{utilization * 100:.1f}%"
            )


# ============================================================
# WHAT-IF SIMULATOR
# ============================================================

elif page == "🎯 What-If Simulator":

    st.title("🎯 What-If Financial Simulator")

    st.write(
        "Experiment with your spending and see how it "
        "could affect your monthly budget."
    )

    monthly_income = st.number_input(
        "💵 Monthly Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    extra_spending = st.number_input(
        "🛒 Additional Monthly Spending",
        min_value=0.0,
        value=0.0,
        step=500.0
    )

    current_daily = (
        expenses.groupby("Date")["Amount"].sum().mean()
        if not expenses.empty
        else 0
    )

    projected = (current_daily * 30) + extra_spending

    savings = monthly_income - projected

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Projected Spending",
            f"₹{projected:,.0f}"
        )

    with col2:

        st.metric(
            "Projected Savings",
            f"₹{savings:,.0f}"
        )

    with col3:

        if monthly_income > 0:

            savings_rate = (
                savings / monthly_income
            ) * 100

        else:

            savings_rate = 0

        st.metric(
            "Savings Rate",
            f"{savings_rate:.1f}%"
        )

    if savings >= 0:

        st.success(
            "🟢 This scenario keeps you within your income."
        )

    else:

        st.error(
            "🔴 This scenario would exceed your income."
        )


# ============================================================
# RISK DETECTION
# ============================================================

elif page == "🚨 Risk Detection":

    st.title("🚨 Spending Risk Detection")

    if expenses.empty:

        st.warning(
            "Add expenses to detect unusual spending."
        )

    else:

        mean_amount = expenses["Amount"].mean()

        std_amount = expenses["Amount"].std()

        threshold = mean_amount + (2 * std_amount)

        risky_expenses = expenses[
            expenses["Amount"] > threshold
        ].sort_values(
            "Amount",
            ascending=False
        )

        st.metric(
            "Risk Threshold",
            f"₹{threshold:,.0f}"
        )

        if risky_expenses.empty:

            st.success(
                "🟢 No unusually large expenses detected."
            )

        else:

            st.warning(
                f"⚠️ {len(risky_expenses)} unusual "
                "expense(s) detected."
            )

            st.dataframe(
                risky_expenses,
                use_container_width=True
            )

            for _, row in risky_expenses.iterrows():

                st.markdown(
                    f"""
                    <div class="warning-box">
                    <b>🚨 Unusual Spending Detected</b><br><br>
                    Category: <b>{row['Category']}</b><br>
                    Amount: <b>₹{row['Amount']:,.0f}</b><br>
                    Description: {row['Description']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "FinSight AI • Personal Finance Intelligence"
)