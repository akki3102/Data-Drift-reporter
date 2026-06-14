"""
tests/test_basic.py

Happy-path tests for the Data Drift Reporter core logic.
Run with: python -m pytest tests/test_basic.py -v
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from drift_engine import compute_snapshot_stats, compare_snapshots, classify_drift


# ── Fixtures ────────────────────────────────────────────────────────────────

def make_orders_df(n=20, avg_amount=150.0, null_email_frac=0.0):
    """Create a sample orders dataframe for testing."""
    emails = [f"user{i}@example.com" if i / n >= null_email_frac else None
              for i in range(n)]
    amounts = np.round(np.random.normal(avg_amount, 5, n), 2)
    return pd.DataFrame({
        "order_id": range(1001, 1001 + n),
        "customer_email": emails,
        "order_amount": amounts,
        "quantity": np.random.randint(1, 5, n),
        "region": ["East", "West", "South", "North"] * (n // 4 + 1)[:n],
    })


# ── Test 1: Stats dict has all required keys ─────────────────────────────────

def test_compute_stats_returns_required_keys():
    df = make_orders_df()
    stats = compute_snapshot_stats(df)
    assert "row_count" in stats
    assert "overall_null_rate" in stats
    assert "overall_mean" in stats
    assert "columns" in stats
    print("PASS: Stats dict has all required keys")


# ── Test 2: Row count is correct ─────────────────────────────────────────────

def test_compute_stats_row_count():
    df = make_orders_df(n=15)
    stats = compute_snapshot_stats(df)
    assert stats["row_count"] == 15
    print("PASS: Row count matches DataFrame length")


# ── Test 3: Null rate is between 0 and 100 ───────────────────────────────────

def test_compute_stats_null_rate_between_0_and_100():
    df = make_orders_df(n=20, null_email_frac=0.3)
    stats = compute_snapshot_stats(df)
    assert 0.0 <= stats["overall_null_rate"] <= 100.0
    print("PASS: Null rate is between 0 and 100")


# ── Test 4: compare_snapshots returns drift_score and drift_level ─────────────

def test_compare_snapshots_returns_score_and_level():
    df1 = make_orders_df(n=20, avg_amount=150.0)
    df2 = make_orders_df(n=17, avg_amount=130.0)
    s1 = compute_snapshot_stats(df1)
    s2 = compute_snapshot_stats(df2)
    result = compare_snapshots(s2, s1)
    assert "drift_score" in result
    assert "drift_level" in result
    print("PASS: compare_snapshots returns drift_score and drift_level")


# ── Test 5: drift_level is one of Low / Medium / High ────────────────────────

def test_drift_level_valid_values():
    df1 = make_orders_df(n=20)
    df2 = make_orders_df(n=15)
    s1 = compute_snapshot_stats(df1)
    s2 = compute_snapshot_stats(df2)
    result = compare_snapshots(s2, s1)
    assert result["drift_level"] in ["Low", "Medium", "High"]
    print("PASS: drift_level is one of Low / Medium / High")


# ── Test 6: drift_score is non-negative ──────────────────────────────────────

def test_drift_score_non_negative():
    df1 = make_orders_df(n=20)
    df2 = make_orders_df(n=15)
    s1 = compute_snapshot_stats(df1)
    s2 = compute_snapshot_stats(df2)
    result = compare_snapshots(s2, s1)
    assert result["drift_score"] >= 0
    print("PASS: drift_score is non-negative")


# ── Test 7: Identical snapshots give Low drift ───────────────────────────────

def test_identical_snapshots_give_low_drift():
    df = make_orders_df(n=20, avg_amount=150.0, null_email_frac=0.0)
    stats = compute_snapshot_stats(df)
    result = compare_snapshots(stats, stats)
    assert result["drift_level"] == "Low"
    assert result["drift_score"] == 0.0
    print("PASS: Identical snapshots give Low drift (score = 0)")


# ── Test 8: classify_drift thresholds are correct ────────────────────────────

def test_classify_drift_thresholds():
    assert classify_drift(3.0) == "Low"
    assert classify_drift(10.0) == "Medium"
    assert classify_drift(20.0) == "High"
    assert classify_drift(4.9) == "Low"
    assert classify_drift(5.0) == "Medium"
    assert classify_drift(15.0) == "Medium"
    assert classify_drift(15.1) == "High"
    print("PASS: classify_drift thresholds are correct (Low<5, Medium 5-15, High>15)")


# ── Run all tests ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_compute_stats_returns_required_keys()
    test_compute_stats_row_count()
    test_compute_stats_null_rate_between_0_and_100()
    test_compare_snapshots_returns_score_and_level()
    test_drift_level_valid_values()
    test_drift_score_non_negative()
    test_identical_snapshots_give_low_drift()
    test_classify_drift_thresholds()
    print("\n✅ All 8 tests passed!")
