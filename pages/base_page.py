# base_page.py
import logging
from jsonschema import validate, ValidationError
import pytest
from utils.helpers import *
import time
from utils.logger import LOGGER

class BasePage():
    default_timeout = 10
    logger = LOGGER
    file_content = "input_content_file"


    def verify_status_code(self, actual, expected):
        assert actual == expected, "Status Code mismatch"

    def get_test_data(self, test_data_file):
        test_data = read_data_from_json(test_data_file + ".json")
        return test_data



    def verify_response_headers(self, response_data):
        assert 'Content-Type' in response_data.headers

    def validate_response_schema(self, response_json, schema_reference):
        if schema_reference == "get_public_gists":
            file = "response_schema_get_public.json"
        elif schema_reference == "create_gist":
            file = "response_schema_create_gist.json"
        elif schema_reference=="get_gist_by_id":
            file = "response_schema_get_gist_by_id.json"
        elif schema_reference=="list_user_gists":
            file = "response_schema_list_user_gists.json"
        expected_schema = read_data_from_json(file)

        try:
            validate(response_json, expected_schema)==True,"Response Schema validation failed"
        except ValidationError as e:
            self.logger.info(e)
            pytest.fail("Response Schema validation failed!"+str(e))


    def request_data_file(self,size):
        file_name = self.file_content
        create_data_file(file_name,size)
        content = read_data_file(file_name)
        return content

    def waitFor(self,seconds):
        time.sleep(seconds)

