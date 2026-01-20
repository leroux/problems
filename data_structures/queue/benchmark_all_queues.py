import time
import matplotlib.pyplot as plt
from queue_linked import QueueLinked
from queue_circular import QueueCircular
from queue_dynamic_circular import QueueDynamicCircular
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
    circular_times = []
    dynamic_times = []
    deque_times = []

    for size in sizes:
        # Linked queue
        q_linked = QueueLinked()
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_linked.enqueue, i)
            total_time += elapsed
        avg_linked = (total_time / size) * 1000000
        linked_times.append(avg_linked)
        print(f"  Size {size}: {avg_linked:.2f} μs per enqueue (linked)")

        # Circular queue (dynamic capacity)
        q_circular = QueueCircular(size + 1000)  # Give it plenty of space
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_circular.enqueue, i)
            total_time += elapsed
        avg_circular = (total_time / size) * 1000000
        circular_times.append(avg_circular)
        print(f"  Size {size}: {avg_circular:.2f} μs per enqueue (circular)")

        # Dynamic circular queue
        q_dynamic = QueueDynamicCircular()
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_dynamic.enqueue, i)
            total_time += elapsed
        avg_dynamic = (total_time / size) * 1000000
        dynamic_times.append(avg_dynamic)
        print(f"  Size {size}: {avg_dynamic:.2f} μs per enqueue (dynamic)")

        # Python deque
        q_deque = deque()
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_deque.append, i)
            total_time += elapsed
        avg_deque = (total_time / size) * 1000000
        deque_times.append(avg_deque)
        print(f"  Size {size}: {avg_deque:.2f} μs per enqueue (deque)")

    return sizes, linked_times, circular_times, dynamic_times, deque_times


def benchmark_dequeue():
    print("\nBenchmarking dequeue...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    linked_times = []
    circular_times = []
    dynamic_times = []
    deque_times = []

    for size in sizes:
        # Linked queue - pre-populate
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

        # Circular queue - pre-populate
        q_circular = QueueCircular(size + 1000)
        for i in range(size):
            q_circular.enqueue(i)

        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_circular.dequeue)
            total_time += elapsed
        avg_circular = (total_time / size) * 1000000
        circular_times.append(avg_circular)
        print(f"  Size {size}: {avg_circular:.2f} μs per dequeue (circular)")

        # Dynamic circular queue - pre-populate
        q_dynamic = QueueDynamicCircular()
        for i in range(size):
            q_dynamic.enqueue(i)

        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_dynamic.dequeue)
            total_time += elapsed
        avg_dynamic = (total_time / size) * 1000000
        dynamic_times.append(avg_dynamic)
        print(f"  Size {size}: {avg_dynamic:.2f} μs per dequeue (dynamic)")

        # Python deque - pre-populate
        q_deque = deque(range(size))
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_deque.popleft)
            total_time += elapsed
        avg_deque = (total_time / size) * 1000000
        deque_times.append(avg_deque)
        print(f"  Size {size}: {avg_deque:.2f} μs per dequeue (deque)")

    return sizes, linked_times, circular_times, dynamic_times, deque_times


def benchmark_front():
    print("\nBenchmarking front/peek...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    linked_times = []
    circular_times = []
    dynamic_times = []
    deque_times = []

    for size in sizes:
        # Linked queue
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

        # Circular queue
        q_circular = QueueCircular(size + 1000)
        for i in range(size):
            q_circular.enqueue(i)

        total_time = 0
        for i in range(num_peeks):
            elapsed, _ = time_operation(q_circular.front)
            total_time += elapsed
        avg_circular = (total_time / num_peeks) * 1000000
        circular_times.append(avg_circular)
        print(f"  Size {size}: {avg_circular:.2f} μs per front (circular)")

        # Dynamic circular queue
        q_dynamic = QueueDynamicCircular()
        for i in range(size):
            q_dynamic.enqueue(i)

        total_time = 0
        for i in range(num_peeks):
            elapsed, _ = time_operation(q_dynamic.front)
            total_time += elapsed
        avg_dynamic = (total_time / num_peeks) * 1000000
        dynamic_times.append(avg_dynamic)
        print(f"  Size {size}: {avg_dynamic:.2f} μs per front (dynamic)")

        # Python deque
        q_deque = deque(range(size))
        total_time = 0
        for i in range(num_peeks):
            elapsed, _ = time_operation(lambda: q_deque[0])
            total_time += elapsed
        avg_deque = (total_time / num_peeks) * 1000000
        deque_times.append(avg_deque)
        print(f"  Size {size}: {avg_deque:.2f} μs per front (deque)")

    return sizes, linked_times, circular_times, dynamic_times, deque_times


def benchmark_mixed_operations():
    print("\nBenchmarking mixed operations...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    linked_times = []
    circular_times = []
    dynamic_times = []
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

        # Circular queue
        q_circular = QueueCircular(size * 2)  # Give enough space
        start = time.perf_counter()
        for i in range(size):
            q_circular.enqueue(i)
        for i in range(size // 2):
            q_circular.dequeue()
        for i in range(size, size + size // 2):
            q_circular.enqueue(i)
        while not q_circular.is_empty():
            q_circular.dequeue()
        circular_time = (time.perf_counter() - start) * 1000000
        circular_times.append(circular_time)
        print(f"  Size {size}: {circular_time:.2f} μs mixed ops (circular)")

        # Dynamic circular queue
        q_dynamic = QueueDynamicCircular()
        start = time.perf_counter()
        for i in range(size):
            q_dynamic.enqueue(i)
        for i in range(size // 2):
            q_dynamic.dequeue()
        for i in range(size, size + size // 2):
            q_dynamic.enqueue(i)
        while not q_dynamic.is_empty():
            q_dynamic.dequeue()
        dynamic_time = (time.perf_counter() - start) * 1000000
        dynamic_times.append(dynamic_time)
        print(f"  Size {size}: {dynamic_time:.2f} μs mixed ops (dynamic)")

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

    return sizes, linked_times, circular_times, dynamic_times, deque_times


def benchmark_wraparound_stress():
    print("\nBenchmarking wraparound stress (circular only)...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    circular_times = []

    for size in sizes:
        # Fixed capacity circular queue - force lots of wraparound
        capacity = size // 4  # Small capacity forces wraparound
        q_circular = QueueCircular(capacity)

        start = time.perf_counter()
        # Fill to near capacity
        for i in range(capacity - 1):
            q_circular.enqueue(i)

        # Now alternate: add one, remove one (lots of wraparound)
        for i in range(size):
            if not q_circular.is_full():
                q_circular.enqueue(i + capacity)
            if not q_circular.is_empty():
                q_circular.dequeue()

        # Clean up remaining
        while not q_circular.is_empty():
            q_circular.dequeue()

        circular_time = (time.perf_counter() - start) * 1000000
        circular_times.append(circular_time)
        print(f"  Size {size}: {circular_time:.2f} μs wraparound stress")

    return sizes, circular_times


def plot_results():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 14))

    # Enqueue comparison
    sizes, linked_times, circular_times, dynamic_times, deque_times = benchmark_enqueue()
    ax1.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax1.plot(sizes, circular_times, 'g-s', label='Circular Buffer', linewidth=2, markersize=6)
    ax1.plot(sizes, dynamic_times, 'm-d', label='Dynamic Circular', linewidth=2, markersize=6)
    ax1.plot(sizes, deque_times, 'b-^', label='Python deque', linewidth=2, markersize=6)
    ax1.set_title('Enqueue Performance (Should be O(1))')
    ax1.set_xlabel('Queue Size')
    ax1.set_ylabel('Time per enqueue (μs)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Dequeue comparison
    sizes, linked_times, circular_times, dynamic_times, deque_times = benchmark_dequeue()
    ax2.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax2.plot(sizes, circular_times, 'g-s', label='Circular Buffer', linewidth=2, markersize=6)
    ax2.plot(sizes, dynamic_times, 'm-d', label='Dynamic Circular', linewidth=2, markersize=6)
    ax2.plot(sizes, deque_times, 'b-^', label='Python deque', linewidth=2, markersize=6)
    ax2.set_title('Dequeue Performance (Should be O(1))')
    ax2.set_xlabel('Queue Size')
    ax2.set_ylabel('Time per dequeue (μs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Front/peek comparison
    sizes, linked_times, circular_times, dynamic_times, deque_times = benchmark_front()
    ax3.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax3.plot(sizes, circular_times, 'g-s', label='Circular Buffer', linewidth=2, markersize=6)
    ax3.plot(sizes, dynamic_times, 'm-d', label='Dynamic Circular', linewidth=2, markersize=6)
    ax3.plot(sizes, deque_times, 'b-^', label='Python deque', linewidth=2, markersize=6)
    ax3.set_title('Front/Peek Performance (Should be O(1))')
    ax3.set_xlabel('Queue Size')
    ax3.set_ylabel('Time per front (μs)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Mixed operations
    sizes, linked_times, circular_times, dynamic_times, deque_times = benchmark_mixed_operations()
    ax4.plot(sizes, linked_times, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax4.plot(sizes, circular_times, 'g-s', label='Circular Buffer', linewidth=2, markersize=6)
    ax4.plot(sizes, dynamic_times, 'm-d', label='Dynamic Circular', linewidth=2, markersize=6)
    ax4.plot(sizes, deque_times, 'b-^', label='Python deque', linewidth=2, markersize=6)
    ax4.set_title('Mixed Operations Performance')
    ax4.set_xlabel('Operation Size')
    ax4.set_ylabel('Total time (μs)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Wraparound stress (circular only)
    sizes, circular_times = benchmark_wraparound_stress()
    ax5.plot(sizes, circular_times, 'g-s', label='Circular Buffer Wraparound', linewidth=2, markersize=6)
    ax5.set_title('Wraparound Stress Test (Circular Only)')
    ax5.set_xlabel('Operations')
    ax5.set_ylabel('Total time (μs)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # Performance ratios
    sizes, linked_times, circular_times, dynamic_times, deque_times = benchmark_enqueue()
    linked_vs_circular = [l/c for l, c in zip(linked_times, circular_times)]
    circular_vs_deque = [c/d for c, d in zip(circular_times, deque_times)]
    ax6.plot(sizes, linked_vs_circular, 'purple', marker='o', label='Linked/Circular Ratio', linewidth=2)
    ax6.plot(sizes, circular_vs_deque, 'orange', marker='s', label='Circular/Deque Ratio', linewidth=2)
    ax6.axhline(y=1.0, color='black', linestyle='--', alpha=0.7, label='Equal Performance')
    ax6.set_title('Performance Ratios (Enqueue)')
    ax6.set_xlabel('Queue Size')
    ax6.set_ylabel('Ratio (>1 = slower)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('all_queue_benchmarks.png', dpi=150, bbox_inches='tight')
    print(f"\nBenchmark plot saved as 'all_queue_benchmarks.png'")


if __name__ == "__main__":
    plot_results()