import pytest 
from api.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()
   