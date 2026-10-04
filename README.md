# REST API Test Automation Framework

**A Modular and Scalable API Testing Framework using Python, Pytest and Requests**

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC)
![License](https://img.shields.io/badge/license-MIT-green)

A layered test automation framework for REST APIs. It separates HTTP communication, assertions, configuration and test data, so new endpoints and environments can be added without rewriting tests. It is demonstrated against the public [GoRest](https://gorest.co.in) v2 `/users` API with 14 automated test cases covering positive, negative, boundary and response-validation scenarios.

## Tech Stack
| Tool | Purpose |
|---|---|
| Python 3.11+ | Language |
| Pytest | Test runner, fixtures, parametrization, markers |
| Requests | HTTP client |
| jsonschema | Response schema validation |
| pytest-html | HTML reports |
| Git + GitHub Actions | Version control and CI |

## Architecture
```text
Test cases (pytest) -> Service layer -> API client -> REST API -> Assertions / schema -> Reports and logs
```
| Layer | Responsibility |
|---|---|
| `tests/` | What to check |
| `services/user_service.py` | Which endpoint to call (one method per operation) |
| `core/api_client.py` | How to communicate: HTTP, logging, retries (no assertions) |
| `assertions/` | How to verify responses |
| `config/`, `test_data/` | Settings and data, kept out of test code |
| `utils/` | Logging and data loading |

The client has no assertions on purpose: a 404 is a failure in one test and the expected result in another, so only the test decides. See `docs/System_Design.md` for diagrams.

## Features
- Reusable `APIClient` (GET, POST, PUT, DELETE, headers, params, timeout, Bearer-token ready)
- Service layer: endpoint paths live in one place, so tests never build URLs
- Automatic retry with backoff for rate limits and gateway errors (429, 502, 503, 504); timeouts and connection errors are never retried
- Clear exceptions for timeouts and connection errors (failures are never hidden)
- Readable assertions: `assert_status_code`, `assert_required_fields`, `assert_field_types`, `assert_matches_schema`, `assert_response_time`
- Test data in JSON, loaded through one utility
- Environment config through variables; the token is never logged or committed
- Structured logs (timestamp, level, test name, method, endpoint, status)
- Self-cleaning tests: users created by tests are deleted afterwards
- Markers: `smoke`, `regression`, `get`, `post`, `put`, `delete`
- HTML report and GitHub Actions pipeline

## Project Structure
```text
config/        settings.py, environments.py
core/          api_client.py
services/      user_service.py
models/        user_model.py
assertions/    status, response, schema assertions
test_data/     payloads/ and test_data.json
schemas/       user_schema.json
tests/         conftest.py, users/, validation/
utils/         logger.py, data_loader.py
docs/          requirements, design, test plan, API docs, report
.github/       workflows/api-tests.yml
```

## API Endpoints
Base URL: `https://gorest.co.in/public/v2`

| Method | Endpoint | Success | Failure |
|---|---|---|---|
| GET | `/users` | 200 | |
| GET | `/users/{id}` | 200 | 404 |
| POST | `/users` | 201 | 422 |
| PUT | `/users/{id}` | 200 | 404 / 422 |
| DELETE | `/users/{id}` | 204 | 404 |

## Test Strategy
Positive testing, negative testing, equivalence partitioning (valid / invalid / boundary) and boundary value analysis, plus response validation. Full list of cases: [`docs/Test_Plan.md`](docs/Test_Plan.md).

| ID | Area | Scenario |
|---|---|---|
| TC-001 to TC-004 | GET | all users, valid id, invalid ids, structure |
| TC-005 to TC-007 | POST | valid, missing fields, invalid data |
| TC-008 to TC-010 | PUT | update, non-existing, boundary/invalid |
| TC-011, TC-012 | DELETE | existing, non-existing |
| TC-013, TC-014 | Validation | status and response time, fields and types |

## Test Coverage
| Technique | GET | POST | PUT | DELETE |
|---|:-:|:-:|:-:|:-:|
| Functional | ✓ | ✓ | ✓ | ✓ |
| Negative | ✓ | ✓ | ✓ | ✓ |
| Boundary | - | - | ✓ | - |
| Response validation | ✓ | ✓ | ✓ | ✓ |

## Installation
```bash
git clone https://github.com/SatisMorya/rest-api-test-automation.git
cd rest-api-test-automation
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Get a free token at [gorest.co.in](https://gorest.co.in), then:
```bash
cp .env.example .env        # put your token in .env (never commit it)
# or: export GOREST_TOKEN="your_token"
```
Without a token, GET tests that need no data creation still run and POST/PUT/DELETE tests are reported as **skipped**.

## Execution
```bash
pytest                      # all tests
pytest -v                   # verbose
pytest -m smoke             # smoke tests
pytest -m "post or put"     # by marker
pytest --html=reports/test_report.html --self-contained-html
```
Configuration: `APP_ENV` (development/testing/production), `API_BASE_URL`, `API_TIMEOUT`, `API_MAX_RETRIES`, `MAX_RESPONSE_TIME`.

Lint (PEP 8): `pip install -r requirements-dev.txt && flake8 .`

## Reporting
The HTML report is written to `reports/test_report.html` (test name, status, duration, failure details, summary). Logs go to `logs/api_tests.log`.

## CI/CD
`.github/workflows/api-tests.yml` runs on every push and pull request: checkout, set up Python (3.11 and 3.12), install pinned dependencies, lint with flake8, run pytest, generate the report and upload the report and logs as an artifact. Add your token as the repository secret `GOREST_TOKEN` (Settings > Secrets and variables > Actions).

## Results
Live-run results have not been recorded yet. After running against GoRest, fill in [`docs/Test_Report.md`](docs/Test_Report.md) from the real pytest output.

## Documentation
| Document | Content |
|---|---|
| [Software Requirements](docs/Software_Requirements.md) | Scope, functional and non-functional requirements |
| [System Design](docs/System_Design.md) | Architecture, flows, module responsibilities |
| [Test Plan](docs/Test_Plan.md) | Strategy, 14 test cases, assumptions to verify |
| [API Documentation](docs/API_Documentation.md) | Endpoints, fields, error formats |
| [Test Report](docs/Test_Report.md) | Results (filled in after a real run) |

## Adding a New Endpoint
1. Add a schema in `schemas/` and payloads in `test_data/`.
2. Add a service class in `services/` (one method per operation).
3. Add a fixture in `tests/conftest.py` and tests in a new `tests/<resource>/` folder.

The client, assertions, config and logging need no changes.

## Future Enhancements
Not implemented yet: Allure reports, Docker, database validation, authentication testing (OAuth/JWT), parallel execution, performance testing, cloud execution, Slack/email notifications, test data factories, secret management.

## Author
**Satish Morya** - B.Tech (AI & ML), Apex University, Jaipur
GitHub: [SatisMorya](https://github.com/SatisMorya) | LinkedIn: [satish-m-8ba531293](https://linkedin.com/in/satish-m-8ba531293)
