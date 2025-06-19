import mysql.connector

# Cấu hình kết nối MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='lethithao082006',          # ← Đổi thành mật khẩu MySQL thật của bạn
        database='restaurant_db'    # ← Đổi thành tên DB thật đã tạo
    )
if __name__ == "__main__":
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("✅ Kết nối MySQL thành công!")
        else:
            print("❌ Không thể kết nối đến MySQL.")
    except mysql.connector.Error as err:
        print(f"❌ Lỗi khi kết nối: {err}")
