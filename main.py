import os
import requests
import json


def creat_release(tag_name, name, body):
    repository_owner = os.environ.get('GITHUB_REPOSITORY_OWNER')
    repository_name = os.environ.get('GITHUB_REPOSITORY_NAME')
    vtoken = os.environ.get('SECRETS_VOKEN')
    print(repository_owner, repository_name, vtoken)

    url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/releases'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + vtoken,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    payload = {
        'tag_name': tag_name,
        'target_commitish': 'master',
        'name': name,
        'body': body,
        'draft': False,
        'prerelease': False,
        'generate_release_notes': False
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print('Release created successfully.')
    else:
        print('Failed to create release. Status code:', response.status_code)
        print('Response:', response.text)