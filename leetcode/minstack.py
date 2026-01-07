class MinStack:

    def __init__(self):
        self.st = []
        self.min_st = []

    def push(self, val: int) -> None:
        self.st.append(val)
        if not self.min_st or val < self.min_st[-1][0]:
            self.min_st.append((val, len(self.st)))

    def pop(self) -> None:
        popped = self.st.pop()
        if len(self.st) < self.min_st[-1][1]:
            self.min_st.pop()
        return popped

    def top(self) -> int:
        return self.st[-1]

    def getMin(self) -> int:
        return self.min_st[-1][0]
        

