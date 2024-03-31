import bcrypt

def hashPassword(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verifyPassword(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)