import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
class SettingsView(tk.Toplevel):
    def __init__(self, master:Any)->None:
        super().__init__(master)
        self.title("设置")
        self.geometry("300x400")
        self.create_widgets()

    def create_widgets(self) -> None:
        # (Req026) 
        ttk.Label(self, text="颜色主题:").pack(pady=5)
        theme_cb = ttk.Combobox(self, values=["亮色", "深色 (TODO)"])
        theme_cb.pack(pady=5)
        
        # (Req024) 
        ttk.Label(self, text="字体大小:").pack(pady=5)
        font_cb = ttk.Combobox(self, values=["标准", "大字模式 (TODO)"])
        font_cb.pack(pady=5)

        # (Req027) 
        ttk.Label(self, text="图标包:").pack(pady=5)
        icon_cb = ttk.Combobox(self, values=["默认", "风格A (TODO)"])
        icon_cb.pack(pady=5)

        # (Req025) [cite: 106]
        bg_btn = ttk.Button(self, text="自定义背景图片 (TODO)", command=self.set_background)
        bg_btn.pack(pady=10)
        
        # (Req008) [cite: 38]
        ttk.Label(self, text="数据保留期限:").pack(pady=5)
        retention_cb = ttk.Combobox(self, values=["永久保存", "保存一年", "保存半年"])
        retention_cb.pack(pady=5)
        
        save_btn = ttk.Button(self, text="保存设置", command=self.save_settings)
        save_btn.pack(pady=20)

    def set_background(self)->None:
        messagebox.showinfo("TODO", "(Req025) 实现自定义背景图片 [cite: 106]")
        
    def save_settings(self)->None:
        # TODO: 保存所有设置
        messagebox.showinfo("TODO", "设置已保存 (TODO)")
        self.destroy()