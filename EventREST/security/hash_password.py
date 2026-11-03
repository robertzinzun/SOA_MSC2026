from pwdlib import PasswordHash
class PaswordHash:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()
    def create_hash(self,password:str):
        return self.password_hash.hash(password)
    def verify_hash(self,plain_password:str,hashed_password:str):
        return self.password_hash.verify(plain_password,hashed_password)