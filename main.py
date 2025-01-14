import os
import json
from datetime import datetime
from pydriller import Repository
import benedict
from jinja2 import Environment, FileSystemLoader
from binaryornot.helpers import is_binary_string

def get_changes(repo_path):
    changes = []
    # gr = Git(repo_path)
    print(f"Reading repository: {repo_path}")
    repo = Repository(repo_path)
    for commit in repo.traverse_commits():
        changes.append( _get_commit_changes(commit) )

    return changes

def _get_commit_changes(commit):
    cc = benedict.BeneDict()

    cc.hash = commit.hash
    cc.message = commit.msg
    cc.author = commit.author.name
    cc.datetime = commit.author_date
    cc.date = commit.author_date.date()
    cc.time = commit.author_date.time()

    cc.files = {}
    cc.files.added = {}
    cc.files.deleted = []
    cc.files.modified = {}

    for file in commit.modified_files:
        if file.change_type.name == "ADD":
            str_to_check = file.source_code.encode('utf-8')[:16] if file.source_code else None
            if is_binary_string(str_to_check):
                cc.files.added[file.filename] = 'Binary Data'
            elif file.source_code == None:
                cc.files.added[file.filename] = 'NO DATA'
            elif len(file.source_code) > 1024:
                cc.files.added[file.filename] = file.source_code[:1024] + "\n[FILE TRUCATED]"
            else:
                cc.files.added[file.filename] = file.source_code
            # print(f'is_binary_string:  {is_binary_string(str_to_check)}, file: {file.filename}, str_to_check: {str_to_check}' )           
        if file.change_type.name == "DELETE":
            cc.files.deleted.append(file.filename)
        if file.change_type.name == "MODIFY":
            cc.files.modified[file.filename] = file.diff
            # cc.files.differences.append(file.diff)
              
    return cc

def print_history(repo_path, changes):
    print(f"Repository: {repo_path}")
    for commit in changes:
        print(f"Commit: {commit.hash}")
        print(f"Author: {commit.author}")
        print(f"Date: {commit.date}")
        print(f"Message: {commit.message}")
        print(f"Added Files: {len(commit.files.added)}")
        for file in commit.files.added:
            print(f"+++ {file}")
        
        print(f"Deleted Files: {len(commit.files.deleted)}")
        for file in commit.files.deleted:
            print(f"--- {file}")
        print(f"Modified Files: {len(commit.files.modified)}")
        for file in commit.files.modified:
            print(f"*** {file}")
            print(f"{commit.files.modified[file]}")

        print("-" * 80)
    print("\n")

def generate_html(repo_path, changes, output_path="output.html", template='bs'):
    # Load the template
    env = Environment(loader=FileSystemLoader('./templates'))
    template_filename = os.path.join( f'{template}_template.html')
    template = env.get_template(template_filename)

    # Render the template with data
    html_content = template.render(repo_path=repo_path, changes=changes)

    # Write to file
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"HTML report generated at {output_path}")    

def load_config(file_path):
    try:
        with open(file_path, "r") as config_file:
            config = json.load(config_file)
            return config.get("repositories", [])
    except FileNotFoundError:
        print(f"File di configurazione {file_path} non trovato.")
        return []
    except json.JSONDecodeError:
        print(f"Errore nel parsing del file di configurazione {file_path}.")
        return []    
    
def check_folder(repo_path):
    if os.path.exists(repo_path) and os.path.isdir(repo_path):
        return True
    else:
        print(f"Path: {repo_path} does not exists or is not a directory")
        return False

if __name__ == "__main__":
    config_path = "config.json"
    repositories = load_config(config_path)

    if not repositories:
        print("Nessun repository trovato nel file di configurazione.")
    else:
        for repo_path in repositories:
            if check_folder(repo_path):
                try:
                    # history = get_git_changes(repo_path)
                    # print_commit_history(repo_path, history)
                    changes = get_changes(repo_path)
                    # print_history(repo_path, changes)
                    generate_html(repo_path, changes, output_path=f"{repo_path.replace('/', '_')}_history.html")
                except ValueError as e:
                    print(e)
