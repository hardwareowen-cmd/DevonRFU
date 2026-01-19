from functools import wraps
from flask_login import current_user
from flask import jsonify, redirect, url_for

def access_level_requireds(level, requestonly=False):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if current_user.is_authenticated and current_user.adminLevel >= level:
                return f(*args, **kwargs)
            if requestonly:
                if not current_user.is_authenticated:
                    return jsonify({'error': 'unauthenticated'}), 401
            return jsonify({'error': 'forbidden'}), 403
            return redirect(url_for('index'))
        return decorated_func
    return decorator
