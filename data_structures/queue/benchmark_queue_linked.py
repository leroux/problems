import time
import matplotlib.pyplot as plt
from queue_linked import QueueLinked
from collections import deque


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def benchmark_enqueue():
    print("Benchmarking enqueue...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    linked_times = []
    deque_times = []

    for size in sizes:
        # Linked list queue
        q_linked = QueueLinked()
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_linked.enqueue, i)
            total_time += elapsed
        avg_linked = (total_time / size) * 1000000
        linked_times.append(avg_linked)
        print(f"  Size {size}: {avg_linked:.2f} μs per enqueue (linked)")

        # Python deque
        q_deque = deque()
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_deque.append, i)
            total_time += elapsed
        avg_deque = (total_time / size) * 1000000
        deque_times.append(avg_deque)
        print(f"  Size {size}: {avg_deque:.2f} μs per enqueue (deque)")

    return sizes, linked_times, deque_times


def benchmark_dequeue():
    print("\nBenchmarking dequeue...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    linked_times = []
    deque_times = []

    for size in sizes:
        # Linked list queue - pre-populate
        q_linked = QueueLinked()
        for i in range(size):
            q_linked.enqueue(i)

        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_linked.dequeue)
            total_time += elapsed
        avg_linked = (total_time / size) * 1000000
        linked_times.append(avg_linked)
        print(f"  Size {size}: {avg_linked:.2f} μs per dequeue (linked)")

        # Python deque - pre-populate
        q_deque = deque(range(size))
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_deque.popleft)
            total_time += elapsed
        avg_deque = (total_time / size) * 1000000
        deque_times.append(avg_deque)
        print(f"  Size {size}: {avg_deque:.2f} μs per dequeue (deque)")

    return sizes, linked_times, deque_times


def benchmark_front():
    print("\nBenchmarking front/peek...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    linked_times = []
    deque_times = []

    for size in sizes:
        # Linked list queue
        q_linked = QueueLinked()
        for i in range(size):
            q_linked.enqueue(i)

        total_time = 0
        num_peeks = 1000
        for i in range(num_peeks):
            elapsed, _ = time_operation(q_linked.front)
            total_time += elapsed
        avg_linked = (total_time / num_peeks) * 1000000
        linked_times.append(avg_linked)
        print(f"  Size {size}: {avg_linked:.2f} μs per front (linked)")

        # Python deque
        q_deque = deque(range(size))
        total_time = 0
        for i in range(num_peeks):
            elapsed, _ = time_operation(lambda: q_deque[0])
            total_time += elapsed
        avg_deque = (total_time / num_peeks) * 1000000
        deque_times.append(avg_deque)
        print(f"  Size {size}: {avg_deque:.2f} μs per front (deque)")

    return sizes, linked_times, deque_times


def benchmark_size():
    print("\nBenchmarking size...")
    sizes = [1000, 5000, 10000, 25000, 50000]
    linked_times = []
    deque_times = []

    for size in sizes:
        # Linked list queue - O(n) size calculation
        q_linked = QueueLinked()
        for i in range(size):
            q_linked.enqueue(i)

        elapsed, _ = time_operation(q_linked.size)
        linked_times.append(elapsed * 1000000)
        print(f"  Size {size}: {elapsed * 1000000:.2f} μs for size() (linked)")

        # Python deque - O(1) size
        q_deque = deque(range(size))
        elapsed, _ = time_operation(len, q_deque)
        deque_times.append(elapsed * 1000000)
        print(f"  Size {size}: {elapsed * 1000000:.2f} μs for size() (deque)")

    return sizes, linked_times, deque_times


def benchmark_mixed_operations():
    print("\nBenchmarking mixed operations (enqueue/dequeue pattern)...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    linked_times = []
    deque_times = []

    for size in sizes:
        # Linked queue
        q_linked = QueueLinked()
        start = time.perf_counter()
        # Pattern: enqueue N, dequeue N/2, enqueue N/2, dequeue all
        for i in range(size):
            q_linked.enqueue(i)
        for i in range(size // 2):
            q_linked.dequeue()
        for i in range(size, size + size // 2):
            q_linked.enqueue(i)
        while not q_linked.is_empty():
            q_linked.dequeue()
        linked_time = (time.perf_counter() - start) * 1000000
        linked_times.append(linked_time)
        print(f"  Size {size}: {linked_time:.2f} μs mixed ops (linked)")

        # Python deque
        q_deque = deque()
        start = time.perf_counter()
        for i in range(size):
            q_deque.append(i)
        for i in range(size // 2):
            q_deque.popleft()
        for i in range(size, size + size // 2):
            q_deque.append(i)
        while q_deque:
            q_deque.popleft()
        deque_time = (time.perf_counter() - start) * 1000000
        deque_times.append(deque_time)
        print(f"  Size {size}: {deque_time:.2f} μs mixed ops (deque)")

    return sizes, linked_times, deque_times


def plot_results():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, _)) = plt.subplots(3, 2, figsize=(14, 12))

    # Enqueue comparison
    sizes, linked_times, deque_times = benchmark_enqueue()
    ax1.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax1.plot(sizes, deque_times, 'b-s', label='Python deque', linewidth=2, markersize=6)
    ax1.set_title('Enqueue Performance (Should be O(1))')
    ax1.set_xlabel('Queue Size')
    ax1.set_ylabel('Time per enqueue (μs)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Dequeue comparison
    sizes, linked_times, deque_times = benchmark_dequeue()
    ax2.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax2.plot(sizes, deque_times, 'b-s', label='Python deque', linewidth=2, markersize=6)
    ax2.set_title('Dequeue Performance (Should be O(1))')
    ax2.set_xlabel('Queue Size')
    ax2.set_ylabel('Time per dequeue (μs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Front/peek comparison
    sizes, linked_times, deque_times = benchmark_front()
    ax3.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax3.plot(sizes, deque_times, 'b-s', label='Python deque', linewidth=2, markersize=6)
    ax3.set_title('Front/Peek Performance (Should be O(1))')
    ax3.set_xlabel('Queue Size')
    ax3.set_ylabel('Time per front (μs)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Size comparison
    sizes, linked_times, deque_times = benchmark_size()
    ax4.plot(sizes, linked_times, 'r-o', label='Linked Queue O(n)', linewidth=2, markersize=6)
    ax4.plot(sizes, deque_times, 'b-s', label='Python deque O(1)', linewidth=2, markersize=6)
    ax4.set_title('Size Operation Performance')
    ax4.set_xlabel('Queue Size')
    ax4.set_ylabel('Time for size() (μs)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_yscale('log')

    # Mixed operations
    sizes, linked_times, deque_times = benchmark_mixed_operations()
    ax5.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax5.plot(sizes, deque_times, 'b-s', label='Python deque', linewidth=2, markersize=6)
    ax5.set_title('Mixed Operations Performance')
    ax5.set_xlabel('Operation Size')
    ax5.set_ylabel('Total time (μs)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('queue_linked_benchmarks.png', dpi=150, bbox_inches='tight')
    print(f"\nBenchmark plot saved as 'queue_linked_benchmarks.png'")


if __name__ == "__main__":
    plot_results()