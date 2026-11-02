import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def mk(fmt, books, approved=True, credit=False):
    return {"intake_approved": approved, "format": fmt, "payout_in_credit": credit, "books": books}


def bk(missing=0, cond="good", fake=False):
    return {"missing_pages": missing, "condition": cond, "counterfeit": fake}


def test_single_paperback_good():
    r = process_book_buybacks([mk("paperback", [bk()])], 5.0)
    assert r == {"total_payout": 8.0, "status": "COMPLETED"}


def test_invalid_input_raises():
    with pytest.raises(ValueError):
        process_book_buybacks("not a list", 1.0)


def test_unapproved_batch_skipped():
    assert process_book_buybacks([mk("paperback", [bk()], approved=False)], 0)["status"] == "ZERO_CREDIT"


def test_textbook_mint_and_hardcover_poor():
    r = process_book_buybacks([mk("textbook", [bk(cond="mint")]), mk("hardcover", [bk(cond="poor")])], 0)
    assert r["total_payout"] == 56.0


def test_unknown_format_rejected():
    assert process_book_buybacks([mk("comic", [bk()])], 0)["status"] == "ZERO_CREDIT"


def test_missing_pages_rejected():
    assert process_book_buybacks([mk("paperback", [bk(missing=2)])], 0)["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook_zeroes_batch():
    r = process_book_buybacks([mk("textbook", [bk(), bk(fake=True), bk()])], 0)
    assert r["status"] == "ZERO_CREDIT"


def test_counterfeit_paperback_ignored_and_credit_bonus():
    r = process_book_buybacks([mk("paperback", [bk(fake=True), bk()], credit=True)], 5.0)
    assert r["total_payout"] == 13.0


def test_audit_rejected():
    r = process_book_buybacks([mk("paperback", [bk(missing=1)] * 5 + [bk()])], 0)
    assert r["status"] == "AUDIT_REJECTED"


def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibrate():
    assert inspect_scanner_calibration([[1, 6, 7]]) == "RECALIBRATE"


def test_scanner_calibrated_streak_reset():
    assert inspect_scanner_calibration([[6, 1, 6, 1]]) == "CALIBRATED"
