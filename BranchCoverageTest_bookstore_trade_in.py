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


# ---- extra edge/decision-branch tests for branch coverage ----
def test_negative_bonus_raises():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1)


def test_empty_batches_zero_credit():
    assert process_book_buybacks([], 0) == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_batch_without_books_and_defaults():
    # missing keys fall back to defaults: paperback, no books, no credit bonus
    assert process_book_buybacks([{"intake_approved": True}], 5)["status"] == "ZERO_CREDIT"


def test_book_defaults_are_good_paperback():
    r = process_book_buybacks([{"intake_approved": True, "books": [{}]}], 0)
    assert r["total_payout"] == 8.0


def test_missing_intake_flag_skips_batch():
    assert process_book_buybacks([{"format": "textbook", "books": [{}]}], 0)["status"] == "ZERO_CREDIT"


def test_credit_bonus_on_empty_batch_and_not_taken():
    r = process_book_buybacks([mk("hardcover", [], credit=True), mk("hardcover", [bk()], credit=False)], 3)
    assert r["total_payout"] == 18.0 and r["status"] == "COMPLETED"


def test_mint_paperback_and_poor_textbook():
    assert process_book_buybacks([mk("paperback", [bk(cond="mint")])], 0)["total_payout"] == 10.0
    assert process_book_buybacks([mk("textbook", [bk(cond="poor")])], 0)["total_payout"] == 16.0


def test_exactly_four_rejections_not_audit():
    r = process_book_buybacks([mk("paperback", [bk(missing=1)] * 4 + [bk()])], 0)
    assert r["status"] == "COMPLETED"


def test_unknown_format_counts_toward_audit():
    r = process_book_buybacks([mk("zine", [bk()])] * 5 + [mk("paperback", [bk()])], 0)
    assert r["status"] == "AUDIT_REJECTED" and r["total_payout"] == 8.0


def test_counterfeit_textbook_still_adds_bonus():
    r = process_book_buybacks([mk("textbook", [bk(fake=True)], credit=True)], 5)
    assert r["total_payout"] == 5.0


def test_scanner_boundary_five_is_ok():
    assert inspect_scanner_calibration([[5, 5, 5]]) == "CALIBRATED"


def test_scanner_second_device_triggers():
    assert inspect_scanner_calibration([[1, 2], [9, 9]]) == "RECALIBRATE"


def test_scanner_empty_device_readings():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"
