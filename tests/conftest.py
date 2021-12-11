import os
import sys
from pathlib import Path

import pytest
from config import ENV


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(shared_datadir):
    tmpdir = shared_datadir
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    ENV.DATA_DIR = str(tmpdir) + "/ext"
    os.chdir(str(tmpdir))
