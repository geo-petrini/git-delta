import os
import json
from datetime import datetime
from pydriller import Repository
import benedict

def get_changes(repo_path):
    changes = []
    # gr = Git(repo_path)
    print(f"Reading repository: {repo_path}")
    for commit in Repository(repo_path).traverse_commits():
        changes.append( _get_commit_changes(commit) )
    return changes

def _get_commit_changes(commit):
    cc = benedict.BeneDict()

    cc.hash = commit.hash
    cc.message = commit.msg
    cc.author = commit.author.name
    cc.date = commit.author_date

    cc.files = {}
    cc.files.added = []
    cc.files.deleted = []
    cc.files.modified = {}

    for file in commit.modified_files:
        if file.change_type.name == "ADD":
            cc.files.added.append(file.filename)
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
                    print_history(repo_path, changes)
                except ValueError as e:
                    print(e)
