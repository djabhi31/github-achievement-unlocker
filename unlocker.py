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
                login = data['login']
                if login.endswith("[bot]") or login == "github-actions":
                    print(f"\n[X] Error: Authenticated as bot account '@{login}'!")
                    print("    The default GitHub Actions GITHUB_TOKEN belongs to a bot.")
                    print("    GitHub Achievements CANNOT be unlocked on a bot account!")
                    print("    Fix: Create a GitHub Personal Access Token (PAT) with 'repo' scope,")
                    print("    and configure it as repository secret 'PERSONAL_ACCESS_TOKEN'.")
                    sys.exit(1)
                print(f"[+] Authenticated successfully as @{login} ({data.get('name', 'Developer')})")
                return login
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

        self.rest_request(f"/repos/{self.user}/{repo_name}", method="PATCH", data={"has_discussions": True})
        return repo_name

    def unlock_quickdraw(self, repo_name):
        print("\n" + "="*50)
        print("⚡ Unlocking QUICKDRAW Badge...")
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

    def unlock_yolo(self, repo_name):
        print("\n" + "="*50)
        print("🚀 Unlocking YOLO Badge...")
        print("="*50)
        main_ref = self.rest_request(f"/repos/{self.user}/{repo_name}/git/ref/heads/main")
        main_sha = main_ref["object"]["sha"]
        branch = f"yolo-{int(time.time() * 1000)}"

        self.rest_request(f"/repos/{self.user}/{repo_name}/git/refs", method="POST", data={
            "ref": f"refs/heads/{branch}", "sha": main_sha
        })
        content_b64 = base64.b64encode("YOLO commit".encode('utf-8')).decode('utf-8')
        self.rest_request(f"/repos/{self.user}/{repo_name}/contents/yolo.txt", method="PUT", data={
            "message": "Direct commit for YOLO badge", "content": content_b64, "branch": branch
        })
        pr = self.rest_request(f"/repos/{self.user}/{repo_name}/pulls", method="POST", data={
            "title": "YOLO Achievement PR", "head": branch, "base": "main", "body": "PR merged without review."
        })
        pr_num = pr.get("number")
        time.sleep(0.5)
        self.rest_request(f"/repos/{self.user}/{repo_name}/pulls/{pr_num}/merge", method="PUT", data={
            "commit_title": f"Merge pull request #{pr_num}", "merge_method": "merge"
        })
        print(f"    Merged PR #{pr_num} directly without code review! [YOLO Unlocked!]")

    def unlock_pull_shark(self, repo_name, pr_count=16, delay=1.5):
        print("\n" + "="*50)
        print(f"🦈 Unlocking PULL SHARK ({pr_count} PRs)...")
        print("="*50)

        for i in range(1, pr_count + 1):
            main_ref = self.rest_request(f"/repos/{self.user}/{repo_name}/git/ref/heads/main")
            if "object" not in main_ref:
                print(f"    [!] Error fetching main branch: {main_ref}")
                break
            main_sha = main_ref["object"]["sha"]

            branch = f"pull-shark-{i}-{int(time.time() * 1000)}"
            ref_res = self.rest_request(f"/repos/{self.user}/{repo_name}/git/refs", method="POST", data={
                "ref": f"refs/heads/{branch}", "sha": main_sha
            })
            if "ref" not in ref_res:
                print(f"    [!] Error creating branch {branch}: {ref_res}")
                continue

            content_b64 = base64.b64encode(f"Shark commit #{i}\nTimestamp: {time.time()}".encode('utf-8')).decode('utf-8')
            self.rest_request(f"/repos/{self.user}/{repo_name}/contents/shark/update_{i}.txt", method="PUT", data={
                "message": f"Update #{i}", "content": content_b64, "branch": branch
            })
            pr = self.rest_request(f"/repos/{self.user}/{repo_name}/pulls", method="POST", data={
                "title": f"Pull Shark PR #{i}", "head": branch, "base": "main", "body": f"Pull Shark PR #{i}."
            })
            pr_num = pr.get("number")
            if not pr_num:
                print(f"    [!] Error creating PR #{i}: {pr}")
                continue

            time.sleep(delay)
            merge_res = self.rest_request(f"/repos/{self.user}/{repo_name}/pulls/{pr_num}/merge", method="PUT", data={
                "commit_title": f"Merge pull request #{pr_num}", "merge_method": "merge"
            })
            if merge_res.get("merged"):
                print(f"    [{i}/{pr_count}] Merged PR #{pr_num} successfully")
            else:
                print(f"    [{i}/{pr_count}] PR #{pr_num} merge response: {merge_res.get('message', 'Failed')}")
            time.sleep(delay)
        print("    [Pull Shark Trigger Sequence Completed!]")

    def unlock_pair_extraordinaire(self, repo_name, pr_count=24, coauthor_name="The Octocat", coauthor_email="583231+octocat@users.noreply.github.com", delay=1.5):
        print("\n" + "="*50)
        print(f"👥 Unlocking PAIR EXTRAORDINAIRE ({pr_count} Co-Authored PRs)...")
        print(f"   Co-Author: {coauthor_name} <{coauthor_email}>")
        print("="*50)

        for i in range(1, pr_count + 1):
            main_ref = self.rest_request(f"/repos/{self.user}/{repo_name}/git/ref/heads/main")
            if "object" not in main_ref:
                print(f"    [!] Error fetching main branch: {main_ref}")
                break
            main_sha = main_ref["object"]["sha"]

            branch = f"pair-branch-{i}-{int(time.time() * 1000)}"
            ref_res = self.rest_request(f"/repos/{self.user}/{repo_name}/git/refs", method="POST", data={
                "ref": f"refs/heads/{branch}", "sha": main_sha
            })
            if "ref" not in ref_res:
                print(f"    [!] Error creating branch {branch}: {ref_res}")
                continue

            content_b64 = base64.b64encode(f"Pair commit #{i}\nTimestamp: {time.time()}".encode('utf-8')).decode('utf-8')
            commit_msg = f"Add pair update #{i}\n\nCo-authored-by: {coauthor_name} <{coauthor_email}>"
            self.rest_request(f"/repos/{self.user}/{repo_name}/contents/pairing/update_{i}.txt", method="PUT", data={
                "message": commit_msg, "content": content_b64, "branch": branch
            })
            pr = self.rest_request(f"/repos/{self.user}/{repo_name}/pulls", method="POST", data={
                "title": f"Pair Extraordinaire PR #{i}", "head": branch, "base": "main", "body": f"Co-authored PR #{i} with {coauthor_name}."
            })
            pr_num = pr.get("number")
            if not pr_num:
                print(f"    [!] Error creating PR #{i}: {pr}")
                continue

            time.sleep(delay)
            merge_res = self.rest_request(f"/repos/{self.user}/{repo_name}/pulls/{pr_num}/merge", method="PUT", data={
                "commit_title": f"Merge pull request #{pr_num}", "merge_method": "merge"
            })
            if merge_res.get("merged"):
                print(f"    [{i}/{pr_count}] Merged Co-Authored PR #{pr_num}")
            else:
                print(f"    [{i}/{pr_count}] PR #{pr_num} merge response: {merge_res.get('message', 'Failed')}")
            time.sleep(delay)
        print("    [Pair Extraordinaire Trigger Sequence Completed!]")

    def unlock_galaxy_brain(self, repo_name, count=32):
        print("\n" + "="*50)
        print(f"💎 Unlocking GALAXY BRAIN ({count} Discussions)...")
        print("="*50)
        print("    ⚠️  IMPORTANT NOTICE ABOUT GALAXY BRAIN:")
        print("    1. GitHub's algorithm requires answers to be accepted by ANOTHER user.")
        print("       Self-answering your own questions does not count toward the achievement.")
        print("    2. GitHub has officially restricted achievement triggers on newly created")
        print("       sandbox repositories to prevent automated badge farming.")
        print("    Proceeding with Q&A creation for testing...\n")

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
            if "errors" in d_res:
                print(f"    [!] Error creating discussion #{d}: {d_res['errors']}")
                continue

            disc_id = d_res.get("data", {}).get("createDiscussion", {}).get("discussion", {}).get("id")
            if not disc_id:
                continue

            time.sleep(0.5)

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
            if not comment_id:
                continue

            time.sleep(0.5)

            mark_answer = """
            mutation($id: ID!) {
              markDiscussionCommentAsAnswer(input: {id: $id}) {
                discussion { id }
              }
            }
            """
            m_res = self.graphql_request(mark_answer, {"id": comment_id})
            if "errors" in m_res:
                print(f"    [!] Error marking answer for discussion #{d}: {m_res['errors']}")
            else:
                print(f"    [{d}/{count}] Discussion #{d} Answer Marked")
            time.sleep(0.5)

        print("    [Galaxy Brain Trigger Sequence Completed!]")

def prompt_interactive_choice():
    print("\nSelect which badge(s) you want to unlock:")
    print("  [1] ⚡ Quickdraw (Instant issue closure)")
    print("  [2] 🦈 Pull Shark (Merge PRs)")
    print("  [3] 👥 Pair Extraordinaire (Co-authored PRs)")
    print("  [4] 🧠 Galaxy Brain (Q&A discussions accepted answers)")
    print("  [5] 🚀 YOLO (Direct PR merge without review)")
    print("  [6] 👑 ALL BADGES (Complete Suite up to Diamond/Gold)\n")
    
    choice = input("Enter choice [1-6] (default 6): ").strip()
    mapping = {
        "1": "quickdraw",
        "2": "pull-shark",
        "3": "pair-extraordinaire",
        "4": "galaxy-brain",
        "5": "yolo",
        "6": "all",
        "": "all"
    }
    return mapping.get(choice, "all")

def main():
    parser = argparse.ArgumentParser(description="GitHub Achievements Hunter & Auto-Unlocker")
    parser.add_argument("--automated", action="store_true", help="Run in non-interactive CI/CD mode")
    parser.add_argument("--badge", choices=["all", "quickdraw", "pull-shark", "pair-extraordinaire", "galaxy-brain", "yolo"], default=None, help="Specific badge to unlock")
    parser.add_argument("--tier", choices=["bronze", "silver", "max"], default="max", help="Tier level for multi-tier badges")
    parser.add_argument("--repo", default="github-achievement-sandbox", help="Sandbox repo name")
    parser.add_argument("--coauthor-name", default="The Octocat", help="Co-author display name for Pair Extraordinaire (default: 'The Octocat')")
    parser.add_argument("--coauthor-email", default="583231+octocat@users.noreply.github.com", help="Co-author verified GitHub email (default: '583231+octocat@users.noreply.github.com')")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay in seconds between API actions to avoid rate limits (default: 1.5)")
    args = parser.parse_args()

    print(BANNER)
    token = get_token()
    if not token:
        print("[X] Token is required to proceed.")
        sys.exit(1)

    unlocker = AchievementUnlocker(token)
    repo_name = unlocker.setup_sandbox_repo(args.repo)

    # Determine badge selection
    badge = args.badge
    if not badge and not args.automated:
        badge = prompt_interactive_choice()
    elif not badge:
        badge = "all"

    # Determine counts based on tier
    pull_count = 25 if args.tier == "max" else (16 if args.tier == "silver" else 2)
    pair_count = 24 if args.tier == "max" else (10 if args.tier == "silver" else 1)
    qna_count = 32 if args.tier == "max" else (8 if args.tier == "silver" else 2)

    print(f"\n🎯 Target Selection: BADGE='{badge.upper()}' | TIER='{args.tier.upper()}'\n")

    if badge == "quickdraw":
        unlocker.unlock_quickdraw(repo_name)
    elif badge == "yolo":
        unlocker.unlock_yolo(repo_name)
    elif badge == "pull-shark":
        unlocker.unlock_pull_shark(repo_name, pr_count=pull_count, delay=args.delay)
    elif badge == "pair-extraordinaire":
        unlocker.unlock_pair_extraordinaire(
            repo_name,
            pr_count=pair_count,
            coauthor_name=args.coauthor_name,
            coauthor_email=args.coauthor_email,
            delay=args.delay
        )
    elif badge == "galaxy-brain":
        unlocker.unlock_galaxy_brain(repo_name, count=qna_count)
    elif badge == "all":
        unlocker.unlock_quickdraw(repo_name)
        unlocker.unlock_yolo(repo_name)
        unlocker.unlock_pair_extraordinaire(
            repo_name,
            pr_count=pair_count,
            coauthor_name=args.coauthor_name,
            coauthor_email=args.coauthor_email,
            delay=args.delay
        )
        unlocker.unlock_pull_shark(
            repo_name,
            pr_count=pull_count,
            delay=args.delay
        )
        unlocker.unlock_galaxy_brain(repo_name, count=qna_count)

    print("\n" + "="*60)
    print("🎉 REQUESTED ACHIEVEMENT(S) TRIGGERED SUCCESSFULLY!")
    print("="*60)
    print("GitHub computes achievements asynchronously.")
    print("Check your profile in 15-30 minutes: https://github.com/" + unlocker.user + "?tab=achievements")
    print("\n⭐ If this tool helped you, please Star the repository:")
    print("   https://github.com/djabhi31/github-achievement-unlocker")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
