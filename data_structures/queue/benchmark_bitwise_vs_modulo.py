import time
import matplotlib.pyplot as plt
from queue_circular import QueueCircular
from queue_circular_optimized import QueueCircularOptimized


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def benchmark_enqueue_comparison():
    print("Benchmarking enqueue: Modulo vs Bitwise...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    modulo_times = []
    bitwise_times = []

    for size in sizes:
        # Original modulo version
        q_modulo = QueueCircular(size + 1000)
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_modulo.enqueue, i)
            total_time += elapsed
        avg_modulo = (total_time / size) * 1000000
        modulo_times.append(avg_modulo)
        print(f"  Size {size}: {avg_modulo:.2f} μs per enqueue (modulo)")

        # Optimized bitwise version
        q_bitwise = QueueCircularOptimized(size + 1000)
        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_bitwise.enqueue, i)
            total_time += elapsed
        avg_bitwise = (total_time / size) * 1000000
        bitwise_times.append(avg_bitwise)
        print(f"  Size {size}: {avg_bitwise:.2f} μs per enqueue (bitwise)")

        speedup = avg_modulo / avg_bitwise
        print(f"  Speedup: {speedup:.2f}x")

    return sizes, modulo_times, bitwise_times


def benchmark_dequeue_comparison():
    print("\nBenchmarking dequeue: Modulo vs Bitwise...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    modulo_times = []
    bitwise_times = []

    for size in sizes:
        # Original modulo version - pre-populate
        q_modulo = QueueCircular(size + 1000)
        for i in range(size):
            q_modulo.enqueue(i)

        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_modulo.dequeue)
            total_time += elapsed
        avg_modulo = (total_time / size) * 1000000
        modulo_times.append(avg_modulo)
        print(f"  Size {size}: {avg_modulo:.2f} μs per dequeue (modulo)")

        # Optimized bitwise version - pre-populate
        q_bitwise = QueueCircularOptimized(size + 1000)
        for i in range(size):
            q_bitwise.enqueue(i)

        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(q_bitwise.dequeue)
            total_time += elapsed
        avg_bitwise = (total_time / size) * 1000000
        bitwise_times.append(avg_bitwise)
        print(f"  Size {size}: {avg_bitwise:.2f} μs per dequeue (bitwise)")

        speedup = avg_modulo / avg_bitwise
        print(f"  Speedup: {speedup:.2f}x")

    return sizes, modulo_times, bitwise_times


def benchmark_mixed_operations_comparison():
    print("\nBenchmarking mixed operations: Modulo vs Bitwise...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    modulo_times = []
    bitwise_times = []

    for size in sizes:
        # Original modulo version
        q_modulo = QueueCircular(size * 2)
        start = time.perf_counter()
        # Pattern: enqueue N, dequeue N/2, enqueue N/2, dequeue all
        for i in range(size):
            q_modulo.enqueue(i)
        for i in range(size // 2):
            q_modulo.dequeue()
        for i in range(size, size + size // 2):
            q_modulo.enqueue(i)
        while not q_modulo.is_empty():
            q_modulo.dequeue()
        modulo_time = (time.perf_counter() - start) * 1000000
        modulo_times.append(modulo_time)
        print(f"  Size {size}: {modulo_time:.2f} μs mixed ops (modulo)")

        # Optimized bitwise version
        q_bitwise = QueueCircularOptimized(size * 2)
        start = time.perf_counter()
        for i in range(size):
            q_bitwise.enqueue(i)
        for i in range(size // 2):
            q_bitwise.dequeue()
        for i in range(size, size + size // 2):
            q_bitwise.enqueue(i)
        while not q_bitwise.is_empty():
            q_bitwise.dequeue()
        bitwise_time = (time.perf_counter() - start) * 1000000
        bitwise_times.append(bitwise_time)
        print(f"  Size {size}: {bitwise_time:.2f} μs mixed ops (bitwise)")

        speedup = modulo_time / bitwise_time
        print(f"  Speedup: {speedup:.2f}x")

    return sizes, modulo_times, bitwise_times


def benchmark_wraparound_stress():
    print("\nBenchmarking wraparound stress: Modulo vs Bitwise...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    modulo_times = []
    bitwise_times = []

    for size in sizes:
        # Original modulo version - force lots of wraparound
        capacity = max(16, size // 4)  # Ensure power of 2 for fair comparison
        q_modulo = QueueCircular(capacity)

        start = time.perf_counter()
        # Fill to near capacity
        for i in range(capacity - 1):
            q_modulo.enqueue(i)

        # Now alternate: add one, remove one (lots of wraparound)
        for i in range(size):
            if not q_modulo.is_full():
                q_modulo.enqueue(i + capacity)
            if not q_modulo.is_empty():
                q_modulo.dequeue()

        # Clean up remaining
        while not q_modulo.is_empty():
            q_modulo.dequeue()

        modulo_time = (time.perf_counter() - start) * 1000000
        modulo_times.append(modulo_time)
        print(f"  Size {size}: {modulo_time:.2f} μs wraparound stress (modulo)")

        # Optimized bitwise version
        q_bitwise = QueueCircularOptimized(capacity)

        start = time.perf_counter()
        # Fill to near capacity
        for i in range(capacity - 1):
            q_bitwise.enqueue(i)

        # Now alternate: add one, remove one (lots of wraparound)
        for i in range(size):
            if not q_bitwise.is_full():
                q_bitwise.enqueue(i + capacity)
            if not q_bitwise.is_empty():
                q_bitwise.dequeue()

        # Clean up remaining
        while not q_bitwise.is_empty():
            q_bitwise.dequeue()

        bitwise_time = (time.perf_counter() - start) * 1000000
        bitwise_times.append(bitwise_time)
        print(f"  Size {size}: {bitwise_time:.2f} μs wraparound stress (bitwise)")

        speedup = modulo_time / bitwise_time
        print(f"  Speedup: {speedup:.2f}x")

    return sizes, modulo_times, bitwise_times


def plot_comparison():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # Enqueue comparison
    sizes, modulo_times, bitwise_times = benchmark_enqueue_comparison()
    ax1.plot(sizes, modulo_times, 'r-o', label='Modulo (%)', linewidth=2, markersize=6)
    ax1.plot(sizes, bitwise_times, 'g-s', label='Bitwise (&)', linewidth=2, markersize=6)
    ax1.set_title('Enqueue Performance: Modulo vs Bitwise')
    ax1.set_xlabel('Queue Size')
    ax1.set_ylabel('Time per enqueue (μs)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Dequeue comparison
    sizes, modulo_times, bitwise_times = benchmark_dequeue_comparison()
    ax2.plot(sizes, modulo_times, 'r-o', label='Modulo (%)', linewidth=2, markersize=6)
    ax2.plot(sizes, bitwise_times, 'g-s', label='Bitwise (&)', linewidth=2, markersize=6)
    ax2.set_title('Dequeue Performance: Modulo vs Bitwise')
    ax2.set_xlabel('Queue Size')
    ax2.set_ylabel('Time per dequeue (μs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Mixed operations
    sizes, modulo_times, bitwise_times = benchmark_mixed_operations_comparison()
    ax3.plot(sizes, modulo_times, 'r-o', label='Modulo (%)', linewidth=2, markersize=6)
    ax3.plot(sizes, bitwise_times, 'g-s', label='Bitwise (&)', linewidth=2, markersize=6)
    ax3.set_title('Mixed Operations: Modulo vs Bitwise')
    ax3.set_xlabel('Operation Size')
    ax3.set_ylabel('Total time (μs)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Wraparound stress test
    sizes, modulo_times, bitwise_times = benchmark_wraparound_stress()
    ax4.plot(sizes, modulo_times, 'r-o', label='Modulo (%)', linewidth=2, markersize=6)
    ax4.plot(sizes, bitwise_times, 'g-s', label='Bitwise (&)', linewidth=2, markersize=6)
    ax4.set_title('Wraparound Stress Test: Modulo vs Bitwise')
    ax4.set_xlabel('Operations')
    ax4.set_ylabel('Total time (μs)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('bitwise_vs_modulo_benchmark.png', dpi=150, bbox_inches='tight')
    print(f"\nBenchmark comparison saved as 'bitwise_vs_modulo_benchmark.png'")


if __name__ == "__main__":
    plot_comparison()