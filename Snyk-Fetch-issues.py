import os
import requests
import csv

# Snyk API credentials
SNYK_API_TOKEN = os.environ.get("SNYK_API_TOKEN")

# Snyk API URLs
SNYK_BASE_URL = "https://snyk.io/api/v1"
SNYK_ORG_ID = "YOUR_ORG_ID"
SNYK_PROJECTS_URL = f"{SNYK_BASE_URL}/org/{SNYK_ORG_ID}/projects"

# Fetch Snyk projects
def fetch_snyk_projects():
    headers = {"Authorization": f"token {SNYK_API_TOKEN}"}
    response = requests.get(SNYK_PROJECTS_URL, headers=headers)
    return response.json()["projects"]

# Fetch high and critical severity issues from Snyk project
def fetch_high_critical_issues(project_id):
    headers = {"Authorization": f"token {SNYK_API_TOKEN}"}
    params = {
        "filters[severity][]": ["high", "critical"],
        "per_page": 100,  # Adjust the number according to the maximum expected issues per project
    }
    issues_url = f"{SNYK_BASE_URL}/org/{SNYK_ORG_ID}/project/{project_id}/issues"
    response = requests.get(issues_url, headers=headers, params=params)
    return response.json()["issues"]

# Write issues to a CSV file
def write_issues_to_csv(issues):
    with open("high_critical_issues.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["issue_id", "title", "severity", "package", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for issue in issues:
            writer.writerow({
                "issue_id": issue["id"],
                "title": issue["title"],
                "severity": issue["severity"].capitalize(),
                "package": f"{issue['packageName']}@{issue['packageVersion']}",
                "url": issue["url"]
            })

# Main function to fetch issues and write to CSV
def main():
    projects = fetch_snyk_projects()
    all_issues = []

    for project in projects:
        issues = fetch_high_critical_issues(project["id"])
        all_issues.extend(issues)

    write_issues_to_csv(all_issues)
    print("High and critical severity issues have been written to high_critical_issues.csv")

if __name__ == "__main__":
    main()
