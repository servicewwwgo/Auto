"""
启动入口：将 stdout/stderr 重定向到 log.txt 后执行 main.py。
供 .vscode/launch.json 使用，便于调试时把标准输出保存到文件。
"""
import runpy
import sys

if __name__ == "__main__":
    with open("log.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        sys.stderr = f
        # 让 main.py 看到正确的脚本名
        sys.argv[0] = "main.py"
        runpy.run_path("main.py", run_name="__main__")
