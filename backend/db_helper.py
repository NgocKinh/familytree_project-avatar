# ============================================
# db_helper.py
# Mô-đun quản lý kết nối MySQL trung tâm
# ============================================
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
# ============================================
# 🔸 Hàm tạo kết nối MySQL
# ============================================
def get_connection():
    """
    Tạo và trả về connection tới MySQL.
    Tự động commit = False để chủ động kiểm soát giao dịch.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "familytreedb"),
            autocommit=True
        )
        return conn
    except Error as e:
        print("❌ Lỗi khi kết nối MySQL:", e)
        raise


# ============================================
# 🔸 Hàm an toàn để đóng connection
# ============================================
def close_connection(conn, cur):
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
    except:
        pass
# ============================================
# 🔸 Hàm thực thi truy vấn có rollback an toàn
# ============================================
def execute_query(query, values=None, fetch=False):
    """
    Thực thi truy vấn SQL có rollback nếu lỗi.
    - query: câu lệnh SQL
    - values: tuple chứa giá trị (%s, ...)
    - fetch: True nếu cần trả kết quả SELECT
    """
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, values or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {"affected_rows": cursor.rowcount}
        return result
    except Error as e:
        if conn:
            conn.rollback()
        print("❌ SQL Error:", e)
        raise
    finally:
        close_connection(conn, cursor)