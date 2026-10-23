# Demo video script (target: 2 minutes 20 seconds)

**0:00–0:15 — Introduction**
“SmartSpend AI is a student budgeting agent. Strands Decider 2B chooses which tool should run, and Amazon Bedrock explains the result.”

**0:15–0:35 — Show architecture**
Briefly show `decision_pattern.py`, the three explicit options, and the local Decider server running.

**0:35–1:10 — First live request**
Enter fictional budget values and ask: “Can I buy headphones for ₹2,000?” Show the actual selected action, confidence, tool output, and Bedrock explanation.

**1:10–1:40 — Second request**
Ask for saving advice or upcoming-expense help. Show whether Decider selects a different tool and explain why the routing matters.

**1:40–2:05 — Reusable pattern**
Show `DECISION_PATTERN.md`: typed question, option set, wiring, and low-confidence fallback.

**2:05–2:20 — Close**
“This is an experimental learning prototype. The repository contains setup instructions and a reusable tool-selection recipe.”

Only record actual output from a running, tested implementation. Keep the video publicly accessible and under three minutes.
