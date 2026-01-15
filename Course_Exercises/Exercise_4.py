# =========================================
# Question 2 – QuickSelect (quick_kth)
# =========================================

def partition(arr, left, right, key):
    pivot = arr[right]
    pivot_key = key(pivot)
    i = left

    for j in range(left, right):
        if key(arr[j]) <= pivot_key:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1

    arr[i], arr[right] = arr[right], arr[i]
    return i


def quick_kth(arr, left, right, k, key=lambda x: x):
    if left <= right:
        pivot_index = partition(arr, left, right, key)

        if pivot_index == k:
            return arr[pivot_index]
        elif k < pivot_index:
            return quick_kth(arr, left, pivot_index - 1, k, key)
        else:
            return quick_kth(arr, pivot_index + 1, right, k, key)




# =========================================
# Question 4 – Binary Search Tree with key
# =========================================

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self, key=lambda x: x):
        self.root = None
        self.key = key

    def insert(self, value):
        new_node = Node(value)

        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if self.key(value) < self.key(current.value):
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right


# ---- Example input / output ----
if __name__ == "__main__":
# Question 2
    arr = [7, 2, 1, 6, 8, 5, 3, 4]
    k = 2
    result = quick_kth(arr, 0, len(arr) - 1, k)
    print("k-th element:", result)
# Question 4
    tree = Tree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)

    people_tree = Tree(key=lambda p: p["age"])
    people_tree.insert({"name": "Dan", "age": 30})
    people_tree.insert({"name": "Noa", "age": 25})
    people_tree.insert({"name": "Avi", "age": 40})

    print("BST created successfully")
S