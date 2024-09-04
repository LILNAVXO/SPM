from db_man import table_creation, init_connect, db_creation, db_connect
from spm_int import mpass_dialog, addpass_ui
from encryptor import key_gen

def main():
    try:
        open("secret.key", "rb")
    except:
        key_gen()
    init_connect()
    db_creation()
    table_creation()
    mpass_dialog()
    addpass_ui()

if __name__ == "__main__":
    main()
