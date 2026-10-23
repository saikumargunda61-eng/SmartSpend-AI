import os
import streamlit as st
from decision_pattern import choose_action, DECIDER_URL
from agent import explain_with_bedrock
from tools import check_budget, check_upcoming_expenses, saving_advice

st.set_page_config(page_title="SmartSpend AI", page_icon="💸", layout="centered")
st.title("💸 SmartSpend AI")
st.caption("A student spending assistant powered by Strands Decider 2B + Amazon Bedrock")
st.info("Demo mode: use fictional values only. This is an educational budgeting helper, not financial advice.")

with st.sidebar:
    st.header("Your demo budget")
    available = st.number_input("Available spending money (₹)", min_value=0, value=5000, step=500)
    upcoming = st.number_input("Upcoming essential expenses (₹)", min_value=0, value=1800, step=100)
    st.caption("These values stay in this session; do not enter bank credentials or sensitive data.")
    st.markdown(f"**Decider endpoint:** `{DECIDER_URL}`")

question = st.text_area(
    "What would you like help deciding?",
    value="Can I buy headphones for ₹2,000 if I have ₹5,000 available and ₹1,800 in upcoming expenses?",
    height=100,
)
if st.button("Make a decision", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Enter a question first.")
        st.stop()
    state = (
        f"User request: {question}\n"
        f"Available spending money in INR: {available}\n"
        f"Upcoming essential expenses in INR: {upcoming}"
    )
    with st.spinner("Decider 2B is selecting the next action..."):
        try:
            decision = choose_action(state)
        except Exception as e:
            st.error(
                "Could not reach the Decider 2B server. Start it using the README instructions. "
                f"Technical detail: {e}"
            )
            st.stop()

    st.subheader("Decider 2B decision")
    c1, c2 = st.columns(2)
    c1.metric("Selected action", decision["choice"])
    c2.metric("Confidence", f'{decision["confidence"]:.1%}')
    st.caption(f"Decision model: {decision.get('model', 'Strands Decider 2B')}")

    if decision["confidence"] < 0.60:
        st.warning("Confidence is below 60%. SmartSpend will avoid making a strong recommendation; try clarifying your question.")
        result = {
            "tool": "clarify",
            "summary": "The decision model was not confident enough to select a tool reliably.",
            "data": {"available_inr": available, "upcoming_expenses_inr": upcoming},
        }
    elif decision["choice"] == "CHECK_BUDGET":
        result = check_budget(available, upcoming, question)
    elif decision["choice"] == "CHECK_UPCOMING_EXPENSES":
        result = check_upcoming_expenses(available, upcoming, question)
    else:
        result = saving_advice(available, upcoming, question)

    st.subheader("Tool result")
    st.write(result["summary"])
    with st.expander("Inspect structured tool output"):
        st.json(result)

    with st.spinner("Amazon Bedrock is preparing an explanation..."):
        try:
            answer = explain_with_bedrock(question, result, available, upcoming)
            st.subheader("SmartSpend's explanation")
            st.write(answer)
        except Exception as e:
            st.warning(
                "The decision and tool ran, but the Bedrock explanation could not be generated. "
                "Check AWS credentials, region, and Bedrock model access. "
                f"Technical detail: {e}"
            )
            st.write(result["summary"])

st.divider()
st.caption("Decision pattern: #tool-selection | Experimental model: use for learning, not production decisions.")
