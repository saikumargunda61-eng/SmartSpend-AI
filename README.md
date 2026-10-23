# SmartSpend AI — Strands Decider 2B + Amazon Bedrock

A student-focused budgeting demo that routes a request to a suitable tool using **Strands Decider 2B**, then asks **Amazon Bedrock via Strands Agents** to explain the deterministic tool result.

> Status: starter implementation. It must be run and tested in your own environment before you claim it works or submit it. Decider 2B is experimental; this project is not financial advice.

## What makes the decision meaningful?

Decider 2B chooses one of three actions from the user's request and the supplied budget state:

- `CHECK_BUDGET`
- `CHECK_UPCOMING_EXPENSES`
- `GIVE_SAVING_ADVICE`

The typed choice question, options, HTTP wiring, confidence threshold, and tool dispatch are in `decision_pattern.py` and `app.py`. This is the reusable **tool-selection** recipe.

## Architecture

1. Streamlit collects a question and fictional demo budget values.
2. `decision_pattern.py` sends the state and typed choice question to the local Decider HTTP server.
3. The chosen deterministic Python tool calculates or summarizes budget information.
4. Strands Agents calls Amazon Bedrock to explain the tool result.
5. The UI shows the selected action, confidence, structured result, and explanation.

## Requirements

- Python 3.11 recommended
- A machine with enough memory to run the selected Decider 2B model (the model downloads weights on first use)
- AWS account/credentials with access to an enabled Amazon Bedrock model in your selected region
- Permission to use the chosen Bedrock model in that region

## Run locally

### 1. Create an environment and install packages

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
pip install strands-decider
```

### 2. Configure AWS credentials

Use an AWS profile or environment variables according to AWS guidance. Do not put access keys in source code or commit them.

```bash
aws configure
aws sts get-caller-identity
```

Confirm `AWS_REGION` and `BEDROCK_MODEL_ID` are valid for your account. Bedrock model availability and access differ by region/account.

### 3. Start Decider 2B

In terminal 1:

```bash
strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8099
```

The first start may download model weights. Keep this process running. If your machine cannot run the model, use a suitable machine you control and set `STRANDS_DECIDER_URL` to its reachable server URL; do not expose an unauthenticated server to the public internet.

### 4. Start SmartSpend

In terminal 2, from the project directory:

```bash
# Windows PowerShell
$env:AWS_REGION="us-east-1"
$env:BEDROCK_MODEL_ID="anthropic.claude-3-haiku-20240307-v1:0"
$env:STRANDS_DECIDER_URL="http://127.0.0.1:8099"
streamlit run app.py
```

For macOS/Linux use `export VARIABLE=value` instead. Choose a Bedrock model ID enabled for your AWS account and region.

## Example test prompts

- “Can I buy headphones for ₹2,000?”
- “What upcoming essentials should I reserve money for?”
- “Give me a few ways to save this month.”

Use the numeric controls in the UI as the source of truth for available money and upcoming expenses. The example parser for a purchase amount is intentionally simple; test it and improve it before relying on it.

## Reusable decision recipe

**Question type:** `choice`

**State:** user's request plus available spending money and upcoming essential expenses.

**Options:** `CHECK_BUDGET`, `CHECK_UPCOMING_EXPENSES`, `GIVE_SAVING_ADVICE`.

**Confidence behavior:** if returned confidence is below `0.60`, the app does not route to a strong recommendation and asks the user to clarify. The threshold is an initial heuristic, not a validated safety guarantee. Evaluate and tune it using a labelled test set.

**Reuse:** copy `decision_pattern.py`, update the typed question's instructions/options to match your own tools, keep strict option validation, and define a low-confidence fallback before executing a tool.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Evaluation plan

Before submission, run at least 15-30 labelled prompts across all three actions and ambiguous cases. Record expected action, actual action, confidence, and correctness. Report measured accuracy and latency only after collecting real results; do not invent benchmark numbers.

## Security and limitations

- Use fictional demo data; this is not connected to bank accounts.
- Never commit AWS credentials, `.env`, or personal financial information.
- Decider confidence is not a guarantee of correctness.
- The purchase-amount parser is a simple demo parser and can misread complex natural language.
- This app is a learning prototype, not a production financial product.
