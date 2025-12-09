# Algorithms Exercise 3 - Solutions


# Q1 – Explanation

# In an array-based binary heap, the tree is stored in a linear
# structure without pointers. This representation is efficient
# because the positions of parent and child nodes can be computed
# using simple arithmetic formulas. As a result, heap navigation,
# insertion, and structural maintenance become fast and memory-efficient.
# The purpose of this question is to understand why heaps are stored
# in arrays and how this structure enables logarithmic-time operations.



# ---------------------------------------------------
# Q2 – Explanation
# ---------------------------------------------------
# This question examines the structural relationships inside a
# binary heap. Using the formulas parent(i), left(i), and right(i),
# we can determine how nodes are connected and verify whether the
# heap property holds. For a max-heap, each parent must be greater
# than or equal to its children. By checking these index relationships,
# we can confirm whether an array represents a valid heap.



# ---------------------------------------------------
# Q3 – parent, left, right
# Explanation:
# These helper functions allow constant-time navigation inside
# the heap. They compute the index of a node’s parent, left child,
# and right child directly from its index. All heap algorithms,
# including heapify, building a heap, and heap sort, rely on these
# functions to traverse the implicit tree stored in the array.
# ---------------------------------------------------

def parent(i):
    return (i - 1) // 2

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2



# ---------------------------------------------------
# Q4 – is_max_heap
#
# ---------------------------------------------------

def is_max_heap(arr, key=lambda x: x):
    n = len(arr)
    for i in range(1, n):
        if key(arr[parent(i)]) < key(arr[i]):
            return False
    return True



# ---------------------------------------------------
# Q5 – max_heapify
# (No explanation required)
# ---------------------------------------------------

def max_heapify(arr, i, heap_size, key=lambda x: x):
    l = left(i)
    r = right(i)
    largest = i

    if l < heap_size and key(arr[l]) > key(arr[largest]):
        largest = l
    if r < heap_size and key(arr[r]) > key(arr[largest]):
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, largest, heap_size, key)



# ---------------------------------------------------
# Q6 – build_max_heap
# (No explanation required)
# ---------------------------------------------------

def build_max_heap(arr, key=lambda x: x):
    heap_size = len(arr)
    # Start from the last internal node and push down each one
    for i in range((len(arr)//2) - 1, -1, -1):
        max_heapify(arr, i, heap_size, key)



# ---------------------------------------------------
# Q7 – heap_sort
# Detailed Explanation:
# Heap Sort operates in two main phases. In the first phase, a max-heap
# is constructed from the input array. Although this may seem expensive,
# the build process actually runs in O(n), since most heapify operations
# occur on lower tree levels where subtrees are small. In the second
# phase, the algorithm repeatedly extracts the maximum element by swapping
# the root with the last active position and shrinking the heap. Each
# extraction requires a heapify call that costs O(log n), and since this
# is performed n times, the dominant term becomes O(n log n). Therefore,
# the overall running time of Heap Sort is O(n log n), making it an
# efficient comparison-based sorting algorithm with good worst-case guarantees.
# ---------------------------------------------------

def heap_sort(arr, key=lambda x: x):
    build_max_heap(arr, key)
    heap_size = len(arr)

    for i in range(len(arr) - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heap_size -= 1
        max_heapify(arr, 0, heap_size, key)

    return arr



# ---------------------------------------------------
# Q8 – Explanation (Time Complexity of max_heapify)
# ---------------------------------------------------
# The max_heapify procedure restores the heap property by moving
# the element at index i downward until it reaches its correct position.
# Each step of the algorithm descends one level in the tree, and since
# a binary heap has height ⌊log n⌋, max_heapify performs at most log n
# recursive or iterative steps. Every level involves only constant-time
# operations (comparisons and possibly a single swap), so the total
# running time of max_heapify is O(log n).



# ---------------------------------------------------
# Q9 – Explanation (Time Complexity of heap_sort)
# ---------------------------------------------------
# The heap_sort algorithm consists of two phases. The first phase,
# build_max_heap, runs in O(n) time because most heapify operations occur
# close to the leaves, where subtrees are small. The second phase performs
# n extract-max operations. Each extraction triggers a max_heapify call,
# which costs O(log n). Therefore, the total time for the second phase is
# n * O(log n) = O(n log n). Since this term dominates, the overall running
# time of heap_sort is O(n log n). This makes heap sort efficient even in
# the worst case and ensures stable performance regardless of input order.



# ---------------------------------------------------
# Q10 – merge_sorted_lists
# Detailed Explanation:
# This algorithm merges k individually sorted lists into a single sorted
# output list using a min-heap as a priority queue. Initially, the first
# element of each list is inserted into the heap. At each step, the
# smallest element among all active heads is extracted, and the next
# element from the same list is pushed into the heap. Each heap push
# and pop costs O(log k), and since exactly N elements (the total size
# of all lists) are processed, the overall running time is O(N log k).
# This is significantly more efficient than concatenating and sorting
# all lists, which would require O(N log N).
# ---------------------------------------------------

import heapq

def merge_sorted_lists(lists, key=lambda x: x):
    heap = []
    result = []

    for li, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (key(lst[0]), li, 0, lst[0]))

    while heap:
        _, li, idx, val = heapq.heappop(heap)
        result.append(val)

        next_idx = idx + 1
        if next_idx < len(lists[li]):
            next_val = lists[li][next_idx]
            heapq.heappush(heap, (key(next_val), li, next_idx, next_val))

    return result



# ---------------------------------------------------
# Test Runs (Optional)
# ---------------------------------------------------

if __name__ == "__main__":
    print("\n-- Q4 is_max_heap test --")
    print(is_max_heap([50, 30, 40, 10, 20]))  # True
    print(is_max_heap([10, 50, 40]))          # False

    print("\n-- Q6 build_max_heap test --")
    arr = [3, 1, 6, 5, 2, 4]
    build_max_heap(arr)
    print(arr)

    print("\n-- Q7 heap_sort test --")
    arr = [3, 1, 6, 5, 2, 4]
    print(heap_sort(arr.copy()))

    print("\n-- Q10 merge_sorted_lists test --")
    lists = [[1, 4, 9], [2, 6], [0, 7, 8]]
    print(merge_sorted_lists(lists))

