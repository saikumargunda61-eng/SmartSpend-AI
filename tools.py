"""Deterministic tools used after Decider 2B selects an action."""
import re

def _purchase_amount(question: str):
    # Simple demo parser: finds currency-like numbers; production code should use
    # a validated structured input or robust parser instead.
    values = re.findall(r"(?:₹|rs\.?\s*)\s*([0-9,]+)|\b([0-9,]+)\s*(?:inr|rupees)\b", question, flags=re.I)
    nums = []
    for pair in values:
        raw = next((x for x in pair if x), "")
        if raw:
            nums.append(int(raw.replace(",", "")))
    # Avoid treating the budget examples as a purchase; only use this when a
    # purchase cue is present, and take the first parsed amount as a best-effort demo.
    if any(word in question.lower() for word in ["buy", "purchase", "cost", "price", "headphones", "phone", "laptop"]):
        return nums[0] if nums else None
    return None

def check_budget(available: int, upcoming: int, question: str) -> dict:
    remaining = available - upcoming
    purchase = _purchase_amount(question)
    affordable = None if purchase is None else purchase <= remaining
    if purchase is None:
        summary = f"After setting aside ₹{upcoming:,} for upcoming essentials, ₹{remaining:,} remains. Provide a clear planned purchase amount to compare affordability."
    elif affordable:
        summary = f"₹{remaining:,} remains after essential expenses. The planned purchase of ₹{purchase:,} fits within that amount, leaving ₹{remaining-purchase:,}."
    else:
        summary = f"₹{remaining:,} remains after essential expenses. The planned purchase of ₹{purchase:,} exceeds that amount by ₹{purchase-remaining:,}."
    return {"tool": "check_budget", "summary": summary, "data": {
        "available_inr": available, "upcoming_expenses_inr": upcoming,
        "remaining_after_essentials_inr": remaining, "purchase_amount_inr": purchase,
        "purchase_fits_remaining_budget": affordable
    }}

def check_upcoming_expenses(available: int, upcoming: int, question: str) -> dict:
    remaining = available - upcoming
    return {"tool": "check_upcoming_expenses",
            "summary": f"Your entered upcoming essential expenses total ₹{upcoming:,}. Setting that amount aside leaves ₹{remaining:,} from the ₹{available:,} available.",
            "data": {"available_inr": available, "upcoming_expenses_inr": upcoming,
                     "remaining_after_essentials_inr": remaining}}

def saving_advice(available: int, upcoming: int, question: str) -> dict:
    remaining = available - upcoming
    return {"tool": "saving_advice",
            "summary": f"Start by reserving ₹{upcoming:,} for essentials, then plan discretionary spending from the remaining ₹{remaining:,}. Compare alternatives, wait 24 hours before non-essential purchases, and avoid borrowing just to buy wants.",
            "data": {"available_inr": available, "upcoming_expenses_inr": upcoming,
                     "remaining_after_essentials_inr": remaining}}
