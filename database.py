import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, DB_NAME

def create_connection(database=None):
    """Tạo kết nối đến MySQL database"""
    try:
        config = DB_CONFIG.copy()
        if database:
            config['database'] = database
            
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Rất tiếc, không thể kết nối tới MySQL: {e}\nGợi ý: Hãy thử chạy lệnh 'brew services start mysql' để đảm bảo MySQL đang hoạt động nhé!")
        return None

def setup_database():
    """Tạo database và các bảng dữ liệu nếu chưa tồn tại"""
    connection = create_connection()
    if connection is None:
        return False
        
    try:
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {DB_NAME}")
        
        # Bảng thống kê
        create_stats_table = """
        CREATE TABLE IF NOT EXISTS marathon_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            distance VARCHAR(20) NOT NULL,
            registered_runners INT NOT NULL,
            finished_runners INT NOT NULL,
            completion_rate DECIMAL(5, 2) NOT NULL
        )
        """
        cursor.execute(create_stats_table)
        
        # Cập nhật: Drop bảng runner_details cũ để tạo cấu trúc mới chứa tên
        cursor.execute("DROP TABLE IF EXISTS runner_details")
        
        # Bảng danh sách vận động viên
        create_runners_table = """
        CREATE TABLE runner_details (
            bib_number VARCHAR(10) PRIMARY KEY,
            runner_name VARCHAR(100) NOT NULL,
            distance VARCHAR(20) NOT NULL,
            finishing_time VARCHAR(10) NOT NULL,
            rank_position INT NOT NULL,
            total_runners INT NOT NULL
        )
        """
        cursor.execute(create_runners_table)
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"Lỗi khi thiết lập cơ sở dữ liệu: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def insert_marathon_data(data):
    """Chèn dữ liệu vào bảng marathon_stats"""
    connection = create_connection(DB_NAME)
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM marathon_stats")
        if cursor.fetchone()[0] == 0:
            insert_query = """
            INSERT INTO marathon_stats (distance, registered_runners, finished_runners, completion_rate)
            VALUES (%s, %s, %s, %s)
            """
            cursor.executemany(insert_query, data)
            connection.commit()
        return True
    except Error as e:
        print(f"Lỗi khi thêm dữ liệu thống kê: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def insert_bib_data(data):
    """Chèn dữ liệu vào bảng runner_details"""
    connection = create_connection(DB_NAME)
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM runner_details")
        if cursor.fetchone()[0] == 0:
            insert_query = """
            INSERT INTO runner_details (bib_number, runner_name, distance, finishing_time, rank_position, total_runners)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, data)
            connection.commit()
        return True
    except Error as e:
        print(f"Lỗi khi thêm dữ liệu BIB: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_all_data():
    """Lấy tất cả dữ liệu từ bảng marathon_stats"""
    connection = create_connection(DB_NAME)
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT distance, registered_runners, finished_runners, completion_rate FROM marathon_stats")
        return cursor.fetchall()
    except Error as e:
        print(f"Lỗi khi truy xuất dữ liệu: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def search_runner_by_bib(bib_number):
    """Tra cứu kết quả chạy bằng số BIB"""
    connection = create_connection(DB_NAME)
    if connection is None:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT runner_name, distance, finishing_time, rank_position, total_runners FROM runner_details WHERE bib_number = %s"
        cursor.execute(query, (bib_number,))
        return cursor.fetchone()
    except Error as e:
        print(f"Lỗi khi tra cứu BIB: {e}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
