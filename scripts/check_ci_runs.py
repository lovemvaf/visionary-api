import urllib.request
import json
import time

def check_runs():
    url = "https://api.github.com/repos/lovemvaf/visionary-api/actions/runs?per_page=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Total runs: {data.get('total_count', 0)}")
            for r in data.get("workflow_runs", []):
                print(f"ID: {r['id']} | Workflow: {r['name']} | SHA: {r['head_sha'][:7]} | Status: {r['status']} | Conclusion: {r['conclusion']} | URL: {r['html_url']}")
    except Exception as e:
        print("Error checking runs:", e)

if __name__ == "__main__":
    check_runs()
