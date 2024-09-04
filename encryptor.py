from cryptography.fernet import Fernet

def key_gen():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def key_read():
    return open("secret.key", "rb").read()

def pass_encypt(password):
    key = key_read()
    crypter = Fernet(key)
    crypted_pass = crypter.encrypt(password.encode())
    return crypted_pass

def pass_decrypt(crypted_pass):
    key = key_read()
    decrypter = Fernet(key)
    if isinstance(crypted_pass, memoryview):
        crypted_pass = crypted_pass.tobytes()
    elif isinstance(crypted_pass, str):
        crypted_pass = crypted_pass.encode('utf-8')

        
    try:
        decrypted_pass = decrypter.decrypt(crypted_pass).decode()
        return decrypted_pass
    except Exception as e:
        print(type(crypted_pass))
        print(f"SPM: Error while decryption {e}")
