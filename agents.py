class Agents:
    def __init__(self):
        self.agents = ["Ubuntu", "Windows", "macOS", "Alpine"]
        self.status = {agent: "Libre" for agent in self.agents}

    def get_status(self):
        return self.status
