import json
import os
from datetime import datetime
from pathlib import Path
import sqlite3

class TimeExtractor:
    """Trích xuất và quản lý thông tin thời gian phân tích thời tiết"""
    
    def __init__(self, db_path='analysis_history.db'):
        """
        Khởi tạo TimeExtractor
        
        Args:
            db_path: Đường dẫn tới cơ sở dữ liệu SQLite
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Khởi tạo cơ sở dữ liệu nếu chưa tồn tại"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                hour INTEGER,
                minute INTEGER,
                second INTEGER,
                image_name TEXT,
                prediction TEXT,
                confidence REAL,
                duration REAL,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_time_components(self, dt=None):
        """
        Trích xuất các thành phần thời gian từ datetime
        
        Args:
            dt: datetime object (nếu None sử dụng thời gian hiện tại)
            
        Returns:
            dict: Chứa year, month, day, hour, minute, second, và timestamp
        """
        if dt is None:
            dt = datetime.now()
        
        time_components = {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'timestamp': dt.isoformat(),
            'formatted': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M:%S'),
            'week_day': dt.strftime('%A'),
            'day_name': dt.strftime('%A'),
            'month_name': dt.strftime('%B'),
            'iso_week': dt.isocalendar()[1],
            'quarter': (dt.month - 1) // 3 + 1,
            'day_of_year': dt.timetuple().tm_yday,
            'unix_timestamp': int(dt.timestamp())
        }
        
        return time_components
    
    def record_analysis(self, image_name, prediction, confidence, duration=None, notes=None):
        """
        Ghi lại kết quả phân tích với thông tin thời gian
        
        Args:
            image_name: Tên file ảnh
            prediction: Kết quả dự đoán (tên lớp)
            confidence: Độ tin cậy (0-1)
            duration: Thời gian xử lý (giây)
            notes: Ghi chú thêm
            
        Returns:
            dict: Thông tin phân tích đã ghi
        """
        dt = datetime.now()
        time_comp = self.extract_time_components(dt)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_history 
            (year, month, day, hour, minute, second, image_name, prediction, confidence, duration, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            time_comp['year'],
            time_comp['month'],
            time_comp['day'],
            time_comp['hour'],
            time_comp['minute'],
            time_comp['second'],
            image_name,
            prediction,
            confidence,
            duration,
            notes
        ))
        
        conn.commit()
        analysis_id = cursor.lastrowid
        conn.close()
        
        return {
            'id': analysis_id,
            'time': time_comp,
            'image': image_name,
            'prediction': prediction,
            'confidence': confidence,
            'duration': duration,
            'notes': notes
        }
    
    def get_analysis_by_date(self, year, month=None, day=None):
        """
        Lấy lịch sử phân tích theo năm/tháng/ngày
        
        Args:
            year: Năm
            month: Tháng (tùy chọn)
            day: Ngày (tùy chọn)
            
        Returns:
            list: Danh sách các bản ghi phân tích
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM analysis_history WHERE year = ?"
        params = [year]
        
        if month is not None:
            query += " AND month = ?"
            params.append(month)
        
        if day is not None:
            query += " AND day = ?"
            params.append(day)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append(dict(row))
        
        return results
    
    def get_analysis_by_time_range(self, start_hour, end_hour, year=None, month=None, day=None):
        """
        Lấy lịch sử phân tích trong khoảng thời gian (giờ/phút)
        
        Args:
            start_hour: Giờ bắt đầu (0-23)
            end_hour: Giờ kết thúc (0-23)
            year: Năm (tùy chọn)
            month: Tháng (tùy chọn)
            day: Ngày (tùy chọn)
            
        Returns:
            list: Danh sách các bản ghi phân tích
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM analysis_history WHERE hour >= ? AND hour <= ?"
        params = [start_hour, end_hour]
        
        if year is not None:
            query += " AND year = ?"
            params.append(year)
        
        if month is not None:
            query += " AND month = ?"
            params.append(month)
        
        if day is not None:
            query += " AND day = ?"
            params.append(day)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append(dict(row))
        
        return results
    
    def get_statistics_by_date(self, year, month=None, day=None):
        """
        Lấy thống kê phân tích theo ngày/tháng/năm
        
        Args:
            year: Năm
            month: Tháng (tùy chọn)
            day: Ngày (tùy chọn)
            
        Returns:
            dict: Thống kê (tổng số, phân loại, độ tin cậy trung bình, etc.)
        """
        records = self.get_analysis_by_date(year, month, day)
        
        if not records:
            return {
                'total': 0,
                'by_prediction': {},
                'average_confidence': 0,
                'max_confidence': 0,
                'min_confidence': 0,
                'total_duration': 0,
                'average_duration': 0
            }
        
        by_prediction = {}
        total_confidence = 0
        total_duration = 0
        max_conf = 0
        min_conf = 1
        
        for record in records:
            pred = record['prediction']
            if pred not in by_prediction:
                by_prediction[pred] = 0
            by_prediction[pred] += 1
            
            if record['confidence']:
                total_confidence += record['confidence']
                max_conf = max(max_conf, record['confidence'])
                min_conf = min(min_conf, record['confidence'])
            
            if record['duration']:
                total_duration += record['duration']
        
        return {
            'total': len(records),
            'by_prediction': by_prediction,
            'average_confidence': round(total_confidence / len(records), 4) if records else 0,
            'max_confidence': round(max_conf, 4) if max_conf > 0 else 0,
            'min_confidence': round(min_conf, 4) if min_conf < 1 else 0,
            'total_duration': round(total_duration, 2),
            'average_duration': round(total_duration / len(records), 4) if records else 0
        }
    
    def get_hourly_statistics(self, year, month, day):
        """
        Lấy thống kê phân tích theo từng giờ trong ngày
        
        Args:
            year: Năm
            month: Tháng
            day: Ngày
            
        Returns:
            dict: Thống kê theo giờ (từ 0 đến 23)
        """
        records = self.get_analysis_by_date(year, month, day)
        
        hourly_stats = {}
        for hour in range(24):
            hourly_stats[hour] = {
                'count': 0,
                'predictions': {},
                'average_confidence': 0,
                'total_duration': 0
            }
        
        for record in records:
            hour = record['hour']
            hourly_stats[hour]['count'] += 1
            
            pred = record['prediction']
            if pred not in hourly_stats[hour]['predictions']:
                hourly_stats[hour]['predictions'][pred] = 0
            hourly_stats[hour]['predictions'][pred] += 1
            
            if record['confidence']:
                hourly_stats[hour]['average_confidence'] = (
                    (hourly_stats[hour]['average_confidence'] * (hourly_stats[hour]['count'] - 1) + 
                     record['confidence']) / hourly_stats[hour]['count']
                )
            
            if record['duration']:
                hourly_stats[hour]['total_duration'] += record['duration']
        
        return hourly_stats
    
    def export_history_to_json(self, output_path='analysis_history.json', 
                               year=None, month=None, day=None):
        """
        Xuất lịch sử phân tích ra file JSON
        
        Args:
            output_path: Đường dẫn file output
            year: Năm (tùy chọn, nếu None xuất tất cả)
            month: Tháng (tùy chọn)
            day: Ngày (tùy chọn)
            
        Returns:
            str: Đường dẫn file được tạo
        """
        if year is None:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM analysis_history ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            conn.close()
            records = [dict(row) for row in rows]
        else:
            records = self.get_analysis_by_date(year, month, day)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def get_all_history(self, limit=100):
        """
        Lấy toàn bộ lịch sử phân tích
        
        Args:
            limit: Giới hạn số bản ghi
            
        Returns:
            list: Danh sách phân tích
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM analysis_history ORDER BY timestamp DESC LIMIT ?",
            [limit]
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def clear_old_records(self, days_old=30):
        """
        Xóa các bản ghi cũ hơn số ngày chỉ định
        
        Args:
            days_old: Số ngày (xóa bản ghi cũ hơn số này)
            
        Returns:
            int: Số bản ghi đã xóa
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Lấy datetime cách đây n ngày
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        cursor.execute(
            "DELETE FROM analysis_history WHERE timestamp < ?",
            [cutoff_date.isoformat()]
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
