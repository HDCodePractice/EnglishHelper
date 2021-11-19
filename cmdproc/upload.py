from zipfile import ZipFile
from utils.fileproc import gen_pic_dict_from_csv
from pathlib import Path
from telegram.ext import CommandHandler,CallbackContext
from telegram import Update
from utils.filters import check_admin_filter
from config import ENV
from shutil import rmtree

if not Path(ENV.DATA_DIR).exists():
    Path(ENV.DATA_DIR).mkdir()

def get_zip_file(file_path):
    """
    Returns a ZipFile object for the given file path.
    """
    if file_path.endswith(".zip"):
        with ZipFile(file_path, 'r') as zip_file:
            return zip_file
    return None

def get_csv_files(zip_file):
    """
    Returns a list of CSV files in the given ZipFile object.
    """
    return [file for file in zip_file.namelist() if file.endswith('.csv')]

def get_jpg_files(zip_file):
    """
    Returns a list of JPG files in the given ZipFile object.
    """
    return [file for file in zip_file.namelist() if file.endswith('.jpg')]


@check_admin_filter
def update_dict(update: Update, context: CallbackContext):
    if update.effective_message.reply_to_message is None:
        update.message.reply_text("请将你的res目录使用zip压缩发送上来，然后使用/u回复上传的zip文件，注意大小不能超过20MB")
        return
    if update.effective_message.reply_to_message.document is None:
        update.message.reply_text("Please reply to a file.")
        return
    document = update.effective_message.reply_to_message.document
    file_name = document.file_name
    if file_name.endswith((".zip","ZIP")):
        file = update.effective_message.reply_to_message.document.get_file()
        if file.file_size > 20*1024*1024:
            update.message.reply_text("File size too big(20MB).")
            return
        # 清空目录
        rmtree(f"{ENV.DATA_DIR}")
        Path(ENV.DATA_DIR).mkdir()
        # 下载文件
        down_file = file.download(f"{ENV.DATA_DIR}/{file_name}")
        with ZipFile(down_file, 'r') as zip_file:
            # 解压
            zip_file.extractall(ENV.DATA_DIR)
        update.message.reply_text("File extracted.")
    else:
        update.message.reply_text("Please reply to a zip file.")
        return

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("u", update_dict))
    return []