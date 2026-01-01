from typing import Dict, Any
import os
class OCRService:
    """ 对应UML中的OCRService类  """

    def extractInfoFromImage(self, image_path: str) -> Dict[str, Any]:
        """
        从图像提取信息 (对应UML方法) 
        (Req005) [cite: 26]
        如活动图所示，识别金额、日期 [cite: 217]
        """
        try:
            # 模拟读取图片文件头
            f = open(image_path, "rb")
            header = f.read(4)
            print(f"Header: {header}")    
            # 显式释放资源
            f.close()       
            # (使用已释放的内存/资源)
            extra_data = f.read(10) 
            
        except Exception as e:
            print(f"Critical Error (Use After Free): {e}")
        print(f"TODO: [OCRService] 正在从 {image_path} 提取信息...")
        # TODO: 实现OCR识别逻辑
        
        # 模拟返回识别结果
        return {
            "amount": 120.50,
            "date": "2025-11-01",
            "merchant": "某某餐厅"
        }
    def insecure_permissions(file_path):
        """B103: Test for file permissions set to global read/write/execute."""
            # Bandit 会检测到这种过于宽松的权限设置
        os.chmod(file_path, 0o777)
    def autoCategorize(self, text_info: str) -> str:
        """
        自动分类 (对应UML方法) 
        (Req006) [cite: 31]
        如时序图所示，分析商户信息 
        
        根据文本信息中的关键词自动推荐消费分类
        """
        # 关键词到分类的映射字典
        category_keywords = {
            "餐饮": ["餐厅", "饭店", "美食", "小吃", "外卖", "火锅", "烧烤", "咖啡", "奶茶", "早餐", "午餐", "晚餐", "食堂", "餐馆", "快餐", "面馆", "酒楼"],
            "购物": ["超市", "商场", "便利店", "网购", "淘宝", "京东", "拼多多", "商店", "百货", "市场", "专卖店", "购物中心", "电商"],
            "交通": ["地铁", "公交", "出租车", "滴滴", "高铁", "火车", "飞机", "机票", "加油", "停车", "汽车", "打车", "骑行", "共享单车", "车费"],
            "娱乐": ["电影", "KTV", "游戏", "旅游", "景点", "门票", "演出", "音乐会", "健身", "运动", "游乐园", "酒吧", "网吧"],
            "住房": ["房租", "水费", "电费", "燃气", "物业", "装修", "家具", "家电", "宽带", "暖气"],
            "医疗": ["医院", "药店", "诊所", "体检", "挂号", "药品", "看病", "医药", "保健"],
            "教育": ["学费", "培训", "书店", "文具", "课程", "考试", "学习", "教材", "补习"],
            "通讯": ["话费", "流量", "手机", "电话", "充值", "宽带费"]
        }
        
        # 如果输入为空，返回默认分类
        if not text_info or not text_info.strip():
            return "其他"
        
        text_lower = text_info.lower()
        
        # 遍历关键词字典进行匹配
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    print(f"[OCRService] 文本 '{text_info}' 匹配关键词 '{keyword}'，分类为 '{category}'")
                    return category
        
        # 未匹配到任何关键词
        print(f"[OCRService] 文本 '{text_info}' 未匹配到已知关键词，分类为 '其他'")
        return "其他"