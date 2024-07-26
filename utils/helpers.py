import json
import os
import base64


def read_data_from_json(file_name):
    data_list = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, '..', 'test_data', file_name)
    relative_path = os.path.normpath(relative_path)
    with open(relative_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def create_data_file(file_name, size_in_mb):
    test_data_dir = os.path.join(os.getcwd(), 'test_data')
    file_path = os.path.join(test_data_dir, file_name)
    with open(file_path, 'wb') as f:
        f.write(os.urandom(size_in_mb * 1024 * 1024))

def read_data_file(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, '..', 'test_data', file_name)
    relative_path = os.path.normpath(relative_path)
    with open(relative_path, 'rb') as file:
        file_content = file.read()
        file_content_base64 = base64.b64encode(file_content).decode('ascii')
    return file_content_base64


