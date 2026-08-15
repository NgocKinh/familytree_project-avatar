# ============================================
# db_helper.py
# Mô-đun quản lý kết nối MySQL trung tâm
# ============================================
from mysql.connector import Error
from backend.db import get_connection

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