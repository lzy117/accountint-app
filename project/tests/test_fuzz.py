"""
模糊测试 (Fuzz Testing) 模块

测试工具：Hypothesis
测试目标：RecordManager.createRecord 和 OCRService.autoCategorize
测试策略：基于属性的测试 (Property-Based Testing)

Hypothesis 会自动生成大量随机输入来尝试触发程序崩溃
"""

import sys
import os
import traceback
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hypothesis import given, settings, Verbosity, Phase, HealthCheck
from hypothesis import strategies as st
from hypothesis.database import DirectoryBasedExampleDatabase

from logic.record_manager import RecordManager
from logic.ocr_service import OCRService
from data.models import RecordType
from unittest.mock import Mock

# 保存发现的崩溃用例
CRASH_LOG_FILE = os.path.join(os.path.dirname(__file__), "fuzz_crashes.log")

def log_crash(func_name: str, input_data: Any, error: Exception):
    """记录崩溃信息到文件"""
    with open(CRASH_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"函数: {func_name}\n")
        f.write(f"时间: {datetime.now().isoformat()}\n")
        f.write(f"输入: {input_data}\n")
        f.write(f"错误类型: {type(error).__name__}\n")
        f.write(f"错误信息: {str(error)}\n")
        f.write(f"堆栈跟踪:\n{traceback.format_exc()}\n")


# ============================================================
# 模糊测试 1：RecordManager.createRecord
# ============================================================

# 定义随机数据生成策略
record_type_strategy = st.sampled_from(["收入", "支出", "借款", "转账", "", None, 123, [], {}])

amount_strategy = st.one_of(
    st.floats(allow_nan=True, allow_infinity=True),
    st.integers(),
    st.text(),
    st.none(),
    st.binary(),
    st.lists(st.integers()),
)

date_strategy = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.dates(),
    st.datetimes(),
    st.binary(),
    st.floats(),
)

note_strategy = st.one_of(
    st.text(max_size=10000),
    st.none(),
    st.integers(),
    st.binary(),
)

# 组合策略生成完整的记录数据
record_data_strategy = st.fixed_dictionaries({
    "type": record_type_strategy,
    "amount": amount_strategy,
    "date": date_strategy,
}, optional={
    "note": note_strategy,
})


@settings(
    max_examples=10000,  # 运行10000个测试用例
    deadline=None,  # 不限制单个测试时间
    verbosity=Verbosity.normal,
    phases=[Phase.generate, Phase.target],
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
    database=DirectoryBasedExampleDatabase(".hypothesis_db"),
)
@given(data=record_data_strategy)
def test_fuzz_create_record(data: Dict[str, Any]):
    """
    模糊测试 RecordManager.createRecord
    
    尝试使用各种随机输入来触发程序崩溃
    预期：函数应该抛出 ValueError 或正常返回，不应该发生意外崩溃
    """
    manager = RecordManager()
    manager.db = Mock()
    manager.db.saveData = Mock(return_value="fuzz_record_id")
    
    try:
        result = manager.createRecord(data)
        # 如果成功创建，验证返回值不为 None
        assert result is not None
    except ValueError as e:
        # ValueError 是预期的校验错误，正常
        pass
    except TypeError as e:
        # TypeError 也是预期的类型错误
        pass
    except Exception as e:
        # 其他意外异常 - 记录为潜在崩溃
        if not isinstance(e, (ValueError, TypeError, AttributeError)):
            log_crash("RecordManager.createRecord", data, e)
            raise  # 重新抛出以让 Hypothesis 记录


# ============================================================
# 模糊测试 2：OCRService.autoCategorize
# ============================================================

# 文本输入策略 - 包括各种边界情况
text_strategy = st.one_of(
    st.text(max_size=100000),  # 超长文本
    st.binary().map(lambda b: b.decode('utf-8', errors='ignore')),  # 二进制转文本
    st.none(),
    st.just(""),
    st.just("   "),
    st.text(alphabet=st.characters(blacklist_categories=('Cs',))),  # 特殊字符
)


@settings(
    max_examples=10000,
    deadline=None,
    verbosity=Verbosity.normal,
    phases=[Phase.generate, Phase.target],
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
    database=DirectoryBasedExampleDatabase(".hypothesis_db"),
)
@given(text=text_strategy)
def test_fuzz_auto_categorize(text):
    """
    模糊测试 OCRService.autoCategorize
    
    尝试使用各种随机文本输入来触发程序崩溃
    预期：函数应该返回一个分类字符串，不应该崩溃
    """
    service = OCRService()
    
    try:
        result = service.autoCategorize(text)
        # 验证返回值是字符串
        assert isinstance(result, str)
        # 验证返回值非空
        assert len(result) > 0
    except TypeError as e:
        # None 输入可能导致 TypeError，这是预期行为
        pass
    except Exception as e:
        # 其他意外异常 - 记录为潜在崩溃
        if not isinstance(e, (ValueError, TypeError, AttributeError)):
            log_crash("OCRService.autoCategorize", text, e)
            raise


# ============================================================
# 模糊测试 3：组合测试 - OCR到记录创建流程
# ============================================================

@settings(
    max_examples=5000,
    deadline=None,
    verbosity=Verbosity.normal,
    phases=[Phase.generate, Phase.target],
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
)
@given(
    merchant=st.text(max_size=1000),
    amount=st.one_of(st.floats(allow_nan=True, allow_infinity=True), st.integers(), st.text()),
    date_str=st.one_of(st.text(), st.none()),
)
def test_fuzz_ocr_to_record_flow(merchant, amount, date_str):
    """
    模糊测试完整的 OCR 到记录创建流程
    """
    service = OCRService()
    manager = RecordManager()
    manager.db = Mock()
    manager.db.saveData = Mock(return_value="fuzz_id")
    
    try:
        # Step 1: 分类
        category = service.autoCategorize(merchant)
        
        # Step 2: 创建记录
        record_data = {
            "type": "支出",
            "amount": amount,
            "date": date_str if date_str else "2025-01-01",
            "note": f"{merchant} - {category}"
        }
        record = manager.createRecord(record_data)
        
    except (ValueError, TypeError, AttributeError):
        # 预期的错误类型
        pass
    except Exception as e:
        log_crash("OCR_to_Record_Flow", {"merchant": merchant, "amount": amount, "date": date_str}, e)
        raise


# ============================================================
# 极端边界测试
# ============================================================

@settings(max_examples=1000, deadline=None)
@given(
    size=st.integers(min_value=0, max_value=1000000),
)
def test_fuzz_extreme_string_length(size):
    """测试极端长度的字符串输入"""
    service = OCRService()
    
    try:
        # 生成超长字符串
        long_text = "餐厅" * size
        result = service.autoCategorize(long_text)
        assert isinstance(result, str)
    except MemoryError:
        # 内存不足是预期的
        pass
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            log_crash("autoCategorize_extreme_length", f"length={size}", e)
            raise


@settings(max_examples=1000, deadline=None)
@given(
    amount=st.floats(allow_nan=True, allow_infinity=True, allow_subnormal=True),
)
def test_fuzz_extreme_float_amounts(amount):
    """测试极端浮点数金额"""
    manager = RecordManager()
    manager.db = Mock()
    manager.db.saveData = Mock(return_value="test_id")
    
    try:
        data = {
            "type": "支出",
            "amount": amount,
            "date": "2025-01-01"
        }
        result = manager.createRecord(data)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            log_crash("createRecord_extreme_float", f"amount={amount}", e)
            raise


if __name__ == "__main__":
    import time
    
    print("=" * 60)
    print("模糊测试 (Fuzz Testing) - Hypothesis")
    print("=" * 60)
    print(f"开始时间: {datetime.now().isoformat()}")
    print(f"崩溃日志: {CRASH_LOG_FILE}")
    print()
    
    start_time = time.time()
    
    # 清空之前的崩溃日志
    with open(CRASH_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"模糊测试崩溃日志\n")
        f.write(f"开始时间: {datetime.now().isoformat()}\n")
    
    tests = [
        ("RecordManager.createRecord", test_fuzz_create_record),
        ("OCRService.autoCategorize", test_fuzz_auto_categorize),
        ("OCR到记录流程", test_fuzz_ocr_to_record_flow),
        ("极端字符串长度", test_fuzz_extreme_string_length),
        ("极端浮点数金额", test_fuzz_extreme_float_amounts),
    ]
    
    for name, test_func in tests:
        print(f"\n{'─'*40}")
        print(f"运行: {name}")
        print(f"{'─'*40}")
        try:
            test_func()
            print(f"✅ {name} - 完成")
        except Exception as e:
            print(f"❌ {name} - 发现崩溃: {e}")
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print()
    print("=" * 60)
    print(f"测试完成!")
    print(f"结束时间: {datetime.now().isoformat()}")
    print(f"总耗时: {elapsed:.2f} 秒 ({elapsed/60:.2f} 分钟)")
    print(f"崩溃日志: {CRASH_LOG_FILE}")
    print("=" * 60)
