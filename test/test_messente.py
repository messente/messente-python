import unittest
import messente


class TestMessente(unittest.TestCase):
    def test_invalid_config_path(self):
        with self.assertRaises(messente.api.error.ConfigurationError):
            messente.Messente(ini_path="invalid-path.ini")

    def test_modules(self):
        api = messente.Messente()
        self.assertIsInstance(api.sms, messente.api.sms.SmsAPI)
        self.assertIsInstance(api.credit, messente.api.credit.CreditsAPI)
        self.assertIsInstance(api.delivery, messente.api.delivery.DeliveryAPI)
        apis = [api.sms, api.credit, api.delivery]
        for item in apis:
            self.assertIsInstance(item, messente.api.api.API)

    def test_error_messages(self):
        codes = messente.api.error.ERROR_CODES
        self.assertGreater(len(codes), 0)
        for c in codes:
            self.assertGreater(len(codes[c]), 0)
