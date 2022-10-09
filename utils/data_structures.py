from copy import deepcopy


class Stack:
    """Class representing stack data structure."""

    def __init__(self):
        self._arr = []

    def push(self, value):
        self._arr.append(value)

    def pop(self):
        if len(self._arr):
            return self._arr.pop()
        return None

    def top(self):
        if len(self._arr):
            return self._arr[-1]
        return None


class Queue:
    """Class representing queue data structure."""

    def __init__(self):
        self._arr = []

    def push(self, value):
        self._arr.append(value)

    def pop(self):
        return self._arr.pop(0)

    def get_copy(self):
        """
        Function to get copy of the self protected arr member
        to be able to modify or access it without changing the queue state.
        """
        return deepcopy(self._arr)
