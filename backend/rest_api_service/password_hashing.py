import bcrypt


def verify_password(hashed_password, user_password):
  return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

password =  bcrypt.hashpw(b'busi', bcrypt.gensalt())

print(verify_password(password, "busi"))