import sys
import gc
import matplotlib.pyplot as plt
from queue_linked import QueueLinked
from queue_circular import QueueCircular
from queue_dynamic_circular import QueueDynamicCircular
from collections import deque


def get_size(obj):
    """Calculate approximate memory size of queue object and its data"""
    size = sys.getsizeof(obj)

    # Add size of internal data structures
    if hasattr(obj, 'data') and obj.data is not None:
        size += sys.getsizeof(obj.data)
        # Add size of stored elements (approximation)
        if len(obj.data) > 0:
            # Sample first non-None element to estimate size
            sample_element = next((x for x in obj.data if x is not None), None)
            if sample_element is not None:
                element_size = sys.getsizeof(sample_element)
                actual_elements = sum(1 for x in obj.data if x is not None)
                size += element_size * actual_elements

    # Handle linked list nodes (our implementation uses dummy_head)
    if hasattr(obj, 'dummy_head') and obj.dummy_head is not None:
        # Walk the linked list starting from dummy_head.next
        size += sys.getsizeof(obj.dummy_head)  # Include dummy node
        current = obj.dummy_head.next
        node_count = 0
        while current and node_count < 100000:  # Safety limit
            size += sys.getsizeof(current)
            if hasattr(current, 'val') and current.val is not None:
                size += sys.getsizeof(current.val)
            current = getattr(current, 'next', None)
            node_count += 1

    # Handle deque
    if hasattr(obj, '__len__') and hasattr(obj, '__iter__'):
        try:
            for item in obj:
                size += sys.getsizeof(item)
                break  # Just sample one element and multiply
            size += sys.getsizeof(next(iter(obj), 0)) * len(obj)
        except:
            pass

    return size


def benchmark_memory_per_element():
    print("Benchmarking memory per element...")
    sizes = [1000, 5000, 10000, 25000, 50000]

    linked_memory = []
    circular_memory = []
    dynamic_memory = []
    deque_memory = []

    for size in sizes:
        gc.collect()  # Clean up before measuring

        # Linked queue
        q_linked = QueueLinked()
        for i in range(size):
            q_linked.enqueue(i)
        linked_size = get_size(q_linked)
        linked_per_element = linked_size / size
        linked_memory.append(linked_per_element)
        print(f"  Size {size}: {linked_per_element:.2f} bytes/element (linked)")

        # Circular buffer (fixed capacity)
        q_circular = QueueCircular(size + 100)  # Some extra space
        for i in range(size):
            q_circular.enqueue(i)
        circular_size = get_size(q_circular)
        circular_per_element = circular_size / size
        circular_memory.append(circular_per_element)
        print(f"  Size {size}: {circular_per_element:.2f} bytes/element (circular)")

        # Dynamic circular buffer
        q_dynamic = QueueDynamicCircular()
        for i in range(size):
            q_dynamic.enqueue(i)
        dynamic_size = get_size(q_dynamic)
        dynamic_per_element = dynamic_size / size
        dynamic_memory.append(dynamic_per_element)
        print(f"  Size {size}: {dynamic_per_element:.2f} bytes/element (dynamic)")

        # Python deque
        q_deque = deque(range(size))
        deque_size = get_size(q_deque)
        deque_per_element = deque_size / size
        deque_memory.append(deque_per_element)
        print(f"  Size {size}: {deque_per_element:.2f} bytes/element (deque)")

        print()

    return sizes, linked_memory, circular_memory, dynamic_memory, deque_memory


def benchmark_memory_overhead():
    print("Benchmarking fixed memory overhead...")

    # Empty structures
    gc.collect()

    # Empty overhead
    q_linked_empty = QueueLinked()
    q_circular_empty = QueueCircular(1000)
    q_dynamic_empty = QueueDynamicCircular()
    q_deque_empty = deque()

    linked_overhead = get_size(q_linked_empty)
    circular_overhead = get_size(q_circular_empty)
    dynamic_overhead = get_size(q_dynamic_empty)
    deque_overhead = get_size(q_deque_empty)

    print(f"  Linked queue overhead: {linked_overhead} bytes")
    print(f"  Circular buffer overhead: {circular_overhead} bytes")
    print(f"  Dynamic circular overhead: {dynamic_overhead} bytes")
    print(f"  Python deque overhead: {deque_overhead} bytes")

    return {
        'linked': linked_overhead,
        'circular': circular_overhead,
        'dynamic': dynamic_overhead,
        'deque': deque_overhead
    }


def benchmark_resize_memory_spike():
    print("\nBenchmarking memory spikes during resize...")

    # Test dynamic queue resize memory usage
    sizes = [1000, 2000, 4000, 8000]
    memory_spikes = []

    for target_size in sizes:
        gc.collect()
        q_dynamic = QueueDynamicCircular(8)  # Start small

        # Fill up to just before resize
        for i in range(7):
            q_dynamic.enqueue(i)

        before_resize = get_size(q_dynamic)

        # Trigger resize
        q_dynamic.enqueue(7)
        after_resize = get_size(q_dynamic)

        # Fill to target size
        for i in range(8, target_size):
            q_dynamic.enqueue(i)

        final_size = get_size(q_dynamic)
        spike_ratio = after_resize / before_resize
        memory_spikes.append(spike_ratio)

        print(f"  Size {target_size}: {spike_ratio:.2f}x memory spike during resize")
        print(f"    Before: {before_resize} bytes, After resize: {after_resize} bytes, Final: {final_size} bytes")

    return sizes, memory_spikes


def benchmark_memory_efficiency_patterns():
    print("\nBenchmarking memory efficiency under different patterns...")

    size = 10000
    patterns = ['fill_only', 'alternating', 'burst_drain', 'steady_state']

    results = {}

    for pattern in patterns:
        print(f"\n  Pattern: {pattern}")
        gc.collect()

        # Test each queue type
        for name, queue_factory in [
            ('linked', lambda: QueueLinked()),
            ('circular', lambda: QueueCircular(size + 1000)),
            ('dynamic', lambda: QueueDynamicCircular()),
            ('deque', lambda: deque())
        ]:
            gc.collect()
            q = queue_factory()

            if pattern == 'fill_only':
                # Just fill it up
                for i in range(size):
                    q.enqueue(i) if hasattr(q, 'enqueue') else q.append(i)

            elif pattern == 'alternating':
                # Alternating enqueue/dequeue
                for i in range(size):
                    q.enqueue(i) if hasattr(q, 'enqueue') else q.append(i)
                    if i % 2 == 1 and (q.size() if hasattr(q, 'size') else len(q)) > 0:
                        q.dequeue() if hasattr(q, 'dequeue') else q.popleft()

            elif pattern == 'burst_drain':
                # Burst fill, then drain half, repeat
                for burst in range(4):
                    # Fill burst
                    for i in range(size // 4):
                        q.enqueue(burst * (size//4) + i) if hasattr(q, 'enqueue') else q.append(burst * (size//4) + i)
                    # Drain half
                    drain_count = (size // 4) // 2
                    for _ in range(drain_count):
                        if (q.size() if hasattr(q, 'size') else len(q)) > 0:
                            q.dequeue() if hasattr(q, 'dequeue') else q.popleft()

            elif pattern == 'steady_state':
                # Fill to half, then maintain steady state
                for i in range(size // 2):
                    q.enqueue(i) if hasattr(q, 'enqueue') else q.append(i)
                # Steady state operations
                for i in range(size // 2):
                    q.enqueue(size // 2 + i) if hasattr(q, 'enqueue') else q.append(size // 2 + i)
                    q.dequeue() if hasattr(q, 'dequeue') else q.popleft()

            memory_used = get_size(q)
            current_size = q.size() if hasattr(q, 'size') else len(q)
            efficiency = memory_used / max(current_size, 1)  # bytes per stored element

            if pattern not in results:
                results[pattern] = {}
            results[pattern][name] = {
                'memory': memory_used,
                'elements': current_size,
                'efficiency': efficiency
            }

            print(f"    {name:8}: {memory_used:6} bytes, {current_size:4} elements, {efficiency:.1f} bytes/element")

    return results


def plot_memory_results():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # Memory per element
    sizes, linked_memory, circular_memory, dynamic_memory, deque_memory = benchmark_memory_per_element()
    ax1.plot(sizes, linked_memory, 'r-o', label='Linked Queue', linewidth=2, markersize=6)
    ax1.plot(sizes, circular_memory, 'g-s', label='Circular Buffer', linewidth=2, markersize=6)
    ax1.plot(sizes, dynamic_memory, 'm-d', label='Dynamic Circular', linewidth=2, markersize=6)
    ax1.plot(sizes, deque_memory, 'b-^', label='Python deque', linewidth=2, markersize=6)
    ax1.set_title('Memory Efficiency (bytes per element)')
    ax1.set_xlabel('Queue Size')
    ax1.set_ylabel('Bytes per Element')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Fixed overhead comparison
    overhead = benchmark_memory_overhead()
    names = list(overhead.keys())
    values = list(overhead.values())
    colors = ['red', 'green', 'magenta', 'blue']
    ax2.bar(names, values, color=colors, alpha=0.7)
    ax2.set_title('Fixed Memory Overhead')
    ax2.set_ylabel('Bytes')
    ax2.grid(True, alpha=0.3)

    # Resize memory spikes
    sizes, spikes = benchmark_resize_memory_spike()
    ax3.plot(sizes, spikes, 'm-o', label='Dynamic Circular Resize Spike', linewidth=2, markersize=6)
    ax3.axhline(y=2.0, color='red', linestyle='--', alpha=0.7, label='2x Memory Usage')
    ax3.set_title('Memory Spike During Resize')
    ax3.set_xlabel('Queue Size')
    ax3.set_ylabel('Memory Multiplier')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Pattern efficiency comparison
    pattern_results = benchmark_memory_efficiency_patterns()
    patterns = list(pattern_results.keys())
    queue_types = ['linked', 'circular', 'dynamic', 'deque']

    x_pos = range(len(patterns))
    width = 0.2
    colors = ['red', 'green', 'magenta', 'blue']

    for i, queue_type in enumerate(queue_types):
        efficiencies = [pattern_results[pattern][queue_type]['efficiency'] for pattern in patterns]
        ax4.bar([x + i*width for x in x_pos], efficiencies, width,
                label=queue_type.title(), color=colors[i], alpha=0.7)

    ax4.set_title('Memory Efficiency by Usage Pattern')
    ax4.set_xlabel('Usage Pattern')
    ax4.set_ylabel('Bytes per Stored Element')
    ax4.set_xticks([x + width*1.5 for x in x_pos])
    ax4.set_xticklabels(patterns, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('queue_memory_benchmarks.png', dpi=150, bbox_inches='tight')
    print(f"\nMemory benchmark plot saved as 'queue_memory_benchmarks.png'")


if __name__ == "__main__":
    plot_memory_results()