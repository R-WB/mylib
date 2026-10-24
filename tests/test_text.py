"""mylib.text 的测试。"""

import pytest

from mylib.text import is_palindrome, mask, slugify, truncate, word_count


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_punctuation_and_whitespace(self):
        assert slugify("Hello,  World!!!") == "hello-world"

    def test_diacritics_removed(self):
        assert slugify("Café Münster") == "cafe-munster"

    def test_chinese_characters_become_hyphens(self):
        assert slugify("你好 World") == "world"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_only_separators(self):
        assert slugify("---") == ""

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            slugify(123)

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("Hello World", "hello-world"),
            ("Hello, World!", "hello-world"),
            ("Café Münster", "cafe-munster"),
            ("A_B-C", "a-b-c"),
        ],
    )
    def test_parametrized(self, raw, expected):
        assert slugify(raw) == expected

    def test_from_shared_fixture(self, dirty_slugs):
        for raw, expected in dirty_slugs:
            assert slugify(raw) == expected


class TestTruncate:
    def test_short_text_unchanged(self):
        assert truncate("abc", 10) == "abc"

    def test_exact_length_unchanged(self):
        assert truncate("abcde", 5) == "abcde"

    def test_long_text_truncated_with_suffix(self):
        assert truncate("abcdefgh", 5) == "abcd…"

    def test_custom_suffix(self):
        assert truncate("abcdefgh", 5, suffix="...") == "ab..."

    def test_suffix_longer_than_max_len(self):
        assert truncate("abcdefgh", 3, suffix="...") == "..."

    @pytest.mark.parametrize("bad", [0, -1])
    def test_invalid_max_len(self, bad):
        with pytest.raises(ValueError):
            truncate("abc", bad)

    def test_non_int_max_len(self):
        with pytest.raises(TypeError):
            truncate("abc", 5.0)


class TestWordCount:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("hello world", 2),
            ("  hello   world  ", 2),
            ("", 0),
            ("   ", 0),
            ("one", 1),
        ],
    )
    def test_counts(self, text, expected):
        assert word_count(text) == expected


class TestIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("level", True),
            ("Level", True),
            ("A man, a plan, a canal: Panama", True),
            ("上海自来水来自海上", True),
            ("hello", False),
            ("", False),
            ("!!!", False),
        ],
    )
    def test_palindromes(self, text, expected):
        assert is_palindrome(text) is expected


class TestMask:
    @pytest.mark.parametrize(
        "text,visible,expected",
        [
            ("13812345678", 3, "138*****678"),
            ("13812345678", 4, "1381***5678"),
            ("abc", 4, "***"),
            ("", 4, ""),
            ("13812345678", 0, "***********"),
        ],
    )
    def test_mask(self, text, visible, expected):
        assert mask(text, visible) == expected

    def test_negative_visible_raises(self):
        with pytest.raises(ValueError):
            mask("secret", -1)
