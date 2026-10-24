"""mylib —— 一个小型 Python 工具库。"""

from mylib.numbers import (
    clamp,
    format_cny,
    moving_average,
    percentage,
    safe_div,
)
from mylib.text import (
    is_palindrome,
    mask,
    slugify,
    truncate,
    word_count,
)
from mylib.validators import (
    is_email,
    is_id_card_cn,
    is_phone_cn,
    is_url,
)

__version__ = "0.1.0"

__all__ = [
    # text
    "slugify",
    "truncate",
    "word_count",
    "is_palindrome",
    "mask",
    # numbers
    "clamp",
    "safe_div",
    "moving_average",
    "format_cny",
    "percentage",
    # validators
    "is_email",
    "is_phone_cn",
    "is_url",
    "is_id_card_cn",
]
