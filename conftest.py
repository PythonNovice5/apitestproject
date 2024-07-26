import pytest
import os

from utils.api_client import APIClient


@pytest.fixture(scope='module', autouse=True)
def api_client():
    return APIClient()


# @pytest.fixture(scope="session", autouse=True)
# def create_bulk_gists(request):
#     # Load request data from JSON file
#     json_file_path = os.path.join(os.path.dirname(__file__), "..", "test_data", "create_gist.json")
#     with open(json_file_path, "r") as file:
#         request_data = json.load(file)
#
#     gists_created = []
#
#     # Generate unique filenames and descriptions
#     for i in range(500):
#         filename = f"file_{i + 1}.txt"
#         description = f"Description {i + 1}"
#
#         # Update request data with dynamic values
#         request_data["description"] = description
#         request_data["files"][filename] = {"content": "Test content"}
#
#         # Create gist using requests directly
#         url = 'https://api.github.com/gists'
#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(url, json=request_data, headers=headers)
#
#         # Handle response and add gist ID to the list of created gists
#         if response.status_code == 201:
#             gist_id = response.json().get('id')
#             gists_created.append(gist_id)
#         else:
#             # Handle error if gist creation fails
#             raise Exception(f"Failed to create gist with filename: {filename}")
#
#     yield gists_created
#
#     # Clean up: Delete all created gists after the test session ends
#     for gist_id in gists_created:
#         url = f'https://api.github.com/gists/{gist_id}'
#         response = requests.delete(url)
#         if response.status_code != 204:
#             # Handle error if deletion fails
#             print(f"Failed to delete gist with ID: {gist_id}")
