from queue_linked import QueueLinked


def test_empty_queue():
    """Test operations on empty queue"""
    q = QueueLinked()
    assert q.is_empty() == True
    assert q.size() == 0
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
    q = QueueLinked()
    q.enqueue(42)

    assert q.is_empty() == False
    assert q.size() == 1
    assert q.front() == 42
    assert q.to_list() == [42]

    # Remove the single element
    assert q.dequeue() == 42
    assert q.is_empty() == True
    assert q.size() == 0


def test_fifo_order():
    """Test First-In-First-Out behavior"""
    q = QueueLinked()

    # Enqueue: 1, 2, 3
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    assert q.to_list() == [1, 2, 3]
    assert q.front() == 1
    assert q.size() == 3

    # Dequeue should give: 1, 2, 3 (FIFO)
    assert q.dequeue() == 1
    assert q.front() == 2
    assert q.size() == 2

    assert q.dequeue() == 2
    assert q.front() == 3
    assert q.size() == 1

    assert q.dequeue() == 3
    assert q.is_empty() == True


def test_multiple_operations():
    """Test mixed enqueue/dequeue operations"""
    q = QueueLinked()

    # Build queue: [1, 2, 3]
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.to_list() == [1, 2, 3]

    # Remove front: [2, 3]
    q.dequeue()
    assert q.to_list() == [2, 3]

    # Add more: [2, 3, 4, 5]
    q.enqueue(4)
    q.enqueue(5)
    assert q.to_list() == [2, 3, 4, 5]

    # Remove two: [4, 5]
    q.dequeue()
    q.dequeue()
    assert q.to_list() == [4, 5]

    # Add one: [4, 5, 6]
    q.enqueue(6)
    assert q.to_list() == [4, 5, 6]


def test_front_without_modifying():
    """Test that front() doesn't modify queue"""
    q = QueueLinked()
    q.enqueue(100)
    q.enqueue(200)

    # Multiple front() calls shouldn't change anything
    assert q.front() == 100
    assert q.front() == 100
    assert q.size() == 2
    assert q.to_list() == [100, 200]


def test_large_queue():
    """Test with larger number of elements"""
    q = QueueLinked()

    # Enqueue 100 items
    for i in range(100):
        q.enqueue(i)

    assert q.size() == 100
    assert q.front() == 0

    # Dequeue first 50
    for i in range(50):
        assert q.dequeue() == i

    assert q.size() == 50
    assert q.front() == 50

    # Enqueue 50 more
    for i in range(100, 150):
        q.enqueue(i)

    assert q.size() == 100

    # Should be [50, 51, ..., 99, 100, 101, ..., 149]
    expected = list(range(50, 150))
    assert q.to_list() == expected


def test_alternating_operations():
    """Test alternating enqueue/dequeue"""
    q = QueueLinked()

    # Pattern: enqueue, enqueue, dequeue, enqueue, dequeue, dequeue
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1  # Queue: [2]

    q.enqueue(3)  # Queue: [2, 3]
    assert q.dequeue() == 2  # Queue: [3]
    assert q.dequeue() == 3  # Queue: []

    assert q.is_empty() == True

    # Build back up
    q.enqueue(4)
    q.enqueue(5)
    assert q.to_list() == [4, 5]


if __name__ == "__main__":
    test_empty_queue()
    test_single_element()
    test_fifo_order()
    test_multiple_operations()
    test_front_without_modifying()
    test_large_queue()
    test_alternating_operations()
    print("All queue tests passed!")