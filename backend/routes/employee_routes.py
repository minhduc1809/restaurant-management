from flask import Blueprint, request, jsonify
from db_config import get_db_connection

employee_bp = Blueprint('employee_bp', __name__)

# 📋 Lấy danh sách nhân viên
@employee_bp.route('/', methods=['GET'])
def get_employees():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM nhanvien")
    employees = cursor.fetchall()
    db.close()
    return jsonify(employees)

# ➕ Thêm nhân viên
@employee_bp.route('/', methods=['POST'])
def add_employee():
    data = request.json
    ten = data.get('HoTenNhanVien')
    vaitro = data.get('VaiTro')
    sdt = data.get('SoDienThoai')

    if not ten or not vaitro or not sdt:
        return jsonify({'message': 'Thiếu thông tin nhân viên'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO nhanvien (HoTenNhanVien, VaiTro, SoDienThoai)
        VALUES (%s, %s, %s)
    """, (ten, vaitro, sdt))
    db.commit()
    db.close()
    return jsonify({'message': 'Thêm nhân viên thành công'}), 201

# ✏️ Cập nhật thông tin nhân viên
@employee_bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    ten = data.get('HoTenNhanVien')
    vaitro = data.get('VaiTro')
    sdt = data.get('SoDienThoai')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE nhanvien
        SET HoTenNhanVien=%s, VaiTro=%s, SoDienThoai=%s
        WHERE NhanVienID=%s
    """, (ten, vaitro, sdt, id))
    db.commit()
    db.close()
    return jsonify({'message': 'Cập nhật thành công'})

# ❌ Xóa nhân viên
@employee_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM nhanvien WHERE NhanVienID=%s", (id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Xóa nhân viên thành công'})
