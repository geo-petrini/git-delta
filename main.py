import json
from git import Repo
from datetime import datetime

def get_git_changes(repo_path):
    # Inizializza il repository
    repo = Repo(repo_path)
    if repo.bare:
        raise ValueError("La directory specificata non è un repository Git valido.")

    # Ottieni tutti i commit
    commits = list(repo.iter_commits())
    commit_history = []

    for i in range(len(commits) - 1):
        current_commit = commits[i]
        previous_commit = commits[i + 1]

        commit_info = {
            "hash": current_commit.hexsha,
            "author": current_commit.author.name,
            "date": datetime.fromtimestamp(current_commit.committed_date).strftime("%Y-%m-%d %H:%M:%S"),
            "message": current_commit.message.strip(),
            "added_files": [],
            "removed_files": [],
            "modified_files": [],
            "file_differences": {}
        }

        # Ottieni le differenze tra i commit
        diff = current_commit.diff(previous_commit, create_patch=True)

        for change in diff:
            if change.new_file:
                commit_info["added_files"].append(change.b_path)
            elif change.deleted_file:
                commit_info["removed_files"].append(change.a_path)
            elif change.change_type == "M":
                commit_info["modified_files"].append(change.a_path)

                # Aggiungi le differenze del file
                commit_info["file_differences"][change.a_path] = change.diff.decode("utf-8", errors="ignore")

        commit_history.append(commit_info)

    return commit_history


def print_commit_history(commit_history):
    for commit in commit_history:
        print(f"Commit: {commit['hash']}")
        print(f"Author: {commit['author']}")
        print(f"Date: {commit['date']}")
        print(f"Message: {commit['message']}\n")
        print("Added Files (+):")
        for file in commit["added_files"]:
            print(f"  + {file}")
        print("Removed Files (-):")
        for file in commit["removed_files"]:
            print(f"  - {file}")
        print("Modified Files:")
        for file in commit["modified_files"]:
            print(f"  * {file}")
        print("\nFile Differences:")
        for file, diff in commit["file_differences"].items():
            print(f"  File: {file}")
            print(diff)
        print("-" * 80)


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

if __name__ == "__main__":
    config_path = "config.json"
    repositories = load_config(config_path)

    if not repositories:
        print("Nessun repository trovato nel file di configurazione.")
    else:
        for repo_path in repositories:
            try:
                history = get_git_changes(repo_path)
                print_commit_history(repo_path, history)
            except ValueError as e:
                print(e)
