# init_db.py
from app import db, create_app
from models import User, Student
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# recreate DB
db.drop_all()
db.create_all()

# create default admin
admin = User(username="admin", password_hash=generate_password_hash("admin123"))
db.session.add(admin)

# Danh sách sinh viên Việt Nam mẫu phong phú
students_data = [
    {"name": "Đào Đức Mạnh", "usn": "SV22001", "branch": "Công nghệ thông tin", "year": 4, "email": "manh.dao@donga.edu.vn", "phone": "0987654321"},
    {"name": "Nguyễn Văn An", "usn": "SV22002", "branch": "Kỹ thuật phần mềm", "year": 3, "email": "an.nguyen@donga.edu.vn", "phone": "0912345678"},
    {"name": "Trần Thị Mai Phương", "usn": "SV22003", "branch": "Trí tuệ nhân tạo", "year": 2, "email": "phuong.tran@donga.edu.vn", "phone": "0905123456"},
    {"name": "Lê Hoàng Nam", "usn": "SV22004", "branch": "An toàn thông tin", "year": 4, "email": "nam.le@donga.edu.vn", "phone": "0934567890"},
    {"name": "Phạm Minh Quân", "usn": "SV22005", "branch": "Công nghệ thông tin", "year": 1, "email": "quan.pham@donga.edu.vn", "phone": "0978112233"},
    {"name": "Vũ Phương Thảo", "usn": "SV22006", "branch": "Hệ thống thông tin", "year": 3, "email": "thao.vu@donga.edu.vn", "phone": "0969887766"},
    {"name": "Đặng Quốc Huy", "usn": "SV22007", "branch": "Kỹ thuật phần mềm", "year": 2, "email": "huy.dang@donga.edu.vn", "phone": "0945667788"},
    {"name": "Bùi Thị Thu Trang", "usn": "SV22008", "branch": "Quản trị kinh doanh", "year": 4, "email": "trang.bui@donga.edu.vn", "phone": "0918990011"},
    {"name": "Hoàng Đình Trọng", "usn": "SV22009", "branch": "Công nghệ thông tin", "year": 3, "email": "trong.hoang@donga.edu.vn", "phone": "0982334455"},
    {"name": "Ngô Thanh Tùng", "usn": "SV22010", "branch": "Trí tuệ nhân tạo", "year": 2, "email": "tung.ngo@donga.edu.vn", "phone": "0931223344"},
    {"name": "Dương Gia Bảo", "usn": "SV22011", "branch": "An toàn thông tin", "year": 1, "email": "bao.duong@donga.edu.vn", "phone": "0977889900"},
    {"name": "Lý Ngọc Ánh", "usn": "SV22012", "branch": "Kỹ thuật phần mềm", "year": 4, "email": "anh.ly@donga.edu.vn", "phone": "0903445566"},
    {"name": "Đỗ Quang Hải", "usn": "SV22013", "branch": "Công nghệ thông tin", "year": 2, "email": "hai.do@donga.edu.vn", "phone": "0915667788"},
    {"name": "Hồ Khánh Linh", "usn": "SV22014", "branch": "Hệ thống thông tin", "year": 3, "email": "linh.ho@donga.edu.vn", "phone": "0944112233"},
    {"name": "Võ Minh Khang", "usn": "SV22015", "branch": "Kỹ thuật phần mềm", "year": 1, "email": "khang.vo@donga.edu.vn", "phone": "0989556677"},
    {"name": "Phan Hoài Thương", "usn": "SV22016", "branch": "Quản trị kinh doanh", "year": 4, "email": "thuong.phan@donga.edu.vn", "phone": "0936778899"},
    {"name": "Mai Văn Phúc", "usn": "SV22017", "branch": "Công nghệ thông tin", "year": 2, "email": "phuc.mai@donga.edu.vn", "phone": "0972331122"},
    {"name": "Trịnh Mỹ Duyên", "usn": "SV22018", "branch": "Trí tuệ nhân tạo", "year": 3, "email": "duyen.trinh@donga.edu.vn", "phone": "0908443322"},
    {"name": "Đinh Công Thành", "usn": "SV22019", "branch": "An toàn thông tin", "year": 4, "email": "thanh.dinh@donga.edu.vn", "phone": "0961225588"},
    {"name": "Cao Thị Tuyết Nhung", "usn": "SV22020", "branch": "Hệ thống thông tin", "year": 1, "email": "nhung.cao@donga.edu.vn", "phone": "0948991144"},
    {"name": "Lương Tiến Đạt", "usn": "SV22021", "branch": "Kỹ thuật phần mềm", "year": 3, "email": "dat.luong@donga.edu.vn", "phone": "0919337722"},
    {"name": "Trương Bảo Ngọc", "usn": "SV22022", "branch": "Công nghệ thông tin", "year": 2, "email": "ngoc.truong@donga.edu.vn", "phone": "0984119933"},
    {"name": "Vũ Đình Duy", "usn": "SV22023", "branch": "Trí tuệ nhân tạo", "year": 1, "email": "duy.vu@donga.edu.vn", "phone": "0938552211"},
    {"name": "Chu Kim Ngân", "usn": "SV22024", "branch": "Quản trị kinh doanh", "year": 4, "email": "ngan.chu@donga.edu.vn", "phone": "0975664422"},
    {"name": "Tạ Quang Dũng", "usn": "SV22025", "branch": "Công nghệ thông tin", "year": 3, "email": "dung.ta@donga.edu.vn", "phone": "0909118833"}
]

for item in students_data:
    s = Student(
        name=item["name"],
        usn=item["usn"],
        branch=item["branch"],
        year=item["year"],
        email=item["email"],
        phone=item["phone"]
    )
    db.session.add(s)

db.session.commit()
print(f"Cơ sở dữ liệu đã được khởi tạo thành công với tài khoản admin và {len(students_data)} hồ sơ sinh viên Việt Nam!")
