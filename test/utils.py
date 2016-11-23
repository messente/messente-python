import responses
import re


TEST_URL = "https://example.com"
ANY_URL = re.compile(TEST_URL + "/.*")


def mock_response(http_code, response_text):
    def request_callback(request):
        return (http_code, {}, str(response_text))
    return request_callback
