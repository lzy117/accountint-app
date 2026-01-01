"""
集成测试模块

测试方法：自底向上 (Bottom-Up) 集成测试
- 先测试底层模块的集成 (Database + RecordManager)
- 再测试上层业务流程 (OCRService + RecordManager 端到端流程)

测试组：
1. 数据层集成测试：RecordManager + LocalDatabase
2. 业务流程集成测试：OCRService + RecordManager (OCR识别到记账完整流程)
"""

import pytest
import sys
import os
from datetime import date
from unittest.mock import Mock, patch

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.record_manager import RecordManager
from logic.ocr_service import OCRService
from data.database import LocalDatabase
from data.models import RecordType


# ============================================================
# 集成测试组 1：数据层集成 (RecordManager + LocalDatabase)
# ============================================================

class TestIntegrationRecordManagerDatabase:
    """
    集成测试组 1：RecordManager 与 LocalDatabase 的集成
    
    测试目的：验证 RecordManager 能正确调用 LocalDatabase 进行数据持久化
    测试方法：自底向上集成，使用 Mock 模拟数据库响应
    """
    
    @pytest.fixture
    def integrated_manager(self):
        """创建带有模拟数据库的 RecordManager"""
        manager = RecordManager()
        # 使用 Mock 模拟数据库行为
        manager.db = Mock(spec=LocalDatabase)
        return manager
    
    def test_integration_create_and_save_income_record(self, integrated_manager):
        """
        集成测试 1.1：创建收入记录并保存到数据库"""
        # 配置 Mock
        integrated_manager.db.saveData = Mock(return_value="income_001")
        
        # 输入数据
        input_data = {
            "type": "收入",
            "amount": 8000.0,
            "date": "2025-12-25",
            "note": "年终奖金"
        }
        # 执行集成操作
        record = integrated_manager.createRecord(input_data)
        # 验证数据库被正确调用
        integrated_manager.db.saveData.assert_called_once()
        saved_data = integrated_manager.db.saveData.call_args[0][0]
        # 验证传递给数据库的数据
        assert saved_data["type"] == "收入"
        assert saved_data["amount"] == 8000.0
        assert saved_data["date"] == date(2025, 12, 25)  # 日期被转换
        
        # 验证返回的 Record 对象
        assert record.record_id == "income_001"
        assert record.type == "收入"
        assert record.amount == 8000.0
        assert record.note == "年终奖金"
    
    def test_integration_create_and_save_expense_record(self, integrated_manager):
        """
        集成测试 1.2：创建支出记录并保存到数据库
        """
        integrated_manager.db.saveData = Mock(return_value="expense_002")
        input_data = {
            "type": "支出",
            "amount": 299.0,
            "date": "2025-12-20",
            "note": "购买书籍"
        }
        record = integrated_manager.createRecord(input_data)
        # 验证调用链
        assert integrated_manager.db.saveData.called
        assert record.record_id == "expense_002"
        assert record.type == "支出"
    
    def test_integration_create_record_validation_before_save(self, integrated_manager):
        """
        集成测试 1.3：验证数据校验在保存前执行
        
        测试目的：确保无效数据不会到达数据库层
        """
        integrated_manager.db.saveData = Mock(return_value="should_not_be_called")
        
        invalid_data = {
            "type": "借款",  # 无效类型
            "amount": 100.0,
            "date": "2025-12-01"
        }
        
        # 验证校验失败时不调用数据库
        with pytest.raises(ValueError):
            integrated_manager.createRecord(invalid_data)
        
        # 确认数据库未被调用
        integrated_manager.db.saveData.assert_not_called()
    
    def test_integration_get_records_from_database(self, integrated_manager):
        """
        集成测试 1.4：从数据库获取记录列表
        """
        mock_db_data = [
            {"id": "rec_001", "type": "支出", "amount": 50.0, "date": "2025-11-01", "note": "午餐"},
            {"id": "rec_002", "type": "收入", "amount": 5000.0, "date": "2025-11-01", "note": "工资"},
        ]
        integrated_manager.db.fetchData = Mock(return_value=mock_db_data)
        
        # 执行查询
        records = integrated_manager.getRecords({"date": "2025-11"})
        
        # 验证数据库被调用
        integrated_manager.db.fetchData.assert_called_once_with({"date": "2025-11"})
        
        # 验证返回的对象列表
        assert len(records) == 2
        assert records[0].record_id == "rec_001"
        assert records[0].type == "支出"
        assert records[1].amount == 5000.0
    
    def test_integration_empty_records_from_database(self, integrated_manager):
        """
        集成测试 1.5：数据库返回空结果
        """
        integrated_manager.db.fetchData = Mock(return_value=[])
        
        records = integrated_manager.getRecords({"type": "不存在"})
        
        assert records == []


# ============================================================
# 集成测试组 2：业务流程集成 (OCRService + RecordManager)
# ============================================================

class TestIntegrationOCRToRecord:
    """
    集成测试组 2：OCR 识别到记账的完整业务流程
    
    测试目的：验证从 OCR 图片识别到自动分类再到创建记录的端到端流程
    测试方法：自底向上集成，模拟完整用户操作流程
    """
    
    @pytest.fixture
    def ocr_service(self):
        """创建 OCRService 实例"""
        return OCRService()
    
    @pytest.fixture
    def record_manager(self):
        """创建带有模拟数据库的 RecordManager"""
        manager = RecordManager()
        manager.db = Mock(spec=LocalDatabase)
        manager.db.saveData = Mock(return_value="auto_record_001")
        return manager
    
    def test_integration_ocr_extract_to_categorize(self, ocr_service):
        """
        集成测试 2.1：OCR 提取信息后自动分类
        
        测试流程：
        1. 模拟 OCR 从图片提取商户信息
        2. 将商户信息传入 autoCategorize
        3. 验证分类结果正确
        """
        # 模拟 OCR 提取结果
        ocr_result = {
            "amount": 88.0,
            "date": "2025-12-15",
            "merchant": "星巴克咖啡"
        }
        
        # 使用商户信息进行分类
        category = ocr_service.autoCategorize(ocr_result["merchant"])
        
        # 验证分类结果
        assert category == "餐饮"
    
    def test_integration_full_ocr_to_record_flow(self, ocr_service, record_manager):
        """
        集成测试 2.2：完整的 OCR 到记录创建流程
        
        测试流程（端到端）：
        1. OCR 识别图片提取信息（模拟）
        2. 根据商户信息自动分类
        3. 组合数据创建记录
        4. 验证完整流程的数据一致性
        """
        # Step 1: 模拟 OCR 识别结果
        ocr_result = {
            "amount": 156.0,
            "date": "2025-12-10",
            "merchant": "沃尔玛超市"
        }
        
        # Step 2: 自动分类
        category = ocr_service.autoCategorize(ocr_result["merchant"])
        assert category == "购物"
        
        # Step 3: 组合数据创建记录
        record_data = {
            "type": "支出",  # OCR 识别的通常是支出
            "amount": ocr_result["amount"],
            "date": ocr_result["date"],
            "note": f"{ocr_result['merchant']} - {category}"
        }
        
        record = record_manager.createRecord(record_data)
        
        # Step 4: 验证完整流程
        assert record.type == "支出"
        assert record.amount == 156.0
        assert "沃尔玛超市" in record.note
        assert "购物" in record.note
    
    def test_integration_ocr_unknown_merchant_flow(self, ocr_service, record_manager):
        """
        集成测试 2.3：OCR 识别未知商户的处理流程
        
        测试目的：验证当商户信息无法识别分类时的处理
        """
        # 模拟 OCR 识别结果 - 未知商户
        ocr_result = {
            "amount": 200.0,
            "date": "2025-12-08",
            "merchant": "ABC贸易公司"
        }
        
        # 自动分类 - 应返回 "其他"
        category = ocr_service.autoCategorize(ocr_result["merchant"])
        assert category == "其他"
        
        # 仍然可以创建记录
        record_data = {
            "type": "支出",
            "amount": ocr_result["amount"],
            "date": ocr_result["date"],
            "note": f"{ocr_result['merchant']} - 待分类"
        }
        
        record = record_manager.createRecord(record_data)
        assert record.amount == 200.0
    
    def test_integration_ocr_restaurant_full_flow(self, ocr_service, record_manager):
        """
        集成测试 2.4：餐饮消费完整流程
        """
        # OCR 结果
        ocr_result = {
            "amount": 68.0,
            "date": "2025-12-05",
            "merchant": "海底捞火锅"
        }
        
        # 分类
        category = ocr_service.autoCategorize(ocr_result["merchant"])
        assert category == "餐饮"
        
        # 创建记录
        record_data = {
            "type": "支出",
            "amount": ocr_result["amount"],
            "date": ocr_result["date"],
            "note": f"{category}: {ocr_result['merchant']}"
        }
        
        record = record_manager.createRecord(record_data)
        
        assert record.record_id == "auto_record_001"
        assert "餐饮" in record.note
    
    def test_integration_ocr_transport_full_flow(self, ocr_service, record_manager):
        """
        集成测试 2.5：交通消费完整流程
        """
        ocr_result = {
            "amount": 35.0,
            "date": "2025-12-01",
            "merchant": "滴滴出行"
        }
        
        category = ocr_service.autoCategorize(ocr_result["merchant"])
        assert category == "交通"
        
        record_data = {
            "type": "支出",
            "amount": ocr_result["amount"],
            "date": ocr_result["date"],
            "note": f"{category}: {ocr_result['merchant']}"
        }
        
        record = record_manager.createRecord(record_data)
        assert "交通" in record.note


# ============================================================
# 集成测试组 3：异常处理集成测试
# ============================================================

class TestIntegrationErrorHandling:
    """
    集成测试组 3：异常处理的集成测试
    
    测试目的：验证各模块间的错误传递和处理机制
    """
    
    @pytest.fixture
    def record_manager(self):
        manager = RecordManager()
        manager.db = Mock(spec=LocalDatabase)
        return manager
    
    def test_integration_invalid_ocr_data_to_record(self, record_manager):
        """
        集成测试 3.1：OCR 返回无效数据时的处理
        
        测试目的：验证无效 OCR 数据在创建记录时被正确拦截
        """
        # 模拟 OCR 返回无效金额
        ocr_result = {
            "amount": -50.0,  # 无效金额
            "date": "2025-12-01",
            "merchant": "测试商户"
        }
        
        record_data = {
            "type": "支出",
            "amount": ocr_result["amount"],
            "date": ocr_result["date"],
            "note": ocr_result["merchant"]
        }
        
        # 验证校验层拦截无效数据
        with pytest.raises(ValueError) as excinfo:
            record_manager.createRecord(record_data)
        
        assert "金额必须是正数" in str(excinfo.value)
    
    def test_integration_invalid_date_from_ocr(self, record_manager):
        """
        集成测试 3.2：OCR 返回无效日期时的处理
        """
        ocr_result = {
            "amount": 100.0,
            "date": "invalid-date",  # 无效日期
            "merchant": "测试商户"
        }
        
        record_data = {
            "type": "支出",
            "amount": ocr_result["amount"],
            "date": ocr_result["date"],
            "note": ocr_result["merchant"]
        }
        
        with pytest.raises(ValueError) as excinfo:
            record_manager.createRecord(record_data)
        
        assert "日期格式无效" in str(excinfo.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
