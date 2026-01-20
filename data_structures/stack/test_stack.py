from stack import Stack


def test_empty_stack():
    """Test operations on empty stack"""
    s = Stack()
    assert s.is_empty() == True
    assert s.size() == 0
    assert s.to_list() == []

    # Test exceptions on empty stack
    try:
        s.pop()
        assert False, "Should raise exception"
    except (IndexError, RuntimeError):
        pass

    try:
        s.peek()
        assert False, "Should raise exception"
    except (IndexError, RuntimeError):
        pass


def test_push_single():
    """Test pushing single element"""
    s = Stack()
    s.push(42)

    assert s.is_empty() == False
    assert s.size() == 1
    assert s.peek() == 42
    assert s.to_list() == [42]


def test_push_multiple():
    """Test pushing multiple elements"""
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)

    assert s.size() == 3
    assert s.peek() == 3  # Last in, first out
    assert s.to_list() == [3, 2, 1]  # Top to bottom


def test_pop():
    """Test popping elements"""
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)

    # Pop elements in LIFO order
    assert s.pop() == 30
    assert s.size() == 2
    assert s.peek() == 20

    assert s.pop() == 20
    assert s.size() == 1
    assert s.peek() == 10

    assert s.pop() == 10
    assert s.size() == 0
    assert s.is_empty() == True


def test_peek_without_modifying():
    """Test that peek doesn't modify the stack"""
    s = Stack()
    s.push(100)
    s.push(200)

    # Multiple peeks shouldn't change anything
    assert s.peek() == 200
    assert s.peek() == 200
    assert s.size() == 2
    assert s.to_list() == [200, 100]


def test_mixed_operations():
    """Test combination of push/pop operations"""
    s = Stack()

    # Build stack: [3, 2, 1] (top to bottom)
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.to_list() == [3, 2, 1]

    # Pop one
    s.pop()
    assert s.to_list() == [2, 1]

    # Push more
    s.push(4)
    s.push(5)
    assert s.to_list() == [5, 4, 2, 1]

    # Pop all
    assert s.pop() == 5
    assert s.pop() == 4
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty() == True


def test_lifo_behavior():
    """Test Last-In-First-Out behavior explicitly"""
    s = Stack()

    # Push in order: A, B, C, D
    items = ['A', 'B', 'C', 'D']
    for item in items:
        s.push(item)

    # Pop should give: D, C, B, A
    expected = ['D', 'C', 'B', 'A']
    actual = []
    while not s.is_empty():
        actual.append(s.pop())

    assert actual == expected


def test_edge_cases():
    """Test edge cases"""
    s = Stack()

    # Single element operations
    s.push(999)
    assert s.peek() == 999
    assert s.pop() == 999
    assert s.is_empty() == True

    # Push after emptying
    s.push(111)
    assert s.size() == 1
    assert s.peek() == 111


def test_size_tracking():
    """Test that size is tracked correctly"""
    s = Stack()
    assert s.size() == 0

    # Size increases with pushes
    for i in range(5):
        s.push(i)
        assert s.size() == i + 1

    # Size decreases with pops
    for i in range(5):
        s.pop()
        assert s.size() == 4 - i


if __name__ == "__main__":
    test_empty_stack()
    test_push_single()
    test_push_multiple()
    test_pop()
    test_peek_without_modifying()
    test_mixed_operations()
    test_lifo_behavior()
    test_edge_cases()
    test_size_tracking()
    print("All stack tests passed!")