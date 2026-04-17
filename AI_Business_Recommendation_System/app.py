from utils.preprocessing import load_data, preprocess_data
from utils.prediction import train_model, predict_sales, calculate_metrics
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI System", layout="wide")

st.markdown("""
<style>
/* Main background */
body {
    background-color: #0E1117;
}

/* Card style */
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1E1E2F;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Titles */
h1, h2, h3 {
    color: #FFFFFF;
}

/* Text */
.stMarkdown {
    color: #D1D5DB;
}
</style>
""", unsafe_allow_html=True)

# Import your recommendation logic
from utils.recommendation import generate_recommendations, generate_insights


st.title("AI-Based Business Recommendation System")

# Sidebar Navigation
st.sidebar.title("🤖 AI System")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "",
    ["📊 Dashboard", "📂 Upload Data", "📈 Predictions", "💡 Recommendations", "📄 Reports"]
)

# ---------------- DASHBOARD ----------------
if page == "📊 Dashboard":
    st.markdown("## 📊 Dashboard")

    if "data" not in st.session_state:
        st.warning("Please upload data first!")
    else:
        data = st.session_state["data"]

        col1, col2, col3 = st.columns(3)

        col1.metric("📦 Total Sales", f"{data['Sales'].sum():,.0f}")
        col2.metric("📊 Avg Sales", f"{data['Sales'].mean():,.0f}")
        col3.metric("🔥 Peak Sales", f"{data['Sales'].max():,.0f}")

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Total Sales", f"{data['Sales'].sum():,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Average Sales", f"{data['Sales'].mean():,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Peak Sales", f"{data['Sales'].max():,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Chart
        import plotly.express as px

        fig = px.line(data, x="Order Date", y="Sales", title="Sales Trend")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- UPLOAD ----------------
elif page == "📂 Upload Data":
    st.header("Upload Dataset")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = load_data(uploaded_file)
        df = preprocess_data(df)

        st.session_state["data"] = df  # store data

        st.success("Data uploaded and processed!")
        st.dataframe(df)

# ---------------- PREDICTIONS ----------------
elif page == "📈 Predictions":
    st.markdown("## 📈 Predictions")

    if "data" not in st.session_state:
        st.warning("Please upload data first!")
    else:
        data = st.session_state["data"]

        model, processed_data = train_model(data)
        predictions = predict_sales(model, processed_data)

        last_date = processed_data["Order Date"].iloc[-1]
        future_dates = pd.date_range(start=last_date, periods=8)[1:]

        pred_df = pd.DataFrame({
            "Order Date": future_dates,
            "Predicted Sales": predictions
        })

        st.markdown("### 📊 Forecast Data")
        st.dataframe(pred_df)

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=processed_data["Order Date"],
            y=processed_data["Sales"],
            mode='lines',
            name='Actual'
        ))

        fig.add_trace(go.Scatter(
            x=pred_df["Order Date"],
            y=pred_df["Predicted Sales"],
            mode='lines',
            name='Predicted'
        ))

        st.plotly_chart(fig, use_container_width=True)

        metrics = calculate_metrics(processed_data, predictions)

        st.markdown("### 📉 Performance Insights")
        st.metric("Vs Last Day", f"{metrics['percent_change_vs_last_day']:.2f}%")
        st.metric("Vs Average", f"{metrics['percent_change_vs_average']:.2f}%")
        st.metric("Vs Peak", f"{metrics['percent_change_vs_peak']:.2f}%")

        st.session_state["metrics"] = metrics
        st.session_state["predictions"] = predictions

        change = metrics['percent_change_vs_last_day']

        if change < 0:
            st.error(f"Sales Decreasing: {change:.2f}%")
        else:
            st.success(f"Sales Increasing: {change:.2f}%")

# ---------------- RECOMMENDATIONS ----------------
elif page == "💡 Recommendations":
    st.markdown("## 💡 AI Recommendations")

    if "metrics" not in st.session_state:
        st.warning("Run predictions first!")
    else:
        metrics = st.session_state["metrics"]
        predictions = st.session_state["predictions"]

        insight = generate_insights(metrics)

        st.markdown(f"""
        <div class="card">
        <h3>🤖 AI Insight</h3>
        <p style="font-size:16px;">{insight}</p>
        </div>
        """, unsafe_allow_html=True)

        recs = generate_recommendations(predictions, metrics)

        for rec in recs:
            st.markdown(f"""
            <div class="card">
            <h4>{rec['title']}</h4>
            <p>{rec['description']}</p>
            <p><b>Impact:</b> {rec['expected_impact']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------- REPORTS ----------------
elif page == "📄 Reports":
    st.header("Reports")

    st.write("Summary Report")

    st.download_button("Download Report", "Report content here")

st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>
AI Business Recommendation System • Built with Streamlit
</p>
""", unsafe_allow_html=True)