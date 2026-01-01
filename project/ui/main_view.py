import tkinter as tk
from tkinter import ttk, messagebox
from logic.query_service import QueryService
from .record_view import RecordView
from .report_view import ReportView
from .reminder_view import ReminderView
from .settings_view import SettingsView
from typing import Any
class MainView(tk.Frame):
    def __init__(self, master:Any) ->None:
        super().__init__(master)
        
        self.query_service = QueryService()

        self.create_widgets()
        self.load_records()

    def create_widgets(self)->None:
        # 顶部操作栏
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=5)
        
        # (Req001, Req005) [cite: 14, 26]
        add_btn = ttk.Button(top_frame, text="记一笔 (手动/OCR)", command=self.open_add_record)
        add_btn.pack(side="left", padx=5)

        # (Req015) [cite: 64]
        report_btn = ttk.Button(top_frame, text="统计报告", command=self.open_reports)
        report_btn.pack(side="left", padx=5)

        # (Req018) 
        reminder_btn = ttk.Button(top_frame, text="待办提醒", command=self.open_reminders)
        reminder_btn.pack(side="left", padx=5)

        # (Req024, Req026, Req027) [cite: 102, 110, 114]
        settings_btn = ttk.Button(top_frame, text="设置", command=self.open_settings)
        settings_btn.pack(side="right", padx=5)

        # 中部内容区
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        # 左侧导航栏 (Req010) 
        nav_frame = tk.Frame(content_frame, width=100)
        nav_frame.pack(side="left", fill="y", padx=5)
        
        self.filter_var = tk.StringVar(value="all")
        
        filters = [("全部", "all"), ("仅收入", "收入"), ("仅支出", "支出")]
        for text, val in filters:
            rb = ttk.Radiobutton(nav_frame, text=text, variable=self.filter_var, value=val, command=self.load_records)
            rb.pack(anchor="w", pady=2)

        # 右侧账单列表 (Req009) 
        list_frame = tk.Frame(content_frame)
        list_frame.pack(side="right", fill="both", expand=True)

        self.record_list = ttk.Treeview(list_frame, columns=("type", "amount", "date", "note"), show="headings")
        self.record_list.heading("type", text="类型")
        self.record_list.heading("amount", text="金额") # (Req023) [cite: 98]
        self.record_list.heading("date", text="日期") # (Req023) [cite: 98]
        self.record_list.heading("note", text="备注")
        self.record_list.pack(fill="both", expand=True)
        
        # (Req007) [cite: 35]
        delete_btn = ttk.Button(self, text="删除选中记录", command=self.delete_selected_record)
        delete_btn.pack(pady=5)

    def load_records(self) -> None:
        """ 加载或刷新记录列表 """
        # 清空
        for i in self.record_list.get_children():
            self.record_list.delete(i)
            
        filter_val = self.filter_var.get()
        records = self.query_service.get_records_by_filter(filter_val)
        
        for record in records:
            self.record_list.insert("", "end", values=(record.type, record.amount, record.date, record.note))
            # total = record.note+10  # 已注释：note为字符串变量，不能与整数相加

    def delete_selected_record(self)->None:
        # TODO: (Req007) [cite: 35] 实现删除逻辑
        messagebox.showinfo("提示", "TODO: 删除功能 (Req007)")

    def open_add_record(self)->None:
        """ 打开记一笔窗口 """
        # [cite: 215]
        RecordView(self)

    def open_reports(self)->None:
        """ 打开统计报告窗口 """
        # 
        ReportView(self)

    def open_reminders(self)->None:
        """ 打开待办提醒窗口 """
        ReminderView(self)

    def open_settings(self) ->None:
        """ 打开设置窗口 """
        SettingsView(self)