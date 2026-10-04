# Software Requirements Specification

**Project:** REST API Test Automation Framework

## 1. Introduction
This document specifies the requirements of a modular test automation framework for REST APIs, built with Python, Pytest and Requests. The framework is demonstrated against the public GoRest v2 `/users` API.

## 2. Problem Statement
Manual API testing is slow, hard to repeat and error-prone. Ad-hoc scripts duplicate request code, hard-code URLs and give no consistent reports. A structured framework is needed so API behaviour can be verified repeatedly and automatically.

## 3. Project Objective
Design and implement a maintainable, scalable framework that sends HTTP requests, validates responses (status, fields, types, schema, timing), covers positive, negative and boundary scenarios, produces HTML reports and runs in CI.

## 4. Scope
**In scope:** CRUD tests for `/users` (GET, POST, PUT, DELETE), response validation, configuration management, logging, HTML reporting, GitHub Actions CI.
**Out of scope:** UI testing, load/performance testing, database validation, OAuth/JWT flows.

## 5. Functional Requirements
| ID | Requirement |
|---|---|
| FR-01 | The framework shall send GET, POST, PUT and DELETE requests through one reusable client. |
| FR-02 | The framework shall validate HTTP status codes. |
| FR-03 | The framework shall validate required fields and data types of responses. |
| FR-04 | The framework shall validate responses against a JSON Schema. |
| FR-05 | The framework shall support positive, negative and boundary-value tests. |
| FR-06 | Test data shall be stored outside test code and loaded by a reusable utility. |
| FR-07 | The framework shall log method, endpoint, status code, errors and test name. |
| FR-08 | The framework shall generate an HTML test report. |
| FR-09 | Tests shall run locally and in GitHub Actions. |
| FR-10 | Tests shall be selectable by marker (smoke, regression, get, post, put, delete). |

## 6. Non-Functional Requirements
- **Maintainability:** changing the base URL requires editing no test.
- **Reusability:** HTTP and assertion logic is written once.
- **Scalability:** a new endpoint needs only new tests and data.
- **Reliability:** tests create and remove their own data to stay deterministic.
- **Readability:** tests read like specifications.
- **Security:** no secrets in the repository; tokens never logged.

## 7. System Constraints
- Requires Python 3.11+ and internet access.
- GoRest is a shared public service with rate limits and public data.
- Write requests need a GoRest access token.

## 8. Assumptions
- GoRest behaves as described in its public documentation (status codes 200/201/204/404/422, `[{"field","message"}]` validation errors).
- Emails on the configured domain are accepted.
- Boundary expectations in `test_data/payloads/boundary_user.json` match the live API (see Test Plan, "Assumptions to verify").

## 9. Dependencies
Python, pytest, requests, pytest-html, jsonschema, Git, GitHub Actions, a GoRest token.

## 10. Expected Outcomes
A working framework with 14 automated test cases, an HTML report, a CI pipeline and professional documentation, suitable for a portfolio.
