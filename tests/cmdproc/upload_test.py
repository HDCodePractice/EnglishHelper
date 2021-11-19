import pytest
from zipfile import ZipFile
from config import ENV
from pathlib import Path

@pytest.fixture
def res_zip(shared_datadir):
    file_path=f"{shared_datadir}/res.zip"
    return file_path

def test_get_csv_files(res_zip,shared_datadir):
    Path(str(shared_datadir) + "/res").mkdir(parents=True, exist_ok=True)
    ENV.DATA_DIR = str(shared_datadir) + "/res"
    from cmdproc.upload import get_csv_files, get_zip_file, get_jpg_files

    zip_file = get_zip_file(res_zip)
    print(get_csv_files(zip_file))
    assert 'res/iverbs.csv' in get_csv_files(zip_file)
    assert 'res/picwords.csv' in get_csv_files(zip_file)
    assert 'res/inouns.csv' in get_csv_files(zip_file)

def test_get_jpg_files(res_zip,shared_datadir):
    Path(str(shared_datadir) + "/res").mkdir(parents=True, exist_ok=True)
    ENV.DATA_DIR = str(shared_datadir) + "/res"
    from cmdproc.upload import get_csv_files, get_zip_file, get_jpg_files
    
    zip_file = get_zip_file(res_zip)
    print(get_jpg_files(zip_file))
    assert 'res/picwords/9999.jpg' in get_jpg_files(zip_file)