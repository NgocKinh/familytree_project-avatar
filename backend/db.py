import mysql.connector

def get_connection():
    print("CONNECTING TO DATABASE: family_test")
    return mysql.connector.connect(
        host="localhost",
        user="root",             # thay user MySQL
        password="Msand@167",# thay mật khẩu
        database="family_test"   # dùng DB test
    )

    return conn