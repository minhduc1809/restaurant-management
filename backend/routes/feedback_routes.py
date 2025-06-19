from flask import Blueprint, request, jsonify
from db_config import get_db_connection

feedback_bp = Blueprint('feedback_bp', __name__)

# 📩 Gửi phản hồi
@feedback_bp.route('/', methods=['POST'])
def send_feedback():
    data = request.json
    khach_hang_id = data.get('KhachHangID')
    noi_dung = data.get('NoiDung')
    diem_danh_gia = data.get('DiemDanhGia')  # Thang điểm 10

    if not khach_hang_id or noi_dung is None or diem_danh_gia is None:
        return jsonify({'message': 'Thiếu thông tin phản hồi'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO phanhoi (KhachHangID, NoiDung, DiemDanhGia)
        VALUES (%s, %s, %s)
    """, (khach_hang_id, noi_dung, diem_danh_gia))

    db.commit()
    db.close()
    return jsonify({'message': 'Gửi phản hồi thành công'}), 201

# 📋 Lấy tất cả phản hồi
@feedback_bp.route('/', methods=['GET'])
def get_all_feedback():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.PhanHoiID, f.NoiDung, f.DiemDanhGia, kh.HoTenKhachHang
        FROM phanhoi f
        JOIN khachhang kh ON f.KhachHangID = kh.KhachHangID
        ORDER BY f.PhanHoiID DESC
    """)
    feedbacks = cursor.fetchall()
    db.close()
    return jsonify(feedbacks)
