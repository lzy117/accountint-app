import os
import sys

# 1. 定义 Mock 基础类 (全局定义，确保可见性)
class MockTk:
    """ 模拟 tk.Tk 类 """
    def __init__(self, *args, **kwargs):
        pass
    def title(self, *args, **kwargs):
        pass
    def geometry(self, *args, **kwargs):
        pass
    def mainloop(self):
        pass
    def pack(self, *args, **kwargs):
        pass
    # 捕获所有属性访问，返回自身或新 Mock，防止 AttributeError
    def __getattr__(self, name):
        return MockTk

# 2. 定义 Mock 模块类
class MockModule:
    """ 模拟 tkinter 模块 """
    Tk = MockTk
    Frame = MockTk
    Label = MockTk
    Button = MockTk
    Entry = MockTk
    Toplevel = MockTk
    StringVar = MockTk
    DoubleVar = MockTk
    # 模拟 ttk 和其他子模块
    def __getattr__(self, name):
        return MockTk

# 3. 检测模式
IS_ESBMC_MODE = os.environ.get("ESBMC_MODE") == "TRUE"

# 4. 设置 BaseClass 和 注入 Mock
if IS_ESBMC_MODE:
    # 注入 Mock 模块实例到 sys.modules
    # 这样 ui/main_view.py 中的 import tkinter 就会得到这个 Mock 对象
    mock_module_instance = MockModule()
    sys.modules['tkinter'] = mock_module_instance
    sys.modules['tkinter.ttk'] = mock_module_instance
    
    # 明确指定基类为 MockTk 类
    BaseClass = MockTk
else:
    # 正常模式导入
    import tkinter
    BaseClass = tkinter.Tk

# 5. 导入业务逻辑 (必须在 sys.modules 注入之后)
from ui.main_view import MainView
from data.database import LocalDatabase

# 6. 定义 App 类
# 此时 BaseClass 是具体的类 (MockTk 或 tkinter.Tk)，不再是 Any
class App(BaseClass):
    def __init__(self):
        super().__init__()
        
        # 仅在非 ESBMC 模式下执行 GUI 设置
        if not IS_ESBMC_MODE:
            self.title("记账本 App")
            self.geometry("450x700")

        # 初始化数据库核心逻辑
        db = LocalDatabase()
        db.initialize_database()

        # 加载主视图
        main_view = MainView(self)
        main_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    if not IS_ESBMC_MODE:
        app.mainloop()