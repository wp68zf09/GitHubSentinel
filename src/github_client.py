# src/github_client.py

import requests
import datetime
import os
class GitHubClient:
    def __init__(self, token):
        self.token = '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'
        self.headers = {'Authorization': f'token {self.token}'}

    def fetch_updates(self, repo):
        # 获取特定 repo 的更新（commits, issues, pull requests）
        updates = {
            'commits': self.fetch_commits(repo),
            'issues': self.fetch_issues(repo),
            'pull_requests': self.fetch_pull_requests(repo)
        }
        return updates

    def fetch_commits(self, repo):
        url = f'https://api.github.com/repos/{repo}/commits'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, repo):
        url = f'https://api.github.com/repos/{repo}/issues'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_pull_requests(self, repo):
        url = f'https://api.github.com/repos/{repo}/pulls'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


    def export_daily_progress(self, repo):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        issues = self.fetch_issues(repo)
        pull_requests = self.fetch_pull_requests(repo)
    
     # 构造文件名
        filename = f'daily_progress/{repo.replace("/", "_")}_{date_str}.md'
    
        # 自动创建目录（如果不存在）
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # 新增目录创建逻辑
    
    # 写入文件内容
        with open(filename, 'w') as f:
            f.write(f"# {repo} Daily Progress - {date_str}\n\n")
            f.write("## Issues\n")
            for issue in issues:
                f.write(f"- {issue['title']} #{issue['number']}\n")
            f.write("\n## Pull Requests\n")
            for pr in pull_requests:
                f.write(f"- {pr['title']} #{pr['number']}\n")

        print(f"Exported daily progress to {filename}")

        return filename