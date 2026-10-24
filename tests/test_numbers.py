"""mylib.numbers 的测试。"""

import pytest

from mylib.numbers import clamp, format_cny, moving_average, percentage, safe_div


class TestClamp:
    @pytest.mark.parametrize(
        "value,low,high,expected",
        [
            (5, 0, 10, 5),
            (-3, 0, 10, 0),
            (15, 0, 10, 10),
            (0, 0, 10, 0),
            (10, 0, 10, 10),
        ],
    )
    def test_in_range(self, value, low, high, expected):
        assert clamp(value, low, high) == expected

    def test_float_values(self):
        assert clamp(3.5, 0, 1) == 1

    def test_low_greater_than_high_raises(self):
        with pytest.raises(ValueError):
            clamp(5, 10, 0)


class TestSafeDiv:
    def test_normal_division(self):
        assert safe_div(6, 3) == 2

    def test_zero_denominator_returns_default(self):
        assert safe_div(6, 0) is None

    def test_zero_denominator_custom_default(self):
        assert safe_div(6, 0, default=0) == 0

    def test_negative(self):
        assert safe_div(-6, 3) == -2


class TestMovingAverage:
    def test_basic(self, sample_prices):
        result = moving_average(sample_prices, 3)
        assert result == [11.0, 11.5, 12.166666666666666]

    def test_window_equals_length(self, sample_prices):
        assert moving_average([1, 2, 3], 3) == [2.0]

    def test_window_one(self):
        assert moving_average([1, 2, 3], 1) == [1, 2, 3]

    def test_window_too_large_raises(self):
        with pytest.raises(ValueError):
            moving_average([1, 2], 3)

    @pytest.mark.parametrize("bad", [0, -2])
    def test_invalid_window(self, bad):
        with pytest.raises(ValueError):
            moving_average([1, 2, 3], bad)

    def test_non_int_window(self):
        with pytest.raises(TypeError):
            moving_average([1, 2, 3], 2.0)

    def test_accepts_generator(self):
        assert moving_average(iter([1, 2, 3, 4]), 2) == [1.5, 2.5, 3.5]


class TestFormatCny:
    @pytest.mark.parametrize(
        "amount,expected",
        [
            (1234.5, "¥1,234.50"),
            (0, "¥0.00"),
            (-88.125, "¥-88.13"),  # 负数同样半向上取整
            (9999999.999, "¥10,000,000.00"),
            (0.005, "¥0.01"),  # 浮点坑：str(0.005) 精确表示
        ],
    )
    def test_format(self, amount, expected):
        assert format_cny(amount) == expected

    def test_accepts_decimal_and_str(self):
        assert format_cny("12.3") == "¥12.30"


class TestPercentage:
    def test_basic(self):
        assert percentage(25, 100) == 25.0

    def test_zero_whole_returns_zero(self):
        assert percentage(5, 0) == 0.0

    def test_digits(self):
        assert percentage(1, 3, digits=4) == 33.3333

    def test_over_hundred(self):
        assert percentage(150, 100) == 150.0
