# gist_page.py
from pages.base_page import BasePage
from utils.config import OWNER

class GistPage(BasePage):

    GET_USER_GISTS = '/gists'
    CREATE_GIST = '/gists'

    def __init__(self, api_client):
        self.api_client = api_client

    def create_gist(self,gist_data,additional_endpoint=None):
        if additional_endpoint:
            endpoint =self.CREATE_GIST+additional_endpoint
        endpoint = self.CREATE_GIST
        return self.api_client.post_req(endpoint, gist_data)

    # def get_gists_belowng_to_owner(self):

    def create_gist_bulk(self,num_of_gists):
        req_body = self.get_test_data("create_gist")["valid_data"]
        self.logger.info("Creating Gists: " +str(num_of_gists))
        for i in range(num_of_gists):
            req_body['description'] = req_body['description'] + str(i)
            list(req_body['files'].values())[0]['content'] = "Testing Content" + str(i)
            response_data_post = self.create_gist(req_body)
            assert response_data_post.status_code == 201, f"Failed to create gist {response_data_post.json()['message']}"
        self.logger.info(f"Created {num_of_gists} user gists successfully!")


    def create_gist_unauthorized(self,gist_data):
        endpoint=self.CREATE_GIST
        return self.api_client.post_req_unauthorized(endpoint,gist_data)

    def list_gist_by_id(self,endpoint):
        self.logger.info(f"GET {endpoint}")
        return self.api_client.get_response(endpoint)

    def list_gists(self, endpoint=GET_USER_GISTS, parameters=None, headers=None):
        return self.api_client.get_response(endpoint=endpoint, parameters=parameters, headers=headers)

    def del_gists(self, endpoint):
        return self.api_client.delete(endpoint)

    def del_all_gists(self):
        response_data = self.list_gists('/gists')
        assert response_data.status_code == 200, "Failed to get gists"
        response_data = response_data.json()
        num_of_gists = len(response_data)
        self.logger.info("Deleting the Gists ...")
        while True:
            response_data = self.list_gists('/gists')
            response_data = response_data.json()
            num_of_gists=len(response_data)
            if num_of_gists==0:
                break
            for r in range(num_of_gists):
                user_gist_id = response_data[r]['id']
                self.del_gists('/gists/%s' % user_gist_id)
        self.logger.info("Data clean up done!!")

    def list_public_gists(self, endpoint, parameters=None, headers=None):
        return self.api_client.get_response(endpoint, parameters, headers=headers)

    def list_gists_for_unauthorized(self,endpoint,parameters=None,headers=None):
        return self.api_client.get_response_unauthorized(endpoint, parameters, headers=headers)

    def get_owner(self):
        return OWNER


