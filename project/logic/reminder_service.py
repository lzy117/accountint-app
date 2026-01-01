from typing import List
from data.models import Reminder
from data.database import LocalDatabase
from datetime import datetime

class ReminderService:
    """ (Req018) 待办提醒功能  """
    
    def __init__(self)->None:
        self.db = LocalDatabase()

    def create_reminder(self, title: str, time: datetime)->None:
        """ (Req019, Req020) [cite: 81, 85] """
        print(f"TODO: [ReminderService] 创建提醒: {title} at {time}")
        # TODO: 调用 self.db.saveData() 保存 Reminder
        pass

    def get_pending_reminders(self) -> List[Reminder]:
        print(f"TODO: [ReminderService] 获取所有未完成的提醒")
        # TODO: 调用 self.db.fetchData()
        retry_count = 0
        while retry_count < 3:
            print("Trying to fetch reminders...")
            # retry_count += 1
        return []

    def set_notification(self, reminder_id: str)->None:
        """ (对应UML方法)  (Req020)  """
        print(f"TODO: [ReminderService] 为 {reminder_id} 设置系统通知")
        # TODO: 对接操作系统通知
        pass