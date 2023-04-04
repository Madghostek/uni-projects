import algorythms

tests = [
    ("", "", []),
    ("", "tekst", []),
    ("nic", "", []),
    ("A", "A", [0]),
    ("ABCDEF", "ABCDEF", [0]),
    ("C", "AABABABABAC", [10]),
    ("ABA", "ABABABABA", [0, 2, 4, 6]),
    ("AAA", "ABAABAAABAAAABAAAAA", [5, 9, 10, 14, 15, 16]),
    ("AACB", "AACACCBABCBAABCACBAACABCABCCBAACBABCABC", [29]),
    ("NOTFOUND", "ASDFGHJKLPOIUYTREQZXCVBMN", [])

]


def test_kmp_table():
    assert algorythms.make_prefix_table("AAA") == [0, 1, 2]
    assert algorythms.make_prefix_table("AAB") == [0, 1, 0]
    assert algorythms.make_prefix_table("ACB") == [0, 0, 0]
    assert algorythms.make_prefix_table("AABB") == [0, 1, 0, 0]
    assert algorythms.make_prefix_table("AABBAA") == [0, 1, 0, 0, 1, 2]
    assert algorythms.make_prefix_table("ABCAAC") == [0, 0, 0, 1, 1, 0]


def test_naive():
    for pattern, text, expected in tests:
        assert algorythms.naive(pattern, text) == expected


def test_KMP():
    for pattern, text, expected in tests:
        assert algorythms.KMP(pattern, text) == expected


def test_rabin_karp():
    for pattern, text, expected in tests:
        assert algorythms.rabin_karp(pattern, text) == expected
