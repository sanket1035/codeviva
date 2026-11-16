"""Stack and queue built on Python lists (class-based lab program)."""


class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        if len(self.items) == 0:
            raise IndexError("queue is empty")
        return self.items.pop(0)


def balanced(text):
    """Check brackets using a stack."""
    s = Stack()
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in text:
        if ch in "([{":
            s.push(ch)
        elif ch in pairs:
            if s.is_empty() or s.pop() != pairs[ch]:
                return False
    return s.is_empty()


print(balanced("{[()]}"), balanced("{[(])}"))
