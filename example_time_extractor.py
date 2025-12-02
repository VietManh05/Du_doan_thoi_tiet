"""
Ví dụ sử dụng TimeExtractor
Tệp này minh họa cách sử dụng module trích xuất thời gian và quản lý lịch sử phân tích
"""

from time_extractor import TimeExtractor
from datetime import datetime, timedelta
import json

def example_1_extract_time():
    """Ví dụ 1: Trích xuất thông tin thời gian"""
    print("\n" + "="*60)
    print("VÍ DỤ 1: TRÍCH XUẤT THÔNG TIN THỜI GIAN")
    print("="*60)
    
    extractor = TimeExtractor()
    
    # Lấy thời gian hiện tại
    time_info = extractor.extract_time_components()
    
    print("\nThông tin thời gian hiện tại:")
    print(f"  Ngày: {time_info['date']}")
    print(f"  Giờ: {time_info['time']}")
    print(f"  Năm: {time_info['year']}")
    print(f"  Tháng: {time_info['month']}")
    print(f"  Ngày: {time_info['day']}")
    print(f"  Giờ: {time_info['hour']}")
    print(f"  Phút: {time_info['minute']}")
    print(f"  Giây: {time_info['second']}")
    print(f"  Ngày trong tuần: {time_info['week_day']}")
    print(f"  Tháng: {time_info['month_name']}")
    print(f"  Quý: Q{time_info['quarter']}")
    print(f"  Unix Timestamp: {time_info['unix_timestamp']}")


def example_2_record_analysis():
    """Ví dụ 2: Ghi lại kết quả phân tích"""
    print("\n" + "="*60)
    print("VÍ DỤ 2: GHI LẠI KẾT QUẢ PHÂN TÍCH")
    print("="*60)
    
    extractor = TimeExtractor()
    
    # Mô phỏng các kết quả phân tích
    analyses = [
        {'image': 'weather_001.jpg', 'prediction': 'Sunny', 'confidence': 0.95, 'duration': 0.234},
        {'image': 'weather_002.jpg', 'prediction': 'Rainy', 'confidence': 0.87, 'duration': 0.201},
        {'image': 'weather_003.jpg', 'prediction': 'Snowy', 'confidence': 0.92, 'duration': 0.218},
    ]
    
    print("\nGhi lại 3 phân tích:")
    for analysis in analyses:
        record = extractor.record_analysis(
            image_name=analysis['image'],
            prediction=analysis['prediction'],
            confidence=analysis['confidence'],
            duration=analysis['duration'],
            notes=f"Weather analysis for {analysis['image']}"
        )
        print(f"  ✓ Ghi lại: {analysis['image']} -> {analysis['prediction']} "
              f"({analysis['confidence']:.0%}) - ID: {record['id']}")


def example_3_get_history():
    """Ví dụ 3: Lấy lịch sử phân tích"""
    print("\n" + "="*60)
    print("VÍ DỤ 3: LẤY LỊCH SỬ PHÂN TÍCH")
    print("="*60)
    
    extractor = TimeExtractor()
    today = datetime.now()
    
    # Lấy lịch sử hôm nay
    records = extractor.get_analysis_by_date(
        year=today.year,
        month=today.month,
        day=today.day
    )
    
    print(f"\nLịch sử phân tích hôm nay ({today.strftime('%Y-%m-%d')}):")
    print(f"Tìm thấy {len(records)} phân tích")
    
    if records:
        for i, record in enumerate(records[:5], 1):
            print(f"\n  Phân tích #{i}:")
            print(f"    Ảnh: {record['image_name']}")
            print(f"    Dự đoán: {record['prediction']}")
            print(f"    Độ tin cậy: {record['confidence']:.2%}" if record['confidence'] else "    Độ tin cậy: N/A")
            print(f"    Thời gian xử lý: {record['duration']:.3f}s" if record['duration'] else "    Thời gian xử lý: N/A")
            print(f"    Thời gian: {record['timestamp']}")


def example_4_statistics():
    """Ví dụ 4: Lấy thống kê"""
    print("\n" + "="*60)
    print("VÍ DỤ 4: LẤY THỐNG KÊ PHÂN TÍCH")
    print("="*60)
    
    extractor = TimeExtractor()
    today = datetime.now()
    
    # Lấy thống kê hôm nay
    stats = extractor.get_statistics_by_date(
        year=today.year,
        month=today.month,
        day=today.day
    )
    
    print(f"\nThống kê hôm nay ({today.strftime('%Y-%m-%d')}):")
    print(f"  Tổng phân tích: {stats['total']}")
    print(f"  Phân loại: {stats['by_prediction']}")
    if stats['total'] > 0:
        print(f"  Độ tin cậy trung bình: {stats['average_confidence']:.2%}")
        print(f"  Độ tin cậy cao nhất: {stats['max_confidence']:.2%}")
        print(f"  Độ tin cậy thấp nhất: {stats['min_confidence']:.2%}")
        print(f"  Tổng thời gian xử lý: {stats['total_duration']:.2f}s")
        print(f"  Thời gian xử lý trung bình: {stats['average_duration']:.4f}s")


def example_5_hourly_stats():
    """Ví dụ 5: Thống kê theo giờ"""
    print("\n" + "="*60)
    print("VÍ DỤ 5: THỐNG KÊ THEO GIỜ")
    print("="*60)
    
    extractor = TimeExtractor()
    today = datetime.now()
    
    # Lấy thống kê theo giờ
    hourly = extractor.get_hourly_statistics(
        year=today.year,
        month=today.month,
        day=today.day
    )
    
    print(f"\nThống kê theo giờ ({today.strftime('%Y-%m-%d')}):")
    print("\nCác giờ có phân tích:")
    
    for hour in range(24):
        if hourly[hour]['count'] > 0:
            print(f"\n  Giờ {hour:02d}:00")
            print(f"    Số lượng: {hourly[hour]['count']}")
            print(f"    Dự đoán: {hourly[hour]['predictions']}")
            if hourly[hour]['count'] > 0:
                print(f"    Độ tin cậy TB: {hourly[hour]['average_confidence']:.2%}")
                print(f"    Tổng thời gian: {hourly[hour]['total_duration']:.2f}s")


def example_6_export():
    """Ví dụ 6: Xuất dữ liệu"""
    print("\n" + "="*60)
    print("VÍ DỤ 6: XUẤT DỮ LIỆU")
    print("="*60)
    
    extractor = TimeExtractor()
    today = datetime.now()
    
    # Xuất dữ liệu hôm nay
    export_path = extractor.export_history_to_json(
        output_path=f'analysis_export_{today.strftime("%Y%m%d")}.json',
        year=today.year,
        month=today.month,
        day=today.day
    )
    
    print(f"\nĐã xuất dữ liệu vào: {export_path}")


def example_7_cleanup():
    """Ví dụ 7: Dọn dẹp dữ liệu cũ"""
    print("\n" + "="*60)
    print("VÍ DỤ 7: DỌN DẸP DỮ LIỆU CŨ")
    print("="*60)
    
    extractor = TimeExtractor()
    
    # Xóa dữ liệu cũ hơn 90 ngày
    deleted = extractor.clear_old_records(days_old=90)
    print(f"\nĐã xóa {deleted} bản ghi cũ hơn 90 ngày")


def example_8_time_range():
    """Ví dụ 8: Lấy lịch sử trong khoảng thời gian"""
    print("\n" + "="*60)
    print("VÍ DỤ 8: LẤY LỊCH SỬ TRONG KHOẢNG THỜI GIAN")
    print("="*60)
    
    extractor = TimeExtractor()
    today = datetime.now()
    
    # Lấy lịch sử từ 8h đến 17h hôm nay
    records = extractor.get_analysis_by_time_range(
        start_hour=8,
        end_hour=17,
        year=today.year,
        month=today.month,
        day=today.day
    )
    
    print(f"\nLịch sử phân tích từ 8h đến 17h hôm nay ({today.strftime('%Y-%m-%d')}):")
    print(f"Tìm thấy {len(records)} phân tích")
    
    if records:
        for i, record in enumerate(records[:5], 1):
            print(f"\n  Phân tích #{i}:")
            print(f"    Ảnh: {record['image_name']}")
            print(f"    Thời gian: {record['timestamp']}")
            print(f"    Dự đoán: {record['prediction']}")


def main():
    """Chạy tất cả các ví dụ"""
    print("\n" + "="*60)
    print("TIME EXTRACTOR - HƯỚNG DẪN VÍ DỤ")
    print("="*60)
    
    try:
        # Ví dụ 1: Trích xuất thời gian
        example_1_extract_time()
        
        # Ví dụ 2: Ghi lại phân tích
        example_2_record_analysis()
        
        # Ví dụ 3: Lấy lịch sử
        example_3_get_history()
        
        # Ví dụ 4: Thống kê
        example_4_statistics()
        
        # Ví dụ 5: Thống kê theo giờ
        example_5_hourly_stats()
        
        # Ví dụ 6: Xuất dữ liệu
        example_6_export()
        
        # Ví dụ 7: Lấy lịch sử trong khoảng thời gian
        example_8_time_range()
        
        # Ví dụ 8: Dọn dẹp (không chạy mặc định vì sẽ xóa dữ liệu)
        # example_7_cleanup()
        
        print("\n" + "="*60)
        print("HOÀN THÀNH")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
