def create_random_tuples(n, k, types=None):
    """
    Create a list of n tuples, each containing k random elements of specified types.

    Parameters:
    n (int): Number of tuples to create.
    k (int): Number of elements in each tuple.
    types (list): List of types for each element in the tuple. Length must be k.

    Returns:
    list: A list of n tuples with random elements.
    """
    import random
    import string

    if types is None:
        types = [int] * k  # Default to int if no types provided

    if len(types) != k:
        raise ValueError("Length of types must be equal to k")

    def random_element(t):
        if t == int:
            return random.randint(0, 1000)
        elif t == float:
            return random.uniform(0.0, 1000.0)
        elif t == str:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        else:
            raise ValueError(f"Unsupported type: {t}")

    result = []
    for _ in range(n):
        tuple_elements = tuple(random_element(t) for t in types)
        result.append(tuple_elements)

    return result


if __name__ == "__main__":
    # Example usage
    tuples_list = create_random_tuples(10, 3, [int, float, str])
    for t in tuples_list:
        print(t)

# ============================================
#               EXERCISE 4
# ============================================



def find_min(a, key):
    """
    Finds the minimum and maximum elements in a list based on a given key function.
    Does NOT use Python's built-in min() or max().
    """
    if not a:
        return None, None

    min_item = a[0]
    max_item = a[0]

    for item in a[1:]:
        if key(item) < key(min_item):
            min_item = item
        if key(item) > key(max_item):
            max_item = item

    return min_item, max_item


def exercise_4_demo():
    """
    Creates a list of 100 random tuples and prints the min/max based on the 3rd field.
    """
    data = create_random_tuples(100, 3, [int, float, str])

    min_val, max_val = find_min(data, key=lambda x: x[2])

    print("=== Exercise 4 Output ===")
    print(f"min={min_val}")
    print(f"max={max_val}")
    print()


# ============================================
#               EXERCISE 5
# ============================================

def insertion_sort(a, key):
    """
    Generic insertion sort that sorts a list based on a key function.
    """
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1

        # Move items that are greater than current to the right
        while j >= 0 and key(a[j]) > key(current):
            a[j + 1] = a[j]
            j -= 1

        a[j + 1] = current

    return a


def exercise_5_demo():
    """
    Runs insertion sort on 3 different random tuple lists,
    each time sorting by a different tuple field.
    """

    print("=== Exercise 5 Output ===")

    # First sort (by field 0 - int)
    a1 = create_random_tuples(10, 3, [int, float, str])
    print("\nSorting by field 0 (int):")
    print(insertion_sort(a1, key=lambda x: x[0]))

    # Second sort (by field 1 - float)
    a2 = create_random_tuples(10, 3, [int, float, str])
    print("\nSorting by field 1 (float):")
    print(insertion_sort(a2, key=lambda x: x[1]))

    # Third sort (by field 2 - str)
    a3 = create_random_tuples(10, 3, [int, float, str])
    print("\nSorting by field 2 (str):")
    print(insertion_sort(a3, key=lambda x: x[2]))
    print()


# ============================================
#                   MAIN
# ============================================

if __name__ == "__main__":
    exercise_4_demo()
    exercise_5_demo()
