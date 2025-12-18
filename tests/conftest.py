import copy

import pytest


@pytest.fixture(autouse=True)
def _reset_in_memory_activities():
    """Ensure tests don't leak state via the global in-memory DB."""
    from src import app as app_module

    original = copy.deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities = copy.deepcopy(original)
