import os
import re
import sys
import yaml
from git import Repo

# Variáveis globais
FORBIDDEN_TERM = 'house'
CHECK_KEY1 = 'servers'
CHECK_KEY2 = 'paths'
LINK_WITH_EXAMPLE = 'servers: [url: "https://example.com"]'
LINK_WITH_EXAMPLE2 = 'paths: use /accounts instead of /ob/v2/accounts"]'

def find_swagger_file(repo_path):
    for file in os.listdir(repo_path):
        if re.search(r'swagger.*\.yaml$', file, re.IGNORECASE):
            return os.path.join(repo_path, file)
    return None

def file_modified(repo, file_path):
    if not has_enough_commits(repo):
        print("Not enough commits to perform diff. Assuming first commit.")
        return True
    diff = repo.git.diff('HEAD~1', 'HEAD', '--', file_path)
    return bool(diff)

def has_enough_commits(repo, num_commits=2):
    return len(list(repo.iter_commits())) >= num_commits

def validate_swagger(file_path):
    with open(file_path, 'r') as f:
        content = yaml.safe_load(f)

    if CHECK_KEY1 not in content or not isinstance(content[CHECK_KEY1], list):
        print(f"Error: Missing key '{CHECK_KEY1}' in {file_path}. Example: {LINK_WITH_EXAMPLE}")
        exit(1)
    print(f"{CHECK_KEY1}: {content[CHECK_KEY1]}")

    if CHECK_KEY2 not in content or not isinstance(content[CHECK_KEY2], dict):
        print(f"Error: Missing key '{CHECK_KEY2}' in {file_path}.")
        exit(1)

    flagged_paths = [key for key in content[CHECK_KEY2] if FORBIDDEN_TERM in key]
    if flagged_paths:
        print(f"Error: Forbidden term '{FORBIDDEN_TERM}' found in paths: {flagged_paths}")
        exit(1)
    else:
        print(f"{file_path} is valid.")

def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    repo = Repo(repo_path)

    swagger_file = find_swagger_file(repo_path)
    if not swagger_file:
        print("No Swagger file found. Skipping validation.")
        return

    if not file_modified(repo, swagger_file):
        print(f"No changes detected in {swagger_file}. Skipping validation.")
        return

    print(f"Validating {swagger_file}...")
    validate_swagger(swagger_file)

if __name__ == '__main__':
    main()
