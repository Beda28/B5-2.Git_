def topological_sort(commits):
    indegree = {}
    children = {}

    for commit_hash, commit in commits.items():
        indegree[commit_hash] = len(commit.parents)
        children[commit_hash] = []

    for commit_hash, commit in commits.items():
        for parent in commit.parents:
            children[parent].append(commit_hash)

    queue = []

    for commit_hash in commits:
        if indegree[commit_hash] == 0:
            queue.append(commit_hash)

    result = []
    front  = 0

    while front < len(queue):
        current = queue[front]
        result.append(current)
        front += 1

        for child in children[current]:
            indegree[child] -= 1

            if indegree[child] == 0: queue.append(child)

    return result

def sort_hashes(values):
    for i in range(1, len(values)):
        value = values[i]
        j     = i - 1

        while j >= 0 and values[j] > value:
            values[j + 1] = values[j]
            j -= 1

        values[j + 1] = value

    return values

def bfs(graph, start, end):
    if start == end: return [start]

    queue = [start]
    front = 0
    visit = {start}
    prev  = {}

    while front < len(queue):
        current = queue[front]
        front  += 1

        neighbors = list(graph[current])
        sort_hashes(neighbors)

        for neighbor in neighbors:
            if neighbor in visit: continue

            visit.add(neighbor)
            prev[neighbor] = current
            queue.append(neighbor)

            if neighbor == end:
                path    = [end]
                current = end

                while current != start:
                    current = prev[current]
                    path.append(current)

                return path[::-1]

    return None

def update_index(keyword_index, author_index, commit):
    keywords = commit.message.lower().split()
    visit    = set()

    for keyword in keywords:
        if keyword in visit: continue

        visit.add(keyword)

        if keyword not in keyword_index:
            keyword_index[keyword] = []

        keyword_index[keyword].append(commit.hash)

    author = commit.author.lower()

    if author not in author_index:
        author_index[author] = []

    author_index[author].append(commit.hash)

def dfs(commits, commit_hash):
    visited = set()
    result  = []

    def dfs_loop(point):
        for parent in commits[point].parents:
            if parent in visited: continue

            visited.add(parent)
            result.append(parent)

            dfs_loop(parent)

    dfs_loop(commit_hash)
    return result

def merge_sort(values, key):
    if len(values) <= 1: return values

    middle = len(values) // 2

    left  = merge_sort(values[:middle], key)
    right = merge_sort(values[middle:], key)

    result = []
    l = 0
    r = 0

    while l < len(left) and r < len(right):
        if key(left[i]) <= key(right[i]):
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    
    while l < len(left):
        result.append(left[l])
        l += 1

    while r < len(right):
        result.append(right[r])
        r += 1

    return result