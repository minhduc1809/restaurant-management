CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;

-- XÓA TRƯỚC (NẾU ĐÃ CÓ)
DROP TABLE IF EXISTS chitiet_hoadon, hoadon, monan, banan, khachhang, nhanvien, lichlam, nguyenlieu, luotdatban, phanhoi;

-- 1. BẢNG KHÁCH HÀNG
CREATE TABLE khachhang (
    KhachHangID INT AUTO_INCREMENT PRIMARY KEY,
    HoTenKhachHang VARCHAR(100),
    SoDienThoai VARCHAR(20)
);

-- 2. BẢNG NHÂN VIÊN
CREATE TABLE nhanvien (
    NhanVienID INT AUTO_INCREMENT PRIMARY KEY,
    HoTenNhanVien VARCHAR(100),
    VaiTro VARCHAR(50),
    SoDienThoai VARCHAR(20)
);

-- 3. BẢNG LỊCH LÀM
CREATE TABLE lichlam (
    LichLamID INT AUTO_INCREMENT PRIMARY KEY,
    TenNhanVien VARCHAR(100),
    SoGioLam INT,
    Ca VARCHAR(20),
    Ngay DATE
);

-- 4. BẢNG MÓN ĂN
CREATE TABLE monan (
    MonAnID INT AUTO_INCREMENT PRIMARY KEY,
    TenMonAn VARCHAR(100),
    Gia DECIMAL(10, 2),
    Loai VARCHAR(50)
);

-- 5. BẢNG HÓA ĐƠN
CREATE TABLE hoadon (
    HoaDonID INT AUTO_INCREMENT PRIMARY KEY,
    ThoiDiemTao DATETIME,
    HoTenKhachHang VARCHAR(100),
    TongTien DECIMAL(10, 2)
);

-- 6. BẢNG CHI TIẾT HÓA ĐƠN
CREATE TABLE chitiet_hoadon (
    HoaDonID INT,
    MonAnID INT,
    SoLuongMonAn INT,
    Gia DECIMAL(10, 2),
    ThanhTien DECIMAL(10, 2),
    PRIMARY KEY (HoaDonID, MonAnID),
    FOREIGN KEY (HoaDonID) REFERENCES hoadon(HoaDonID) ON DELETE CASCADE,
    FOREIGN KEY (MonAnID) REFERENCES monan(MonAnID)
);

-- 7. BẢNG BÀN ĂN
CREATE TABLE banan (
    BanAnID INT AUTO_INCREMENT PRIMARY KEY,
    SoBan INT,
    TrangThai VARCHAR(50)
);

-- 8. BẢNG LƯỢT ĐẶT BÀN
CREATE TABLE luotdatban (
    LuotDatBanID INT AUTO_INCREMENT PRIMARY KEY,
    TenKhachHang VARCHAR(100),
    ThoiGianDat DATETIME,
    SoBan INT
);

-- 9. BẢNG PHẢN HỒI
CREATE TABLE phanhoi (
    PhanHoiID INT AUTO_INCREMENT PRIMARY KEY,
    KhachHangID INT,
    NoiDung TEXT,
    FOREIGN KEY (KhachHangID) REFERENCES khachhang(KhachHangID)
);

-- 10. BẢNG NGUYÊN LIỆU
CREATE TABLE nguyenlieu (
    NguyenLieuID INT AUTO_INCREMENT PRIMARY KEY,
    TenNguyenLieu VARCHAR(100),
    SoLuongTonKho INT,
    SoLuongDaTieuThu INT,
    TrangThai VARCHAR(50)
);
CREATE TABLE taikhoan (
    TaiKhoanID INT AUTO_INCREMENT PRIMARY KEY,
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(100) NOT NULL,
    VaiTro VARCHAR(50), -- VD: admin, nhanvien
    NhanVienID INT,      -- Nếu liên kết với bảng nhanvien
    FOREIGN KEY (NhanVienID) REFERENCES nhanvien(NhanVienID)
);
INSERT INTO taikhoan (TenDangNhap, MatKhau, VaiTro) VALUES ('admin', 'admin123', 'admin');

