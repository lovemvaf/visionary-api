import urllib.request
import json
import sys

headers = {"User-Agent": "Antigravity-Agent/1.0"}

def fetch(endpoint):
    url = f"https://api.github.com/repos/lovemvaf/visionary-api/{endpoint}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code} for {endpoint}: {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"Error for {endpoint}: {e}")
        return None

def main():
    print("=== REPOSITORY INFO ===")
    repo = fetch("")
    if repo:
        print(f"Full Name: {repo.get('full_name')}")
        print(f"Default Branch: {repo.get('default_branch')}")
        print(f"Open Issues / PRs Count: {repo.get('open_issues_count')}")

    print("\n=== CONTRIBUTORS API ===")
    contributors = fetch("contributors")
    if contributors:
        for c in contributors:
            print(f"- {c.get('login')} ({c.get('type')}): {c.get('contributions')} commits, avatar: {c.get('avatar_url')}")
    else:
        print("No contributors returned or error.")

    print("\n=== PULL REQUESTS (ALL) ===")
    prs = fetch("pulls?state=all&per_page=30")
    if prs:
        for pr in prs:
            print(f"PR #{pr.get('number')} [{pr.get('state').upper()}]: {pr.get('title')}")
            print(f"  User: {pr.get('user', {}).get('login')}")
            print(f"  Head: {pr.get('head', {}).get('ref')} ({pr.get('head', {}).get('sha')[:7]})")
            print(f"  Base: {pr.get('base', {}).get('ref')}")
            print(f"  Merged At: {pr.get('merged_at')}")
            print(f"  Merge Commit SHA: {pr.get('merge_commit_sha')}")
            print(f"  HTML URL: {pr.get('html_url')}")

    print("\n=== BRANCHES ===")
    branches = fetch("branches")
    if branches:
        for b in branches:
            print(f"- {b.get('name')}: {b.get('commit', {}).get('sha')[:7]}")

    print("\n=== RECENT WORKFLOW RUNS ===")
    runs = fetch("actions/runs?per_page=10")
    if runs:
        for r in runs.get("workflow_runs", []):
            print(f"Run {r.get('id')} | {r.get('name')} | Branch: {r.get('head_branch')} | SHA: {r.get('head_sha')[:7]} | Status: {r.get('status')} | Conclusion: {r.get('conclusion')} | Event: {r.get('event')}")

if __name__ == "__main__":
    main()
