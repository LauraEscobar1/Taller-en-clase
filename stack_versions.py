class VersionStack:
    def __init__(self):
        self.stack = []

    def push(self, version):
        self.stack.append(version)

    def rollback(self):
        if len(self.stack) > 1:
            return self.stack.pop()
        return None

    def current(self):
        if self.stack:
            return self.stack[-1]
        return None

    def get_all(self):
        return self.stack
