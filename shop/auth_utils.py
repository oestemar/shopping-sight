
from flask import session
from models.user import User

def get_current_user():
    user_id = session.get("user_id")
    if user_id:
        return User.query.get(user_id)
    return None


def user_login_required(func):
    from functools import wraps
    from flask import redirect, url_for, flash

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("ログインしてください。", "warning")
            return redirect(url_for("shop.login"))
        return func(*args, **kwargs)

    return wrapper
