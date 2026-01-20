from queue_circular import QueueCircular


def test_empty_queue():
    """Test operations on empty queue"""
    q = QueueCircular(5)
    assert q.is_empty() == True
    assert q.is_full() == False
    assert q.size() == 0
    assert q.capacity() == 5
    print(q.to_list())
    assert q.to_list() == []

    # Test exceptions on empty queue
    try:
        q.dequeue()
        assert False, "Should raise exception"
    except (IndexError, RuntimeError):
        pass

    try:
        q.front()
        assert False, "Should raise exception"
    except (IndexError, RuntimeError):
        pass


def test_single_element():
    """Test queue with single element"""
    q = QueueCircular(3)
    q.enqueue(42)

    assert q.is_empty() == False
    assert q.is_full() == False
    assert q.size() == 1
    assert q.front() == 42
    assert q.to_list() == [42]

    # Remove the single element
    assert q.dequeue() == 42
    assert q.is_empty() == True
    assert q.size() == 0


def test_fill_to_capacity():
    """Test filling queue to capacity"""
    q = QueueCircular(4)  # Can hold 3 items (waste one slot)

    # Fill to capacity
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    assert q.size() == 3
    assert q.is_full() == True
    assert q.to_list() == [1, 2, 3]

    # Try to add one more - should fail
    try:
        q.enqueue(4)
        assert False, "Should raise exception when full"
    except (IndexError, RuntimeError):
        pass


def test_fifo_order():
    """Test First-In-First-Out behavior"""
    q = QueueCircular(5)

    # Add 3 items
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)

    assert q.to_list() == [10, 20, 30]
    assert q.front() == 10

    # Remove in FIFO order
    assert q.dequeue() == 10
    assert q.front() == 20
    assert q.size() == 2

    assert q.dequeue() == 20
    assert q.dequeue() == 30
    assert q.is_empty() == True


def test_wraparound():
    """Test wraparound behavior - the key feature!"""
    q = QueueCircular(4)  # Capacity 3

    # Fill completely
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.is_full() == True

    # Remove some to make space
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.size() == 1

    # Add more - should wrap around
    q.enqueue(4)
    q.enqueue(5)
    assert q.size() == 3
    assert q.is_full() == True

    # Should be [3, 4, 5] in FIFO order
    assert q.to_list() == [3, 4, 5]

    # Remove all
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    assert q.dequeue() == 5
    assert q.is_empty() == True


def test_alternating_operations():
    """Test alternating enqueue/dequeue with wraparound"""
    q = QueueCircular(5)  # Capacity 4

    # Pattern: add 2, remove 1, repeat
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1  # [2]

    q.enqueue(3)
    q.enqueue(4)
    assert q.dequeue() == 2  # [3, 4]

    q.enqueue(5)
    q.enqueue(6)  # Should wrap around
    assert q.to_list() == [3, 4, 5, 6]
    assert q.is_full() == True

    # Remove all
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    assert q.dequeue() == 5
    assert q.dequeue() == 6
    assert q.is_empty() == True


def test_front_without_modifying():
    """Test that front() doesn't modify queue"""
    q = QueueCircular(4)
    q.enqueue(100)
    q.enqueue(200)

    # Multiple front() calls shouldn't change anything
    assert q.front() == 100
    assert q.front() == 100
    assert q.size() == 2
    assert q.to_list() == [100, 200]


def test_size_calculation():
    """Test size calculation with wraparound"""
    q = QueueCircular(5)  # Capacity 4

    # Test various sizes
    sizes = []
    for i in range(4):  # Fill to capacity
        q.enqueue(i)
        sizes.append(q.size())

    assert sizes == [1, 2, 3, 4]
    assert q.is_full() == True

    # Remove some and check sizes
    sizes = []
    for i in range(4):
        sizes.append(q.size())
        q.dequeue()

    assert sizes == [4, 3, 2, 1]
    assert q.is_empty() == True


def test_edge_case_capacity_one():
    """Test edge case: capacity of 1"""
    q = QueueCircular(2)  # Effective capacity 1

    assert q.is_empty() == True
    q.enqueue(99)
    assert q.is_full() == True
    assert q.size() == 1

    assert q.dequeue() == 99
    assert q.is_empty() == True


if __name__ == "__main__":
    test_empty_queue()
    test_single_element()
    test_fill_to_capacity()
    test_fifo_order()
    test_wraparound()
    test_alternating_operations()
    test_front_without_modifying()
    test_size_calculation()
    test_edge_case_capacity_one()
    print("All circular queue tests passed!")