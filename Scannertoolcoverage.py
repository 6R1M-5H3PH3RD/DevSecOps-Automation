import os
import requests
import csv
import re
from pathlib import Path

# Fetch all projects from Snyk
SNYK_API_KEY = os.environ['SNYK_API_KEY']
SNYK_API_URL = 'https://snyk.io/api/v1/org/YOUR_ORG_ID/projects'
headers = {'Authorization': f'token {SNYK_API_KEY}'}
response = requests.get(SNYK_API_URL, headers=headers)
projects = response.json()['projects']

# Write project names to a text file
with open('snyk_projects.txt', 'w') as f:
    for project in projects:
        f.write(project['name'] + '\n')

# Read the text file and clean the data
with open('snyk_projects.txt', 'r') as f:
    project_names = [re.search('/scm/(.+)', line).group(1) for line in f]

# Write cleaned data to a CSV file
with open('Snyk-SCA-Repos.csv', 'w', newline='') as csvfile:
    fieldnames = ['Snyk-SCA-Repos']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for name in project_names:
        writer.writerow({'Snyk-SCA-Repos': name})

# Read Bitbucket.csv and compare with Snyk-SCA-Repos.csv
snyk_validation_dir = Path("Snyk_validation")
with open(snyk_validation_dir / 'Bitbucket.csv', 'r') as bitbucket_csv:
    bitbucket_reader = csv.reader(bitbucket_csv)
    next(bitbucket_reader)  # skip header
    bitbucket_repos = [row[0] for row in bitbucket_reader]

# Find missing repos and write to Missing_from_Snyk_SCA.csv
missing_repos = set(bitbucket_repos) - set(project_names)
with open('Missing_from_Snyk_SCA.csv', 'w', newline='') as csvfile:
    fieldnames = ['Missing_from_Snyk_SCA']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for repo in missing_repos:
        writer.writerow({'Missing_from_Snyk_SCA': repo})
