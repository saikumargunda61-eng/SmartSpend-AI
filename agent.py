"""Generative explanation via Strands Agents with Amazon Bedrock."""
import os
from strands import Agent
from strands.models import BedrockModel

def explain_with_bedrock(question: str, result: dict, available: int, upcoming: int) -> str:
    model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    region = os.getenv("AWS_REGION", "us-east-1")
    model = BedrockModel(model_id=model_id, region_name=region)
    agent = Agent(
        model=model,
        system_prompt=(
            "You are SmartSpend AI, a cautious educational budgeting helper for students. "
            "Explain the supplied structured tool result in plain language. Never invent "
            "financial data. Do not request credentials or account numbers. State that this "
            "is educational guidance, not professional financial advice. If the tool result "
            "says the purchase amount is missing or decision confidence is low, ask a concise "
            "clarifying question instead of guessing."
        ),
    )
    prompt = (
        f"User question: {question}\n"
        f"Available spending money (INR): {available}\n"
        f"Upcoming essential expenses (INR): {upcoming}\n"
        f"Selected tool result (treat as source of truth): {result}\n"
        "Explain the result in 2-4 concise sentences."
    )
    response = agent(prompt)
    return str(response)
