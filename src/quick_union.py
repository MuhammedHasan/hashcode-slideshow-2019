class QuickUnion:
    def __init__(self, size):
        self.connections = list(range(size))
        self.size_of_root = [1] * size

    def is_connected(self, i, j):
        return self.root(i - 1) == self.root(j - 1)

    def connect(self, i, j):
        root_i = self.root(i - 1)
        root_j = self.root(j - 1)
        if self.size_of_root[root_i] > self.size_of_root[root_j]:
            self.connections[root_i] = root_j
            self.size_of_root[root_j] += root_i
        else:
            self.connections[root_j] = root_i
            self.size_of_root[root_i] += root_j

    def root(self, i):
        i = i - 1
        while self.connections[i] != i:
            self.connections[i] = self.connections[self.connections[i]]
            i = self.connections[i]
        return i
