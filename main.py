import os
import random
import requests
import json
import string


def creat_release(name, body, target_commitish="main"):
    repository = os.environ.get('GITHUB_REPOSITORY')
    vtoken = os.environ.get('SECRETS_VTOKEN')
    tag_name = str("files." + os.environ.get('GITHUB_RUN_NUMBER') + "." + str(random.randint(1000, 9999)) + "." + str(random.randint(10000, 99999)))
    print(repository, vtoken, tag_name)

    url = f'https://api.github.com/repos/{repository}/releases'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + vtoken,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    payload = {
        'tag_name': tag_name,
        'target_commitish': target_commitish,
        'name': name,
        'body': body,
        'draft': False,
        'prerelease': False,
        'generate_release_notes': False
    }
    payload = json.dumps(payload)
    print(payload)
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 201:
        print('Release created successfully.')
        return json.loads(response.text)
    else:
        print('Failed to create release. Status code:', response.status_code)
        print('Response:', response.text)
        return None


def upload_file_in_chunks(url, file_path):
    vtoken = os.environ.get('SECRETS_VTOKEN')

    url = str(url).replace("{?name,label}", "?name=" + os.path.basename(file_path))

    cy = f'''curl -L -X POST -H "Accept: application/vnd.github+json" -H "Authorization: Bearer {vtoken}" -H "X-GitHub-Api-Version: 2022-11-28" -H "Content-Type: application/octet-stream" {url} --data-raw "@{file_path}"'''

    print(os.system(cy))
    print("文件上传完成")


namec = os.environ.get('TASK_NAME')
if namec == "":
    namec = ''.join(random.choices(string.ascii_letters + string.digits, k=32)).lower()

cv = creat_release(namec, namec + "\n\n" + ''.join(random.choices(string.ascii_letters + string.digits, k=256)).lower())

if cv is not None:

    upload_url = cv['upload_url']

    for root, _, files in os.walk("/opt/dls"):
        for file in files:
            file_path = os.path.join(root, file)
            # 调用上传函数进行文件上传
            upload_file_in_chunks(upload_url, file_path)

else:
    exit(1)
