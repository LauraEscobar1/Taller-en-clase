class Node:
    def __init__(self, stage):
        self.stage = stage
        self.next = None
        self.status = "pending"  # pending, running, success

class Pipeline:
    def __init__(self):
        self.head = None

    def add_stage(self, stage):
        new_node = Node(stage)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_stages(self):
        stages = []
        current = self.head
        while current:
            stages.append(current)
            current = current.next
        return stages

    def reset(self):
        current = self.head
        while current:
            current.status = "pending"
            current = current.next