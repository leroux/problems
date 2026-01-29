def op(c: str):
    if c == '+':
        return lambda a, b: a + b
    elif c == '-':
        return lambda a, b: a - b
    elif c == '*':
        return lambda a, b: a * b
    elif c == '/':
        return lambda a, b: int(a / b)
    else:
        raise ValueError


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for t in tokens:
            if t in '+-*/':
                r = stack.pop()
                l = stack.pop()
                res = op(t)(l, r)
                stack.append(res)
            else:
                stack.append(int(t))
        assert len(stack) == 1
        return stack[-1]

