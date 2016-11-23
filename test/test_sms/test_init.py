import unittest
from messente.api import sms
from messente.api.error import ConfigurationError


class TestInit(unittest.TestCase):
    def test_invalid_config_path(self):
        with self.assertRaises(ConfigurationError):
            sms.SmsAPI(
                ini_path="non-existent-and-thus-invalid.ini"
            )
