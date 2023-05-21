import os
import random
import requests
import json


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
    chunk_size = 40 * 1024 * 1024  # 每块大小为 40MB
    total_size = os.path.getsize(file_path)
    vtoken = os.environ.get('SECRETS_VTOKEN')

    headers = {
        "Accept": "application/vnd.github+json",
        'Authorization': 'Bearer ' + vtoken,
        'X-GitHub-Api-Version': '2022-11-28',
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, 'rb') as file:
        chunk_number = 0
        while True:
            chunk_data = file.read(chunk_size)
            if not chunk_data:
                break

            # 设置当前块的起始位置和结束位置
            start_byte = chunk_number * chunk_size
            end_byte = start_byte + len(chunk_data) - 1
            content_range = f"bytes {start_byte}-{end_byte}/{total_size}"

            # 设置当前块的请求头
            current_headers = headers.copy()
            current_headers['Content-Range'] = content_range

            # 发送当前块的上传请求
            response = requests.put(upload_url, headers=current_headers, data=chunk_data)
            response.raise_for_status()

            chunk_number += 1

            print(response.status_code, response.text)

    print("文件上传完成")


cv = creat_release("hi", "hi")
if cv is not None:

    upload_url = cv['upload_url']

    file_path = "/path/to/file"  # 替换为实际的文件路径
    upload_file_in_chunks(upload_url, file_path)
else:
    exit(1)
