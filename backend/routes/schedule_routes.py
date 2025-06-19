from flask import Blueprint, request, jsonify
from db_config import get_db_connection
from datetime import datetime

schedule_bp = Blueprint('schedule_bp', __name__)

# 📝 API tạo lịch làm
@schedule_bp.route('/', methods=['POST'])
def create_schedule():
    data = request.json

    ten_nhan_vien = data.get('TenNhanVien')
    so_gio_lam = data.get('SoGioLam')
    ca = data.get('Ca')
    ngay = data.get('Ngay')  # Định dạng: 'YYYY-MM-DD'

    if not all([ten_nhan_vien, so_gio_lam, ca, ngay]):
        return jsonify({'message': 'Thiếu thông tin'}), 400

    db = get_db_connection()
    cursor = db.cursor()

    # Kiểm tra xem lịch đã có chưa
    cursor.execute("""
        SELECT * FROM lichlam 
        WHERE TenNhanVien = %s AND Ca = %s AND Ngay = %s
    """, (ten_nhan_vien, ca, ngay))
    exists = cursor.fetchone()

    if exists:
        db.close()
        return jsonify({'message': 'Lịch làm đã tồn tại'}), 409

    # Thêm lịch mới
    cursor.execute("""
        INSERT INTO lichlam (TenNhanVien, SoGioLam, Ca, Ngay)
        VALUES (%s, %s, %s, %s)
    """, (ten_nhan_vien, so_gio_lam, ca, ngay))

    db.commit()
    db.close()
    return jsonify({'message': 'Tạo lịch làm thành công'}), 201

# 📋 API lấy lịch làm của 1 nhân viên (theo tên hoặc ngày)
@schedule_bp.route('/<ten_nhan_vien>', methods=['GET'])
def get_schedule_by_name(ten_nhan_vien):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM lichlam WHERE TenNhanVien = %s
        ORDER BY Ngay DESC
    """, (ten_nhan_vien,))
    rows = cursor.fetchall()
    db.close()

    return jsonify(rows)
