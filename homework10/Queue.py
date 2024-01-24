class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:

    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, value):
        if self.first is None:
            self.first = Node(value)
            self.last = self.first
        else:
            self.last.next = Node(value)
            self.last = self.last.next

    def head(self):
        if self.first is None:
            return None
        else:
            return self.first.value

    def dequeue(self):
        if self.first is None:
            return None
        else:
            headValue = self.first.value
            self.first = self.first.next
            return headValue
