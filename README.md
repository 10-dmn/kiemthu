# 📘 BÁO CÁO ĐỒ ÁN: KIỂM THỬ HỆ THỐNG QUẢN LÝ HỒ SƠ SINH VIÊN (FLASK & SELENIUM)
### Môn học: Kiểm thử phần mềm (Software Testing / QA)
**Nhóm thực hiện**: Nhóm 21  
**Sinh viên**: Đào Đức Mạnh  
**Trường**: Đại học Đông Á  

---

## 📑 Mục lục
1. [Giới thiệu tổng quan](#giới-thiệu-tổng-quan)
2. [Kiến trúc công nghệ](#kiến-trúc-công-nghệ)
3. [Nơi lưu trữ dữ liệu sinh viên](#nơi-lưu-trữ-dữ-liệu-sinh-viên)
4. [Mô hình kiểm thử (V-Model & POM)](#mô-hình-kiểm-thử-v-model--pom)
5. [Bảng đặc tả Test Cases (TC01 - TC09)](#bảng-đặc-tả-test-cases-tc01---tc09)
6. [Kỹ thuật kiểm thử áp dụng](#kỹ-thuật-kiểm-thử-áp-dụng)
7. [Hướng dẫn cài đặt & Thực thi](#hướng-dẫn-cài-đặt--thực-thi)
8. [Báo cáo kết quả kiểm thử](#báo-cáo-kết-quả-kiểm-thử)

---

## 📘 Giới thiệu tổng quan
Hệ thống **Quản lý Hồ sơ Sinh viên (Student Management System - SMS)** là một ứng dụng web xây dựng trên nền tảng **Python Flask** kết hợp cơ sở dữ liệu **SQLite**. Hệ thống đi kèm một bộ khung kiểm thử tự động hóa hoàn chỉnh (**Selenium WebDriver + PyTest**) nhằm xác minh tính đúng đắn của toàn bộ các chức năng CRUD, kiểm tra tính toàn vẹn dữ liệu và bắt lỗi validation.

### Các chức năng chính của hệ thống:
* 🔐 **Xác thực Admin**: Đăng nhập/Đăng xuất bảo vệ các trang quản trị.
* 📋 **Quản lý danh sách sinh viên**: Xem danh sách 25+ sinh viên Việt Nam, widget thống kê KPI (tổng số sinh viên, số ngành đào tạo).
* 🔍 **Tìm kiếm & Lọc hồ sơ**: Tìm kiếm theo Tên hoặc Mã sinh viên (MSSV); lọc theo Chuyên ngành và Năm học.
* ➕ **Thêm mới sinh viên**: Có validation chặt chẽ (bắt buộc nhập, kiểm tra trùng mã SV, định dạng email).
* ✏️ **Chỉnh sửa hồ sơ**: Cập nhật thông tin sinh viên linh hoạt.
* 🗑️ **Xóa hồ sơ an toàn**: Hộp thoại cảnh báo JavaScript Confirm trước khi xóa.
* 👁️ **Xem chi tiết hồ sơ**: Trang Profile thẻ sinh viên hiện đại.

---

## 🧰 Kiến trúc công nghệ
* **Backend**: Python 3.10+, Flask 2.2.5, Flask-SQLAlchemy, Werkzeug Security
* **Frontend**: HTML5, Modern CSS3 (Grid/Flexbox, Glassmorphism, Responsive), Vanilla JS
* **Cơ sở dữ liệu**: SQLite (`instance/students.db`)
* **Framework kiểm thử**: PyTest 7.4+
* **Tự động hóa trình duyệt**: Selenium WebDriver 4.x (Tự động quản lý driver qua Selenium Manager)
* **Báo cáo kiểm thử**: pytest-html (Sinh báo cáo HTML tự động)

---

## 💾 Nơi lưu trữ dữ liệu sinh viên
1. **File Database thực tế**: Lưu tại thư mục `instance/students.db` (file nhị phân SQLite).
2. **File khởi tạo & nạp dữ liệu mẫu**: Lưu tại file `init_db.py`.
   - File này chứa sẵn **25 hồ sơ sinh viên Việt Nam** với đầy đủ thông tin: Họ tên tiếng Việt, Mã sinh viên (SV22001 - SV22025), các chuyên ngành thực tế (Công nghệ thông tin, Kỹ thuật phần mềm, Trí tuệ nhân tạo, An toàn thông tin, Hệ thống thông tin, Quản trị kinh doanh), Năm học (1-4), Email và Số điện thoại.
   - Để làm mới hoặc reset dữ liệu ban đầu, chỉ cần chạy:
     ```powershell
     python init_db.py
     ```

---

## 📐 Mô hình kiểm thử (V-Model & POM)
1. **Mô hình chữ V (V-Model)**: Selenium WebDriver thực thi kiểm thử chức năng ở nhánh bên phải (System Testing & Acceptance Testing), đảm bảo phần mềm thỏa mãn đúng các đặc tả yêu cầu ở nhánh bên trái.
2. **Mô hình Page Object Model (POM)**:
   - `tests/pages/login_page.py`: Đóng gói các hành vi của trang Đăng nhập.
   - `tests/pages/dashboard_page.py`: Đóng gói các hành vi của bảng điều khiển sinh viên.
   - `tests/test_student_crud.py`: Tập trung kịch bản kiểm thử, độc lập với cấu trúc HTML.

---

## 🧪 Bảng đặc tả Test Cases (TC01 - TC09)

| Mã TC | Tên kịch bản | Kỹ thuật kiểm thử | Đầu vào kiểm thử | Kết quả mong đợi | Trạng thái |
|:---:|:---|:---|:---|:---|:---:|
| **TC01** | Đăng nhập thành công | Positive Testing | `admin` / `admin123` | Chuyển hướng vào trang `/dashboard` | **PASSED** |
| **TC02** | Đăng nhập thất bại | Negative Testing | `admin` / `wrongpassword` | Ở lại trang `/login`, hiển thị flash lỗi | **PASSED** |
| **TC03** | Thêm sinh viên mới | Functional Testing | Nhập đầy đủ thông tin hợp lệ (`SVTEST01`) | Hồ sơ xuất hiện trong bảng sinh viên | **PASSED** |
| **TC04** | Tìm kiếm sinh viên | Search / Filter Testing | Tìm từ khóa `SVTEST01` | Bảng chỉ hiển thị sinh viên khớp | **PASSED** |
| **TC05** | Sửa hồ sơ sinh viên | Functional CRUD | Sửa tên thành `Nguyễn Văn Kiểm Thử (Đã Cập Nhật)` | Bảng cập nhật tên mới thành công | **PASSED** |
| **TC06a**| Hủy thao tác xóa | GUI / Dialog Testing | Bấm Xóa $\rightarrow$ Chọn **Cancel** trên Alert | Hồ sơ sinh viên **không bị xóa** | **PASSED** |
| **TC06** | Xác nhận xóa sinh viên | Functional CRUD | Bấm Xóa $\rightarrow$ Chọn **OK** trên Alert | Hồ sơ sinh viên bị xóa khỏi bảng | **PASSED** |
| **TC07** | Email sai định dạng | **Phân vùng tương đương (EP)** | Email: `email_khong_hop_le_chua_domain` | Báo lỗi `Định dạng email không hợp lệ` | **PASSED** |
| **TC08** | Trùng mã sinh viên | **Kiểm thử biên / Ràng buộc (BVA)** | Nhập MSSV `SV22001` (đã có) | Báo lỗi `Mã sinh viên này đã tồn tại` | **PASSED** |
| **TC09** | Để trống trường bắt buộc | **Phân vùng tương đương (EP)** | Bỏ trống Họ tên và Mã sinh viên | Báo lỗi `Vui lòng điền đầy đủ...` | **PASSED** |

---

## 🔬 Kỹ thuật kiểm thử áp dụng (Đạt chuẩn điểm 9 - 10)
1. **Phân vùng tương đương (Equivalence Partitioning)**:
   - Phân chia tập dữ liệu Email thành:
     - *Vùng hợp lệ*: `sinhvien@donga.edu.vn` (chứa `@` và tên miền hợp lệ).
     - *Vùng không hợp lệ*: chuỗi ký tự thông thường, thiếu `@`, thiếu đuôi tên miền.
   - Phân chia trường bắt buộc thành:
     - *Vùng hợp lệ*: chuỗi có nội dung.
     - *Vùng không hợp lệ*: chuỗi rỗng / chỉ có khoảng trắng.
2. **Kiểm thử giá trị biên & Ràng buộc toàn vẹn (Boundary & Constraint Testing)**:
   - Ràng buộc tính duy nhất của Mã sinh viên (Unique constraint): Kiểm tra hệ thống khi người dùng nhập mã đã có sẵn trong cơ sở dữ liệu.
   - Ràng buộc năm học: Giới hạn từ 1 đến 8.
3. **Kiểm thử giao diện & Trạng thái (UI & State Verification)**:
   - Bắt tương tác với hộp thoại JavaScript Alert (`accept()` và `dismiss()`).
   - Kiểm tra các thông báo Flash với màu sắc tương ứng (`success`, `danger`, `info`).

---

## 🚀 Hướng dẫn cài đặt & Thực thi

### 1. Khởi tạo lại dữ liệu mẫu
```powershell
.\venv\Scripts\python.exe init_db.py
```

### 2. Chạy ứng dụng web Flask
```powershell
.\venv\Scripts\python.exe app.py
```
👉 Mở trình duyệt truy cập: **http://127.0.0.1:5000**  
*(Tài khoản đăng nhập: `admin` / `admin123`)*

### 3. Chạy toàn bộ kiểm thử tự động
```powershell
.\venv\Scripts\pytest -v --html=tests_reports/report.html --self-contained-html
```
Hoặc nhấp đúp chạy trực tiếp file:
```powershell
.\run_tests.bat
```

---

## 📊 Báo cáo kết quả kiểm thử
* Báo cáo HTML trực quan: `tests_reports/report.html`
* Chụp ảnh màn hình khi có lỗi: `tests_reports/screenshots/` (được cấu hình tự động nhúng vào báo cáo HTML khi có test case thất bại).
