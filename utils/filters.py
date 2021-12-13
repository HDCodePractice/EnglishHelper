from functools import wraps
from config import ENV

def check_admin_permission(uid):
    # 检查uid是否为管理员
    if str(uid) in ENV.ADMIN_IDS:
        return True
    else:
        return False

def check_chaid_permission(chatid):
    if str(chatid) in ENV.CHATIDS:
        return True
    else:
        return False

def check_chatids_valid(chatids):
    for i in chatids:
        if not _check_chatid_valid(i):
            return False
    return True

def check_callback_user(uid,data):
    if str(uid) == data:
        return True
    else:
        return False

def _check_chatid_valid(chatid):
    if len(chatid) > 1 and (chatid[0] == '-' or chatid[0].isnumeric()) and chatid[1:].isnumeric():
        return True
    else:
        return False

def check_chatid_filter(func):
    @wraps(func)
    def decorator_check_chatid_permission(*args, **kwargs):
        update = args[0]
        chatid = update.effective_chat.id
        if check_chaid_permission(chatid):
            func(*args, **kwargs)
    return decorator_check_chatid_permission

def check_admin_filter(func):
    @wraps(func)
    def decorator_check_admin(*args, **kwargs):
        update = args[0]
        uid = update.effective_user.id
        if check_admin_permission(uid):
            func(*args, **kwargs)
    return decorator_check_admin