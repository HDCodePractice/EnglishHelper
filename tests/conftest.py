import sys
import pytest
import shutil

# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # copy test data to tmpdir
    shutil.copyfile("pic_dict.json", str(tmpdir) + "/pic_dict.json")
    shutil.copyfile("word_dict.json", str(tmpdir) + "/word_dict.json")
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield