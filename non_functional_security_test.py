import unittest
from Payment_Processing import PaymentProcessing

class TestPaymentSecurity(unittest.TestCase):
    """
    Non-functional security test:
    Makes sure that code doesnt allow dangerous inputs
    """

    def test_rejects_potentially_malicious_input(self):
        """
        tests that program doesnt allow sql injections as card number
        """
        pp = PaymentProcessing()

        order = {"total_amount": 10.00}
        malicious_payment_details = {
            "card_number": "1234'; DROP TABLE users; --",
            "expiry_date": "12/25",
            "cvv": "123"
        }

        # Odotamme virheen tulevan validoinnista
        result = pp.process_payment(order, "credit_card", malicious_payment_details)

        # Maksun EI pidä mennä läpi — pitäisi antaa virheilmoitus
        self.assertIn("Error", result)


if __name__ == "__main__":
    unittest.main()
