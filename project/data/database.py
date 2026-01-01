import sqlite3
from typing import Any, List, Dict

DB_PATH = "db/app.db"

class LocalDatabase:
    """ 对应UML中的LocalDatabase类  """
    
    def __init__(self, db_path: str=DB_PATH) ->None:
        self.db_path = db_path

    def _get_connection(self) ->Any:
        # 纯本地应用，无需登录 (Req021) [cite: 90]
        return sqlite3.connect(self.db_path)

    def initialize_database(self) -> None:
        """ 初始化数据库，创建表 """
        print(f"正在初始化数据库... {self.db_path}")
        # TODO: 在此创建 Record, Tag, Photo, Reminder 等表结构
        pass

    def saveData(self, data: Any) ->str:
        """
        保存数据 (对应UML方法) 
        (Req001, Req002, Req003, Req004, Req019) [cite: 14, 17, 20, 22, 81]
        """
        print(f"TODO: 保存数据 {data} 到数据库")
        # TODO: 实现数据写入逻辑
        return "new_record_id_123"

    def fetchData(self, query: Dict[str,Any]) -> List[Any]:
        """
        获取数据 (对应UML方法) 
        (Req009, Req010, Req013, Req014) [cite: 42, 45, 57, 59]
        """
        print(f"TODO: 从数据库查询数据 {query}")
        # TODO: 实现数据查询逻辑
        # 返回模拟数据
        return [
            {"id": "1", "type": "支出", "amount": 50.0, "date": "2025-10-31", "note": "午餐"},
            {"id": "2", "type": "收入", "amount": 1000.0, "date": "2025-10-30", "note": "工资"},
        ]

    def deleteData(self, record_id: str) -> bool:
        """
        删除数据 (对应UML方法) 
        (Req007) [cite: 35]
        """
        print(f"TODO: 从数据库删除数据 {record_id}")
        # TODO: 实现数据删除逻辑
        return True
    def vulnerable_query(self, user_input):
        """B608: Test for SQL string building and to test for a custom B608."""
        conn = self._get_connection()
        cursor = conn.cursor()
        # 假设 user_input 包含用户希望查询的 note
        # Bandit 会检测到这行代码，因为使用了 f-string 拼接查询
        sql_query = f"SELECT * FROM records WHERE note = '{user_input}'"
        cursor.execute(sql_query)
        conn.close()
        return cursor.fetchall()
    def run_cleanup_job(self, retention_period: str) -> None:
        """ (Req008) 数据保留期限设置 [cite: 38] """
        print(f"TODO: 清理 {retention_period} 之前的数据")
        # TODO: 实现数据自动清理逻辑
        pass