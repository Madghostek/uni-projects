from sorting_algs import bubble_sort, selection_sort, merge_sort, quick_sort_run

# bubble

def test_bubble_sort_empty():
    assert bubble_sort([]) == []

def test_bubble_sort_int():
    assert bubble_sort([0]) == [0]
    assert bubble_sort([3,2,1]) == [1,2,3]
    assert bubble_sort([-1, -100, 21, 0]) == [-100,-1,0,21]

def test_bubble_sort_float():
    assert bubble_sort([1.2, 34.5, 0.678]) == [0.678, 1.2, 34.5]

def test_bubble_sort_words():
    assert bubble_sort(["koniec","i", "bomba", "a", "kto", "czytał", "ten", "trąba"])\
           == ["a", "bomba", "czytał", "i", "koniec", "kto", "ten", "trąba"]

# selection

def test_selection_sort_empty():
    assert selection_sort([]) == []

def test_selection_sort_int():
    assert selection_sort([0]) == [0]
    assert selection_sort([3,2,1]) == [1,2,3]
    assert selection_sort([-1, -100, 21, 0]) == [-100,-1,0,21]

def test_selection_sort_float():
    assert selection_sort([1.2, 34.5, 0.678]) == [0.678, 1.2, 34.5]

def test_selection_sort_words():
    assert selection_sort(["koniec","i", "bomba", "a", "kto", "czytał", "ten", "trąba"])\
           == ["a", "bomba", "czytał", "i", "koniec", "kto", "ten", "trąba"]

# quicksort

def test_quicksort_sort_empty():
    assert quick_sort_run([]) == []

def test_quick_sort_int():
    assert quick_sort_run([0]) == [0]
    assert quick_sort_run([3,2,1]) == [1,2,3]
    assert quick_sort_run([-1, -100, 21, 0]) == [-100,-1,0,21]

def test_quick_sort_float():
    assert quick_sort_run([1.2, 34.5, 0.678]) == [0.678, 1.2, 34.5]

def test_quick_sort_words():
    assert quick_sort_run(["koniec","i", "bomba", "a", "kto", "czytał", "ten", "trąba"])\
           == ["a", "bomba", "czytał", "i", "koniec", "kto", "ten", "trąba"]

# merge

def test_merge_sort_empty():
    assert merge_sort([]) == []

def test_merge_sort_int():
    assert merge_sort([0]) == [0]
    assert merge_sort([3,2,1]) == [1,2,3]
    assert merge_sort([-1, -100, 21, 0]) == [-100,-1,0,21]

def test_merge_sort_float():
    assert merge_sort([1.2, 34.5, 0.678]) == [0.678, 1.2, 34.5]

def test_merge_sort_words():
    assert merge_sort(["koniec","i", "bomba", "a", "kto", "czytał", "ten", "trąba"])\
           == ["a", "bomba", "czytał", "i", "koniec", "kto", "ten", "trąba"]
