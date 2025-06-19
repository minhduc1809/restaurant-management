from flask import Blueprint, request, jsonify
from db_config import get_db_connection

booking_bp = Blueprint('booking_bp', __name__)

# 📋 Lấy tất cả lượt đặt bàn
@booking_bp.route('/', methods=['GET'])
def get_all_bookings():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM luotdatban ORDER BY ThoiGianDat DESC")
    bookings = cursor.fetchall()
    db.close()
    return jsonify(bookings)

# ➕ Thêm lượt đặt bàn mới
@booking_bp.route('/', methods=['POST'])
def create_booking():
    data = request.json
    ten_khach_hang = data.get('TenKhachHang')
    thoi_gian_dat = data.get('ThoiGianDat')
    so_ban = data.get('SoBan')

    if not ten_khach_hang or not thoi_gian_dat or not so_ban:
        return jsonify({'message': 'Thiếu thông tin đặt bàn'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO luotdatban (TenKhachHang, ThoiGianDat, SoBan)
        VALUES (%s, %s, %s)
    """, (ten_khach_hang, thoi_gian_dat, so_ban))

    db.commit()
    db.close()
    return jsonify({'message': 'Đặt bàn thành công'}), 201

# ❌ Xóa lượt đặt bàn
@booking_bp.route('/<int:luot_dat_ban_id>', methods=['DELETE'])
def delete_booking(luot_dat_ban_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM luotdatban WHERE LuotDatBanID = %s", (luot_dat_ban_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Xóa lượt đặt bàn thành công'})
