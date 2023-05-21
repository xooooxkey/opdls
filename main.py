import os
import random
import requests
import json


def creat_release(name, body):
    repository = os.environ.get('GITHUB_REPOSITORY')
    vtoken = os.environ.get('SECRETS_VTOKEN')
    tag_name = os.environ.get('GITHUB_RUN_NUMBER')
    print(repository, vtoken, tag_name)

    url = f'https://api.github.com/repos/{repository}/releases'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + vtoken,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    payload = {
        'tag_name': "v" + tag_name + "." + str(random.randint(1000, 9999)) + "." + str(random.randint(1000, 9999)),
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


creat_release("hi", "hi")
