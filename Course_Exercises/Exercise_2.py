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

        # פתרון שאלון - כל הסעיפים
    import random
    import string
    import heapq
    from operator import itemgetter
    from typing import Any, Callable, Iterable, List, Tuple, Optional


    # ------------------------------
    # פונקציה שניתנה ברפרנס: create_random_tuples
    # ------------------------------
    def create_random_tuples(n: int, k: int, types: List[type] = None) -> List[Tuple]:
        """
        יצירת רשימה של n טאפלים, כל טאפל באורך k, לפי טיפוסים ב-types.
        """
        if types is None:
            types = [int] * k
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
            tup = tuple(random_element(t) for t in types)
            result.append(tup)
        return result


    # ------------------------------
    # סעיף 1: שימוש ב-sorted עם key למיון טאפלים
    # ------------------------------
    def demo_sorted_on_tuples():

        data = create_random_tuples(7, 3, [int, float, str])
        # מיון לפי הרכיב הראשון (int)
        sorted_by_first = sorted(data, key=lambda x: x[0])
        # מיון לפי הרכיב השני (float)
        sorted_by_second = sorted(data, key=itemgetter(1))
        # מיון לפי הרכיב השלישי (str) - אלפביתי
        sorted_by_third = sorted(data, key=lambda x: x[2])

        return {
            "original": data,
            "by_first": sorted_by_first,
            "by_second": sorted_by_second,
            "by_third": sorted_by_third,
        }


    # ------------------------------
    # סעיף 2: merge(a, b, key) המיזוג בין שתי רשימות ממוינות
    # ------------------------------
    def is_sorted(a: Iterable, key: Callable[[Any], Any]) -> bool:
        """
        בודק אם a מסודר בסדר עולה לפי key.
        """
        it = iter(a)
        try:
            prev = next(it)
        except StopIteration:
            return True
        prev_k = key(prev)
        for item in it:
            k = key(item)
            if k < prev_k:
                return False
            prev_k = k
        return True


    def merge(a: List[Any], b: List[Any], key: Callable[[Any], Any]) -> Optional[List[Any]]:
        """
        ממזג שתי רשימות ממוינות a, b לפי key. מחזיר None אם אחת מהרשימות אינה ממוינת.
        זמן ריצה O(len(a)+len(b)).
        """
        if not is_sorted(a, key) or not is_sorted(b, key):
            return None

        i, j = 0, 0
        res = []
        while i < len(a) and j < len(b):
            if key(a[i]) <= key(b[j]):
                res.append(a[i])
                i += 1
            else:
                res.append(b[j])
                j += 1

        if i < len(a):
            res.extend(a[i:])
        if j < len(b):
            res.extend(b[j:])
        return res


    # ------------------------------
    # סעיף 3: merge_sorted_lists(lists, key) - מיזוג כמה רשימות ממוינות
    # ------------------------------
    def merge_sorted_lists(lists: List[List[Any]], key: Callable[[Any], Any]) -> List[Any]:
        """
        ממזג כמה רשימות ממוינות ליחידה אחת ממוינת, ביעילות בעזרת heap.
        זמן ריצה: אם סה"כ יש N איברים ו-k רשימות אז O(N log k).
        """

        # --- Q3b Answer  ---
        # Time complexity:
        # n = number of lists, k = elements in each.
        # Total elements = N = n*k.
        # Each heap push/pop: O(log n).
        # Total time: O(N log n) = O(n*k*log n).
        # Space complexity: O(n).

        heap = []
        result = []
        for li_idx, lst in enumerate(lists):
            if lst:
                heapq.heappush(heap, (key(lst[0]), li_idx, 0, lst[0]))

        while heap:
            k_val, li_idx, el_idx, value = heapq.heappop(heap)
            result.append(value)
            next_idx = el_idx + 1
            if next_idx < len(lists[li_idx]):
                next_val = lists[li_idx][next_idx]
                heapq.heappush(heap, (key(next_val), li_idx, next_idx, next_val))
        return result


    # ------------------------------
    # סעיף 4: מימוש partition - Lomuto ו-Hoare
    # ------------------------------
    def partition_lomuto(a: List[Any], key: Callable[[Any], Any]) -> int:
        """
        מימוש Lomuto partition in-place.
        pivot = last element.
        """
        if not a:
            return -1
        pivot_val = key(a[-1])
        i = -1
        for j in range(0, len(a) - 1):
            if key(a[j]) <= pivot_val:
                i += 1
                a[i], a[j] = a[j], a[i]

        a[i + 1], a[-1] = a[-1], a[i + 1]
        return i + 1


    def partition_hoare(a: List[Any], key: Callable[[Any], Any]) -> int:
        """
        מימוש Hoare partition in-place.
        pivot = first element.
        """
        if not a:
            return -1
        pivot = key(a[0])
        i = -1
        j = len(a)
        while True:
            i += 1
            while key(a[i]) < pivot:
                i += 1
            j -= 1
            while key(a[j]) > pivot:
                j -= 1
            if i >= j:
                return j
            a[i], a[j] = a[j], a[i]


    # --- Q4c Answer  ---
    # Difference between Lomuto and Hoare:
    # Lomuto:
    # - Pivot = last element.
    # - Ensures pivot ends in exact final sorted position.
    # - More swaps, less efficient.
    #
    # Hoare:
    # - Pivot = first element.
    # - Fewer swaps, more efficient in practice.
    # - Pivot does NOT end in its final sorted index.
    # - Only ensures left <= pivot <= right.

    # --- Q4d Answer ---
    # Both Lomuto and Hoare run in O(n),
    # because each element is examined a constant number of times.

    # ------------------------------
    # סעיף 5: partition ל-3 אזורים (Dutch National Flag)
    # ------------------------------
    def partition_three_way(a: List[Any], key: Callable[[Any], Any], pivot_value: Any = None) -> Tuple[int, int]:

        if not a:
            return (0, 0)
        if pivot_value is None:
            pv = key(a[0])
        else:
            pv = pivot_value

        low, mid, high = 0, 0, len(a) - 1

        while mid <= high:
            k = key(a[mid])
            if k < pv:
                a[low], a[mid] = a[mid], a[low]
                low += 1
                mid += 1
            elif k > pv:
                a[mid], a[high] = a[high], a[mid]
                high -= 1
            else:
                mid += 1
        return (low, high + 1)


    # ------------------------------
    # פונקציות עזר להדגמות / בדיקות
    # ------------------------------
    def demo_all():
        out = {}
        out['s1'] = demo_sorted_on_tuples()

        a = sorted(create_random_tuples(5, 3, [int, float, str]), key=lambda x: x[0])
        b = sorted(create_random_tuples(4, 3, [int, float, str]), key=lambda x: x[0])
        out['s2'] = {'a': a, 'b': b, 'merged': merge(a, b, key=lambda x: x[0])}

        lists = [sorted(create_random_tuples(3, 1, [int]), key=lambda x: x[0]) for _ in range(4)]
        lists_unwrapped = [[t[0] for t in lst] for lst in lists]
        merged_all = merge_sorted_lists(lists_unwrapped, key=lambda x: x)
        out['s3'] = {'lists': lists_unwrapped, 'merged_all': merged_all}

        arr_lom = [5, 2, 8, 1, 3, 7, 4]
        arr_lom_copy = list(arr_lom)
        pivot_pos = partition_lomuto(arr_lom_copy, key=lambda x: x)
        out['s4_lomuto'] = {'before': arr_lom, 'after': arr_lom_copy, 'pivot_pos': pivot_pos}

        arr_hoare = [5, 2, 8, 1, 3, 7, 4]
        arr_hoare_copy = list(arr_hoare)
        hoare_j = partition_hoare(arr_hoare_copy, key=lambda x: x)
        out['s4_hoare'] = {'before': arr_hoare, 'after': arr_hoare_copy, 'j': hoare_j}

        arr_three = [3, 2, 1, 2, 3, 2, 1, 3, 2]
        arr_three_copy = list(arr_three)
        lt_end, gt_start = partition_three_way(arr_three_copy, key=lambda x: x, pivot_value=2)
        out['s5'] = {'before': arr_three, 'after': arr_three_copy, 'lt_end': lt_end, 'gt_start': gt_start}

        return out


    if __name__ == "__main__":
        demo = demo_all()
        import pprint

        pprint.pprint(demo, width=120)

