from collections import deque

class JobQueue:
    def __init__(self):
        self.queue = deque()

    def add_job(self, job):
        self.queue.append(job)

    def get_job(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def list_jobs(self):
        return list(self.queue)
