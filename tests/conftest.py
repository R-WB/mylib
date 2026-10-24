"""共享 fixtures。"""

import pytest


@pytest.fixture
def sample_prices():
    """一组连续交易日的收盘价（元）。"""
    return [10.0, 11.0, 12.0, 11.5, 13.0]


@pytest.fixture
def valid_id_card():
    """一个校验位正确的 18 位身份证号。"""
    return "11010519491231002X"


@pytest.fixture
def dirty_slugs():
    """(输入, 期望 slug) 参数对，供多个测试复用。"""
    return [
        ("Hello World", "hello-world"),
        ("Hello, World!", "hello-world"),
        ("  multiple   spaces  ", "multiple-spaces"),
        ("Café Münster", "cafe-munster"),
        ("已经__特殊!!字符", ""),  # slugify 仅保留 ASCII 字母数字
        ("", ""),
        ("---", ""),
    ]
