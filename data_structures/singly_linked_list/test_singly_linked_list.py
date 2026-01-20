from singly_linked_list import SinglyLinkedList


def test_empty_list():
    """Test operations on empty list"""
    ll = SinglyLinkedList()
    assert ll.is_empty() == True
    assert ll.size() == 0
    assert ll.to_list() == []

    # Test exceptions on empty list
    try:
        ll.get(0)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        ll.delete(0)
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_append():
    """Test append operation"""
    ll = SinglyLinkedList()

    # Append single element
    ll.append(1)
    assert ll.size() == 1
    assert ll.is_empty() == False
    assert ll.to_list() == [1]
    assert ll.get(0) == 1

    # Append multiple elements
    ll.append(2)
    ll.append(3)
    assert ll.size() == 3
    assert ll.to_list() == [1, 2, 3]
    assert ll.get(0) == 1
    assert ll.get(1) == 2
    assert ll.get(2) == 3


def test_prepend():
    """Test prepend operation"""
    ll = SinglyLinkedList()

    # Prepend to empty list
    ll.prepend(1)
    assert ll.to_list() == [1]

    # Prepend multiple elements
    ll.prepend(2)
    ll.prepend(3)
    assert ll.to_list() == [3, 2, 1]
    assert ll.size() == 3


def test_insert():
    """Test insert at various positions"""
    ll = SinglyLinkedList()

    # Insert at beginning (empty list)
    ll.insert(0, 1)
    assert ll.to_list() == [1]

    # Insert at end
    ll.insert(1, 3)
    assert ll.to_list() == [1, 3]

    # Insert in middle
    ll.insert(1, 2)
    assert ll.to_list() == [1, 2, 3]

    # Insert at beginning (non-empty)
    ll.insert(0, 0)
    assert ll.to_list() == [0, 1, 2, 3]

    # Insert at end
    ll.insert(4, 4)
    assert ll.to_list() == [0, 1, 2, 3, 4]

    # Test out of bounds
    try:
        ll.insert(-1, 999)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        ll.insert(10, 999)
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_delete():
    """Test delete at various positions"""
    ll = SinglyLinkedList()
    for i in range(5):  # [0, 1, 2, 3, 4]
        ll.append(i)

    # Delete from middle
    deleted = ll.delete(2)
    assert deleted == 2
    assert ll.to_list() == [0, 1, 3, 4]
    assert ll.size() == 4

    # Delete from beginning
    deleted = ll.delete(0)
    assert deleted == 0
    assert ll.to_list() == [1, 3, 4]

    # Delete from end
    deleted = ll.delete(2)
    assert deleted == 4
    assert ll.to_list() == [1, 3]

    # Delete remaining elements
    ll.delete(0)
    ll.delete(0)
    assert ll.is_empty() == True
    assert ll.size() == 0


def test_get():
    """Test get operation"""
    ll = SinglyLinkedList()
    for i in range(5):
        ll.append(i * 10)  # [0, 10, 20, 30, 40]

    assert ll.get(0) == 0
    assert ll.get(1) == 10
    assert ll.get(4) == 40

    # Test out of bounds
    try:
        ll.get(-1)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        ll.get(5)
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_find():
    """Test find operation"""
    ll = SinglyLinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    ll.append(20)  # duplicate

    # Find existing elements
    assert ll.find(10) == 0
    assert ll.find(20) == 1  # Should return first occurrence
    assert ll.find(30) == 2

    # Find non-existing element
    assert ll.find(999) == -1


def test_mixed_operations():
    """Test combination of operations"""
    ll = SinglyLinkedList()

    # Build: [5, 1, 2, 3, 6]
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(5)
    ll.insert(4, 6)

    assert ll.to_list() == [5, 1, 2, 3, 6]
    assert ll.size() == 5

    # Delete middle element
    ll.delete(2)  # Remove 2
    assert ll.to_list() == [5, 1, 3, 6]

    # Find elements
    assert ll.find(5) == 0
    assert ll.find(6) == 3
    assert ll.find(999) == -1




def test_edge_cases():
    """Test edge cases"""
    ll = SinglyLinkedList()

    # Single element operations
    ll.append(42)
    assert ll.get(0) == 42
    assert ll.find(42) == 0
    assert ll.delete(0) == 42
    assert ll.is_empty() == True

    # Prepend then delete
    ll.prepend(100)
    assert ll.delete(0) == 100
    assert ll.is_empty() == True


if __name__ == "__main__":
    test_empty_list()
    test_append()
    test_prepend()
    test_insert()
    test_delete()
    test_get()
    test_find()
    test_mixed_operations()
    test_edge_cases()
    print("All tests passed!")