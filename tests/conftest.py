'''
fixtures here

- http client
- db accessing (i.e. sqlite for tests)
- creating entities (from data/preparing)
- ... 

'''
import sys
from pathlib import Path

# set app`s parent folder
root_dir = Path(__file__).parent.parent  
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))



from fastapi.testclient import TestClient
from app.setup_app import atom_eco_app
import pytest
@pytest.fixture(scope="function")
def client():
    """Create a new FastAPI TestClient. Will be accessible for all tests"""        
    with TestClient(atom_eco_app, backend="asyncio") as client:
        yield client
