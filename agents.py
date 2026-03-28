class Agents:
    def __init__(self):
        self.agents = ["Ubuntu", "Windows", "macOS", "Alpine"]
        self.status = {agent: "Libre" for agent in self.agents}

    def assign(self, job):
        for agent in self.status:
            if self.status[agent] == "Libre":
                self.status[agent] = f"Ocupado ({job})"
                return agent
        return None

    def release(self, agent):
        self.status[agent] = "Libre"

    def get_status(self):
        return self.status