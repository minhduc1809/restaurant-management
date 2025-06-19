from flask import Blueprint, request, jsonify
from db_config import get_db_connection

ingredient_bp = Blueprint('ingredient_bp', __name__)

# 📋 Lấy danh sách nguyên liệu
@ingredient_bp.route('/', methods=['GET'])
def get_ingredients():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM nguyenlieu")
    ingredients = cursor.fetchall()
    db.close()
    return jsonify(ingredients)

# ➕ Thêm nguyên liệu
@ingredient_bp.route('/', methods=['POST'])
def add_ingredient():
    data = request.json
    ten = data.get('TenNguyenLieu')
    soluong = data.get('SoLuongTonKho', 0)
    tieu_thu = data.get('SoLuongDaTieuThu', 0)
    trangthai = data.get('TrangThai', 'Còn nhiều')

    if not ten:
        return jsonify({'message': 'Thiếu tên nguyên liệu'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO nguyenlieu (TenNguyenLieu, SoLuongTonKho, SoLuongDaTieuThu, TrangThai)
        VALUES (%s, %s, %s, %s)
    """, (ten, soluong, tieu_thu, trangthai))
    db.commit()
    db.close()
    return jsonify({'message': 'Thêm nguyên liệu thành công'}), 201

# ✏️ Sửa nguyên liệu
@ingredient_bp.route('/<int:id>', methods=['PUT'])
def update_ingredient(id):
    data = request.json
    ten = data.get('TenNguyenLieu')
    soluong = data.get('SoLuongTonKho')
    tieu_thu = data.get('SoLuongDaTieuThu')
    trangthai = data.get('TrangThai')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE nguyenlieu
        SET TenNguyenLieu=%s, SoLuongTonKho=%s, SoLuongDaTieuThu=%s, TrangThai=%s
        WHERE NguyenLieuID=%s
    """, (ten, soluong, tieu_thu, trangthai, id))
    db.commit()
    db.close()
    return jsonify({'message': 'Cập nhật thành công'})

# ❌ Xóa nguyên liệu
@ingredient_bp.route('/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM nguyenlieu WHERE NguyenLieuID=%s", (id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Xóa thành công'})
