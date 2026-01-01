from typing import List, Dict, Any
from data.models import Record
from .record_manager import RecordManager

class QueryService:
    """ 负责复杂的查询逻辑 """
    
    def __init__(self)->None:
        self.manager = RecordManager()

    def get_records_by_filter(self, filter_type: str = "all") -> List[Record]:
        """ (Req010) 按 "全部", "仅收入", "仅支出" 筛选"""
        query = {}
        if filter_type == "收入":
            query = {"type": "收入"}
        elif filter_type == "支出":
            query = {"type": "支出"}
        
        return self.manager.getRecords(query) # 

    def search_records(self, term: str, criteria: str) -> List[Record]:
        """
        (Req012, Req013, Req014) 
        criteria 可以是 'date', 'amount', 'tag', 'keyword' (备注)
        """
        print(f"TODO: [QueryService] 正在搜索 {criteria} = {term}")
        
        query = {criteria: term}
        return self.manager.getRecords(query)