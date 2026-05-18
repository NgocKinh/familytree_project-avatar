# =========================================================
# File: backend/app.py
# Mô tả:
#   - Flask API cơ bản
#   - Kết nối MySQL
#   - Fix CORS để React gọi được
# =========================================================

from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import mysql.connector
from api.tree import tree_bp

# ==============================
# Khởi tạo app
# ==============================
app = Flask(__name__)
CORS(app)  # 👈 FIX CORS
app.register_blueprint(tree_bp, url_prefix="/api/tree")
# ==============================
# Kết nối DB
# ==============================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Msand@167",
        database="familytreedb"
    )

# ==============================
# API: Lấy danh sách person
# ==============================
@app.route("/api/person", methods=["GET"])
def get_persons():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *,
        CONCAT(
            COALESCE(sur_name, ''), ' ',
            COALESCE(last_name, ''), ' ',
            COALESCE(middle_name, ''), ' ',
            COALESCE(first_name, '')
        ) AS full_name_vn
        FROM persons
        """)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500    

# ==========================================================
# 🟢 API: THÊM PERSON
# ==========================================================
@app.route("/api/person/basic", methods=["POST"])
def add_person():
    try:
        data = request.json

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO persons (
            sur_name,
            last_name,
            middle_name,
            first_name,
            gender,
            birth_date,
            death_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("sur_name"),
            data.get("last_name"),
            data.get("middle_name"),
            data.get("first_name"),
            data.get("gender"),
            data.get("birth_date"),
            data.get("death_date"),
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================================
# 🔴 API: LẤY DANH SÁCH HÔN NHÂN
# ==========================================================
@app.route("/api/marriage", methods=["GET"])
def get_marriages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        m.id,
        m.spouse_a_id,
        m.spouse_b_id,
        m.start_date,
        m.end_date,
        m.status,
        m.location,
        
        -- tên người A
        CONCAT(
            COALESCE(p1.sur_name, ''), ' ',
            COALESCE(p1.last_name, ''), ' ',
            COALESCE(p1.middle_name, ''), ' ',
            COALESCE(p1.first_name, '')
        ) AS spouse_a_name,

        -- tên người B
        CONCAT(
            COALESCE(p2.sur_name, ''), ' ',
            COALESCE(p2.last_name, ''), ' ',
            COALESCE(p2.middle_name, ''), ' ',
            COALESCE(p2.first_name, '')
        ) AS spouse_b_name

    FROM marriages m
    LEFT JOIN persons p1 ON m.spouse_a_id = p1.person_id
    LEFT JOIN persons p2 ON m.spouse_b_id = p2.person_id
    """)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(result)        

# ==========================================================
# 🟢 API: THÊM QUAN HỆ HÔN NHÂN
# ==========================================================
@app.route("/api/marriage", methods=["POST"])
def add_marriage():
    try:
        data = request.json

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO marriages (
            spouse_a_id,
            spouse_b_id,
            start_date,
            end_date,
            status,
            location
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get("spouse_a_id"),
            data.get("spouse_b_id"),
            data.get("start_date"),
            data.get("end_date"),
            data.get("status"),
            data.get("location"),
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Đã lưu thành công"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================================
# 🔵 API: LẤY DANH SÁCH CHA - CON
# ==========================================================
@app.route("/api/parent_child", methods=["GET"])
def get_parent_child():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        pc.id,
        pc.parent_id,
        pc.child_id,
        pc.type,

        CONCAT(
            COALESCE(p1.sur_name, ''), ' ',
            COALESCE(p1.last_name, ''), ' ',
            COALESCE(p1.middle_name, ''), ' ',
            COALESCE(p1.first_name, '')
        ) AS parent_name,

        CONCAT(
            COALESCE(p2.sur_name, ''), ' ',
            COALESCE(p2.last_name, ''), ' ',
            COALESCE(p2.middle_name, ''), ' ',
            COALESCE(p2.first_name, '')
        ) AS child_name

    FROM parent_child pc
    LEFT JOIN persons p1 ON pc.parent_id = p1.person_id
    LEFT JOIN persons p2 ON pc.child_id = p2.person_id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)
# ==============================
# Run server
# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=5000)