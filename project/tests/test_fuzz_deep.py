"""
深度模糊测试 - 针对所有可能的崩溃点
"""

import sys
import os
import random
import string
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.record_manager import RecordManager
from logic.ocr_service import OCRService
from unittest.mock import Mock
import traceback

CRASH_LOG = os.path.join(os.path.dirname(__file__), "fuzz_crashes.log")

def log_crash(test_name: str, input_data, error: Exception):
    with open(CRASH_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"测试: {test_name}\n")
        f.write(f"时间: {datetime.now().isoformat()}\n")
        f.write(f"输入: {repr(input_data)[:500]}\n")  # 限制长度
        f.write(f"错误: {type(error).__name__}: {error}\n")
        f.write(f"堆栈:\n{traceback.format_exc()}\n")
    print(f"  ❌ 崩溃: {type(error).__name__}")


def random_bytes(size):
    return bytes(random.randint(0, 255) for _ in range(size))


def random_unicode_string(size):
    return ''.join(chr(random.randint(0, 0x10FFFF)) for _ in range(size) 
                   if chr(random.randint(0, 0x10FFFF)).isprintable())


def main():
    print("="*60)
    print("深度模糊测试")
    print("="*60)
    
    crashes = 0
    tests = 0
    
    manager = RecordManager()
    manager.db = Mock()
    manager.db.saveData = Mock(return_value="id")
    manager.db.fetchData = Mock(return_value=[])
    manager.db.deleteData = Mock(return_value=True)
    
    service = OCRService()
    
    # 1. 测试 deleteRecord (已知有 ctypes bug)
    print("\n测试 deleteRecord...")
    tests += 1
    try:
        manager.deleteRecord("any_id")
    except NameError as e:
        print(f"  ✅ 发现 NameError: {e}")
        log_crash("deleteRecord", "any_id", e)
        crashes += 1
    except Exception as e:
        log_crash("deleteRecord", "any_id", e)
        crashes += 1
        
    # 2. 测试 extractInfoFromImage (已知有 use-after-free)
    print("\n测试 extractInfoFromImage...")
    test_cases = [
        "/nonexistent/path/image.jpg",
        "",
        None,
        123,
        "C:\\Windows\\System32\\config\\SAM",  # 无权限文件
        "CON",  # Windows 特殊设备名
        "NUL",
        "PRN",
    ]
    
    for tc in test_cases:
        tests += 1
        try:
            if tc is None:
                result = service.extractInfoFromImage(tc)
            else:
                result = service.extractInfoFromImage(tc)
            print(f"  {repr(tc)[:30]}: 未崩溃")
        except (FileNotFoundError, TypeError, ValueError, OSError) as e:
            print(f"  {repr(tc)[:30]}: {type(e).__name__}")
        except Exception as e:
            log_crash(f"extractInfoFromImage", tc, e)
            crashes += 1
    
    # 3. 测试 addTagToRecord
    print("\n测试 addTagToRecord...")
    tag_tests = [
        (None, None),
        ("", ""),
        ("id", None),
        (None, "tag"),
        (123, 456),
        ([], {}),
    ]
    
    for record_id, tag in tag_tests:
        tests += 1
        try:
            manager.addTagToRecord(record_id, tag)
        except (TypeError, ValueError, AttributeError):
            pass
        except Exception as e:
            log_crash("addTagToRecord", (record_id, tag), e)
            crashes += 1
    
    # 4. 测试 addPhotoToRecord
    print("\n测试 addPhotoToRecord...")
    photo_tests = [
        (None, None),
        ("", ""),
        ("id", "/path/to/nonexistent.jpg"),
        ("id", "CON"),
        ("id", "\\\\?\\C:\\verylongpath" + "a" * 300),
    ]
    
    for record_id, path in photo_tests:
        tests += 1
        try:
            manager.addPhotoToRecord(record_id, path)
        except (TypeError, ValueError, AttributeError):
            pass
        except Exception as e:
            log_crash("addPhotoToRecord", (record_id, path), e)
            crashes += 1
    
    # 5. 随机数据测试 createRecord
    print("\n随机数据测试 createRecord...")
    for i in range(100):
        tests += 1
        try:
            data = {
                "type": random.choice(["收入", "支出", "", None, 123, random_unicode_string(10)]),
                "amount": random.choice([
                    random.uniform(-1e10, 1e10),
                    float('nan'),
                    float('inf'),
                    random.randint(-2**63, 2**63),
                    random_unicode_string(5),
                    None,
                ]),
                "date": random.choice([
                    f"{random.randint(0, 9999)}-{random.randint(0, 99)}-{random.randint(0, 99)}",
                    random_unicode_string(20),
                    None,
                    random.randint(-1000, 3000),
                ]),
                "note": random.choice([
                    random_unicode_string(random.randint(0, 1000)),
                    None,
                    random.randint(0, 1000000),
                ]),
            }
            manager.createRecord(data)
        except (ValueError, TypeError, AttributeError):
            pass
        except Exception as e:
            log_crash("createRecord_random", data, e)
            crashes += 1
    print(f"  完成 100 个随机测试")
    
    # 6. 随机数据测试 autoCategorize
    print("\n随机数据测试 autoCategorize...")
    for i in range(100):
        tests += 1
        try:
            text = random.choice([
                random_unicode_string(random.randint(0, 10000)),
                random_bytes(random.randint(0, 1000)).decode('utf-8', errors='ignore'),
                None,
                random.randint(0, 1000000),
                [],
                {},
            ])
            service.autoCategorize(text)
        except (ValueError, TypeError, AttributeError):
            pass
        except Exception as e:
            log_crash("autoCategorize_random", text, e)
            crashes += 1
    print(f"  完成 100 个随机测试")
    
    # 7. 测试 insecure_permissions (已知安全问题)
    print("\n测试 insecure_permissions...")
    tests += 1
    try:
        test_file = os.path.join(os.path.dirname(__file__), "test_perm.tmp")
        with open(test_file, "w") as f:
            f.write("test")
        service.insecure_permissions(test_file)
        os.remove(test_file)
        print("  ✅ insecure_permissions 执行成功 (存在安全隐患)")
    except Exception as e:
        print(f"  insecure_permissions: {type(e).__name__}: {e}")
        log_crash("insecure_permissions", test_file, e)
        crashes += 1
    
    # 结果
    print()
    print("="*60)
    print(f"测试完成: {tests} 个测试, {crashes} 个崩溃")
    print(f"崩溃日志: {CRASH_LOG}")
    print("="*60)


if __name__ == "__main__":
    main()
