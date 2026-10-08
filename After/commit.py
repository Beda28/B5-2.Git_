class Commit:
    def __init__(self, hash, message, author, timestamp, parents):
        self.hash      = hash
        self.message   = message
        self.author    = author
        self.timestamp = timestamp
        self.parents   = parents