import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from logic.record_manager import RecordManager
from logic.ocr_service import OCRService
from typing import Any
class RecordView(tk.Toplevel):
    def __init__(self, master:Any) ->None:
        super().__init__(master)
        self.title("记一笔")
        self.geometry("350x400")
        
        self.manager = RecordManager() # 
        self.ocr = OCRService() # 
        
        self.create_widgets()

    def create_widgets(self) ->None:
        # OCR 导入 (Req005) [cite: 26]
        ocr_btn = ttk.Button(self, text="OCR 识图导入", command=self.run_ocr)
        ocr_btn.pack(pady=10)

        # 手动输入 (Req001, Req002) [cite: 14, 17]
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="类型:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="支出")
        ttk.Combobox(form_frame, textvariable=self.type_var, values=["支出", "收入"]).grid(row=0, column=1)

        ttk.Label(form_frame, text="金额:").grid(row=1, column=0, sticky="w")
        self.amount_var = tk.DoubleVar()
        ttk.Entry(form_frame, textvariable=self.amount_var).grid(row=1, column=1)

        ttk.Label(form_frame, text="日期:").grid(row=2, column=0, sticky="w")
        self.date_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.date_var).grid(row=2, column=1)
        # TODO: 替换为日期选择控件

        ttk.Label(form_frame, text="备注:").grid(row=3, column=0, sticky="w")
        self.note_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.note_var).grid(row=3, column=1)
        
        # (Req003) [cite: 20]
        ttk.Label(form_frame, text="标签:").grid(row=4, column=0, sticky="w")
        self.tags_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.tags_var).grid(row=4, column=1)

        # (Req004) [cite: 22]
        photo_btn = ttk.Button(form_frame, text="添加图片", command=self.add_photo)
        photo_btn.grid(row=5, column=0, columnspan=2, pady=5)
        
        save_btn = ttk.Button(self, text="保存", command=self.save_record)
        save_btn.pack(pady=20)

    def run_ocr(self) ->None:
        """ (Req005) [cite: 26] """
        file_path = filedialog.askopenfilename(title="上传支付截图") # [cite: 216]
        if not file_path:
            return

        # 1. OCR识别 (Req005) [cite: 26, 217]
        ocr_result = self.ocr.extractInfoFromImage(file_path) # [cite: 3, 213]
        
        # 2. 自动分类 (Req006) [cite: 31]
        category = self.ocr.autoCategorize(ocr_result.get("merchant", "")) # [cite: 3, 213]

        # 3. 回显数据 (活动图) 
        self.amount_var.set(ocr_result.get("amount", 0.0))
        self.date_var.set(ocr_result.get("date", ""))
        self.tags_var.set(category)
        self.note_var.set(ocr_result.get("merchant", ""))
        
        messagebox.showinfo("OCR 成功", "数据已自动填充，请核对后保存。") # [cite: 218]

    def add_photo(self) ->None:
        """ (Req004) [cite: 22] """
        file_path = filedialog.askopenfilename(title="关联图片")
        if file_path:
            print(f"TODO: 关联图片 {file_path}")
            # TODO: 将此路径保存，待保存记录时一并处理
            
    def save_record(self) ->None:
        #假设用户输入了一组标签，如果只输入一个或不输入，访问索引1会崩溃
        raw_tags = self.tags_var.get().split(',')
        if len(raw_tags) > 0:
            print(f"Second tag is: {raw_tags[1]}") # 潜在的崩溃点
        """ (Req001, Req002, Req003, Req004) [cite: 14, 17, 20, 22] """
        data = {
            "type": self.type_var.get(),
            "amount": self.amount_var.get(),
            "date": self.date_var.get(),
            "note": self.note_var.get(),
            "tags": self.tags_var.get().split(','),
            "photos": [] # TODO: 关联已添加的图片
        }
        
        # 校验数据 [cite: 219, 222]
        if not data["amount"] or not data["date"]:
            messagebox.showerror("错误", "金额和日期不能为空")
            return

        try:
            self.manager.createRecord(data) # 
            messagebox.showinfo("成功", "保存成功") # [cite: 220, 222]
            self.master.load_records() # type: ignore
            self.destroy()
        except Exception as e:
            messagebox.showerror("失败", f"保存失败: {e}")