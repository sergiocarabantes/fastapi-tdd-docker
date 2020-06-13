import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_application


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()  # new
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:  # updated

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


# normal run
# $ docker-compose exec web python -m pytest

# disable warnings
# $ docker-compose exec web python -m pytest -p no:warnings

# run only the last failed tests
# $ docker-compose exec web python -m pytest --lf

# run only the tests with names that match the string expression
# $ docker-compose exec web python -m pytest -k "summary and not test_read_summary"

# stop the test session after the first failure
# $ docker-compose exec web python -m pytest -x

# enter PDB after first failure then end the test session
# $ docker-compose exec web python -m pytest -x --pdb

# stop the test run after two failures
# $ docker-compose exec web python -m pytest --maxfail=2

# show local variables in tracebacks
# $ docker-compose exec web python -m pytest -l

# list the 2 slowest tests
# $ docker-compose exec web python -m pytest --durations=2
