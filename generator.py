import numpy as np
import pandas as pd
import random
import os

# Danh sách tên tiếng Việt phổ biến để sinh ngẫu nhiên
HO_LIST = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
DEM_LIST = ["Thị", "Văn", "Hữu", "Đức", "Ngọc", "Minh", "Xuân", "Quang", "Quốc", "Đình", "Thanh", "Bảo", "Gia", "Hoài", "Tuấn", "Thành", "Thu", "Hồng"]
TEN_LIST = ["Anh", "An", "Bảo", "Bình", "Cường", "Dũng", "Đạt", "Đức", "Giang", "Hải", "Hiếu", "Hoàng", "Huy", "Hùng", "Hương", "Hoa", "Khoa", "Kiên", "Linh", "Long", "Lộc", "Minh", "Nam", "Ngọc", "Phong", "Phương", "Quân", "Quang", "Sơn", "Tâm", "Thảo", "Thắng", "Thành", "Tiến", "Trang", "Tuấn", "Tú", "Vinh", "Việt", "Yến"]

def generate_vietnamese_name():
    """Tạo ngẫu nhiên một tên tiếng Việt hợp lệ"""
    ho = random.choice(HO_LIST)
    dem = random.choice(DEM_LIST)
    ten = random.choice(TEN_LIST)
    return f"{ho} {dem} {ten}"

def generate_bib_data(output_file='bib_data.csv'):
    """Sinh dữ liệu BIB kèm tên tiếng Việt ngẫu nhiên"""
    np.random.seed(42) # Đảm bảo random ra kết quả cố định mỗi lần chạy
    random.seed(42)
    
    # Cấu trúc: (Cự ly, Tiền tố, Số người hoàn thành, Trung bình (giây), Độ lệch chuẩn)
    distances_info = [
        ('5km', '5', 4410, 35*60, 10*60),
        ('10km', '1', 4940, 75*60, 15*60),
        ('21.1km', '21', 920, 150*60, 25*60),
        ('42.195km', '42', 850, 270*60, 45*60)
    ]
    
    all_runners = []
    
    for dist, prefix, count, mean_sec, std_sec in distances_info:
        # Sinh số BIB
        if prefix == '5':
            bib_range = range(50000, 59999)
        elif prefix == '1':
            bib_range = range(10000, 19999)
        elif prefix == '21':
            bib_range = range(21000, 21999)
        elif prefix == '42':
            bib_range = range(42000, 42999)
            
        bibs = random.sample(bib_range, count)
        
        # Sinh thời gian hoàn thành (Phân phối chuẩn)
        times = np.random.normal(mean_sec, std_sec, count)
        times = np.clip(times, mean_sec - 3*std_sec, mean_sec + 4*std_sec)
        times = np.round(times).astype(int)
        
        # Ghép cặp bib và thời gian, sau đó sort thời gian để gán rank
        runner_records = list(zip(bibs, times))
        runner_records.sort(key=lambda x: x[1])
        
        for rank, (bib, time_sec) in enumerate(runner_records, start=1):
            # Format giây sang HH:MM:SS
            h = time_sec // 3600
            m = (time_sec % 3600) // 60
            s = time_sec % 60
            formatted_time = f"{h:02d}:{m:02d}:{s:02d}"
            
            all_runners.append({
                'bib_number': str(bib),
                'runner_name': generate_vietnamese_name(),
                'distance': dist,
                'finishing_time': formatted_time,
                'rank': rank,
                'total_runners': count
            })
            
    df = pd.DataFrame(all_runners)
    # Xáo trộn dataframe để dữ liệu file ngẫu nhiên
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(output_file, index=False)
    return len(df)

if __name__ == "__main__":
    count = generate_bib_data()
    print(f"Đã sinh {count} dòng dữ liệu vào bib_data.csv kèm Tên VĐV.")
