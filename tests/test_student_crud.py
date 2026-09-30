# tests/test_student_crud.py
import time
import pytest
from tests.pages.login_page import LoginPage
from tests.pages.dashboard_page import DashboardPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================================================================
# PHẦN 1: KIỂM THỬ XÁC THỰC & ĐĂNG NHẬP (AUTHENTICATION TESTS)
# ==============================================================================

def test_tc02_login_failure(driver, base_url):
    """
    TC02: Đăng nhập thất bại (Negative Testing)
    Mục đích: Đảm bảo hệ thống từ chối đăng nhập khi sai thông tin và hiển thị thông báo lỗi.
    """
    driver.get(base_url + "/logout")
    lp = LoginPage(driver, base_url)
    lp.load()
    lp.login("admin", "wrongpassword123")
    
    # Kiểm tra vẫn ở trang login và có flash message lỗi
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.danger")))
    flash = lp.get_flash()
    assert any(msg in flash for msg in ["không chính xác", "Invalid username or password"])
    assert "/login" in driver.current_url

def test_tc01_login_success(driver, base_url):
    """
    TC01: Đăng nhập thành công (Positive Testing)
    Mục đích: Xác thực tài khoản hợp lệ được chuyển hướng vào Dashboard.
    """
    lp = LoginPage(driver, base_url)
    lp.load()
    lp.login("admin", "admin123")
    
    WebDriverWait(driver, 4).until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url


# ==============================================================================
# PHẦN 2: KIỂM THỬ CHỨC NĂNG CRUD CƠ BẢN (CORE FUNCTIONAL TESTS)
# ==============================================================================

def test_tc03_add_student(driver, base_url):
    """
    TC03: Thêm mới hồ sơ sinh viên hợp lệ
    Mục đích: Đảm bảo có thể tạo mới hồ sơ sinh viên và hiển thị đúng trên bảng.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    dp.click_add()
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").send_keys("Nguyễn Văn Kiểm Thử")
    driver.find_element(By.NAME, "usn").send_keys("SVTEST01")
    driver.find_element(By.NAME, "branch").send_keys("Kỹ thuật phần mềm")
    driver.find_element(By.NAME, "year").send_keys("3")
    driver.find_element(By.NAME, "email").send_keys("kiemthu.nguyen@donga.edu.vn")
    driver.find_element(By.NAME, "phone").send_keys("0912345999")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 3).until(EC.url_contains("/dashboard"))
    rows = dp.get_rows()
    assert any("SVTEST01" in r.text for r in rows)

def test_tc04_search_student(driver, base_url):
    """
    TC04: Tìm kiếm và lọc hồ sơ sinh viên
    Mục đích: Tìm kiếm theo mã USN / Họ tên, kết quả trả về đúng bản ghi mong muốn.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    dp.search("SVTEST01")
    
    WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.students-table tbody tr")))
    rows = dp.get_rows()
    assert len(rows) >= 1
    assert "SVTEST01" in rows[0].text

def test_tc05_edit_student(driver, base_url):
    """
    TC05: Chỉnh sửa hồ sơ sinh viên
    Mục đích: Cập nhật thông tin sinh viên và kiểm tra dữ liệu thay đổi trên bảng.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    
    # Tìm hàng chứa SVTEST01
    rows = dp.get_rows()
    target = None
    for r in rows:
        if "SVTEST01" in r.text:
            target = r
            break
    assert target is not None, "Không tìm thấy hồ sơ SVTEST01 để sửa"
    
    # Click nút Sửa (Edit)
    edit_link = target.find_element(By.CSS_SELECTOR, "a.btn-edit, a[href*='student/edit']")
    edit_link.click()
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.NAME, "name")))
    name_field = driver.find_element(By.NAME, "name")
    name_field.clear()
    name_field.send_keys("Nguyễn Văn Kiểm Thử (Đã Cập Nhật)")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 3).until(EC.url_contains("/dashboard"))
    rows = dp.get_rows()
    assert any("Nguyễn Văn Kiểm Thử (Đã Cập Nhật)" in r.text for r in rows)

def test_tc06a_cancel_delete_student(driver, base_url):
    """
    TC06a: Hủy thao tác xóa hồ sơ sinh viên (Cancel Confirmation)
    Mục đích: Khi bấm Xóa nhưng chọn Cancel trên popup JS confirm, hồ sơ vẫn còn nguyên.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    rows = dp.get_rows()
    target = None
    for r in rows:
        if "SVTEST01" in r.text:
            target = r
            break
    assert target is not None, "Không tìm thấy hồ sơ SVTEST01"
    
    delete_btn = target.find_element(By.CSS_SELECTOR, "form button[type='submit'], .btn-delete")
    delete_btn.click()

    # Bấm Hủy (Dismiss/Cancel alert)
    alert = driver.switch_to.alert
    alert.dismiss()

    # Xác nhận hồ sơ vẫn còn trong bảng
    rows_after = dp.get_rows()
    assert any("SVTEST01" in r.text for r in rows_after)

def test_tc06_delete_student(driver, base_url):
    """
    TC06: Xác nhận xóa hồ sơ sinh viên (Accept Confirmation)
    Mục đích: Khi bấm Xóa và xác nhận OK trên popup JS confirm, hồ sơ bị xóa khỏi bảng.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    rows = dp.get_rows()
    target = None
    for r in rows:
        if "SVTEST01" in r.text:
            target = r
            break
    assert target is not None, "Không tìm thấy hồ sơ SVTEST01"
    
    delete_btn = target.find_element(By.CSS_SELECTOR, "form button[type='submit'], .btn-delete")
    delete_btn.click()

    # Bấm Đồng ý (Accept/OK alert)
    alert = driver.switch_to.alert
    alert.accept()

    WebDriverWait(driver, 3).until(EC.url_contains("/dashboard"))
    rows = dp.get_rows()
    assert not any("SVTEST01" in r.text for r in rows)


# ==============================================================================
# PHẦN 3: KIỂM THỬ NÂNG CAO - PHÂN VÙNG TƯƠNG ĐƯƠNG & GIÁ TRỊ BIÊN (ADVANCED QA)
# ==============================================================================

def test_tc07_add_student_invalid_email(driver, base_url):
    """
    TC07: Phân vùng tương đương (Equivalence Partitioning) - Kiểm tra Email sai định dạng
    Mục đích: Nhập email không hợp lệ (thiếu ký tự @ và tên miền), hệ thống phải bắt lỗi
              và ngăn chặn lưu hồ sơ.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    dp.click_add()
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").send_keys("Sinh Viên Test Email")
    driver.find_element(By.NAME, "usn").send_keys("SV_EMAIL_BAD")
    driver.find_element(By.NAME, "branch").send_keys("Công nghệ thông tin")
    driver.find_element(By.NAME, "year").send_keys("2")
    
    # Nhập email sai định dạng (không có @ hoặc domain)
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys("email_khong_hop_le_chua_domain")
    
    # Tắt HTML5 validation để kiểm thử kiểm tra toàn vẹn ở tầng Backend (Server Validation)
    driver.execute_script("document.querySelector('form').noValidate = true;")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Kiểm tra flash message báo lỗi email
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.danger")))
    flash_text = driver.find_element(By.CSS_SELECTOR, ".flash.danger").text
    assert any(kw in flash_text for kw in ["email không hợp lệ", "Invalid email"])

def test_tc08_add_student_duplicate_usn(driver, base_url):
    """
    TC08: Kiểm thử ràng buộc duy nhất (Uniqueness Constraint) - Trùng mã sinh viên (Duplicate USN)
    Mục đích: Thêm sinh viên với mã MSSV đã tồn tại trong hệ thống (SV22001 - Đào Đức Mạnh),
              hệ thống phải từ chối và cảnh báo trùng lặp.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    dp.click_add()
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").send_keys("Sinh Viên Trùng Mã")
    # SV22001 là mã đã có sẵn trong cơ sở dữ liệu
    driver.find_element(By.NAME, "usn").send_keys("SV22001")
    driver.find_element(By.NAME, "branch").send_keys("Trí tuệ nhân tạo")
    driver.find_element(By.NAME, "year").send_keys("1")
    driver.find_element(By.NAME, "email").send_keys("trungma@donga.edu.vn")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Kiểm tra flash message cảnh báo trùng mã
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.danger")))
    flash_text = driver.find_element(By.CSS_SELECTOR, ".flash.danger").text
    assert any(kw in flash_text for kw in ["đã tồn tại", "already exists"])

def test_tc09_add_student_empty_required_fields(driver, base_url):
    """
    TC09: Phân vùng tương đương (Equivalence Partitioning) - Để trống các trường bắt buộc
    Mục đích: Bỏ trống trường Họ tên và MSSV, gửi form, hệ thống phía server phải từ chối
              và hiển thị yêu cầu nhập đầy đủ.
    """
    dp = DashboardPage(driver, base_url)
    dp.load()
    dp.click_add()
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.NAME, "name")))
    # Không nhập Name và USN
    driver.find_element(By.NAME, "branch").send_keys("Công nghệ thông tin")
    driver.find_element(By.NAME, "year").send_keys("2")
    
    # Bỏ qua client validation để kiểm thử kiểm tra an toàn dữ liệu phía Backend
    driver.execute_script("document.querySelector('form').noValidate = true;")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Kiểm tra flash message thông báo thiếu trường bắt buộc
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.danger")))
    flash_text = driver.find_element(By.CSS_SELECTOR, ".flash.danger").text
    assert any(kw in flash_text for kw in ["đầy đủ", "required", "bắt buộc"])
