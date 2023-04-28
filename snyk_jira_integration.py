import os
import base64
import requests

# Snyk and JIRA API credentials
SNYK_API_TOKEN = os.environ.get("SNYK_API_TOKEN")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

# JIRA project and issue type
JIRA_PROJECT_KEY = "YOUR_PROJECT_KEY"
JIRA_ISSUE_TYPE = "Bug"  # Or any other issue type

# Snyk API URLs
SNYK_BASE_URL = "https://snyk.io/api/v1"
SNYK_ORG_ID = "YOUR_ORG_ID"
SNYK_PROJECTS_URL = f"{SNYK_BASE_URL}/org/{SNYK_ORG_ID}/projects"

# JIRA API URLs
JIRA_BASE_URL = "https://YOUR-INSTANCE.atlassian.net"
JIRA_ISSUE_URL = f"{JIRA_BASE_URL}/rest/api/2/issue"

# Fetch Snyk projects
def fetch_snyk_projects():
    headers = {"Authorization": f"token {SNYK_API_TOKEN}"}
    response = requests.get(SNYK_PROJECTS_URL, headers=headers)
    return response.json()["projects"]

# Fetch high and critical severity issues from Snyk project
def fetch_high_critical_issues(project_id):
    headers = {"Authorization": f"token {SNYK_API_TOKEN}"}
    params = {"filters[severity][]": ["high", "critical"]}
    response = requests.get(SNYK_ISSUES_URL.format(SNYK_PROJECT_ID=project_id), headers=headers, params=params)
    return response.json()["issues"]

# Create JIRA ticket
def create_jira_ticket(summary, description):
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{JIRA_USERNAME}:{JIRA_API_TOKEN}'.encode()).decode()}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": JIRA_ISSUE_TYPE
            }
        }
    }
    response = requests.post(JIRA_ISSUE_URL, headers=headers, json=data)
    return response.json()

# Search JIRA issues using JQL
def search_jira_issues(jql):
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{JIRA_USERNAME}:{JIRA_API_TOKEN}'.encode()).decode()}",
        "Content-Type": "application/json"
    }
    params = {"jql": jql}
    search_url = f"{JIRA_BASE_URL}/rest/api/2/search"
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()["issues"]

# Main function to fetch issues and create JIRA tickets
def main():
    projects = fetch_snyk_projects()

    for project in projects:
        issues = fetch_high_critical_issues(project["id"])
        
        for issue in issues:
            summary = f"{issue['title']} in {project['name']}"
            description = f"Severity: {issue['severity'].capitalize()}\n" \
                          f"Identifier: {issue['id']}\n" \
                          f"Package: {issue['packageName']}@{issue['packageVersion']}\n" \
                          f"URL: {issue['url']}"

            # Check if the issue is not already reported in JIRA
            jql_query = f'project="{JIRA_PROJECT_KEY}" AND summary~"{issue["id"]}"'
        existing_issues = search_jira_issues(jql_query)
        if not existing_issues:
            # Create JIRA ticket if it doesn't exist
            ticket = create_jira_ticket(summary, description)
            print(f"Created JIRA ticket {ticket['key']} for issue {issue['id']}")
if name == "main":
main()

