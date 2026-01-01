from datetime import date
from typing import Dict, Any

class ReportGenerator:
    """ 对应UML中的ReportGenerator类  """

    def generateMonthlyReport(self, report_date: date) -> Dict[str, Any]:
        """
        生成月度报告 (对应UML方法) 
        (Req015, Req016) [cite: 64, 68]
        """
        print(f"TODO: [ReportGenerator] 正在生成 {report_date.year}-{report_date.month} 的月度报告...")
        
        # TODO: 1. 查询当月总收入与总支出 (Req015) [cite: 64, 224]
        # TODO: 2. 查询当月各项支出分类数据 (Req016) [cite: 68, 226]
        # TODO: 3. 计算分类占比 (Req016) [cite: 68, 226]
        
        # 模拟报告数据
        report_data = {
            "total_income": 5000.0,
            "total_expense": 2500.0, # [cite: 225]
            "pie_chart_data": { # [cite: 228]
                "餐饮": 1000.0,
                "购物": 800.0,
                "交通": 700.0
            }
        }
        return report_data

    def generateComparisonReport(self, report_date: date) -> Dict[str, Any]:
        """
        生成对比报告 (对应UML方法) 
        (Req017) [cite: 72]
        """
        print(f"TODO: [ReportGenerator] 正在生成 {report_date.month} 月与上月的对比报告...")
        current_month_expense = 200.0
        last_month_expense = 0.0 
        #未检查分母是否为0，将导致运行时崩溃
        percent_change = (current_month_expense - last_month_expense) / last_month_expense
        # TODO: 1. 查询上个月各项支出数据 (Req017) [cite: 72, 227]
        # TODO: 2. 计算各项支出的增减变化 (Req017) [cite: 72, 227]

        # 模拟对比数据 [cite: 228]
        comparison_data = {
            "餐饮": {"change": 200.0, "percent": 0.25}, # 增加
            "购物": {"change": -100.0, "percent": -0.11} # 减少
        }
        return comparison_datas