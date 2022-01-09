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


def check_callback_user(func):
    @wraps(func)
    def decorator_check_callback_user(*args, **kwargs):
        update = args[0]
        uid = str(update.effective_user.id)
        query = update.callback_query
        data = query.data.split(":")[-1]
        reply_user_name = update.effective_user.full_name
        alert_msg = f"亲爱的{reply_user_name}, 这个不是你的游戏设置，请不要随意点击!\n如果想要设置单词游戏，请自己输入命令/c\n"
        if uid == data:
            func(*args, **kwargs)
        else:
            update.callback_query.answer(alert_msg, show_alert=True)
    return decorator_check_callback_user


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

# def check_user_filter(func):
#     @wraps(func)
#     def decorator_check_user(*args, **kwargs):
#         update = args[0]
#         uid = update.effective_user.id
#         query = update.callback_query
#         data = query.data.split(":")
#         print(uid,data)
#         if check_callback_user(uid,data[-1]):
#             func(*args, **kwargs)
#     return decorator_check_user
