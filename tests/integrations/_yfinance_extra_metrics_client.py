# tests/momentum/services/test_fifty_two_week_logic.py
from datetime import date

from stock_market.integrations.yfinance_extra_metrics_client import ExtraMetricsUpdater
from stock_market.momentum.services.fifty_two_week_logic import (
    compute_52_week_extremes_update,
)

extra_metrics = ExtraMetricsUpdater()


def test_new_high_detected():
    result = compute_52_week_extremes_update(
        current_high=100,
        current_low=50,
        incoming_high=110,
        incoming_low=55,
        run_date=date(2024, 6, 1),
    )
    assert result.new_high == 110
    assert result.new_high_date == date(2024, 6, 1)
    assert result.new_low is None  # 55 is not a new low


def test_no_change_when_within_range():
    result = compute_52_week_extremes_update(
        current_high=100,
        current_low=50,
        incoming_high=90,
        incoming_low=60,
        run_date=date(2024, 6, 1),
    )
    assert result.new_high is None
    assert result.new_low is None


def test_first_time_ticker_has_no_current_values():
    result = compute_52_week_extremes_update(
        current_high=None,
        current_low=None,
        incoming_high=110,
        incoming_low=55,
        run_date=date(2024, 6, 1),
    )
    assert result.new_high == 110
    assert result.new_low == 55
