import unittest
from tools import check_budget, check_upcoming_expenses, saving_advice

class ToolTests(unittest.TestCase):
    def test_budget_math_with_clear_amount(self):
        result = check_budget(5000, 1800, "Can I buy headphones for ₹2,000?")
        self.assertEqual(result["data"]["remaining_after_essentials_inr"], 3200)
        self.assertEqual(result["data"]["purchase_amount_inr"], 2000)
        self.assertTrue(result["data"]["purchase_fits_remaining_budget"])

    def test_purchase_exceeds_remaining(self):
        result = check_budget(3000, 1800, "Can I buy headphones for ₹2,000?")
        self.assertFalse(result["data"]["purchase_fits_remaining_budget"])

    def test_upcoming_expenses(self):
        result = check_upcoming_expenses(5000, 1800, "What about bills?")
        self.assertEqual(result["data"]["remaining_after_essentials_inr"], 3200)

    def test_saving_advice(self):
        result = saving_advice(5000, 1800, "How can I save?")
        self.assertIn("₹3,200", result["summary"])

if __name__ == "__main__":
    unittest.main()
