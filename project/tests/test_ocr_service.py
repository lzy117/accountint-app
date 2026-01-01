"""
OCRService.autoCategorize 单元测试

测试策略：条件覆盖 + 路径覆盖
覆盖以下场景：
1. 各类关键词匹配 (餐饮/购物/交通/娱乐/住房/医疗/教育/通讯)
2. 空输入处理
3. 无匹配关键词返回 "其他"
4. 多关键词优先级测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.ocr_service import OCRService


class TestOCRServiceAutoCategorize:
    """OCRService.autoCategorize 测试类"""
    
    @pytest.fixture
    def service(self):
        """创建 OCRService 实例"""
        return OCRService()
    
    # ==================== 餐饮分类测试 ====================
    
    def test_categorize_restaurant(self, service):
        """测试1: '餐厅' 关键词 -> 餐饮"""
        result = service.autoCategorize("某某餐厅")
        assert result == "餐饮"
    
    def test_categorize_hotel_dining(self, service):
        """测试2: '饭店' 关键词 -> 餐饮"""
        result = service.autoCategorize("北京饭店")
        assert result == "餐饮"
    
    def test_categorize_takeout(self, service):
        """测试3: '外卖' 关键词 -> 餐饮"""
        result = service.autoCategorize("美团外卖")
        assert result == "餐饮"
    
    def test_categorize_coffee(self, service):
        """测试4: '咖啡' 关键词 -> 餐饮"""
        result = service.autoCategorize("星巴克咖啡")
        assert result == "餐饮"
    
    def test_categorize_hotpot(self, service):
        """测试5: '火锅' 关键词 -> 餐饮"""
        result = service.autoCategorize("海底捞火锅")
        assert result == "餐饮"
    
    # ==================== 购物分类测试 ====================
    
    def test_categorize_supermarket(self, service):
        """测试6: '超市' 关键词 -> 购物"""
        result = service.autoCategorize("沃尔玛超市")
        assert result == "购物"
    
    def test_categorize_mall(self, service):
        """测试7: '商场' 关键词 -> 购物"""
        result = service.autoCategorize("万达商场")
        assert result == "购物"
    
    def test_categorize_convenience_store(self, service):
        """测试8: '便利店' 关键词 -> 购物"""
        result = service.autoCategorize("全家便利店")
        assert result == "购物"
    
    def test_categorize_taobao(self, service):
        """测试9: '淘宝' 关键词 -> 购物"""
        result = service.autoCategorize("淘宝网购")
        assert result == "购物"
    
    def test_categorize_jd(self, service):
        """测试10: '京东' 关键词 -> 购物"""
        result = service.autoCategorize("京东商城")
        assert result == "购物"
    
    # ==================== 交通分类测试 ====================
    
    def test_categorize_subway(self, service):
        """测试11: '地铁' 关键词 -> 交通"""
        result = service.autoCategorize("地铁卡充值")
        assert result == "交通"
    
    def test_categorize_bus(self, service):
        """测试12: '公交' 关键词 -> 交通"""
        result = service.autoCategorize("公交车费")
        assert result == "交通"
    
    def test_categorize_didi(self, service):
        """测试13: '滴滴' 关键词 -> 交通"""
        result = service.autoCategorize("滴滴出行")
        assert result == "交通"
    
    def test_categorize_flight(self, service):
        """测试14: '机票' 关键词 -> 交通"""
        result = service.autoCategorize("购买机票")
        assert result == "交通"
    
    def test_categorize_gas(self, service):
        """测试15: '加油' 关键词 -> 交通"""
        result = service.autoCategorize("中石化加油")
        assert result == "交通"
    
    # ==================== 娱乐分类测试 ====================
    
    def test_categorize_movie(self, service):
        """测试16: '电影' 关键词 -> 娱乐"""
        result = service.autoCategorize("电影院")
        assert result == "娱乐"
    
    def test_categorize_ktv(self, service):
        """测试17: 'KTV' 关键词 -> 娱乐"""
        result = service.autoCategorize("KTV唱歌")
        assert result == "娱乐"
    
    def test_categorize_gym(self, service):
        """测试18: '健身' 关键词 -> 娱乐"""
        result = service.autoCategorize("健身房年卡")
        assert result == "娱乐"
    
    # ==================== 住房分类测试 ====================
    
    def test_categorize_rent(self, service):
        """测试19: '房租' 关键词 -> 住房"""
        result = service.autoCategorize("缴纳房租")
        assert result == "住房"
    
    def test_categorize_electricity(self, service):
        """测试20: '电费' 关键词 -> 住房"""
        result = service.autoCategorize("国家电网电费")
        assert result == "住房"
    
    def test_categorize_water(self, service):
        """测试21: '水费' 关键词 -> 住房"""
        result = service.autoCategorize("自来水费")
        assert result == "住房"
    
    # ==================== 医疗分类测试 ====================
    
    def test_categorize_hospital(self, service):
        """测试22: '医院' 关键词 -> 医疗"""
        result = service.autoCategorize("北京医院")
        assert result == "医疗"
    
    def test_categorize_pharmacy(self, service):
        """测试23: '药店' 关键词 -> 医疗"""
        result = service.autoCategorize("同仁堂药店")
        assert result == "医疗"
    
    # ==================== 教育分类测试 ====================
    
    def test_categorize_tuition(self, service):
        """测试24: '学费' 关键词 -> 教育"""
        result = service.autoCategorize("缴纳学费")
        assert result == "教育"
    
    def test_categorize_training(self, service):
        """测试25: '培训' 关键词 -> 教育"""
        result = service.autoCategorize("英语培训班")
        assert result == "教育"
    
    def test_categorize_bookstore(self, service):
        """测试26: '书店' 关键词 -> 教育"""
        result = service.autoCategorize("新华书店")
        assert result == "教育"
    
    # ==================== 通讯分类测试 ====================
    
    def test_categorize_phone_bill(self, service):
        """测试27: '话费' 关键词 -> 通讯"""
        result = service.autoCategorize("手机话费充值")
        assert result == "通讯"
    
    def test_categorize_data(self, service):
        """测试28: '流量' 关键词 -> 通讯"""
        result = service.autoCategorize("流量包")
        assert result == "通讯"
    
    # ==================== 边界情况测试 ====================
    
    def test_categorize_empty_string(self, service):
        """测试29: 空字符串 -> 其他"""
        result = service.autoCategorize("")
        assert result == "其他"
    
    def test_categorize_none(self, service):
        """测试30: None 输入 -> 其他"""
        result = service.autoCategorize(None)
        assert result == "其他"
    
    def test_categorize_whitespace(self, service):
        """测试31: 纯空白字符 -> 其他"""
        result = service.autoCategorize("   ")
        assert result == "其他"
    
    def test_categorize_no_match(self, service):
        """测试32: 无匹配关键词 -> 其他"""
        result = service.autoCategorize("随机文字内容")
        assert result == "其他"
    
    def test_categorize_unknown_merchant(self, service):
        """测试33: 未知商户名 -> 其他"""
        result = service.autoCategorize("ABC公司")
        assert result == "其他"
    
    # ==================== 复杂场景测试 ====================
    
    def test_categorize_long_text_with_keyword(self, service):
        """测试34: 长文本中包含关键词"""
        result = service.autoCategorize("今天在沃尔玛超市购买了日常用品")
        assert result == "购物"
    
    def test_categorize_mixed_text(self, service):
        """测试35: 混合文本 - 优先匹配第一个分类"""
        result = service.autoCategorize("餐厅消费后去超市购物")
        assert result == "餐饮"  # 餐饮在字典中排在购物前面


class TestOCRServiceExtractInfo:
    """OCRService.extractInfoFromImage 测试类"""
    
    @pytest.fixture
    def service(self):
        """创建 OCRService 实例"""
        return OCRService()
    
    @pytest.fixture
    def temp_image_file(self, tmp_path):
        """创建临时图片文件"""
        image_file = tmp_path / "test_receipt.jpg"
        # 写入模拟的JPEG文件头
        image_file.write_bytes(b'\xff\xd8\xff\xe0' + b'\x00' * 100)
        return str(image_file)
    
    def test_extract_info_from_valid_image(self, service, temp_image_file):
        """测试36: 从有效图片提取信息"""
        result = service.extractInfoFromImage(temp_image_file)
        
        # 验证返回结果结构
        assert "amount" in result
        assert "date" in result
        assert "merchant" in result
        assert result["amount"] == 120.50
    
    def test_extract_info_returns_merchant(self, service, temp_image_file):
        """测试37: 提取的商户信息正确"""
        result = service.extractInfoFromImage(temp_image_file)
        assert result["merchant"] == "某某餐厅"
    
    def test_extract_info_returns_date(self, service, temp_image_file):
        """测试38: 提取的日期格式正确"""
        result = service.extractInfoFromImage(temp_image_file)
        assert result["date"] == "2025-11-01"
    
    def test_extract_info_nonexistent_file(self, service):
        """测试39: 处理不存在的文件（应触发异常处理）"""
        # 文件不存在会触发 except 分支
        result = service.extractInfoFromImage("/nonexistent/path/image.jpg")
        # 方法仍返回模拟结果
        assert result is not None
        assert "amount" in result
    
    def test_extract_info_empty_path(self, service):
        """测试40: 空路径处理"""
        result = service.extractInfoFromImage("")
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
