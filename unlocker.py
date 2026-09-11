#!/usr/bin/env python3
"""
GitHub Achievements Hunter & Auto-Unlocker
Author: @djabhi31
Repository: https://github.com/djabhi31/github-achievement-unlocker
License: MIT
"""

import os
import sys
import time
import json
import base64
import urllib.request
import urllib.error
import subprocess
import getpass
import argparse

BANNER = r"""
  ____ _ _   _   _       _         _     _ _                         
 / ___(_) |_| | | |_   _| |__     / \   | |__ (_) _____   _____ _ __ 
| |  _| | __| |_| | | | | '_ \   / _ \  | '_ \| |/ _ \ \ / / _ \ '__|
| |_| | | |_|  _  | |_| | |_) | / ___ \ | | | | |  __/\ V /  __/ |   
 \____|_|\__|_| |_|\__,_|_.__/ /_/   \_\|_| |_|_|\___| \_/ \___|_|   
                     AUTONOMOUS UNLOCKER TOOLKIT
"""

def get_token():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token.strip()
    
    try:
        proc = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', text=True, capture_output=True)
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    
    print("\n[!] No GitHub Token detected automatically.")
    print("Please provide a GitHub Personal Access Token (PAT) with 'repo' scope.")
    print("Create one here: https://github.com/settings/tokens/new?scopes=repo,workflow\n")
    return getpass.getpass("Enter GitHub Token: ").strip()

class AchievementUnlocker:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "User-Agent": "GitHub-Achievement-Unlocker",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        self.user = self._verify_user()

    def _verify_user(self):
        req = urllib.request.Request("https://api.github.com/user", headers=self.headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                print(f"[+] Authenticated successfully as @{data['login']} ({data.get('name', 'Developer')})")
                return data['login']
        except Exception as e:
            print(f"[X] Authentication failed: {e}")
            sys.exit(1)

    def rest_request(self, endpoint, method="GET", data=None):
        url = f"https://api.github.com{endpoint}"
        payload = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(url, data=payload, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status in (200, 201):
                    return json.loads(resp.read().decode('utf-8'))
                return {}
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8')
            try:
                return json.loads(err_msg)
            except Exception:
                return {"error": err_msg, "status": e.code}

    def graphql_request(self, query, variables=None):
        url = "https://api.github.com/graphql"
        payload = json.dumps({"query": query, "variables": variables or {}}).encode('utf-8')
        headers = {**self.headers, "Authorization": f"bearer {self.token}"}
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {"errors": [e.read().decode('utf-8')]}

    def setup_sandbox_repo(self, repo_name="github-achievement-sandbox"):
        print(f"\n[*] Preparing sandbox repository: {self.user}/{repo_name}...")
        existing = self.rest_request(f"/repos/{self.user}/{repo_name}")
        if "id" in existing:
            print(f"    Existing repo found: https://github.com/{self.user}/{repo_name}")
        else:
            payload = {
                "name": repo_name,
                "description": "Sandbox repository for unlocking GitHub Developer Achievements",
                "private": False,
                "auto_init": True,
                "has_issues": True
            }
            new_repo = self.rest_request("/user/repos", method="POST", data=payload)
            print(f"    Created repository: {new_repo.get('html_url', repo_name)}")
            time.sleep(3)

        # Enable discussions
        self.rest_request(f"/repos/{self.user}/{repo_name}", method="PATCH", data={"has_discussions": True})
        return repo_name

    def unlock_quickdraw(self, repo_name):
        print("\n" + "="*50)
        print("⚡ [1/4] Unlocking QUICKDRAW Badge...")
        print("="*50)
        issue = self.rest_request(f"/repos/{self.user}/{repo_name}/issues", method="POST", data={
            "title": "Quickdraw Achievement Verification",
            "body": "Automated issue creation for immediate closure."
        })
        num = issue.get("number")
        print(f"    Created Issue #{num}")
        time.sleep(1)
        self.rest_request(f"/repos/{self.user}/{repo_name}/issues/{num}", method="PATCH", data={"state": "closed"})
        print(f"    Closed Issue #{num} instantly! [Quickdraw Unlocked!]")

    def unlock_pull_and_pair(self, repo_name, pr_count=25):
        print("\n" + "="*50)
        print(f"🦈 [2/4] Unlocking PULL SHARK & 👥 [3/4] PAIR EXTRAORDINAIRE ({pr_count} PRs)...")
        print("="*50)

        main_ref = self.rest_request(f"/repos/{self.user}/{repo_name}/git/ref/heads/main")
        main_sha = main_ref["object"]["sha"]

        for i in range(1, pr_count + 1):
            branch = f"achieve-branch-{i}-{int(time.time() * 1000)}"
            self.rest_request(f"/repos/{self.user}/{repo_name}/git/refs", method="POST", data={
                "ref": f"refs/heads/{branch}",
                "sha": main_sha
            })

            content_b64 = base64.b64encode(f"Milestone commit #{i}".encode('utf-8')).decode('utf-8')
            commit_msg = f"Add milestone update #{i}\n\nCo-authored-by: octocat <octocat@github.com>"
            self.rest_request(f"/repos/{self.user}/{repo_name}/contents/milestones/update_{i}.txt", method="PUT", data={
                "message": commit_msg,
                "content": content_b64,
                "branch": branch
            })

            pr = self.rest_request(f"/repos/{self.user}/{repo_name}/pulls", method="POST", data={
                "title": f"Co-Authored Achievement PR #{i}",
                "head": branch,
                "base": "main",
                "body": f"Milestone pull request #{i}."
            })
            pr_num = pr.get("number")

            time.sleep(0.5)

            self.rest_request(f"/repos/{self.user}/{repo_name}/pulls/{pr_num}/merge", method="PUT", data={
                "commit_title": f"Merge pull request #{pr_num}",
                "merge_method": "merge"
            })
            print(f"    [{i}/{pr_count}] Merged Co-Authored PR #{pr_num}")
            time.sleep(0.5)

        print("    [Pull Shark & Pair Extraordinaire Unlocked / Leveled Up!]")

    def unlock_galaxy_brain(self, repo_name, count=32):
        print("\n" + "="*50)
        print(f"💎 [4/4] Unlocking GALAXY BRAIN ({count} Accepted Q&A Answers)...")
        print("="*50)

        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
            discussionCategories(first: 10) {
              nodes { id name isAnswerable }
            }
          }
        }
        """
        data = self.graphql_request(query, {"owner": self.user, "name": repo_name})
        repo_data = data.get("data", {}).get("repository", {})
        repo_id = repo_data.get("id")
        categories = repo_data.get("discussionCategories", {}).get("nodes", [])

        qna_cat = next((c for c in categories if c.get("isAnswerable")), None)
        if not qna_cat:
            qna_cat = next((c for c in categories if "Q&A" in c.get("name", "") or "Question" in c.get("name", "")), None)

        if not qna_cat or not repo_id:
            print("    [!] Discussions Q&A category not found or discussions not active.")
            return

        cat_id = qna_cat["id"]

        for d in range(1, count + 1):
            create_disc = """
            mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
              createDiscussion(input: {repositoryId: $repoId, categoryId: $catId, title: $title, body: $body}) {
                discussion { id number }
              }
            }
            """
            d_res = self.graphql_request(create_disc, {
                "repoId": repo_id,
                "catId": cat_id,
                "title": f"Community Technical Discussion #{d}",
                "body": f"Discussion topic #{d} regarding software engineering practices."
            })
            disc_id = d_res.get("data", {}).get("createDiscussion", {}).get("discussion", {}).get("id")
            if not disc_id:
                continue

            time.sleep(0.4)

            add_comment = """
            mutation($discId: ID!, $body: String!) {
              addDiscussionComment(input: {discussionId: $discId, body: $body}) {
                comment { id }
              }
            }
            """
            c_res = self.graphql_request(add_comment, {
                "discId": disc_id,
                "body": f"Accepted technical solution and answer for discussion #{d}."
            })
            comment_id = c_res.get("data", {}).get("addDiscussionComment", {}).get("comment", {}).get("id")

            time.sleep(0.4)

            mark_answer = """
            mutation($id: ID!) {
              markDiscussionCommentAsAnswer(input: {id: $id}) {
                discussion { id }
              }
            }
            """
            self.graphql_request(mark_answer, {"id": comment_id})
            print(f"    [{d}/{count}] Discussion #{d} Answer Accepted")
            time.sleep(0.5)

        print("    [Diamond Galaxy Brain Unlocked!]")

def main():
    parser = argparse.ArgumentParser(description="GitHub Achievements Hunter & Auto-Unlocker")
    parser.add_argument("--automated", action="store_true", help="Run without prompts (for CI/CD)")
    parser.add_argument("--level", choices=["standard", "silver", "max"], default="max", help="Level of achievements to unlock")
    parser.add_argument("--repo", default="github-achievement-sandbox", help="Sandbox repo name")
    args = parser.parse_args()

    print(BANNER)
    token = get_token()
    if not token:
        print("[X] Token is required to proceed.")
        sys.exit(1)

    unlocker = AchievementUnlocker(token)
    repo_name = unlocker.setup_sandbox_repo(args.repo)

    pr_count = 25 if args.level == "max" else (16 if args.level == "silver" else 2)
    qna_count = 32 if args.level == "max" else (8 if args.level == "silver" else 2)

    unlocker.unlock_quickdraw(repo_name)
    unlocker.unlock_pull_and_pair(repo_name, pr_count=pr_count)
    unlocker.unlock_galaxy_brain(repo_name, count=qna_count)

    print("\n" + "="*60)
    print("🎉 ALL ACHIEVEMENTS TRIGGERED SUCCESSFULLY!")
    print("="*60)
    print("GitHub computes achievements asynchronously.")
    print("Check your profile in 15-30 minutes: https://github.com/" + unlocker.user + "?tab=achievements")
    print("\n⭐ If this tool helped you, please Star the repository:")
    print("   https://github.com/djabhi31/github-achievement-unlocker")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
