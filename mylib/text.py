"""文本处理工具函数。"""

import re
import unicodedata

_WHITESPACE = re.compile(r"\s+")
_NON_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """把任意文本转换成 URL 友好的 slug。

    规则：转小写 -> 去除变音符号 -> 非字母数字压缩为连字符 -> 去除首尾连字符。

    >>> slugify("Hello, World! 你好")
    'hello-world'
    """
    if not isinstance(text, str):
        raise TypeError(f"slugify() 需要 str，收到 {type(text).__name__}")
    # NFKD 分解后去掉组合标记（如 é -> e）
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in normalized if not unicodedata.combining(c))
    slug = _NON_SLUG.sub("-", ascii_text.lower()).strip("-")
    return slug


def truncate(text: str, max_len: int, suffix: str = "…") -> str:
    """把文本截断到 max_len 个字符（含后缀）以内。

    max_len 必须为正整数；text 短于 max_len 时原样返回。
    """
    if not isinstance(max_len, int) or isinstance(max_len, bool):
        raise TypeError("max_len 必须是 int")
    if max_len <= 0:
        raise ValueError("max_len 必须是正整数")
    if len(text) <= max_len:
        return text
    keep = max_len - len(suffix)
    if keep <= 0:
        return suffix[:max_len]
    return text[:keep] + suffix


def word_count(text: str) -> int:
    """统计英文单词数（按连续空白切分，过滤空串）。"""
    return len([w for w in _WHITESPACE.split(text) if w])


def is_palindrome(text: str) -> bool:
    """判断是否为回文，忽略大小写、空白和标点半角字符。"""
    cleaned = "".join(c for c in text.lower() if c.isalnum())
    return bool(cleaned) and cleaned == cleaned[::-1]


def mask(text: str, visible: int = 4) -> str:
    """脱敏：保留前 visible 位和后 visible 位，中间用 * 代替。

    mask("13812345678") -> "138****5678"
    """
    if visible < 0:
        raise ValueError("visible 不能为负数")
    if len(text) <= visible * 2:
        return "*" * len(text)
    head, tail = text[:visible], text[-visible:] if visible else ""
    return f"{head}{'*' * (len(text) - 2 * visible)}{tail}"
