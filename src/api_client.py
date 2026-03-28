import requests

def fetch_github_user(username: str) -> dict:
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url,timeout=10)

    if response.status_code == 404:
        raise ValueError("GitHub 用户不存在。")
    if response.status_code != 200:
        raise RuntimeError(f"GitHub API 请求失败，状态码: {response.status_code}")

    return response.json()