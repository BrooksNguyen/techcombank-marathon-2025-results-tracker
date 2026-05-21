#!/bin/bash
# Script tự động hoá cài đặt MySQL và chạy dự án (Humanized)

set -e

echo "================================================="
echo " 🏃‍♂️ TECHCOMBANK MARATHON 2025 - AUTO SETUP 🚀 "
echo "================================================="

# Thêm đường dẫn mặc định của Homebrew trên Mac (M1/M2/M3 và Intel) vào PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo -e "\n🔍 Bắt đầu kiểm tra môi trường của bạn..."

# Kiểm tra python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Rất tiếc! Máy bạn chưa có Python. Vui lòng cài Python trước nha."
    exit 1
fi

# Cài đặt thư viện Python
echo -e "\n📦 Đang cài đặt thư viện cần thiết (nếu có thiếu)..."
pip install -r requirements.txt || pip3 install -r requirements.txt

# Kiểm tra Homebrew
if ! command -v brew &> /dev/null; then
    echo -e "\n❌ Chà, máy bạn chưa có Homebrew. Để mình tự cài MySQL cho mượt thì cần có Homebrew."
    echo "Bạn có thể chạy lệnh này trên terminal để cài Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Kiểm tra MySQL
if ! command -v mysql &> /dev/null; then
    echo -e "\n⏳ Chưa thấy MySQL trên máy. Đang gọi Homebrew tới tải về cho bạn..."
    echo " Quá trình này có thể tốn vài phút. Pha tách cà phê nhé ☕..."
    brew install mysql
else
    echo -e "\n✅ Tuyệt vời! MySQL đã sẵn sàng."
fi

# Khởi động MySQL
echo -e "\n🚀 Đang đánh thức dịch vụ MySQL..."
brew services start mysql

echo "⏳ Đang đợi 5 giây cho hệ thống database ổn định..."
sleep 5

echo -e "\n🎉 Mọi thứ đã hoàn tất! Bắt đầu chạy dự án ngay đây...\n"
python main.py || python3 main.py
