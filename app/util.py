from flask_login import current_user

def checkIfLoggedIn(current_user):
    if current_user.is_authenticated:
        return current_user.emaill
