import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from logic.report_generator import ReportGenerator
from typing import Any
class ReportView(tk.Toplevel):
    def __init__(self, master:Any)->None:
        super().__init__(master)
        self.title("月度统计报告")
        self.geometry("500x600")
        
        self.generator = ReportGenerator() # 
        self.create_widgets()

    def create_widgets(self) ->None:
        # (Req015) [cite: 64]
        ttk.Label(self, text="选择月份:").pack(pady=5)
        # TODO: 使用月份选择控件
        self.month_entry = ttk.Entry(self)
        self.month_entry.insert(0, date.today().strftime("%Y-%m"))
        self.month_entry.pack(pady=5)
        
        load_btn = ttk.Button(self, text="生成报告", command=self.load_report)
        load_btn.pack(pady=10)
        
        self.report_text = tk.Text(self, height=20, width=60)
        self.report_text.pack(pady=10, padx=10)

    def load_report(self) -> None:
        self.report_text.delete("1.0", tk.END)
        
        try:
            # TODO: 解析 self.month_entry.get() 为 date 对象
            report_date = date.today()
            
            # 1. 获取月度数据 (Req015, Req016) [cite: 64, 68]
            report = self.generator.generateMonthlyReport(report_date) # [cite: 4, 224, 225, 226]
            
            # 2. 获取对比数据 (Req017) [cite: 72]
            comparison = self.generator.generateComparisonReport(report_date) # [cite: 4, 227]
            
            # 3. 整合渲染 (Req016, Req017) [cite: 68, 72, 228]
            display_text = f"--- {report_date.month}月 总结 ---\n"
            display_text += f"总收入: {report['total_income']}\n"
            display_text += f"总支出: {report['total_expense']}\n\n"
            
            display_text += "--- 支出分类 (饼图) ---\n" # [cite: 68]
            for category, amount in report['pie_chart_data'].items():
                display_text += f"{category}: {amount}\n"
            display_text += "TODO: 在此处渲染饼状图\n\n"
            
            display_text += "--- 与上月对比 ---\n" # [cite: 72]
            for category, change in comparison.items():
                display_text += f"{category}: {change['change']} ({change['percent'] * 100:.1f}%)\n"
            
            self.report_text.insert("1.0", display_text) # [cite: 228]
            
        except Exception as e:
            messagebox.showerror("错误", f"生成报告失败: {e}")