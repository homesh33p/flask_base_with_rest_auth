from . import db,User,token_required,decoded_exp_time_to_str

def list_users(admin=False):    
    users = db.session.query(User).filter(User.admin == admin).all()  # Assuming you have a list of users from the database
    return {'users': users}

def list_all_users():
    users = db.session.query(User).all()  # Assuming you have a list of users from the database
    return {'users': users}

@token_required
def get_logged_in_user():
    public_id = get_logged_in_user.sub
    user = db.session.query(User).filter(User.id==public_id).first()
    expires_at = decoded_exp_time_to_str(get_logged_in_user.exp)
    user.token_expires_at = expires_at
    return user