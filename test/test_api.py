import unittest
import messente
from messente.api.config import configuration
from test import utils


module_name = "test-api"
username = "%s-username" % module_name
password = "%s-password" % module_name


class TestApi(unittest.TestCase):
    def test_configuration(self):
        api = messente.api.api.API(
            username=username,
            password=password,
            config_section=module_name,
            api_url=utils.TEST_URL
        )
        self.assertEqual(
            api.get_str_option("api_url"),
            utils.TEST_URL
        )

        new_url = "https://example.com/test_api/new_url"
        api.set_option("api_url", new_url)
        self.assertEqual(
            api.get_str_option("api_url"),
            new_url
        )

        self.assertTrue(module_name in configuration.sections())
        self.assertEqual(api.get_str_option("username"), username)
        self.assertEqual(api.get_str_option("password"), password)
