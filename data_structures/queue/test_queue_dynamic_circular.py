from queue_dynamic_circular import QueueDynamicCircular


def test_empty_queue():
    """Test operations on empty queue"""
    q = QueueDynamicCircular(4)
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


def test_basic_operations():
    """Test basic enqueue/dequeue without resizing"""
    q = QueueDynamicCircular(8)  # Start with capacity 8

    # Add some items (within initial capacity)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    assert q.size() == 3
    assert q.front() == 1
    print(q.to_list())
    assert q.to_list() == [1, 2, 3]

    # Remove in FIFO order
    assert q.dequeue() == 1
    assert q.front() == 2
    assert q.size() == 2

    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty() == True


def test_wraparound_without_resize():
    """Test wraparound within initial capacity"""
    q = QueueDynamicCircular(8)  # Capacity 8, effective 7

    # Fill partway
    for i in range(4):
        q.enqueue(i)

    # Remove some to create space at front
    assert q.dequeue() == 0
    assert q.dequeue() == 1

    # Add more - should wrap around
    q.enqueue(4)
    q.enqueue(5)
    q.enqueue(6)

    assert q.to_list() == [2, 3, 4, 5, 6]
    assert q.size() == 5


def test_single_resize():
    """Test resizing when queue gets full"""
    q = QueueDynamicCircular(4)  # Start small: capacity 4, effective 3

    # Fill to capacity
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.size() == 3

    # This should trigger resize
    q.enqueue(4)
    assert q.size() == 4
    assert q.to_list() == [1, 2, 3, 4]

    # Verify we can add more after resize
    q.enqueue(5)
    q.enqueue(6)
    assert q.to_list() == [1, 2, 3, 4, 5, 6]


def test_multiple_resizes():
    """Test multiple resize operations"""
    q = QueueDynamicCircular(2)  # Very small start: capacity 2, effective 1

    # This should trigger multiple resizes
    for i in range(10):
        q.enqueue(i)

    assert q.size() == 10
    assert q.to_list() == list(range(10))

    # Verify FIFO order still works
    for i in range(10):
        assert q.dequeue() == i

    assert q.is_empty() == True


def test_resize_with_wraparound():
    """Test resizing when head/tail have wrapped around"""
    q = QueueDynamicCircular(4)  # Capacity 4, effective 3

    # Fill and partially empty to create wraparound
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    # Remove from front
    assert q.dequeue() == 1

    # Add more - now we have wraparound
    q.enqueue(4)
    q.enqueue(5)  # Should be at capacity

    # This should trigger resize with wraparound
    q.enqueue(6)

    assert q.to_list() == [2, 3, 4, 5, 6]
    assert q.size() == 5


def test_alternating_operations_with_resize():
    """Test alternating enqueue/dequeue that triggers resizes"""
    q = QueueDynamicCircular(4)

    # Cycle 0: add [0,1,2,3,4], remove 2 items → leaves [2,3,4]
    for i in range(5):
        q.enqueue(i)
    q.dequeue()  # removes 0
    q.dequeue()  # removes 1

    # Cycle 1: add [5,6,7,8,9], remove 2 items → leaves [4,5,6,7,8,9]
    for i in range(5, 10):
        q.enqueue(i)
    q.dequeue()  # removes 2
    q.dequeue()  # removes 3

    # Cycle 2: add [10,11,12,13,14], remove 2 items → leaves [6,7,8,9,10,11,12,13,14]
    for i in range(10, 15):
        q.enqueue(i)
    q.dequeue()  # removes 4
    q.dequeue()  # removes 5

    # Final queue should be [6,7,8,9,10,11,12,13,14]
    expected = [6, 7, 8, 9, 10, 11, 12, 13, 14]

    print(q.to_list())
    assert q.to_list() == expected


def test_resize_preserves_order():
    """Test that resizing preserves exact FIFO order"""
    q = QueueDynamicCircular(4)

    # Create specific pattern that forces wraparound before resize
    items = [10, 20, 30, 40, 50, 60, 70, 80, 90]

    # Add first 3
    for item in items[:3]:
        q.enqueue(item)

    # Remove 2 (creates space at front)
    q.dequeue()
    q.dequeue()

    # Add rest (should wrap around then resize)
    for item in items[3:]:
        q.enqueue(item)

    # Verify order is preserved
    expected = [items[2]] + items[3:]  # 30 (remaining) + 40,50,60,70,80,90
    assert q.to_list() == expected

    # Verify dequeue order
    for expected_val in expected:
        assert q.dequeue() == expected_val


def test_capacity_tracking():
    """Test that capacity grows as expected"""
    q = QueueDynamicCircular(4)
    initial_capacity = q.capacity

    # Fill beyond initial capacity
    for i in range(10):
        q.enqueue(i)

    # Capacity should have grown
    assert q.capacity > initial_capacity

    # Should be power of 2
    capacity = q.capacity
    assert (capacity & (capacity - 1)) == 0  # Power of 2 check


def test_front_during_resize():
    """Test that front() works correctly during and after resize"""
    q = QueueDynamicCircular(4)

    q.enqueue(100)
    q.enqueue(200)
    q.enqueue(300)

    # Front should be stable
    assert q.front() == 100

    # Trigger resize
    q.enqueue(400)
    q.enqueue(500)

    # Front should still be correct
    assert q.front() == 100
    assert q.to_list() == [100, 200, 300, 400, 500]


def test_empty_after_resize():
    """Test emptying queue after it has been resized"""
    q = QueueDynamicCircular(2)

    # Fill and trigger resizes
    for i in range(8):
        q.enqueue(i)

    # Empty completely
    while not q.is_empty():
        q.dequeue()

    assert q.is_empty() == True
    assert q.size() == 0
    assert q.to_list() == []

    # Should be able to use again
    q.enqueue(999)
    assert q.front() == 999


if __name__ == "__main__":
    test_empty_queue()
    test_basic_operations()
    test_wraparound_without_resize()
    test_single_resize()
    test_multiple_resizes()
    test_resize_with_wraparound()
    test_alternating_operations_with_resize()
    test_resize_preserves_order()
    test_capacity_tracking()
    test_front_during_resize()
    test_empty_after_resize()
    print("All dynamic circular queue tests passed!")