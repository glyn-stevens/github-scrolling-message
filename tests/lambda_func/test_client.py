def test_get_file(repo_api, test_message_file):
    response = repo_api.get_file(test_message_file)
    with open(test_message_file) as f:
        expected_msg = f.read()
    assert response.status_code == 200
    assert response.json()["content"] == expected_msg
