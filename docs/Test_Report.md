# Test Report

**Status: no live execution has been recorded yet. Fill this in after a real run.**

## Execution summary
| Item | Value |
|---|---|
| Date of execution | Not executed yet |
| Environment | Not executed yet |
| Python / pytest versions | Not executed yet |
| API target | GoRest v2 (`https://gorest.co.in/public/v2`) |
| Total test items | Not executed yet |
| Passed | Not executed yet |
| Failed | Not executed yet |
| Skipped | Not executed yet |

## How to complete this report
```bash
export GOREST_TOKEN="your_token"
pytest -v --html=reports/test_report.html --self-contained-html
```
Copy the totals from the pytest summary and attach the HTML report. Do not edit numbers by hand.

## Known limitations
- Behaviour assumptions in `Test_Plan.md` section 5 are unverified until the first live run.
- Without `GOREST_TOKEN`, POST, PUT and DELETE tests are skipped (shown as skipped, never as passed).
- GoRest is shared and rate limited, so occasional failures may come from the service.

## Defects and issues
None recorded yet.
