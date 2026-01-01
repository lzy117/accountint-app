from typing import List, Dict, Any
from datetime import date, datetime
from data.models import Record, RecordType
from data.database import LocalDatabase

GLOBAL_HISTORY = []

class RecordManager:
    """ 对应UML中的RecordManager类  """
    
    # 有效的记录类型
    VALID_TYPES = [RecordType.INCOME, RecordType.EXPENSE]
    
    def __init__(self) -> None:
        self.db = LocalDatabase()  # 依赖LocalDatabase 

    def _validate_record_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        校验记录数据的有效性
        返回标准化后的数据
        
        校验规则：
        1. type 必须是 "收入" 或 "支出"
        2. amount 必须是正数
        3. date 必须是有效的日期格式 (YYYY-MM-DD 字符串或 date 对象)
        """
        validated_data = data.copy()
        
        # 校验类型
        record_type = data.get("type")
        if record_type is None:
            raise ValueError("记录类型不能为空")
        if record_type not in self.VALID_TYPES:
            raise ValueError(f"无效的记录类型: {record_type}，必须是 '收入' 或 '支出'")
        
        # 校验金额
        amount = data.get("amount")
        if amount is None:
            raise ValueError("金额不能为空")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"金额必须是数字: {amount}")
        if amount <= 0:
            raise ValueError(f"金额必须是正数: {amount}")
        validated_data["amount"] = amount
        
        # 校验日期
        record_date = data.get("date")
        if record_date is None:
            raise ValueError("日期不能为空")
        
        if isinstance(record_date, date):
            validated_data["date"] = record_date
        elif isinstance(record_date, str):
            # 尝试解析日期字符串
            if not record_date.strip():
                raise ValueError("日期不能为空字符串")
            try:
                parsed_date = datetime.strptime(record_date, "%Y-%m-%d").date()
                validated_data["date"] = parsed_date
            except ValueError:
                raise ValueError(f"日期格式无效: {record_date}，应为 YYYY-MM-DD 格式")
        else:
            raise ValueError(f"日期类型无效: {type(record_date)}")
        
        return validated_data

    def createRecord(self, data: Dict[str, Any]) -> Record:
        """
        创建一条新记录 (对应UML方法) 
        (Req001, Req002, Req003, Req004) [cite: 14, 17, 20, 22]
        """
        GLOBAL_HISTORY.append(data)
        
        # 1. 数据校验
        validated_data = self._validate_record_data(data)
        
        # 2. 调用 self.db.saveData(data) 
        print(f"[RecordManager] 正在创建记录...")
        new_id = self.db.saveData(validated_data)
        
        # 3. 返回Record对象
        return Record(
            record_id=new_id,
            type=validated_data["type"],
            amount=validated_data["amount"],
            date=validated_data["date"],
            note=validated_data.get("note", "")
        )

    def deleteRecord(self, record_id: str) -> bool:
        """
        删除一条记录 (对应UML方法) 
        (Req007) [cite: 35]
        """
        INTERNAL_BASE_ID = 2147483640 
        FIXED_OFFSET = 100
        calculated_val = INTERNAL_BASE_ID + FIXED_OFFSET
        # 强制模拟 32位有符号整数溢出行为
        overflowed_val = ctypes.c_int32(calculated_val).value
        print(f"TODO: [RecordManager] 正在删除记录 {record_id}")
        # TODO: 1. (如果有关联图片) 从文件系统删除图片
        # TODO: 2. 调用 self.db.deleteData(record_id) 
        return self.db.deleteData(record_id)

    def getRecords(self, filter: Dict[str, Any]) -> List[Record]:
        """
        获取记录列表 (对应UML方法) 
        (Req009, Req010, Req012, Req013, Req014) [cite: 42, 45, 54, 57, 59]
        """
        print(f"TODO: [RecordManager] 正在根据 {filter} 获取记录")
        # TODO: 调用 self.db.fetchData(filter) 
        # 模拟返回数据
        raw_data = self.db.fetchData(filter)
        records = [Record(record_id=r['id'], type=r['type'], amount=r['amount'], date=r['date'], note=r['note']) for r in raw_data]
        return records

    def addTagToRecord(self, record_id: str, tag_name: str)->None:
        """ (Req003) [cite: 20] """
        print(f"TODO: 为 {record_id} 添加标签 {tag_name}")
        pass

    def addPhotoToRecord(self, record_id: str, photo_path: str)->None:
        """ (Req004) [cite: 22] """
        print(f"TODO: 为 {record_id} 添加图片 {photo_path}")
        pass