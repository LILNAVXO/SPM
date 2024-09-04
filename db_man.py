import psycopg2
from psycopg2 import sql
import hashlib


def init_connect():
    user = "postgres"
    host = "localhost"
    try:
        db_link = psycopg2.connect(user = user, host = host)
        print("SPM: DB Connection Status : 200")
        return db_link
    except:
        print("SPM: DB Connection Status : 500")
        print("An error Occured while trying to form a connection to the database ")

def db_creation():
    db_link = init_connect()
    db_link.autocommit = True
    try:
        yap = db_link.cursor()
        yap.execute(sql.SQL("CREATE DATABASE spm"))
        print("SPM: DataBase Creation Status : 200")
    except Exception as error:
        print("SPM: DataBase Creation Status : 500")
        print(f"Error:{error}")


def db_connect():
    user = "postgres"
    dbname = "spm"
    host = "localhost"
    try:
        db_link = psycopg2.connect(user = user, host = host, dbname = dbname)
        print("SPM: spm Connection Status : 200")
        return db_link
    except Exception as error:
        print("SPM: spm Connection Status : 500")
        print(f"Error:{error}")        

def table_creation():
    db_link = db_connect()
    try:
        yap = db_link.cursor()
        yap.execute('''CREATE TABLE IF NOT EXISTS passwords
                    (id SERIAL PRIMARY KEY,
                    account TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password BYTEA NOT NULL)''')
        db_link.commit()
        yap.execute('''CREATE TABLE IF NOT EXISTS master_password
                    (id SERIAL PRIMARY KEY,
                    password BYTEA NOT NULL)''')
        db_link.commit()
        db_link.close()
        print("SPM: Table Creation Status : 200")
    except:
        print("SPM: Table Creation Status : 500")
        print("An error Occured While creating the tables")

def add_pass(account, username, encrypted_pass):
    db_link = db_connect()
    try:
        yap = db_link.cursor()
        yap.execute("INSERT INTO passwords (account, username, password) VALUES (%s, %s, %s)",(account, username, encrypted_pass))
        db_link.commit()
        db_link.close()
        print("SPM: Password Commit Status : 200")
    except:
        print("SPM: Password Commit Status : 500")

def get_pass():
    db_link = db_connect()
    try:
        yap = db_link.cursor()
        yap.execute("SELECT account, username, password FROM passwords")
        passwds = yap.fetchall()
        db_link.close()
        print("SPM: Password Fetch Status : 200")
        return passwds
    except:
        print("SPM: Password Fetch Status : 500")
def add_mpass(new_mpass):
    db_link = db_connect()
    try:
        yap = db_link.cursor()
        mpasshash = hashlib.sha256(new_mpass.encode("utf-8")).hexdigest()
        yap.execute("INSERT INTO master_password (password) VALUES (%s)",(mpasshash,))
        db_link.commit()
        db_link.close()
        print("SPM: Master Password Commit Status : 200")
    except Exception as error:
        print("SPM: Master Password Commit Status : 500")
        print(f"Error:{error}")

def get_mpass():
    db_link = db_connect()
    try:
        yap = db_link.cursor()
        yap.execute("SELECT password FROM master_password WHERE id=1")
        hashfetch = yap.fetchone()
        db_link.close()
        if hashfetch is not None:
            mpasshash = hashfetch[0]
            if isinstance(mpasshash, memoryview):
                mpasshash = mpasshash.tobytes()
                print("SPM: Master Password Fetch Status : 200")
                print(mpasshash)
                return mpasshash
        else:
            print("SPM: Master Password Status : 404!")
    except Exception as error:
        print("SPM: Master Password Fetch Status : 500")
        print(f"Error:{error}")
