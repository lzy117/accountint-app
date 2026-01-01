"""
快速模糊测试 - 专门寻找崩溃

针对已知的潜在问题点进行测试
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.record_manager import RecordManager
from logic.ocr_service import OCRService
from unittest.mock import Mock

CRASH_LOG = os.path.join(os.path.dirname(__file__), "fuzz_crashes.log")

def log_crash(test_name: str, input_data: Any, error: Exception):
    """记录崩溃"""
    import traceback
    with open(CRASH_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"测试: {test_name}\n")
        f.write(f"时间: {datetime.now().isoformat()}\n")
        f.write(f"输入: {repr(input_data)}\n")
        f.write(f"错误: {type(error).__name__}: {error}\n")
        f.write(f"堆栈:\n{traceback.format_exc()}\n")
    print(f"  ❌ 崩溃: {type(error).__name__}: {error}")


def test_case(test_name: str, func, *args, **kwargs):
    """运行单个测试用例"""
    try:
        result = func(*args, **kwargs)
        return True, result
    except (ValueError, TypeError, AttributeError) as e:
        # 预期的错误
        return True, None
    except Exception as e:
        log_crash(test_name, args if args else kwargs, e)
        return False, e


def main():
    print("="*60)
    print("快速模糊测试 - 寻找崩溃")
    print("="*60)
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 清空日志
    with open(CRASH_LOG, "w", encoding="utf-8") as f:
        f.write(f"模糊测试崩溃日志\n开始时间: {datetime.now()}\n")
    
    crashes_found = 0
    tests_run = 0
    
    # 创建测试对象
    manager = RecordManager()
    manager.db = Mock()
    manager.db.saveData = Mock(return_value="test_id")
    manager.db.fetchData = Mock(return_value=[])
    
    service = OCRService()
    
    # ========================================
    # 测试组 1: 特殊数值测试
    # ========================================
    print("测试组 1: 特殊数值")
    special_amounts = [
        float('nan'), float('inf'), float('-inf'),
        1e308, -1e308, 1e-308,
        0.0, -0.0,
        999999999999999999999999999999,
        0.1 + 0.2,  # 浮点精度问题
        2**63, -2**63,
        2**64, -2**64,
    ]
    
    for amount in special_amounts:
        tests_run += 1
        data = {"type": "支出", "amount": amount, "date": "2025-01-01"}
        success, _ = test_case(f"特殊金额:{amount}", manager.createRecord, data)
        if not success:
            crashes_found += 1
    print(f"  完成 {len(special_amounts)} 个测试")
    
    # ========================================
    # 测试组 2: 特殊字符串测试  
    # ========================================
    print("测试组 2: 特殊字符串")
    special_strings = [
        "",
        " " * 10000,
        "\x00" * 100,  # NULL字符
        "\n" * 1000,
        "a" * 100000,  # 超长字符串
        "餐厅" * 50000,  # 超长中文
        "\u0000\u0001\u0002",  # 控制字符
        "\\",
        "\\\\\\",
        "'",
        '"',
        "'''",
        '"""',
        "SELECT * FROM users; DROP TABLE--",  # SQL注入
        "<script>alert(1)</script>",  # XSS
        "{{7*7}}",  # 模板注入
        "${7*7}",
        None,
        123,
        [],
        {},
        object(),
    ]
    
    for s in special_strings:
        tests_run += 1
        success, _ = test_case(f"特殊字符串分类", service.autoCategorize, s)
        if not success:
            crashes_found += 1
    print(f"  完成 {len(special_strings)} 个测试")
    
    # ========================================
    # 测试组 3: 日期边界测试
    # ========================================
    print("测试组 3: 日期边界")
    special_dates = [
        "",
        None,
        "not-a-date",
        "2025/01/01",
        "01-01-2025",
        "2025-13-01",  # 无效月份
        "2025-01-32",  # 无效日期
        "2025-00-00",
        "0000-00-00",
        "9999-12-31",
        "-2025-01-01",
        "2025-01-01T00:00:00",
        "2025-01-01 00:00:00",
        12345,
        12345.67,
        [],
        {},
    ]
    
    for d in special_dates:
        tests_run += 1
        data = {"type": "支出", "amount": 100, "date": d}
        success, _ = test_case(f"特殊日期:{d}", manager.createRecord, data)
        if not success:
            crashes_found += 1
    print(f"  完成 {len(special_dates)} 个测试")
    
    # ========================================
    # 测试组 4: 类型混淆测试
    # ========================================
    print("测试组 4: 类型混淆")
    type_confusion_tests = [
        {"type": [], "amount": 100, "date": "2025-01-01"},
        {"type": {}, "amount": 100, "date": "2025-01-01"},
        {"type": 123, "amount": 100, "date": "2025-01-01"},
        {"type": object(), "amount": 100, "date": "2025-01-01"},
        {"type": "支出", "amount": [], "date": "2025-01-01"},
        {"type": "支出", "amount": {}, "date": "2025-01-01"},
        {"type": "支出", "amount": object(), "date": "2025-01-01"},
        {"type": "支出", "amount": 100, "date": []},
        {"type": "支出", "amount": 100, "date": {}},
        {"type": "支出", "amount": 100, "date": object()},
        # 缺少字段
        {},
        {"type": "支出"},
        {"amount": 100},
        {"date": "2025-01-01"},
        {"type": "支出", "amount": 100},
        {"type": "支出", "date": "2025-01-01"},
        {"amount": 100, "date": "2025-01-01"},
    ]
    
    for data in type_confusion_tests:
        tests_run += 1
        success, _ = test_case(f"类型混淆", manager.createRecord, data)
        if not success:
            crashes_found += 1
    print(f"  完成 {len(type_confusion_tests)} 个测试")
    
    # ========================================
    # 测试组 5: Unicode边界测试
    # ========================================
    print("测试组 5: Unicode边界")
    unicode_tests = [
        "\U0001F4A9",  # 💩 emoji
        "\U0001F600" * 1000,  # 大量 emoji
        "🍜🍜🍜餐厅🍜🍜🍜",
        "\uFFFD",  # 替换字符
        "\uFEFF",  # BOM
        "\u200B" * 100,  # 零宽空格
        "a\u0300",  # 组合字符
        "\u202E反向文本",  # RTL覆盖
        "中" * 100000,
        "\U0010FFFF",  # 最大 Unicode
    ]
    
    for text in unicode_tests:
        tests_run += 1
        success, _ = test_case(f"Unicode测试", service.autoCategorize, text)
        if not success:
            crashes_found += 1
    print(f"  完成 {len(unicode_tests)} 个测试")
    
    # ========================================
    # 测试组 6: 调用已知有bug的方法
    # ========================================
    print("测试组 6: 已知问题方法")
    
    # deleteRecord 有 ctypes 未导入的 bug
    tests_run += 1
    try:
        result = manager.deleteRecord("test_id")
        print("  deleteRecord: 未崩溃")
    except NameError as e:
        print(f"  deleteRecord: 发现 NameError (ctypes未导入)")
        log_crash("deleteRecord-ctypes", "test_id", e)
        crashes_found += 1
    except Exception as e:
        log_crash("deleteRecord", "test_id", e)
        crashes_found += 1
    
    # extractInfoFromImage 有 use-after-free bug
    tests_run += 1
    try:
        # 创建一个临时文件来测试
        test_file = os.path.join(os.path.dirname(__file__), "test_image.tmp")
        with open(test_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        
        result = service.extractInfoFromImage(test_file)
        print("  extractInfoFromImage: 未崩溃 (返回模拟数据)")
        
        os.remove(test_file)
    except Exception as e:
        print(f"  extractInfoFromImage: {type(e).__name__}: {e}")
        log_crash("extractInfoFromImage", test_file, e)
        crashes_found += 1
    
    # ========================================
    # 结果汇总
    # ========================================
    print()
    print("="*60)
    print("测试结果汇总")
    print("="*60)
    print(f"总测试数: {tests_run}")
    print(f"发现崩溃: {crashes_found}")
    print(f"结束时间: {datetime.now()}")
    print(f"崩溃日志: {CRASH_LOG}")
    
    if crashes_found > 0:
        print()
        print("发现的崩溃已记录到日志文件")


if __name__ == "__main__":
    main()
