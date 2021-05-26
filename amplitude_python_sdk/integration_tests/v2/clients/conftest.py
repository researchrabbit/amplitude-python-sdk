import os

from dotenv import load_dotenv
import pytest


@pytest.fixture(scope="session")
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def test_api_key(load_env):
    return os.environ["AMPLITUDE_TEST_API_KEY"]


@pytest.fixture(scope="session")
def test_secret_key(load_env):
    return os.environ["AMPLITUDE_TEST_SECRET_KEY"]
