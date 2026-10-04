"""Base URLs for each supported environment.

GoRest offers a single public instance, so all three environments point to it.
In a real project each entry would hold a different host. Any value can be
overridden at run time with the API_BASE_URL environment variable.
"""

ENVIRONMENTS = {
    "development": {"base_url": "https://gorest.co.in/public/v2"},
    "testing": {"base_url": "https://gorest.co.in/public/v2"},
    "production": {"base_url": "https://gorest.co.in/public/v2"},
}

DEFAULT_ENVIRONMENT = "testing"
