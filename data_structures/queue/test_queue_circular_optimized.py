from queue_circular_optimized import QueueCircularOptimized


def test_power_of_2_capacity():
    """Test that capacity is rounded up to power of 2"""
    q = QueueCircularOptimized(5)
    assert q.capacity_actual() == 8  # Next power of 2 after 5
    assert q.capacity_effective() == 7  # Actual usable capacity

    q = QueueCircularOptimized(16)
    assert q.capacity_actual() == 16  # Already power of 2
    assert q.capacity_effective() == 15

    q = QueueCircularOptimized(1)
    assert q.capacity_actual() == 1
    assert q.capacity_effective() == 0


def test_empty_queue():
    """Test operations on empty queue"""
    q = QueueCircularOptimized(5)  # Will be capacity 8
    assert q.is_empty() == True
    assert q.is_full() == False
    assert q.size() == 0
    assert q.to_list() == []

    # Test exceptions on empty queue
    try:
        q.dequeue()
        assert False, "Should raise exception"
    except IndexError:
        pass

    try:
        q.front()
        assert False, "Should raise exception"
    except IndexError:
        pass


def test_single_element():
    """Test queue with single element"""
    q = QueueCircularOptimized(3)  # Will be capacity 4
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
    """Test filling queue to effective capacity"""
    q = QueueCircularOptimized(4)  # Capacity 4, effective 3

    # Fill to effective capacity
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
    except IndexError:
        pass


def test_fifo_order():
    """Test First-In-First-Out behavior"""
    q = QueueCircularOptimized(5)  # Capacity 8

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


def test_wraparound_with_bitwise():
    """Test wraparound behavior with bitwise operations"""
    q = QueueCircularOptimized(4)  # Capacity 4, effective 3

    # Fill completely
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.is_full() == True

    # Remove some to make space
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.size() == 1

    # Add more - should wrap around using bitwise operations
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
    q = QueueCircularOptimized(5)  # Capacity 8, effective 7

    # Pattern: add 2, remove 1, repeat
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1  # [2]

    q.enqueue(3)
    q.enqueue(4)
    assert q.dequeue() == 2  # [3, 4]

    q.enqueue(5)
    q.enqueue(6)
    q.enqueue(7)
    q.enqueue(8)  # Should wrap around using bitwise operations
    assert q.to_list() == [3, 4, 5, 6, 7, 8]
    assert q.size() == 6

    # Remove all
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    assert q.dequeue() == 5
    assert q.dequeue() == 6
    assert q.dequeue() == 7
    assert q.dequeue() == 8
    assert q.is_empty() == True


def test_large_wraparound():
    """Test many wraparounds to stress bitwise operations"""
    q = QueueCircularOptimized(4)  # Capacity 4, effective 3

    # Fill and empty multiple times to force wraparound
    for cycle in range(10):
        # Fill
        q.enqueue(cycle * 3 + 1)
        q.enqueue(cycle * 3 + 2)
        q.enqueue(cycle * 3 + 3)
        assert q.is_full() == True

        # Empty
        assert q.dequeue() == cycle * 3 + 1
        assert q.dequeue() == cycle * 3 + 2
        assert q.dequeue() == cycle * 3 + 3
        assert q.is_empty() == True


def test_front_without_modifying():
    """Test that front() doesn't modify queue"""
    q = QueueCircularOptimized(4)
    q.enqueue(100)
    q.enqueue(200)

    # Multiple front() calls shouldn't change anything
    assert q.front() == 100
    assert q.front() == 100
    assert q.size() == 2
    assert q.to_list() == [100, 200]


def test_edge_case_capacity_one():
    """Test edge case: requested capacity of 1"""
    q = QueueCircularOptimized(1)  # Will have capacity 1, effective 0

    assert q.is_empty() == True
    assert q.capacity_actual() == 1
    assert q.capacity_effective() == 0

    # Can't add anything due to effective capacity 0
    assert q.is_full() == True
    try:
        q.enqueue(99)
        assert False, "Should raise exception"
    except IndexError:
        pass


if __name__ == "__main__":
    test_power_of_2_capacity()
    test_empty_queue()
    test_single_element()
    test_fill_to_capacity()
    test_fifo_order()
    test_wraparound_with_bitwise()
    test_alternating_operations()
    test_large_wraparound()
    test_front_without_modifying()
    test_edge_case_capacity_one()
    print("All optimized circular queue tests passed!")