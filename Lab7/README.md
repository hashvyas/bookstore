# L6_L7_09 — Bookstore Trade-In

Lab 7: Fuzz Testing with Hypothesis

**Name:** V Vyas  
**SRN:** PES2UG24CS569  
**Section:** 5J

## About

A set of property-based fuzz tests targeting ISBN-10 format validation, book depreciation ratios, and condition multiplier lookups to expose type and bound crashes.

## Files

| File | Description |
|------|-------------|
| `processor.py` | Fixed module: all three functions return `None` on invalid input instead of crashing |
| `test_processor.py` | Hypothesis fuzz tests (`st.text() \| st.none()`) for all three functions |
| `screenshot1_buggy_processor_output.png` | Initial (buggy) `processor.py` run |
| `screenshot2_buggy_hypothesis_tests.png` | Failing Hypothesis tests on the buggy code (3 failed) |
| `screenshot3_fixed_processor_output.png` | Fixed `processor.py` run |
| `screenshot4_fixed_hypothesis_tests.png` | Hypothesis tests on the fixed code (3 passed) |
| `Lab7_Fuzzing_Report.pdf` | Report: bugs found, fixes, and all four screenshots |

## Run

```
pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py
```