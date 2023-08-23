import subprocess
def pull_changes(path):
    subprocess.check_output(["git", "-C", path, "pull"], stderr=subprocess.PIPE)

def push_changes(path):
    git_commands = [
        ["git", "-C", path, "add", "."],
        ["git", "-C", path, "commit", "-m", "New Register"],
        ["git", "-C", path, "push"]
    ]
    for command in git_commands:
        output = subprocess.check_output(command, stderr=subprocess.PIPE)

def clone_repo(path, repo):
    subprocess.check_output(["git", "clone", "https://"+repo, path], stderr=subprocess.PIPE)