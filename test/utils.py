# -*- coding: utf-8 -*-

import re

TEST_BASE_URL = "https://example.com"
TEST_URL = "%s/api" % TEST_BASE_URL
TEST_ANY_URL = re.compile(TEST_URL + "/.*")
TEST_DLR_URL = "%s/dlr" % TEST_BASE_URL
TEST_DLR_ANY_URL = re.compile(TEST_DLR_URL + "/.*")


def mock_response(http_code, response_text, **kwargs):
    def request_callback(request):
        return (http_code, kwargs.get("headers", {}), str(response_text))

    return request_callback
