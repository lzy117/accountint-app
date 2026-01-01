from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime

# 定义 RecordType 枚举 (Req001) [cite: 14]
class RecordType:
    INCOME = "收入"
    EXPENSE = "支出"

@dataclass
class Tag:
    """ 对应UML中的Tag类  """
    tag_id: str
    name: str

@dataclass
class Photo:
    """ 对应UML中的Photo类  """
    photo_id: str
    file_path: str # 

@dataclass
class Record:
    """ 对应UML中的Record类  """
    record_id: str
    type: str # RecordType.INCOME 或 RecordType.EXPENSE [cite: 14]
    amount: float # 
    date: date # [cite: 17]
    note: Optional[str] = "" # [cite: 17]
    tags: List[Tag] = field(default_factory=list) # [cite: 20]
    photos: List[Photo] = field(default_factory=list) # [cite: 22]

@dataclass
class Reminder:
    """ 对应UML中的Reminder类  """
    reminder_id: str
    title: str # 
    reminder_time: datetime # 
    is_completed: bool = False # 
    related_expense: Optional[str] = None # 关联的预支出项目 (Req019)