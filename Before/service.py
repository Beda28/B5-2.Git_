from datetime   import datetime
from commit     import Commit
from algorithms import dfs, topological_sort, bfs, update_index, merge_sort

class MiniGit:
    def __init__(self):
        self.init           = False
        self.author         = None
        self.current_branch = None

        self.commits        = {}
        self.branches       = {}
        self.graph          = {}

        self.keyword_index  = {}
        self.author_index   = {}

        self.commit_count   = 0

    def INIT(self, user_name):
        if self.init: return print("Repository already initalized.")

        self.init             = True
        self.author           = user_name
        self.current_branch   = "main"

        self.branches["main"] = None

        print("Initialized repository.")
        print("Current branch: main")
        print(f"Current user: {user_name}")

    def BRANCH(self, branch_name):
        if not self.init               : return print("Repository not initialized.")
        if branch_name in self.branches: return print(f"Branch already exists: {branch_name}")

        commit = self.branches[self.current_branch]
        self.branches[branch_name] = commit
        print(f"Created branch: {branch_name}")

    def SWITCH(self, branch_name):
        if not self.init                   : return print("Repository not initialized.")
        if branch_name not in self.branches: return print(f"Unknown branch: {branch_name}")

        self.current_branch = branch_name
        print(f"Switched to branch: {branch_name}")
    
    def COMMIT(self, message):
        if not self.init: return print("Repository not initialized.")

        parent = self.branches[self.current_branch]

        self.commit_count += 1
        commit_hash = f"{self.commit_count:06x}"

        parents = []

        if parent is not None: parents.append(parent)

        commit = Commit(
            commit_hash, message, self.author,
            datetime.now(), parents
        )

        self.commits[commit_hash] = commit
        self.graph[commit_hash]   = set()
        update_index(self.keyword_index, self.author_index, commit)

        if parent is not None:
            self.graph[parent].add(commit_hash)
            self.graph[commit_hash].add(parent)

        self.branches[self.current_branch] = commit_hash

        print(
            f"[{self.current_branch} {commit_hash}] "
            f"{message}"
        )

    def LOG(self, option=None):
        if not self.init: return print("Repository not initialized.")

        if option is None:
            commit_hashes = topological_sort(slef.commits)
            commits = [self.commits[commit_hashes] for commit_hash in commit_hashes]

        elif option == "--sort-by=date":
            commits = list(self.commits.values())
            commits = merge_sort(commits, lambda commit: commit.timestamp)

        elif option == "--sort-by=author":
            commits = list(self.commits.values())
            commits = merge_sort(commits, lambda commit: commit.author.lower())

        else: return print("Invalid args")

        for commit in commits:
            print(
                f"commit {commit.hash} "
                f"({commit.author}, {commit.timestamp})"
            )
            print(commit.message)

    def PATH(self, commit1, commit2):
        if not self.init: return print("Repository not initialized.")
        if commit1 not in self.commits: return print(f"Unknown commit: {commit1}")
        if commit2 not in self.commits: return print(f"Unknown commit: {commit2}")

        path = bfs(self.graph, commit1, commit2)

        if path is None: return print("No path")

        print("Path: " + " -> ".join(path))

    def ANCESTORS(self, commit_hash):
        if not self.init: return print("Repository not initialized.")
        if commit_hash not in self.commits: return print(f"Unknown commit: {commit_hash}")

        ancestors = dfs(self.commits, commit_hash)

        for ancestor in ancestors: print(ancestor)

    def SEARCH(self, target):
        if not self.init: return print("Repository not initialized.")
        if target.startswith("--author="):
            author = target.split("=", 1)[1].lower()

            if not author: return print("Invalid args")

            commit_hashes = self.author_index.get(author, [])

        else:
            keyword = target.lower()
            commit_hashes = self.keyword_index.get(keyword, [])

        
        print(f"Found {len(commit_hashes)} commits:")

        for commit_hash in commit_hashes:
            commit = self.commits[commit_hash]

            print(f"{commit.hash}: {commit.message}")