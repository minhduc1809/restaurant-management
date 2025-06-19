from flask import Blueprint, request, jsonify
from db_config import get_db_connection
from datetime import datetime

invoice_bp = Blueprint('invoice_bp', __name__)

# 📋 Lấy tất cả hóa đơn
@invoice_bp.route('/', methods=['GET'])
def get_all_invoices():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM hoadon ORDER BY ThoiDiemTao DESC
    """)
    invoices = cursor.fetchall()

    db.close()
    return jsonify(invoices)

# ➕ Tạo hóa đơn mới (bao gồm nhiều món ăn)
@invoice_bp.route('/', methods=['POST'])
def create_invoice():
    data = request.json
    ho_ten_khach = data.get('HoTenKhachHang')
    chi_tiet = data.get('ChiTiet')  # Danh sách món: [{MonAnID, SoLuong, Gia}]

    if not ho_ten_khach or not chi_tiet:
        return jsonify({'message': 'Thiếu thông tin hóa đơn'}), 400

    db = get_db_connection()
    cursor = db.cursor()

    # Tính tổng tiền
    tong_tien = sum(item['SoLuong'] * item['Gia'] for item in chi_tiet)
    thoi_diem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Thêm hóa đơn
    cursor.execute("""
        INSERT INTO hoadon (ThoiDiemTao, HoTenKhachHang, TongTien)
        VALUES (%s, %s, %s)
    """, (thoi_diem, ho_ten_khach, tong_tien))
    hoa_don_id = cursor.lastrowid

    # Thêm chi tiết hóa đơn
    for item in chi_tiet:
        cursor.execute("""
            INSERT INTO chitiethoadon (HoaDonID, MonAnID, SoLuongMonAn, Gia, ThanhTien)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            hoa_don_id,
            item['MonAnID'],
            item['SoLuong'],
            item['Gia'],
            item['SoLuong'] * item['Gia']
        ))

    db.commit()
    db.close()

    return jsonify({'message': 'Lưu hóa đơn thành công', 'HoaDonID': hoa_don_id}), 201

# 📄 Lấy chi tiết hóa đơn theo ID
@invoice_bp.route('/<int:hoa_don_id>', methods=['GET'])
def get_invoice_detail(hoa_don_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Lấy thông tin hóa đơn
    cursor.execute("SELECT * FROM hoadon WHERE HoaDonID = %s", (hoa_don_id,))
    hoa_don = cursor.fetchone()
    if not hoa_don:
        db.close()
        return jsonify({'message': 'Không tìm thấy hóa đơn'}), 404

    # Lấy chi tiết các món ăn
    cursor.execute("""
        SELECT ct.MonAnID, ma.TenMonAn, ct.SoLuongMonAn, ct.Gia, ct.ThanhTien
        FROM chitiethoadon ct
        JOIN monan ma ON ct.MonAnID = ma.MonAnID
        WHERE ct.HoaDonID = %s
    """, (hoa_don_id,))
    chi_tiet = cursor.fetchall()
    db.close()

    return jsonify({'HoaDon': hoa_don, 'ChiTiet': chi_tiet})
