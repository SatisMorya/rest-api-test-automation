# Test Plan and Test Cases

## 1. Objective and scope
Verify the GoRest `/users` API: correct status codes, response structure, data types, validation rules and error handling.

## 2. Approach
- **Positive testing:** valid requests, expected success.
- **Negative testing:** invalid IDs, missing fields, invalid values, duplicates.
- **Equivalence partitioning:** valid, invalid and boundary classes of input.
- **Boundary value analysis:** values at the edges of rules (0 vs 1 character name, blank email, values outside an allowed set).
- **Response validation:** status, JSON, required fields, types, JSON Schema, response time.
- **Regression:** the whole suite is re-run on every push via CI.

## 3. Environment
Python 3.11+, pytest, requests, pytest-html, jsonschema. Target: GoRest v2. Token via `GOREST_TOKEN`.

## 4. Test cases
"14 test cases" means 14 test functions. Parameters create several pytest items inside one function.

| ID | Function | Description | Technique | Expected |
|---|---|---|---|---|
| TC-001 | `test_tc001_get_all_users` | Retrieve all users | Positive | 200, non-empty array |
| TC-002 | `test_tc002_get_user_by_valid_id` | Retrieve a user created in setup | Equivalence: valid | 200, same id and email |
| TC-003 | `test_tc003_get_user_by_invalid_id` | Missing, zero, negative, non-numeric ID | Equivalence: invalid | 404 |
| TC-004 | `test_tc004_get_users_response_structure` | Every listed user has required fields and matches schema | Schema | fields and schema valid |
| TC-005 | `test_tc005_create_user_with_valid_data` | Create a valid user | Positive | 201, integer id, fields echoed |
| TC-006 | `test_tc006_create_user_with_missing_required_field` | Omit each required field in turn | Negative | 422, error names the field |
| TC-007 | `test_tc007_create_user_with_invalid_data` | Bad email, gender, status; duplicate email | Equivalence: invalid | 422, error names the field |
| TC-008 | `test_tc008_update_existing_user` | Update name and status, then re-read | Positive | 200, change persisted |
| TC-009 | `test_tc009_update_non_existing_user` | Update an ID that does not exist | Negative | 404 |
| TC-010 | `test_tc010_update_user_with_boundary_or_invalid_data` | Name 0 and 1 chars, blank email, gender outside set | Boundary / negative | per `boundary_user.json` |
| TC-011 | `test_tc011_delete_existing_user` | Delete, then confirm it is gone | Positive | 204, empty body, then GET 404 |
| TC-012 | `test_tc012_delete_non_existing_user` | Delete an ID that does not exist | Negative | 404 |
| TC-013 | `test_tc013_status_code_and_response_time` | Status and time limit for list and missing user | Non-functional | expected status, time within limit |
| TC-014 | `test_tc014_response_fields_and_data_types` | Fields, types, schema of a single user | Schema | types match |

## 5. Assumptions to verify on the first live run
These expectations come from documentation, not from an observed run. If one fails, check the real behaviour first, then correct the data file or the test.
1. A non-numeric ID (`abc`) returns 404 (TC-003).
2. A 1-character name is accepted with 200 (TC-010 `name_minimum_1_char`).
3. `example.com` emails are accepted (change `email_domain` in `test_data.json` if not).
4. The `gender` error for the value `other` is reported on field `gender` (TC-010).
5. Response time under 5 seconds (change `MAX_RESPONSE_TIME`).
6. Rate limiting returns 429, which the client retries up to `API_MAX_RETRIES` times.

## 6. Entry and exit criteria
**Entry:** token available, API reachable. **Exit:** all 14 test functions executed; failures analysed and logged as defects or corrected assumptions.

## 7. Risks
Shared public API (rate limits, outages), changing live behaviour, other users' data.
