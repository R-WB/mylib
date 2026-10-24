"""常用格式校验函数。"""

import re

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
_PHONE_CN_RE = re.compile(r"^1[3-9]\d{9}$")
_URL_RE = re.compile(r"^https?://[^\s/$.?#][^\s]*$", re.IGNORECASE)

_ID_WEIGHTS = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
_ID_CHECK_CODES = "10X98765432"


def is_email(text: str) -> bool:
    """判断是否为合法邮箱地址（宽松规则，覆盖绝大多数真实地址）。"""
    if not isinstance(text, str):
        return False
    return bool(_EMAIL_RE.match(text))


def is_phone_cn(text: str) -> bool:
    """判断是否为中国大陆手机号（1 开头，第二位 3-9，共 11 位）。"""
    if not isinstance(text, str):
        return False
    return bool(_PHONE_CN_RE.match(text))


def is_url(text: str) -> bool:
    """判断是否为 http/https URL。"""
    if not isinstance(text, str):
        return False
    return bool(_URL_RE.match(text))


def is_id_card_cn(text: str) -> bool:
    """判断是否为合法 18 位中国大陆身份证号（含末位校验码验证）。"""
    if not isinstance(text, str) or not re.fullmatch(r"\d{17}[\dXx]", text):
        return False
    total = sum(int(d) * w for d, w in zip(text[:17], _ID_WEIGHTS))
    return text[17].upper() == _ID_CHECK_CODES[total % 11]
