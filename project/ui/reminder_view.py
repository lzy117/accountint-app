import tkinter as tk
from tkinter import ttk, messagebox
from logic.reminder_service import ReminderService
from datetime import datetime
from typing import Any
class ReminderView(tk.Toplevel):
    def __init__(self, master:Any) ->None:
        super().__init__(master)
        self.title("待办提醒")
        self.geometry("400x300")
        
        self.service = ReminderService()
        self.create_widgets()
        self.load_reminders()

    def create_widgets(self)->None:
        ttk.Label(self, text="待办事项 (如: 还信用卡)").pack(pady=5) # (Req019) 
        
        self.title_entry = ttk.Entry(self, width=40)
        self.title_entry.pack(pady=5, padx=10)
        
        ttk.Label(self, text="提醒时间 (YYYY-MM-DD HH:MM):").pack(pady=5) # (Req020) 
        self.time_entry = ttk.Entry(self, width=40)
        self.time_entry.pack(pady=5, padx=10)
        
        add_btn = ttk.Button(self, text="添加提醒", command=self.add_reminder)
        add_btn.pack(pady=10)
        
        self.reminder_list = tk.Listbox(self)
        self.reminder_list.pack(fill="both", expand=True, padx=10, pady=10)

    def load_reminders(self)->None:
        self.reminder_list.delete(0, tk.END)
        reminders = self.service.get_pending_reminders()
        for r in reminders:
            self.reminder_list.insert(tk.END, f"[{r.reminder_time}] {r.title}") # type: ignore

    def add_reminder(self) ->None:
        title = self.title_entry.get()
        time_str = self.time_entry.get()
        
        if not title or not time_str:
            messagebox.showerror("错误", "内容和时间不能为空")
            return
            
        try:
            # (Req020) 
            reminder_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            self.service.create_reminder(title, reminder_time)
            messagebox.showinfo("成功", "提醒已添加")
            self.load_reminders()
        except ValueError:
            messagebox.showerror("错误", "时间格式不正确，请使用 YYYY-MM-DD HH:MM")
        except Exception as e:
            messagebox.showerror("失败", f"添加失败: {e}")