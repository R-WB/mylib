"""mylib.validators 的测试。"""

import pytest

from mylib.validators import is_email, is_id_card_cn, is_phone_cn, is_url


class TestIsEmail:
    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "user.name+tag@sub.example.co.uk",
            "a_b-c@d-e.fg",
        ],
    )
    def test_valid(self, email):
        assert is_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "plainaddress",
            "@no-local.com",
            "no-domain@",
            "no-tld@example.",
            "spaces in@example.com",
            "user@example.c",
            "",
        ],
    )
    def test_invalid(self, email):
        assert is_email(email) is False

    def test_non_string_returns_false(self):
        assert is_email(None) is False


class TestIsPhoneCn:
    @pytest.mark.parametrize(
        "phone",
        ["13812345678", "19900001111", "17712345678", "16612345678"],
    )
    def test_valid(self, phone):
        assert is_phone_cn(phone) is True

    @pytest.mark.parametrize(
        "phone",
        [
            "12345678901",  # 第二位非法
            "23812345678",  # 非 1 开头
            "1381234567",  # 10 位
            "138123456789",  # 12 位
            "1381234567a",  # 含字母
            "138 1234 5678",  # 含空格
            "",
        ],
    )
    def test_invalid(self, phone):
        assert is_phone_cn(phone) is False

    def test_non_string_returns_false(self):
        assert is_phone_cn(13812345678) is False


class TestIsUrl:
    @pytest.mark.parametrize(
        "url",
        [
            "http://example.com",
            "https://example.com/path?q=1",
            "https://sub.domain.cn/a/b#c",
        ],
    )
    def test_valid(self, url):
        assert is_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "ftp://example.com",  # 协议不支持
            "example.com",  # 缺协议
            "https://",  # 缺主机
            "",
        ],
    )
    def test_invalid(self, url):
        assert is_url(url) is False

    def test_non_string_returns_false(self):
        assert is_url(12345) is False


class TestIsIdCardCn:
    def test_valid(self, valid_id_card):
        assert is_id_card_cn(valid_id_card) is True

    def test_lowercase_x_accepted(self):
        assert is_id_card_cn("11010519491231002x") is True

    def test_wrong_check_digit_rejected(self):
        # 正确末位应为 X，改成 0 后校验失败
        assert is_id_card_cn("110105194912310020") is False

    @pytest.mark.parametrize(
        "text",
        [
            "1101051949123100",  # 17 位
            "11010519491231002XX",  # 19 位
            "1101051949123100X1",  # 18 位但末位含字母在前
            "110105491231002XX",  # 非纯数字前缀
            "",
        ],
    )
    def test_malformed(self, text):
        assert is_id_card_cn(text) is False
