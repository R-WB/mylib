"""数值计算与格式化工具函数。"""

from decimal import Decimal, ROUND_HALF_UP


def clamp(value, low, high):
    """把 value 限制在 [low, high] 区间内。low > high 时抛出 ValueError。"""
    if low > high:
        raise ValueError(f"low({low}) 不能大于 high({high})")
    return max(low, min(high, value))


def safe_div(a, b, default=None):
    """安全除法：b 为 0 时返回 default，而不是抛出 ZeroDivisionError。"""
    try:
        return a / b
    except ZeroDivisionError:
        return default


def moving_average(values, window: int):
    """计算滑动平均值，返回长度为 len(values)-window+1 的列表。

    window 必须为正整数且不超过 len(values)。
    """
    if not isinstance(window, int) or isinstance(window, bool):
        raise TypeError("window 必须是 int")
    if window <= 0:
        raise ValueError("window 必须是正整数")
    values = list(values)
    if window > len(values):
        raise ValueError(f"window({window}) 超过数据长度({len(values)})")
    return [
        sum(values[i : i + window]) / window
        for i in range(len(values) - window + 1)
    ]


def format_cny(amount) -> str:
    """把数字格式化为人民币字符串，保留两位小数（四舍五入，半向上）。

    format_cny(1234.5) -> "¥1,234.50"
    """
    quantized = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"¥{quantized:,.2f}"


def percentage(part, whole, digits: int = 2) -> float:
    """计算 part 占 whole 的百分比。whole 为 0 时返回 0.0。"""
    if whole == 0:
        return 0.0
    return round(part / whole * 100, digits)
