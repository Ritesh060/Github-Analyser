import requests
from requests_oauthlib import OAuth2Session
from io import StringIO
import nbformat
import chardet
import ctry1

# GitHub OAuth credentials
client_id = '7947b4764cfa4848c9a8'
client_secret = '35fb2e1f96b5ab97831a41798cc7e12d2845b974'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
redirect_uri = 'https://2f69-122-165-72-252.ngrok-free.app//callback'
block_size = 2048

def get_github_access_token(client_id, client_secret, authorization_response):
    github = OAuth2Session(client_id, redirect_uri=redirect_uri)
    token = github.fetch_token(token_url, authorization_response=authorization_response, client_secret=client_secret)
    return token['access_token']

def extract_python_code_from_ipynb(ipynb_content):
    notebook = nbformat.reads(ipynb_content.getvalue(), as_version=4)
    code_cells = [cell['source'] for cell in notebook['cells'] if cell['cell_type'] == 'code']
    return '\n'.join(code_cells)

def get_repo_contents(repo_url, path='', access_token=None):
    # Extract the username and repository name from the URL
    _, username, repo_name = repo_url.rstrip('/').rsplit('/', 2)
    user_input = f"I will provide you code for the repository {repo_name} in the next prompts, keep it in chat history"
    main_list = []
    main_list.append(user_input)

    # Construct the GitHub API URL for the contents
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"

    # Set up headers with authentication (if access_token is provided)
    headers = {}
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"

    # Make a GET request to the GitHub API with authentication headers
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        contents = response.json()

        for i in contents:
            if i:
                # If it's a file, fetch and display the content
                if 'type' in i and i['type'] == 'file' and i['name'].lower().endswith(('.py', '.js', '.java', '.c', '.cpp', '.cs', '.html', '.css', '.rb', '.php', '.swift', '.m', '.sql', '.sh', '.ts', '.go', '.rs', '.kt', '.vue', '.jsx', '.ipynb')):
                    file_content_url = i['download_url']
                    file_response = requests.get(file_content_url, headers=headers)

                    if file_response.status_code == 200:
                        content_input = f"This is the code for {i['name']}"
                        main_list.append(content_input)
                        # Check if the file is in .ipynb format
                        if i['name'].lower().endswith('.ipynb'):
                            ipynb_content = StringIO(file_response.content.decode('utf-8', errors='replace'))
                            python_code = extract_python_code_from_ipynb(ipynb_content)
                            while python_code:
                                block = python_code[:block_size]
                                block_input = block
                                main_list.append(block_input)
                                python_code = python_code[block_size:]
                        else:
                            # If it's a regular file, detect the encoding and decode the content
                            encoding = chardet.detect(file_response.content)['encoding']
                            encoding = encoding if encoding else 'utf-8'
                            file_content = file_response.content.decode(encoding, errors='replace')
                            while file_content:
                                block = file_content[:block_size]
                                block_input = block
                                main_list.append(block_input)
                                file_content = file_content[block_size:]
                    elif 'type' in i and i['type'] == 'dir':
                        # If it's a directory, list the files in the directory
                        folder_input = f"This is content in folder{i}"
                        main_list.append(folder_input)
                        get_repo_contents(repo_url, path=f"{path}/{i}", access_token=access_token)
                        root_input = "Now we are back in the root directory of the repository"
                        main_list.append(root_input)
        s1 = f"This is all the pieces of code I have for {repo_name}, now I will ask you questions about {repo_name}"
        main_list.append(s1)
    else:
        # Print an error message if the request was unsuccessful
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")

    return main_list

def get_repo_list(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repository list. Status code: {response.status_code}")
        return None

def main():
    # Step 1: Get GitHub username from the user
    github_username = input("Enter your GitHub username: ")

    # Step 2: Obtain GitHub OAuth authorization URL
    github = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=['repo'])
    authorization_url, state = github.authorization_url(authorization_base_url)
    print(f'Please go to {authorization_url} and authorize access.')
    
    # Step 3: Obtain GitHub OAuth access token
    authorization_response = input('Paste the full redirect URL here: ')
    token = get_github_access_token(client_id, client_secret, authorization_response)
    
    # Step 4: Get the list of repositories
    repo_list = get_repo_list(token)

    if repo_list:
        # Display the list of repositories
        print("Repositories:")
        for repo in repo_list:
            print(repo['name'])
        print()

        # Step 5: Prompt the user to choose a repository
        selected_repo = input("Enter the name of the repository you want to access: ")

        # Step 6: Get the contents of the selected repository
        u = get_repo_contents(f"https://github.com/{github_username}/{selected_repo}", access_token=token)
        print(u)
        ctry1.chat_with_gpt(u)

if __name__ == "__main__":
    main()