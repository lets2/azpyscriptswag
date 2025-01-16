import os
import re
import yaml
from git import Repo

# variables
FORBIDDEN_TERM = 'house'
CHECK_KEY1 = 'servers'  # contains a array inside
LINK_WITH_EXAMPLE = 'servers: [url: "https://example.com"]'
CHECK_KEY2 = 'paths'  # contains a object inside
LINK_WITH_EXAMPLE2 = 'paths: use /accounts instead of /ob/v2/accounts"]'

# step 1: Locate swagger file
def find_swagger_file():
    for file in os.listdir('.'):
        if re.search(r'swagger', file, re.IGNORECASE):
            return file
    return None

# # step 2: Check if file was modified
# def file_modified(repo, file_path):
#     # diff = repo.git.diff('HEAD~1', 'HEAD', file_path)
#     # diff = repo.git.diff('HEAD', '--', file_path)
#     diff = repo.git.diff('HEAD~1', 'HEAD', '--', file_path)
#     return bool(diff)

# step 3: Load YAML and validate
def validate_swagger(file_path):
    with open(file_path, 'r') as f:
        content = yaml.safe_load(f)

    # check servers
    if CHECK_KEY1 not in content or not isinstance(content[CHECK_KEY1], list):
        print(f"Error: The {'servers'} key is missing or invalid in {file_path}. Example: {LINK_WITH_EXAMPLE}")
        exit(1)
    print(f"{CHECK_KEY1}: {content[CHECK_KEY1]}")

    # check paths
    if CHECK_KEY2 not in content or not isinstance(content[CHECK_KEY2], dict):
        print(f"Error: The {CHECK_KEY2} key is missing in {file_path}.")
        exit(1)

    # validate paths and forbidden term
    flagged_paths = [key for key in content[CHECK_KEY2] if FORBIDDEN_TERM in key]
    if flagged_paths:
        print(f"Error: The following paths contain the forbidden term '{FORBIDDEN_TERM}': {flagged_paths}")
        print(f"Example: {LINK_WITH_EXAMPLE2}")
        exit(1)
    else:
        print(f"{file_path} is within the standard.")

def main():
    repo = Repo('.')
    swagger_file = find_swagger_file()

    if not swagger_file:
        print("No Swagger file found. Skipping this step.")
        return

    # if not file_modified(repo, swagger_file):
    #     print(f"No changes detected in {swagger_file}. Skipping this step.")
    #     return

    print(f"Processing {swagger_file}...")
    validate_swagger(swagger_file)

if __name__ == '__main__':
    main()
