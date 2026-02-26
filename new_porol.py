import hashlib
new_password = "_lioplil0_"  # впиши сюда новый пароль
hash = hashlib.sha256(new_password.encode()).hexdigest()
print(hash)