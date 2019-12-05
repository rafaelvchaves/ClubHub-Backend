from db import db, User


def get_user_by_netid(netid):
    return User.query.filter(User.netid == netid).first()


def get_user_by_session_token(session_token):
    return User.query.filter(User.session_token == session_token).first()


def get_user_by_update_token(update_token):
    return User.query.filter(User.update_token == update_token).first()


def verify_credentials(netid, password):
    optional_user = get_user_by_netid(netid)

    if not optional_user:
        return False, optional_user

    return optional_user.verify_password(password), optional_user


def create_user(name, netid, password):
    optional_user = get_user_by_netid(netid)

    if optional_user:
        return False, optional_user

    user = User(name=name, netid=netid, password=password)

    db.session.add(user)
    db.session.commit()

    return True, user

def renew_session(update_token):
    user = get_user_by_update_token(update_token)

    if not user:
        raise Exception('Invalid update token')

    user.renew_session()
    db.session.commit()
    return user
