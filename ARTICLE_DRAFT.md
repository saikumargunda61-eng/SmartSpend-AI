# SmartSpend AI: A Decider-Powered Agent for Smarter Student Spending

## The problem
Students often need to decide whether a planned purchase fits their budget while accounting for upcoming expenses. SmartSpend AI explores whether a small decision model can route these requests to the right tool before a generative model explains the result.

## What it does
SmartSpend AI is a student-focused budgeting demo built with Strands Decider 2B, Strands Agents, and Amazon Bedrock. It accepts a question and user-entered demo budget values, selects a tool, runs deterministic calculations, and asks Bedrock to explain the result.

## The decision delegated to Decider 2B
The project demonstrates **tool selection**. Given the user's request and budget state, Decider 2B chooses `CHECK_BUDGET`, `CHECK_UPCOMING_EXPENSES`, or `GIVE_SAVING_ADVICE`. The choice determines which tool runs next.

## Reusable decision recipe
The public repository includes the typed choice question, explicit options, API wiring, option validation, confidence handling, and instructions for adapting the recipe. Low-confidence choices trigger a clarification fallback rather than an assertive recommendation.

## Implementation and evaluation
[After testing, describe the environment, Bedrock model ID, Decider model, number of test prompts, tool-selection accuracy, and measured latency. Do not publish unmeasured claims.]

## Demo
[Add a public video link under three minutes showing a prompt, Decider's selected action and confidence, the selected tool's output, and the Bedrock explanation.]

## What I learned
[Replace with your actual observations from implementation, including errors, ambiguous cases, and what you changed.]

## Tags
#strands-decider-2b #tool-selection
