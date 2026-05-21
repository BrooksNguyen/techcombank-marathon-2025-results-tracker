import pandas as pd
import sys
import os
from database import (
    setup_database, 
    insert_marathon_data, 
    insert_bib_data,
    fetch_all_data,
    search_runner_by_bib
)
from generator import generate_bib_data

def init_system():
    """Khởi tạo hệ thống và nạp dữ liệu"""
    print("Đang khởi tạo Hệ thống Cơ sở dữ liệu...")
    if not setup_database():
        print("DỪNG CHƯƠNG TRÌNH: Khởi tạo database thất bại.")
        sys.exit(1)

    data_file = 'marathon_data.csv'
    if os.path.exists(data_file):
        try:
            df_input = pd.read_csv(data_file)
            data_records = list(df_input.itertuples(index=False, name=None))
            insert_marathon_data(data_records)
        except Exception as e:
            print(f"Có lỗi khi đọc file CSV thống kê: {e}")
            
    bib_file = 'bib_data.csv'
    # Đảm bảo tạo file mới nếu file cũ không có tên
    if os.path.exists(bib_file):
        df_check = pd.read_csv(bib_file)
        if 'runner_name' not in df_check.columns:
            os.remove(bib_file)
            
    if not os.path.exists(bib_file):
        print("Đang sinh dữ liệu BIB ngẫu nhiên kèm tên VĐV (Hệ thống mô phỏng)...")
        generate_bib_data(bib_file)
        
    if os.path.exists(bib_file):
        try:
            df_bib = pd.read_csv(bib_file)
            bib_records = list(df_bib.itertuples(index=False, name=None))
            insert_bib_data(bib_records)
        except Exception as e:
            print(f"Có lỗi khi nạp dữ liệu BIB: {e}")
            
    print("Hoàn tất quá trình khởi tạo hệ thống.\n")

def print_statistics():
    """In bảng thống kê tổng quan"""
    records = fetch_all_data()
    if records:
        df_output = pd.DataFrame(records)
        df_output.rename(columns={
            'distance': 'Cự ly',
            'registered_runners': 'Số người đăng ký',
            'finished_runners': 'Số người hoàn thành',
            'completion_rate': 'Tỷ lệ hoàn thành (%)'
        }, inplace=True)
        
        print("\n" + "=" * 65)
        print(" BẢNG THỐNG KÊ CHI TIẾT TECHCOMBANK MARATHON 2025")
        print("=" * 65)
        print(df_output.to_string(index=False))
        print("=" * 65 + "\n")
    else:
        print("\nKhông có dữ liệu thống kê để hiển thị.\n")

def interactive_search():
    """Giao diện tra cứu tương tác"""
    while True:
        print("\n--- TRÌNH TRA CỨU KẾT QUẢ ---")
        bib_input = input("Nhập số BIB (Gõ 'q' để thoát): ").strip()
        
        if bib_input.lower() == 'q':
            break
            
        if not bib_input.isdigit() or len(bib_input) != 5:
            print("\nSố BIB không hợp lệ. Vui lòng nhập số khác (Yêu cầu: 5 chữ số).")
            continue
            
        result = search_runner_by_bib(bib_input)
        
        if result:
            print("\nKẾT QUẢ TRA CỨU:")
            print(f"Số BIB     : {bib_input}")
            print(f"Họ và Tên  : {result['runner_name']}")
            print(f"Cự ly      : {result['distance']}")
            print(f"Thời gian  : {result['finishing_time']}")
            print(f"Thứ hạng   : {result['rank_position']} / {result['total_runners']}")
        else:
            print("\nSố BIB không hợp lệ hoặc không tồn tại. Vui lòng nhập số khác.")

def main():
    print("============================================================")
    print("HỆ THỐNG QUẢN LÝ VÀ TRA CỨU TECHCOMBANK MARATHON HCMC 2025")
    print("============================================================\n")
    
    init_system()
    
    while True:
        print("\nMENU CHÍNH:")
        print("1. Xem thống kê tổng quan")
        print("2. Tra cứu kết quả vận động viên")
        print("3. Thoát ")
        
        choice = input("Vui lòng chọn chức năng (1-3): ").strip()
        
        if choice == '1':
            print_statistics()
        elif choice == '2':
            interactive_search()
        elif choice == '3':
            print("\n" + "═" * 70)
            print("                 TECHCOMBANK HCMC MARATHON 2025")
            print("═" * 70)
            print(" Xin chân thành cảm ơn các Vận động viên đã nỗ lực cống hiến hết mình.")
            print("      Hẹn gặp lại tất cả các bạn tại vạch xuất phát mùa giải 2026!")
            print("═" * 70 + "\n")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

if __name__ == "__main__":
    main()
