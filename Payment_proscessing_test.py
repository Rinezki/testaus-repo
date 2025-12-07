import unittest
from Payment_Processing import PaymentProcessing

class TestPaymentProcessingFunctional(unittest.TestCase):
    """
    Functional test that tests payment processing
    """

    def test_full_payment_flow_success(self):
        """
        Tests successful payment process
        """
        pp = PaymentProcessing()

        order = {"total_amount": 50.00}
        payment_details = {
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }

        result = pp.process_payment(order, "credit_card", payment_details)

        # mock_payment_gateway palauttaa success, koska kortti ei ole kielletty.
        self.assertEqual(result, "Payment successful, Order confirmed")


if __name__ == "__main__":
    unittest.main()
