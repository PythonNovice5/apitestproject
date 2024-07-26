import pytest
from pages.base_page import BasePage
from pages.gist_page import GistPage


class TestGists(BasePage):

    @pytest.fixture(scope="module",autouse=True)
    def clean_up(self,api_client):
        self.pageObj(api_client)
        yield
        self.gistObj.del_all_gists()

    @pytest.mark.testt123
    @pytest.mark.parametrize("datatype",["valid_data_public"])
    def test_gist_for_the_user(self,api_client,datatype):
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        response_data = self.gistObj.create_gist(req_body)
        assert response_data.status_code == 201, f"Failed to create gist {response_data.json()['message']} "
        resp_json_create = response_data.json()
        username = resp_json_create['owner']['login']
        gist_id = resp_json_create['id']

        response_data_get_lists = self.gistObj.list_gists(f"/users/{username}/gists")
        res_json_lists = response_data_get_lists.json()
        resp_status_code = response_data_get_lists.status_code
        assert resp_status_code == 200, "Couldn't fetch the gist " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Response recieved successfully - {resp_status_code}\n\n")

        res_json_lists = response_data_get_lists.json()
        num_responses = len(res_json_lists)
        for i in range(num_responses):
            if res_json_lists[i]['id']==gist_id:
                break
            else:
                continue


    @pytest.mark.smoke
    @pytest.mark.critical
    def test_basic_get_gist(self,api_client):
        self.logger.info("############## TEST FOR GET '/GISTS' AND TO VALIDATE AUTHORIZATION FOR FURTHER TESTING  ############### ")
        self.pageObj(api_client)
        self.gistObj.create_gist_bulk(10)
        response_get = self.gistObj.list_gists()
        response_get_json = response_get.json()
        resp_status_code = response_get.status_code
        assert resp_status_code == 200, "Couldn't fetch the gist " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Response recieved successfully - {resp_status_code}\n\n")


    @pytest.mark.parametrize("datatype", ["valid_data"])
    @pytest.mark.critical
    def test_valid_create_gist(self, api_client, datatype,clean_up):
        self.logger.info("############# TEST - Verifying Create /gist by the authorized user")
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        response_data = self.gistObj.create_gist(req_body)

        assert response_data.status_code == 201, f"Failed to create gist {response_data.json()['message']} "
        resp_json = response_data.json()
        post_response_gist_id = resp_json['id']
        self.logger.info("Gist created successfully with id: " +post_response_gist_id)

        self.logger.info(" ---- ##### Verifying the Response Schema for Creating a Gist ###### ---")
        self.gistObj.validate_response_schema(resp_json, "create_gist")

        self.logger.info("##################### Getting the Gist details from the server ###############")
        response_data = self.gistObj.list_gist_by_id(f"/gists/{post_response_gist_id}")
        self.logger.info(f"Got the response with gist id: {post_response_gist_id} using GET '/gist/gistID' ")
        resp_status_code = response_data.status_code
        resp_get_json = response_data.json()

        assert resp_status_code == 200, "Couldn't fetch the gist " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Response recieved successfully - {response_data.status_code}")

        self.logger.info("Verifying the Response Schema for listing a Gist by ID")
        self.gistObj.validate_response_schema(resp_json, "get_gist_by_id")

        assert resp_get_json['id'] == post_response_gist_id, "The resource returned is not the same"
        self.logger.info("The resource returned is same as created earlier")


    @pytest.mark.critical
    @pytest.mark.parametrize("datatype", ["valid_data"])
    def test_private_gist_accessibility(self,api_client,datatype):
        self.logger.info("############# TEST - Verifying Private GIST accessibility for unauthorized user ")
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        response_data = self.gistObj.create_gist(req_body)

        assert response_data.status_code == 201, f"Failed to create gist {response_data.json()['message']} "
        resp_json = response_data.json()
        post_response_gist_id = resp_json['id']
        self.logger.info("Gist created successfully with id: " + post_response_gist_id)

        self.logger.info(" ---- ##### Verifying the Response Schema for Creating a Gist ###### ---")
        self.gistObj.validate_response_schema(resp_json, "create_gist")

        response_data = self.gistObj.list_gists_for_unauthorized(f"/gists/{post_response_gist_id}")
        resp_status_code = response_data.status_code
        resp_get_json = response_data.json()

        assert resp_status_code == 200, "Couldn't fetch the gist " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Response recieved successfully - {response_data.status_code}")

        self.logger.info("Verifying the Response Schema for listing a Gist by ID")
        self.gistObj.validate_response_schema(resp_json, "get_gist_by_id")

        assert resp_get_json['id'] == post_response_gist_id, "The resource returned is not the same"
        self.logger.info("Private Gist is accessible by an unauthorized user as expected")

    @pytest.mark.high
    @pytest.mark.parametrize("datatype", ["valid_data","valid_data_public"])
    def test_list_user_gists(self,api_client,datatype):
        self.logger.info("################ TEST - Verify LIST '/gists' functionality #################")
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        self.logger.info("Creating the gists for the user to be verified")
        for i in range(2):
            random_char = str(i)
            req_body['description'] = req_body['description']+ str(i)
            list(req_body['files'].values())[0]['content'] = "Testing Content" + str(i)
            response_data_post = self.gistObj.create_gist(req_body)
            assert response_data_post.status_code == 201, f"Failed to create gist {response_data_post.json()['message']} "
        self.logger.info("Created the gists successfully")

        response_data_get = self.gistObj.list_gists('/gists')
        resp_status_code= response_data_get.status_code
        assert resp_status_code == 200, "Couldn't fetch the gists " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason

        resp_json_get = response_data_get.json()
        self.logger.info("Verifying the response schema")
        self.gistObj.validate_response_schema(resp_json_get, "list_user_gists")

        req_owner = self.gistObj.get_owner()
        for i in range(len(resp_json_get)):
            assert req_owner == resp_json_get[i]['owner']['login'], "The Gists recieved do not belong to the owner"
        self.logger.info("Only the gists created by authorized owner were found in the response")


    @pytest.mark.high
    def test_list_gists_anonymously(self,api_client):
        self.logger.info("####################### TEST TO VERIFY GET '/gists' for an anonymous user #########################")
        self.pageObj(api_client)
        response_data_get = self.gistObj.list_gists_for_unauthorized('/gists')
        resp_status_code = response_data_get.status_code
        assert resp_status_code == 200, "Couldn't fetch the gists " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data_get.reason
        resp_json = response_data_get.json()
        print(resp_json)
        num_of_gists_per_page = len(resp_json)

        self.logger.info("Number of gists on current page:"+str(num_of_gists_per_page))
        for p in range(num_of_gists_per_page):
            assert resp_json[p]['public'] == True, "Private gist detected!!"
        self.logger.info(f"Public gists verified in the response successfully")

    @pytest.mark.skip(reason="Failing for an unknown reason, needs to be looked at")
    @pytest.mark.critical
    def test_get_public_gists_schema(self,api_client):
        self.logger.info('############# TEST FOR VERIFYING RESPONSE SCHEMA OF "GET" PUBLIC GISTS ##################')
        self.pageObj(api_client)
        response_data = self.gistObj.list_gists('/gists/public')
        resp_json = response_data.json()
        resp_status_code = response_data.status_code
        assert resp_status_code == 200, "Couldn't fetch the gists " + "GOT THE ERROR: " + str(
        resp_status_code) + " " + response_data.reason
        self.logger.info(f"Expected Status Code verified successfully - {response_data.status_code}")

        self.logger.info("Verifying the response schema")
        self.gistObj.validate_response_schema(resp_json, "get_public_gists")

    @pytest.mark.medium
    @pytest.mark.pagination
    @pytest.mark.parametrize("per_page_gists", ["per_page_100", "per_page_101", "per_page_99", "per_page_29","per_page_0","per_page_empty"])
    def test_gists_per_page(self, api_client, per_page_gists,clean_up):
        self.logger.info(
            '############# TEST FOR GETTING PUBLIC GISTS AND VERIFYING NUMBER OF RECORDS PER PAGE ##################')
        self.pageObj(api_client)
        data = self.gistObj.get_test_data("get_req")[per_page_gists]

        description = data['description']
        parameters = data['params']
        headers = data['headers']
        expectedRecords = data['expectedRecords']

        self.logger.info(" ######################## " + description.upper() + " ######################## ")
        response_data = self.gistObj.list_public_gists('/gists/public', parameters=parameters, headers=headers)
        resp_json = response_data.json()
        resp_status_code = response_data.status_code
        assert resp_status_code == 200, "Couldn't fetch the gists " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Expected Status Code verified successfully - {response_data.status_code}")
        actual_rec = len(resp_json)
        assert actual_rec == expectedRecords, f"Default number of records returned per page is not {expectedRecords} but {actual_rec}"
        self.logger.info(f"The number of records returned per page is verified as {expectedRecords} as expected")
        for p in range(0, len(resp_json)):
            assert resp_json[p]['public'] == True, "Public gists were not found in the response"
        self.logger.info(f"Public gists verified in the response successfully")

    @pytest.mark.skip(reason="Takes a longer time and exceeds rate limit of Github api")
    @pytest.mark.parametrize("per_page_gists",
                             ["per_page_100", "per_page_101", "per_page_99", "per_page_29", "per_page_0",
                              "per_page_empty"])
    def test_user_gists_per_page(self, api_client, per_page_gists, clean_up):
        self.logger.info(
            '############# TEST FOR GETTING USER GISTS AND VERIFYING NUMBER OF RECORDS PER PAGE ##################')
        self.pageObj(api_client)
        data = self.gistObj.get_test_data("get_req")[per_page_gists]

        description = data['description']
        parameters = data['params']
        headers = data['headers']
        expectedRecords = data['expectedRecords']
        self.gistObj.create_gist_bulk(150)
        self.logger.info("Created 150 gists in bulk for testing pagination")
        self.logger.info(" ######################## " + description.upper() + " ######################## ")
        response_data = self.gistObj.list_gists('/gists', parameters=parameters, headers=headers)
        resp_json = response_data.json()
        resp_status_code = response_data.status_code
        assert resp_status_code == 200, "Couldn't fetch the gists " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Expected Status Code verified successfully - {response_data.status_code}")
        actual_rec = len(resp_json)
        assert actual_rec == expectedRecords, f"Default number of records returned per page is not {expectedRecords} but {actual_rec}"
        self.logger.info(f"The number of records returned per page is verified as {expectedRecords} as expected")

    @pytest.mark.medium
    def test_get_invalid_gist_id(self,api_client):
        self.logger.info('############# TEST FOR GETTING A GIST FOR INVALID ID ##################')
        self.pageObj(api_client)
        response_data=self.gistObj.list_gist_by_id("/gists/invalid_id")
        resp_status_code=response_data.status_code
        resp_json = response_data.json()
        assert resp_status_code == 404, "Couldn't fetch the gist  " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        assert resp_json['message']=='Not Found',"404 message could not be verified"
        self.logger.info(f"No Gist found for invalid id - {response_data.status_code}")

    @pytest.mark.critical
    @pytest.mark.parametrize("datatype", ["missing_file"])
    def test_create_gist_without_file(self,api_client,datatype):
        self.logger.info('############# TEST FOR CREATING A GIST WITHOUT A FILE ##################')
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        response_data = self.gistObj.create_gist(req_body)
        resp_json = response_data.json()
        assert response_data.status_code == 422, f"Got - {response_data.status_code}, Recieved response: {resp_json['message']} "
        self.logger.info("The gist couldn't be created without a mandatory field - file")


    @pytest.mark.critical
    @pytest.mark.parametrize("datatype", ["missing_content"])
    def test_create_gist_without_content(self, api_client, datatype):
        self.logger.info('############# TEST FOR CREATING A GIST WITHOUT CONTENT ##################')
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        response_data = self.gistObj.create_gist(req_body)
        resp_json = response_data.json()
        assert response_data.status_code == 422, f"Got - {response_data.status_code}, Recieved response: {resp_json['message']} with error: {resp_json['errors']} "
        self.logger.info(f"The gist couldn't be created without mandatory field -  file content")

    @pytest.mark.high
    def test_create_gist_bad_payload(self, api_client):
        self.logger.info('############# TEST FOR CREATING A GIST WITH BAD PAYLOAD ##################')
        self.pageObj(api_client)
        req_body = {'d':{"abc":[1,2,3]}}
        response_data = self.gistObj.create_gist(req_body)
        resp_json = response_data.json()
        assert response_data.status_code == 422, f"Got - {response_data.status_code}, Recieved response: {resp_json['message']}"
        self.logger.info(f"The gist couldn't be created without due to malformed request body")

    @pytest.mark.critical
    def test_create_gist_empty_payload(self, api_client):
        self.logger.info('############# TEST FOR CREATING A GIST WITH EMPTY PAYLOAD ##################')
        self.pageObj(api_client)
        req_body = {}
        response_data = self.gistObj.create_gist(req_body)
        resp_json = response_data.json()
        print(resp_json)
        assert response_data.status_code == 422, f"Got - {response_data.status_code}, Recieved response: {resp_json['message']}"
        self.logger.info(f"The gist couldn't be created with an empty payload")

    @pytest.mark.critical
    @pytest.mark.parametrize("datatype", ["valid_data"])
    def test_create_gist_unauthorized(self,api_client,datatype):
        self.logger.info('############# TEST FOR CREATING A GIST WITHOUT AUTHORIZATION ##################')
        self.logger.info("TEST - Creating a Gist without authorization")
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        response_data = self.gistObj.create_gist_unauthorized(req_body)
        resp_json = response_data.json()
        assert response_data.status_code == 401, f"Failed to create gist {response_data.json()['message']} "

        assert resp_json['message']=="Requires authentication","Status Code 401 information mismatch"
        self.logger.info(f"The gist couldn't be created with an unauthorized request")


    @pytest.mark.critical
    @pytest.mark.parametrize("datatype", ["valid_data"])
    def test_create_gist_large_size_content(self,api_client,datatype,clean_up):
        size=2
        self.logger.info('############# TEST FOR CREATING A GIST WITH LARGE SIZE CONTENT AND VERIFY TRUNCATION ##################')
        self.logger.info("TEST - Creating a Gist with large content size")
        self.pageObj(api_client)
        req_body = self.gistObj.get_test_data("create_gist")[datatype]
        content_to_upload = self.gistObj.request_data_file(size)
        list(req_body['files'].values())[0]['content']= content_to_upload
        self.logger.info(f"Creating a Gist with file size: {size} MB")
        response_data = self.gistObj.create_gist(req_body)

        assert response_data.status_code == 201, f"Failed to create gist"
        resp_json = response_data.json()

        post_response_gist_id= resp_json['id']
        self.logger.info("##################### Getting the Gist details from the server ###############")
        response_data = self.gistObj.list_gist_by_id(f"/gists/{post_response_gist_id}")
        self.logger.info(f"Got the response with gist id: {post_response_gist_id} using GET '/gist/gistID' ")
        resp_status_code = response_data.status_code
        resp_get_json = response_data.json()

        assert resp_status_code == 200, "Couldn't fetch the gist " + "GOT THE ERROR: " + str(
            resp_status_code) + " " + response_data.reason
        self.logger.info(f"Response recieved successfully - {response_data.status_code}")

        self.logger.info("Verifying the Response Schema for listing a Gist by ID")
        self.gistObj.validate_response_schema(resp_json, "get_gist_by_id")

        truncation_status = list(resp_get_json['files'].values())[0]['truncated']
        assert truncation_status==True,"The File content was not truncated as expected"
        self.logger.info("The File content got truncated as expected")
        print(list(resp_get_json['files'].values())[0])


    def pageObj(self, get_client):
        self.gistObj = GistPage(get_client)


