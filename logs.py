class Logs:
    def __init__(self):
        self.logs = []

    def add(self, message):
        self.logs.append(message)

    def get_logs(self):
        return self.logs[::-1]
