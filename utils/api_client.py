# api_helpers.py
from pages.base_page import BasePage
import pytest
import requests
from requests.exceptions import Timeout
from utils.config import API_BASE_URL, API_TOKEN


class APIClient(BasePage):
    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def post_req(self, endpoint, gist_data):
        url = self.base_url + endpoint
        return requests.post(url, headers=self.headers, json=gist_data)

    def post_req_unauthorized(self,endpoint,gist_data):
        url= self.base_url + endpoint
        return requests.post(url,json=gist_data)

    def get_response_unauthorized(self,endpoint, public=None, parameters=None, headers=None):
        url = self.base_url + endpoint
        try:
            resp = requests.get(url, params=parameters, headers=headers, timeout=2)
        except Timeout:
            status_code = lambda status_code: (resp.status_code) if resp else None
            pytest.fail("Request timed out", status_code)
        return resp

    def delete(self, endpoint):
        url = self.base_url + endpoint
        return requests.delete(url, headers=self.headers)

    def get_response(self, endpoint, parameters=None, headers=None):
        url = self.base_url + endpoint
        if headers:
            headers = self.headers.update(headers)
        else:
            headers = self.headers
        try:
            resp = requests.get(url, params=parameters, headers=headers, timeout=2)
        except Timeout:
            status_code = lambda status_code: (resp.status_code) if resp else None
            pytest.fail("Request timed out", status_code)
        return resp
