"""
AutoJS Python SDK - 自动化浏览器操作框架

================================================================================
文件概述
================================================================================

本文件是一个完整的自动化浏览器操作框架，用于通过CDP（Chrome DevTools Protocol）
和高级指令系统控制浏览器执行各种自动化操作。该框架采用分层架构设计，从底层CDP命令
到高级工作流系统，提供了完整的浏览器自动化解决方案。

================================================================================
架构设计
================================================================================

本框架采用分层架构设计，从底层到高层分为以下几个层次：

1. 日志和异常层（Logger, Exception Classes）
   - Logger: 提供统一的日志记录功能，支持动态启用/禁用
   - AutoJSError: 框架基础异常类
   - NetworkError: 网络请求相关异常
   - ParseError: 数据解析相关异常
   - BusinessError: 业务逻辑相关异常

2. CDP命令层（CdpCommand及其子类）
   - CdpCommand: CDP命令抽象基类，定义CDP命令的基本结构
   - 子类包括：CdpConnectCommand, ListTargetsCommand, ExecuteJavascriptCommand等
   - 用于直接与Chrome浏览器的DevTools协议交互

3. 指令层（Instruction及其子类）
   - Instruction: 指令抽象基类，提供比CDP命令更高级的浏览器操作抽象
   - 子类包括：NavigateInstruction, FindElementInstruction, InputInstruction等
   - 支持延迟执行、重试机制、超时控制、错误处理等功能

4. HTTP命令层（HttpCommand及其子类）
   - HttpCommand: HTTP命令抽象基类，封装HTTP请求为命令对象
   - 子类包括：HttpBitBrowserOpenCommand, HttpBitBrowserCloseCommand等
   - 用于通过HTTP API与浏览器节点服务通信

5. 上下文层（Context）
   - Context: 工作流执行上下文，用于在工作流执行过程中传递状态、结果和变量
   - 支持变量存储、步骤状态跟踪、流程控制等功能

6. 浏览器操作层（Browser）
   - Browser: 浏览器操作类，负责与浏览器节点API通信
   - 封装了所有与节点API的交互逻辑，包括认证、请求构建、响应解析等

7. 网站抽象层（WebSite及其子类）
   - WebSite: 网站抽象基类，封装特定网站的操作逻辑
   - 子类包括：Facebook, Onestream, BitBrowser等
   - 提供网站特定的元素定义、步骤执行等功能

8. 工作流层（main函数）
   - main: 主函数，实现完整的工作流逻辑
   - 协调各个网站对象的操作，实现复杂的自动化任务

================================================================================
核心概念
================================================================================

1. CDP命令（CdpCommand）
   - CDP是Chrome DevTools Protocol的缩写，是Chrome浏览器提供的调试协议
   - CDP命令用于直接与浏览器底层交互，执行JavaScript、截图、获取网络日志等操作
   - 每个CDP命令都有唯一的ID，用于匹配请求和响应

2. 指令（Instruction）
   - 指令是比CDP命令更高级的浏览器操作抽象
   - 提供了更友好的API和更多的功能，如延迟执行、重试机制、超时控制等
   - 指令系统封装了常见的浏览器操作，如导航、元素查找、输入、鼠标键盘操作等

3. HTTP命令（HttpCommand）
   - HTTP命令用于通过HTTP API与浏览器节点服务通信
   - 主要用于浏览器管理操作，如打开、关闭、列表查询、重置等
   - 采用命令模式（Command Pattern），将HTTP请求封装为命令对象

4. 元素（ElementClass）
   - ElementClass用于封装网页中的HTML元素信息
   - 包括元素的选择器、类型、位置关系等
   - 支持多种选择器类型：CSS选择器、ID选择器、标签名选择器、文本内容选择器

5. 上下文（Context）
   - Context用于在工作流执行过程中传递状态、结果和变量
   - 支持变量存储、步骤状态跟踪、流程控制等功能
   - 每个步骤执行后，current_* 会被复制到 last_*

6. 网站对象（WebSite）
   - WebSite是特定网站的抽象，封装了网站的操作逻辑
   - 包括网站的元素定义、步骤执行等功能
   - 每个网站对象都有自己的变量存储空间

================================================================================
使用流程
================================================================================

1. 初始化Browser对象
   - 创建Browser对象，指定节点API基础URL、认证Token、节点名称等
   - Browser对象会自动通过节点名称查找节点ID

2. 创建网站对象
   - 创建WebSite子类对象（如Facebook、Onestream等）
   - 传入Browser对象和网站相关配置

3. 创建工作流上下文
   - 创建Context对象，用于在工作流执行过程中传递状态和变量

4. 执行步骤
   - 调用网站对象的步骤方法（如home_step、login_step等）
   - 步骤方法会自动执行相应的指令和命令

5. 处理结果
   - 从Context对象中获取执行结果和变量
   - 根据结果决定后续操作

================================================================================
注意事项
================================================================================

1. 日志管理
   - 默认情况下日志是禁用的，需要调用Logger.enable()启用
   - 在生产环境建议禁用日志以提高性能

2. 错误处理
   - 框架提供了多种异常类型，便于错误分类和处理
   - 指令和命令都支持ignore_error参数，可以忽略错误继续执行

3. 超时控制
   - 所有HTTP请求都有超时时间，默认180秒
   - 可以根据实际情况调整超时时间

4. 重试机制
   - 指令支持retry参数，可以设置重试次数
   - Browser类的方法都使用了retry_on_error装饰器，自动重试网络错误

5. 变量管理
   - Context对象和WebSite对象都有自己的变量存储空间
   - 变量可以在步骤之间传递和共享

================================================================================
扩展开发
================================================================================

1. 添加新的CDP命令
   - 继承CdpCommand类
   - 设置type属性
   - 实现__init__方法，设置data属性

2. 添加新的指令
   - 继承Instruction类
   - 设置type属性
   - 实现__init__方法，设置params属性

3. 添加新的HTTP命令
   - 继承HttpCommand类
   - 设置type属性
   - 实现__init__方法，设置url、method、headers、body等属性

4. 添加新的网站类
   - 继承WebSite类
   - 实现网站特定的元素定义方法
   - 实现网站特定的步骤执行方法

================================================================================
版本信息
================================================================================

版本: 1.0.0
作者: AutoJS Team
更新日期: 2024-01-01
"""

from abc import ABC
from functools import wraps
from typing import Callable, List
from urllib.parse import urlparse
from datetime import datetime
import requests
import json
import uuid
import time
import threading
import heapq
import pandas as pd
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== 日志管理器 ====================


class FileLogger:
    """
    文件日志记录模块

    功能说明：
    提供专用的文件日志记录功能，用于将日志消息写入文件。
    支持可配置的日志文件路径和编码格式。

    使用示例：
        # 记录日志到文件
        FileLogger.write_log("错误消息内容")
        
        # 自定义日志文件路径
        FileLogger.set_log_file("custom.log")
        FileLogger.write_log("自定义路径的日志")
    """
    
    # 默认日志文件路径
    _log_file = "autojs.log"
    
    # 默认文件编码
    _encoding = "utf-8"
    
    @classmethod
    def write_log(cls, level: str, message: str, **kwargs) -> None:
        """
        将日志消息写入文件
        
        功能说明：
        以追加模式打开日志文件，将日志消息写入文件末尾。
        如果文件不存在会自动创建，如果存在则追加内容。
        
        Args:
            log_message (str): 要写入的日志消息内容
            **kwargs: 额外的上下文信息，以关键字参数形式传递
        
        Returns:
            None: 无返回值
        
        Example:
            FileLogger.write_log("[2024-01-01 12:00:00.123] [ERROR] 发生错误")
        """
        try:
            # 生成时间戳，格式为"YYYY-MM-DD HH:MM:SS.mmm"（毫秒精度）
            # datetime.now()获取当前时间，strftime格式化，[:-3]截取到毫秒
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            # 构建基础日志消息：时间戳 + 日志级别 + 消息内容
            log_msg = f"[{timestamp}] [{level}] {message}"
            
            # 如果有额外的上下文信息（kwargs），格式化为"key1=value1, key2=value2"形式
            # 并追加到日志消息后面，用" | "分隔
            if kwargs:
                # 将kwargs转换为字符串列表，格式为"key=value"
                context = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                log_msg += f" | {context}"

            with open(cls._log_file, "a", encoding=cls._encoding) as f:
                f.write(log_msg + "\n")
        except Exception as e:
            # 如果写入失败，输出错误信息到控制台，但不抛出异常
            # 避免文件写入错误影响主程序运行
            print(f"[FileLogger] 写入日志文件失败: {e}", flush=True)
    
    @classmethod
    def set_log_file(cls, log_file: str) -> None:
        """
        设置日志文件路径
        
        功能说明：
        修改日志文件的保存路径。设置后，后续的日志写入将使用新的路径。
        
        Args:
            log_file (str): 日志文件的路径
        
        Returns:
            None: 无返回值
        
        Example:
            FileLogger.set_log_file("custom.log")
        """
        cls._log_file = log_file
    
    @classmethod
    def set_encoding(cls, encoding: str) -> None:
        """
        设置文件编码格式
        
        功能说明：
        修改日志文件的编码格式。默认使用 UTF-8 编码。
        
        Args:
            encoding (str): 文件编码格式，如 "utf-8", "gbk" 等
        
        Returns:
            None: 无返回值
        
        Example:
            FileLogger.set_encoding("gbk")
        """
        cls._encoding = encoding
    
    @classmethod
    def get_log_file(cls) -> str:
        """
        获取当前日志文件路径
        
        Returns:
            str: 当前设置的日志文件路径
        """
        return cls._log_file


class Logger:
    """
    日志管理器类
    
    提供统一的日志记录功能，支持控制日志的打开和关闭。日志输出到控制台，
    包含时间戳、日志级别和消息内容。支持记录额外的上下文信息（通过kwargs传递）。
    
    设计目的：
    - 提供统一的日志接口，方便调试和问题排查
    - 支持动态启用/禁用日志，避免生产环境产生过多日志
    - 支持记录额外的上下文信息，便于追踪问题
    
    日志格式：
    [YYYY-MM-DD HH:MM:SS.mmm] [LEVEL] message | key1=value1, key2=value2
    
    日志级别：
    - INFO: 一般信息日志，记录正常流程信息
    - DEBUG: 调试日志，记录详细的调试信息
    - WARNING: 警告日志，记录可能的问题但不影响执行
    - ERROR: 错误日志，记录错误信息
    
    Attributes:
        enabled (bool): 日志是否启用，默认为False。当为False时，所有日志方法
            都不会输出任何内容，提高性能。这是类变量，所有Logger实例共享。
    
    Example:
        # 启用日志
        Logger.enable()
        
        # 记录信息日志
        Logger.info("开始执行工作流")
        
        # 记录调试日志（带上下文信息）
        Logger.debug("执行CDP命令", command_id="cmd_123", tab_id=1482755452)
        
        # 记录警告日志
        Logger.warning("元素未找到，将使用备用选择器", element_name="login_button")
        
        # 记录错误日志
        Logger.debug("网络请求失败", url="http://api.example.com", status_code=500)
        
        # 禁用日志
        Logger.disable()
    """
    # 日志启用标志，类变量，所有Logger实例共享
    # 当enabled=False时，所有日志方法都不会输出，提高性能
    # 类型: bool
    # 默认值: False
    enabled = False
    
    @staticmethod
    def enable():
        """
        启用日志输出
        
        功能说明：
        将Logger.enabled设置为True，使所有日志方法开始输出日志到控制台。
        调用此方法后，info、debug、warning、error等方法都会正常输出日志。
        
        使用场景：
        - 在开发或调试时启用日志，查看详细的执行过程
        - 在生产环境需要排查问题时临时启用日志
        
        Returns:
            None: 无返回值
        
        Example:
            Logger.enable()  # 启用日志
            Logger.info("日志已启用")  # 这条日志会输出
        """
        Logger.enabled = True
    
    @staticmethod
    def disable():
        """
        禁用日志输出
        
        功能说明：
        将Logger.enabled设置为False，使所有日志方法停止输出日志。
        调用此方法后，info、debug、warning、error等方法都不会输出任何内容。
        
        使用场景：
        - 在生产环境禁用日志，提高性能
        - 在不需要日志时禁用，避免控制台输出过多信息
        
        Returns:
            None: 无返回值
        
        Example:
            Logger.disable()  # 禁用日志
            Logger.info("这条日志不会输出")  # 不会输出任何内容
        """
        Logger.enabled = False
    
    @staticmethod
    def _log(level: str, message: str, **kwargs):
        """
        内部日志记录方法
        
        功能说明：
        这是所有日志方法（info、debug、warning、error）的内部实现方法。
        负责格式化日志消息并输出到控制台。如果日志未启用，直接返回不执行任何操作。
        
        日志格式：
        [YYYY-MM-DD HH:MM:SS.mmm] [LEVEL] message | key1=value1, key2=value2
        
        参数说明：
        - level: 日志级别，用于标识日志的重要性
        - message: 日志消息，描述发生了什么
        - **kwargs: 额外的上下文信息，会以key=value的格式追加到日志中
        
        Args:
            level (str): 日志级别，可选值："INFO"、"DEBUG"、"WARNING"、"ERROR"
            message (str): 日志消息内容，描述当前发生的事件或状态
            **kwargs: 额外的上下文信息，以关键字参数形式传递，会被格式化为
                "key1=value1, key2=value2"的形式追加到日志消息后面
        
        Returns:
            None: 无返回值
        
        Note:
            - 如果Logger.enabled为False，此方法会直接返回，不执行任何操作
            - 时间戳格式为"YYYY-MM-DD HH:MM:SS.mmm"（毫秒精度）
            - 上下文信息通过kwargs传递，会自动格式化为key=value形式
        
        Example:
            Logger._log("INFO", "执行完成", step_name="login", success=True)
            # 输出: [2024-01-01 12:00:00.123] [INFO] 执行完成 | step_name=login, success=True
        """
        # 如果日志未启用，直接返回，不执行任何操作
        if not Logger.enabled:
            return
        
        # 生成时间戳，格式为"YYYY-MM-DD HH:MM:SS.mmm"（毫秒精度）
        # datetime.now()获取当前时间，strftime格式化，[:-3]截取到毫秒
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # 构建基础日志消息：时间戳 + 日志级别 + 消息内容
        log_msg = f"[{timestamp}] [{level}] {message}"
        
        # 如果有额外的上下文信息（kwargs），格式化为"key1=value1, key2=value2"形式
        # 并追加到日志消息后面，用" | "分隔
        if kwargs:
            # 将kwargs转换为字符串列表，格式为"key=value"
            context = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            log_msg += f" | {context}"
        
        # 输出日志到控制台，立即刷新缓冲区
        print(log_msg, flush=True)
    
    @staticmethod
    def info(message: str, **kwargs):
        """
        记录信息级别日志
        
        功能说明：
        记录一般信息日志，用于记录正常流程中的重要信息。信息日志通常用于
        记录关键步骤的开始、结束或重要状态变化。
        
        Args:
            message (str): 日志消息内容，描述当前发生的信息事件
            **kwargs: 额外的上下文信息，以关键字参数形式传递
        
        Returns:
            None: 无返回值
        
        Example:
            Logger.info("工作流开始执行")
            Logger.info("步骤执行完成", step_name="login", duration=1.5)
        """
        Logger._log("INFO", message, **kwargs)
    
    @staticmethod
    def debug(message: str, **kwargs):
        """
        记录调试级别日志
        
        功能说明：
        记录调试日志，用于记录详细的调试信息。调试日志通常用于开发阶段
        追踪代码执行流程，帮助定位问题。
        
        Args:
            message (str): 日志消息内容，描述当前发生的调试事件
            **kwargs: 额外的上下文信息，以关键字参数形式传递
        
        Returns:
            None: 无返回值
        
        Example:
            Logger.debug("执行CDP命令", command_id="cmd_123", tab_id=1482755452)
            Logger.debug("元素查找", element_name="login_button", selector="button.login")
        """
        Logger._log("DEBUG", message, **kwargs)
    
    @staticmethod
    def warning(message: str, **kwargs):
        """
        记录警告级别日志
        
        功能说明：
        记录警告日志，用于记录可能的问题但不影响正常执行的情况。警告日志
        通常用于提示潜在问题或异常情况，但不中断执行流程。
        
        Args:
            message (str): 日志消息内容，描述当前发生的警告事件
            **kwargs: 额外的上下文信息，以关键字参数形式传递
        
        Returns:
            None: 无返回值
        
        Example:
            Logger.warning("元素未找到，将使用备用选择器", element_name="login_button")
            Logger.warning("网络请求超时，将重试", url="http://api.example.com", retry_count=1)
        """
        Logger._log("WARNING", message, **kwargs)
    
    @staticmethod
    def error(message: str, **kwargs):
        """
        记录错误级别日志
        
        功能说明：
        记录错误日志，用于记录错误信息。错误日志通常用于记录执行失败、
        异常情况或严重问题。
        
        Args:
            message (str): 日志消息内容，描述当前发生的错误事件
            **kwargs: 额外的上下文信息，以关键字参数形式传递
        
        Returns:
            None: 无返回值
        
        Example:
            Logger.debug("网络请求失败", url="http://api.example.com", status_code=500)
            Logger.debug("步骤执行失败", step_name="login", error="元素未找到")
        """
        Logger._log("ERROR", message, **kwargs)

# ==================== 自定义异常类 ==================

class AutoJSError(Exception):
    """
    AutoJS框架基础异常类
    
    功能说明：
    这是AutoJS框架中所有自定义异常的基类，继承自Python标准库的Exception类。
    所有框架内的自定义异常都继承自此类，便于统一处理和识别框架相关的异常。
    
    设计目的：
    - 提供统一的异常基类，便于异常分类和处理
    - 区分框架异常和系统异常
    - 支持异常链（通过original_error属性）
    
    Note:
        - 所有AutoJS框架的异常都应该继承自此类
        - 可以通过捕获AutoJSError来捕获所有框架异常
    
    Example:
        try:
            # 执行框架操作
            pass
        except AutoJSError as e:
            # 捕获所有框架异常
            print(f"框架异常: {e}")
    """
    pass


class NetworkError(AutoJSError):
    """
    网络请求异常类
    
    功能说明：
    用于表示网络请求相关的错误，如连接失败、超时、HTTP错误等。
    包含详细的错误信息，便于问题定位和调试。
    
    使用场景：
    - HTTP请求失败（连接失败、超时等）
    - WebSocket连接失败
    - API请求返回错误状态码
    - 网络不可达
    
    Attributes:
        url (str|None): 请求的URL地址，如果异常发生在网络请求中
        status_code (int|None): HTTP状态码，如果异常发生在HTTP请求中
        original_error (Exception|None): 原始异常对象，用于异常链追踪
    
    Args:
        message (str): 异常消息，描述错误原因
        url (str|None): 可选，请求的URL地址
        status_code (int|None): 可选，HTTP状态码
        original_error (Exception|None): 可选，原始异常对象
    
    Example:
        raise NetworkError(
            "网络请求失败",
            url="http://api.example.com/endpoint",
            status_code=500,
            original_error=requests.exceptions.RequestException("Connection timeout")
        )
    """
    def __init__(self, message: str, url: str = None, status_code: int = None, original_error: Exception = None):
        """
        初始化网络请求异常
        
        Args:
            message (str): 异常消息，描述错误原因
            url (str|None): 可选，请求的URL地址
            status_code (int|None): 可选，HTTP状态码
            original_error (Exception|None): 可选，原始异常对象
        """
        super().__init__(f"网络请求失败: {message}")
        # 请求的URL地址，用于标识是哪个请求失败
        self.url = url
        # HTTP状态码，用于标识HTTP请求的错误类型
        self.status_code = status_code
        # 原始异常对象，用于异常链追踪，便于调试
        self.original_error = original_error


class ParseError(AutoJSError):
    """
    数据解析异常类
    
    功能说明：
    用于表示数据解析相关的错误，如JSON解析失败、XML解析失败、数据格式错误等。
    包含原始数据和原始异常，便于问题定位和调试。
    
    使用场景：
    - JSON解析失败
    - XML解析失败
    - 数据格式不符合预期
    - 响应数据格式错误
    
    Attributes:
        raw_data (str|None): 原始数据，解析失败的数据内容
        original_error (Exception|None): 原始异常对象，用于异常链追踪
    
    Args:
        message (str): 异常消息，描述错误原因
        raw_data (str|None): 可选，原始数据内容
        original_error (Exception|None): 可选，原始异常对象
    
    Example:
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ParseError(
                "JSON解析失败",
                raw_data=response_text,
                original_error=e
            )
    """
    def __init__(self, message: str, raw_data: str = None, original_error: Exception = None):
        """
        初始化数据解析异常
        
        Args:
            message (str): 异常消息，描述错误原因
            raw_data (str|None): 可选，原始数据内容
            original_error (Exception|None): 可选，原始异常对象
        """
        super().__init__(f"数据解析失败: {message}")
        # 原始数据，解析失败的数据内容，便于调试
        self.raw_data = raw_data
        # 原始异常对象，用于异常链追踪，便于调试
        self.original_error = original_error


class BusinessError(AutoJSError):
    """
    业务逻辑异常类
    
    功能说明：
    用于表示业务逻辑相关的错误，如命令执行失败、操作不允许、业务规则违反等。
    包含错误代码和错误数据，便于业务层处理和错误分类。
    
    使用场景：
    - CDP命令执行失败
    - 指令执行失败
    - HTTP命令执行失败
    - 业务规则验证失败
    
    Attributes:
        code (int|None): 错误代码，用于标识错误类型
        data (dict|None): 错误数据，包含详细的错误信息
    
    Args:
        message (str): 异常消息，描述错误原因
        code (int|None): 可选，错误代码
        data (dict|None): 可选，错误数据字典
    
    Example:
        raise BusinessError(
            "命令执行失败",
            code=1001,
            data={"command_id": "cmd_123", "error_detail": "元素未找到"}
        )
    """
    def __init__(self, message: str, code: int = None, data: dict = None):
        """
        初始化业务逻辑异常
        
        Args:
            message (str): 异常消息，描述错误原因
            code (int|None): 可选，错误代码
            data (dict|None): 可选，错误数据字典
        """
        super().__init__(f"业务逻辑异常: {message}")
        # 错误代码，用于标识错误类型，便于业务层处理
        self.code = code
        # 错误数据，包含详细的错误信息，便于问题定位
        self.data = data


class LoginError(AutoJSError):
    """
    登录异常类
    
    功能说明：
    用于表示登录相关的错误，如登录失败、账号密码错误、登录超时等。
    继承自AutoJSError，是业务逻辑异常的一种特殊情况。
    
    使用场景：
    - 网站登录步骤失败
    - 账号密码验证失败
    - 登录页面加载失败
    - 登录超时
    - 需要登录但未登录
    
    Attributes:
        message (str): 异常消息，描述登录失败的原因
        data (dict|None): 错误数据，包含详细的错误信息，如账号、错误码等
    
    Args:
        message (str): 异常消息，描述登录失败的原因
        data (dict|None): 可选，错误数据字典，包含详细的错误信息
    
    Example:
        raise LoginError(
            "登录失败：账号或密码错误",
            data={"account": "user@example.com", "error_code": "INVALID_CREDENTIALS"}
        )
    """
    def __init__(self, message: str, data: dict = None):
        """
        初始化登录异常
        
        Args:
            message (str): 异常消息，描述登录失败的原因
            data (dict|None): 可选，错误数据字典，包含详细的错误信息
        """
        # 调用父类构造函数，传递异常消息和数据
        # BusinessError的构造函数会自动在消息前添加"业务逻辑异常: "前缀
        super().__init__(message, data=data)

# ==================== CDP命令层 ====================

class CdpCommand(ABC):
    """
    CDP命令抽象基类
    
    CDP（Chrome DevTools Protocol）命令的抽象基类，所有具体的CDP命令都继承自此类。
    此类定义了CDP命令的基本结构和行为，包括命令序列化、响应解析和回调机制。
    
    CDP命令用于直接与Chrome浏览器的DevTools协议交互，可以执行底层浏览器操作，
    如执行JavaScript、截图、获取网络日志等。
    
    Attributes:
        type (str): 命令类型，由子类定义，如 "cdp_connect"、"list_targets" 等
        id (str): 命令的唯一标识符，用于匹配请求和响应。如果为空，子类会自动生成
        data (dict): 命令的数据部分，包含命令的具体参数
        ignore_error (bool): 是否忽略错误，如果为True，即使执行失败也不会抛出异常，默认为False
    
    Args:
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Note:
        - 子类必须实现 parse_response 方法来解析特定命令的响应数据
    
    Example:
        class MyCdpCommand(CdpCommand):
            type = "my_command"
            def __init__(self, param1: str, ignore_error=False):
                super().__init__(ignore_error)
                self.id = f"{self.type}_{uuid.uuid4().hex[:16]}"
                self.data = {"param1": param1}
            
            def parse_response(self, data: dict) -> dict:
                if not data.get("success"):
                    raise Exception(data.get("error", "命令执行失败"))
                return data.get("data", {})
    """
    # 命令类型，由子类定义
    type = ""
    
    def __init__(self, ignore_error: bool = False):
        """
        初始化CDP命令对象
        
        Args:
            ignore_error (bool): 是否忽略错误，默认为False
        """
        # 是否忽略错误，如果为True，即使执行失败也不会抛出异常
        self.ignoreError = ignore_error

        # 命令的唯一标识符，用于匹配请求和响应
        self.id = ""
        # 命令的数据部分，包含命令的具体参数
        self.data = {}
     
    def to_dict(self) -> dict:
        """
        将命令对象转换为字典格式，用于API请求
        
        Returns:
            dict: 包含命令类型、ID和数据的字典，格式为：
                {
                    "type": str,    # 命令类型
                    "id": str,      # 命令ID
                    "data": dict    # 命令数据
                }
        
        Example:
            command = CdpConnectCommand(tab_id=1)
            command_dict = command.to_dict()
            # 返回: {"type": "cdp_connect", "id": "...", "data": {"tabId": 1}}
        """
        return {
            "type": self.type,
            "id": self.id,
            "data": self.data
        }

# ==================== 指令层 ========================

class Instruction(ABC):
    """
    指令抽象基类
    
    指令是比CDP命令更高级的浏览器操作抽象，提供了更友好的API和更多的功能，
    如延迟执行、重试机制、超时控制、错误处理等。
    
    指令系统封装了常见的浏览器操作，如导航、元素查找、输入、鼠标键盘操作等，
    使得自动化脚本更加易读和易维护。
    
    Attributes:
        type (str): 指令类型，由子类定义，如 "navigate"、"find_element" 等
        tabId (int): 指令执行的标签页ID
        instructionID (str): 指令的唯一标识符，用于匹配请求和响应
        delay (int): 指令执行前的延迟时间（秒），默认为0
        retry (int): 指令执行失败时的重试次数，默认为0
        timeout (int): 指令执行的超时时间（秒），默认为150
        ignore_error (bool): 是否忽略错误，如果为True，即使执行失败也不会抛出异常
        created_at (int): 指令创建的时间戳，默认为0
        params (dict): 指令的参数，包含指令的具体配置
    
    Args:
        tab_id (int): 指令执行的标签页ID
        instruction_id (str): 可选，指令ID。如果不提供，子类会自动生成
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Note:
        - 子类必须实现 parse_response 方法来解析特定指令的响应数据
        - 子类应该在 __init__ 中设置 type 和 params
    
    Example:
        class MyInstruction(Instruction):
            type = "my_instruction"
            def __init__(self, tab_id: int, param1: str, **kwargs):
                super().__init__(tab_id, **kwargs)
                self.instructionID = self.instructionID or f"{self.type}_{uuid.uuid4().hex[:16]}"
                self.params = {"param1": param1}
            
            def parse_response(self, data: dict) -> dict:
                return super().parse_response(data)
    """
    # 指令类型，由子类定义
    type = ""
    
    def __init__(self, tab_id: int, instruction_id: str = "", delay: int = 1, retry: int = 0, 
                 timeout: int = 150, ignore_error: bool = False, created_at: int = 0):
        """
        初始化指令对象
        
        Args:
            tab_id (int): 指令执行的标签页ID
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        # 指令执行的标签页ID
        self.tabId = tab_id
        # 指令的唯一标识符，用于匹配请求和响应
        self.instructionID = instruction_id if instruction_id else f"{self.type}_{uuid.uuid4().hex[:16]}"
        # 指令执行前的延迟时间（秒）
        self.delay = delay
        # 指令执行失败时的重试次数
        self.retry = retry
        # 指令执行的超时时间（秒）
        self.timeout = timeout
        # 是否忽略错误，如果为True，即使执行失败也不会抛出异常
        self.ignoreError = ignore_error
        # 指令创建的时间戳
        self.created_at = created_at if created_at else int(time.time() * 1000)
        # 指令的参数，包含指令的具体配置（由子类填充）
        self.params = {}

    def to_dict(self) -> dict:
        """
        将指令对象转换为字典格式，用于API请求
        
        功能说明：
        将Instruction对象的所有属性转换为字典格式，便于序列化和API传输。
        只有非空或非默认值的属性会被包含在返回的字典中。
        
        Returns:
            dict: 包含指令所有属性的字典，格式为：
                {
                    "tabId": int,              # 指令执行的标签页ID（必需）
                    "type": str,               # 指令类型（必需）
                    "instructionID": str,      # 指令的唯一标识符（必需）
                    "delay": int,              # 可选，延迟时间（秒），仅在非0时包含
                    "retry": int,              # 可选，重试次数，仅在非0时包含
                    "timeout": int,            # 可选，超时时间（秒），仅在非0时包含
                    "ignoreError": bool,       # 可选，是否忽略错误，仅在True时包含
                    "created_at": int,         # 可选，创建时间戳，仅在非0时包含
                    "params": dict             # 可选，指令参数，仅在非空时包含
                }
        
        Note:
            - 必需属性（tabId, type, instructionID）总是会被包含
            - 可选属性只有在有值或非默认值时才被包含
            - delay、retry、timeout只有在非0时才被包含
            - ignoreError只有在True时才被包含
            - created_at只有在非0时才被包含
            - params只有在非空时才被包含
        
        Example:
            instruction = NavigateInstruction(
                tab_id=1,
                url="https://example.com",
                delay=3,
                timeout=150
            )
            instruction_dict = instruction.to_dict()
            # 返回: {
            #     "tabId": 1,
            #     "type": "navigate",
            #     "instructionID": "navigate_...",
            #     "delay": 3,
            #     "timeout": 180,
            #     "params": {"url": "https://example.com"}
            # }
        """
        # 构建基础结果字典，包含必需属性
        result = {
            "tabId": self.tabId,
            "type": self.type,
            "instructionID": self.instructionID,
        }
        # 如果delay不为0，添加到结果中
        if self.delay:
            result["delay"] = self.delay
        # 如果retry不为0，添加到结果中
        if self.retry:
            result["retry"] = self.retry
        # 如果timeout不为0，添加到结果中
        if self.timeout:
            result["timeout"] = self.timeout
        # 如果ignoreError为True，添加到结果中
        if self.ignoreError:
            result["ignoreError"] = self.ignoreError
        # 如果created_at不为0，添加到结果中
        if self.created_at:
            result["created_at"] = self.created_at
        # 如果params不为空，添加到结果中
        if self.params:
            result["params"] = self.params

        return result

# ==================== HTTP命令层 ====================

class HttpCommand(ABC):
    """
    HTTP命令抽象基类
    
    设计目的：
    HttpCommand 是所有HTTP命令的抽象基类，定义了HTTP命令的标准接口和通用行为。
    它采用命令模式（Command Pattern），将HTTP请求封装为命令对象，支持错误处理。
    
    核心功能：
    1. 封装HTTP请求参数（URL、方法、头部、请求体、超时时间）
    2. 支持错误忽略选项（ignore_error）
    3. 定义响应解析的标准接口（parse_response）
    4. 提供命令序列化方法（to_dict）
    
    使用场景：
    - 通过HTTP API与浏览器节点服务通信
    - 执行浏览器管理操作（打开、关闭、列表查询、重置等）
    - 在工作流中封装HTTP请求步骤
    
    继承关系：
    子类需要实现 parse_response 方法来解析特定类型的HTTP响应。
    常见的子类包括：HttpBitBrowserOpenCommand、HttpBitBrowserCloseCommand 等。
    
    数据流转：
    1. 创建命令对象 -> 2. 设置请求参数 -> 3. 执行HTTP请求 -> 4. 解析响应
    """
    # 命令类型标识符，子类需要设置具体的类型值（如 "http_request"）
    type = ""
    
    def __init__(self, ignore_error: bool = False, timeout: int = 180):
        """
        初始化HTTP命令对象
        
        Args:
            ignore_error (bool, optional): 是否忽略错误，默认为False
                - True: 即使命令执行失败也不抛出异常，返回错误结果
                - False: 命令执行失败时抛出BusinessError异常
                - 用途: 在工作流中允许某些步骤失败而不中断整个流程
        
        Attributes:
            id (str): 命令的唯一标识符，用于跟踪和匹配请求与响应
            url (str): HTTP请求的相对路径（相对于节点API的基础URL）
            method (str): HTTP请求方法（GET、POST、PUT、DELETE等）
            headers (dict): HTTP请求头字典，包含Content-Type等头部信息
            body (dict): HTTP请求体，包含请求参数
            timeout (int): 请求超时时间（秒），默认180秒
        """
        # 错误处理选项：是否忽略命令执行错误
        self.ignoreError = ignore_error

        # HTTP请求参数：由子类在初始化时设置
        self.id = ""  # 命令ID，通常由子类自动生成或从参数传入
        self.url = ""  # 请求路径，如 '/browser/open'
        self.method = ""  # HTTP方法，通常为 'POST'
        self.headers = {}  # 请求头，通常包含 'Content-Type': 'application/json'
        self.body = {}  # 请求体，包含具体的请求参数
        self.timeout = timeout  # 超时时间（秒）

    def to_dict(self) -> dict:
        """
        将命令对象转换为字典格式，用于API请求
        
        用途：
        将命令对象序列化为字典，便于通过HTTP API发送请求。
        这个方法将命令的所有属性打包成标准格式，供Browser类的_execute_http_command方法使用。
        
        Returns:
            dict: 包含命令所有属性的字典，格式如下：
            {
                "type": str,      # 命令类型
                "id": str,         # 命令ID
                "url": str,        # 请求路径
                "method": str,     # HTTP方法
                "headers": dict,   # 请求头
                "body": dict,      # 请求体
                "timeout": int     # 超时时间
            }
        
        使用场景：
        - 在_execute_http_command方法中序列化命令对象
        - 调试时打印命令内容
        - 日志记录命令信息
        """
        return {
            "type": self.type,
            "id": self.id,
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "body": self.body,
            "timeout": self.timeout
        }

# ==================== 上下文 ========================

class Context:
    """
    工作流执行上下文类
    
    用于在工作流执行过程中传递状态、结果和变量。上下文对象在工作流的各个步骤之间共享，
    允许步骤之间传递数据和状态信息。
    
    Attributes:
        last_success (bool): 上一个步骤是否成功执行
        last_error (str|None): 上一个步骤的错误信息（如果失败）
        last_result (dict|None): 上一个步骤的执行结果
    
        current_success (bool): 当前步骤是否成功执行
        current_error (str|None): 当前步骤的错误信息（如果失败）
        current_result (dict|None): 当前步骤的执行结果
    
        variables (dict): 命名变量字典，用于存储步骤执行结果和自定义变量
            - 'stop' (bool): 是否需要停止流程，默认为False
            - 'success' (bool): 工作流是否完美完成，如果最后步骤校验成功则设置为True，默认为False
            - 其他自定义变量：可以在工作流中存储任意数据
    
    Note:
        - 每个步骤执行后，current_* 会被复制到 last_*
        - 可以通过 get_variable 和 set_variable 方法访问和设置变量
        - stop 变量用于控制工作流的提前终止
    
    Example:
        context = Context()
        context.set_variable('user_id', 12345)
        user_id = context.get_variable('user_id')
        if some_condition:
            context.set_stop(True)  # 停止工作流
    """
    def __init__(self):
        """
        初始化工作流执行上下文
        
        创建新的上下文对象，初始化所有状态变量和内置变量。
        """
        # 上一个步骤的执行状态：是否成功
        self.last_success = False
        # 上一个步骤的错误信息（如果失败）
        self.last_error = None 
        # 上一个步骤的执行结果
        self.last_result = None

        # 当前步骤的执行状态：是否成功
        self.current_success = False
        # 当前步骤的错误信息（如果失败）
        self.current_error = None
        # 当前步骤的执行结果
        self.current_result = None
        
        # 命名变量字典，用于存储步骤执行结果和自定义变量
        self.var = dict()
        # 是否需要停止流程，默认为False
        self.var['stop'] = False
        # 工作流是否完美完成，默认为True
        self.var['success'] = True

    def get_var(self, name: str, value: any = None) -> any:
        """
        获取命名变量的值
        
        从上下文的变量字典中获取指定名称的变量值。如果变量不存在，返回默认值。
        
        Args:
            name (str): 变量名称
            value (any): 可选，如果变量不存在时返回的默认值，默认为None
        
        Returns:
            any: 变量的值，如果变量不存在则返回默认值
        
        Example:
            context.set_variable('user_id', 12345)
            user_id = context.get_variable('user_id')  # 返回 12345
            not_exist = context.get_variable('not_exist', 'default')  # 返回 'default'
        """
        return self.var.get(name, value)

    def set_var(self, name: str, value: any) -> None:
        """
        设置命名变量的值
        
        在上下文的变量字典中设置指定名称的变量值。如果变量已存在，会被覆盖。
        
        Args:
            name (str): 变量名称
            value (any): 变量的值，可以是任意类型
        
        Example:
            context.set_variable('user_id', 12345)
            context.set_variable('stream_key', 'abc123')
            context.set_variable('data', {'key': 'value'})
        """
        self.var[name] = value

    def is_stop(self) -> bool:
        """
        检查是否需要停止工作流
        
        返回stop变量的值，用于判断工作流是否应该提前终止。
        
        Returns:
            bool: 是否需要停止流程
                - True: 需要停止流程
                - False: 继续执行流程
        
        Example:
            if some_condition:
                context.set_stop(True)
            
            if context.is_stop():
                return  # 提前退出
        """
        return self.get_var('stop')

    def set_stop(self, stop: bool) -> None:
        """
        设置是否需要停止工作流
        
        设置stop变量的值，用于控制工作流的提前终止。当设置为True时，
        后续步骤的prepare方法可能会返回False，从而跳过步骤执行。
        
        Args:
            stop (bool): 是否需要停止流程
                - True: 设置停止标志，后续步骤可能会被跳过
                - False: 清除停止标志，继续正常执行
        
        Example:
            if error_occurred:
                context.set_stop(True)  # 停止工作流
        """
        self.var['stop'] = stop

# ==================== 浏览器操作类 ========================

class Browser:
    """
    浏览器操作类
    
    负责与浏览器节点API通信，执行CDP命令和指令。此类封装了所有与节点API的交互逻辑，
    包括认证、请求构建、响应解析等。
    
    Attributes:
        node_api_base_url (str): 节点API的基础URL，如 "http://api.example.com"
        auth_token (str): 节点认证Token，用于API请求的Authorization头
        node_name (str): 节点名称，用于查找节点
        node_id (str|None): 节点的唯一标识符，在初始化时通过节点名称查找获得
        timeout (int): HTTP请求的默认超时时间（秒），默认为30秒
    
    Args:
        node_api_base_url (str): 节点API基础URL
        auth_token (str): 节点认证Token
        node_name (str): 节点名称
        timeout (int): 可选，HTTP请求超时时间（秒），默认为30
    
    Note:
        - 初始化时会自动通过节点名称查找节点ID
        - 如果找不到节点或节点不在线，会抛出异常
        - 所有API请求都会自动添加认证头
    
    Example:
        browser = Browser(
            node_api_base_url="http://api.example.com",
            auth_token="your_token_here",
            node_name="local",
            timeout=30
        )
        # 执行CDP命令
        command = ListTargetsCommand()
        result = browser._execute_cdp_command(command)
    """
    def __init__(self, node_api_base_url: str, auth_token: str, node_name: str, timeout: int = 180):
        """
        初始化浏览器操作对象
        
        Args:
            node_api_base_url (str): 节点API基础URL
            auth_token (str): 节点认证Token
            node_name (str): 节点名称
            timeout (int): HTTP请求超时时间（秒）
        
        Raises:
            Exception: 如果找不到节点或节点不在线，抛出异常
        """
        # 节点API的基础URL
        self.node_api_base_url = node_api_base_url
        # 节点认证Token，用于API请求的Authorization头
        self.auth_token = auth_token
        # 节点名称，用于查找节点
        self.node_name = node_name
        # 节点的唯一标识符，在初始化时通过节点名称查找获得
        self.node_id = None
        # HTTP请求的默认超时时间（秒）
        self.timeout = timeout

        # 初始化时自动通过节点名称查找节点ID
        Logger.info("初始化Browser对象", node_name=node_name, node_api_base_url=node_api_base_url, timeout=timeout)
        self._get_node_config_by_name(self.node_name)

    def retry_on_error(max_retries: int = 3, delay: int = 3):
        def retry_on_error_decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_error = None
                for i in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except NetworkError as e:
                        last_error = e
                        if i < max_retries - 1:  # 不是最后一次重试
                            time.sleep(delay)
                # 确保有错误才抛出
                if last_error is not None:
                    raise last_error
                # 如果 last_error 为 None（理论上不应该发生），抛出通用异常
                raise NetworkError("重试失败：未知错误", original_error=None)
            return wrapper
        return retry_on_error_decorator

    @retry_on_error(max_retries=10, delay=15)
    def _get_node_config_by_name(self, node_name: str):
        """
        通过节点名称获取节点配置
        
        此方法通过节点名称查找节点，并获取节点的详细信息（包括节点ID）。
        节点ID是后续API调用所必需的。
        
        Args:
            node_name (str): 节点名称，如 "local"
        
        Raises:
            NetworkError: 如果网络请求失败（连接错误、超时、HTTP错误等）
            ParseError: 如果响应解析失败（JSON解析错误等）
            BusinessError: 如果API返回业务错误码、未找到数据、未找到匹配节点或节点不在线
        
        API请求格式：
            请求URL: {node_api_base_url}/node/detail-by-name
            请求方法: GET
            请求头:
                Authorization: Bearer {auth_token}
            查询参数:
                node_name: 节点名称
        
        API响应格式：
            {
                "code": 0,
                "message": "OK",
                "data": {
                    "list": [
                        {
                            "node_type": str,
                            "node_id": str,
                            "node_name": str,
                            "node_token": str
                        },
                        ...
                    ]
                }
            }
        
        Note:
            - 如果找到多个匹配的节点，使用第一个
            - 节点ID会被自动设置到self.node_id
            - 如果节点不在线（node_id为空），会抛出异常
        
        Example:
            node_config = browser._get_node_config_by_name("local")
            print(node_config.node_id)  # 输出节点ID
        """
        # 第一步：准备请求参数
        # 构建API端点URL
        request_url = f"{self.node_api_base_url}/node/detail-by-name"

        # 设置请求头，包括认证信息
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
        }

        # 设置查询参数
        params = {
            "node_name": node_name
        }

        try:
            # 第二步：执行HTTP GET请求
            Logger.info("发送获取节点配置请求", node_name=node_name)
            response = requests.get(request_url, headers=headers, params=params, timeout=self.timeout)

            # 检查HTTP状态码，如果不是2xx则抛出异常
            response.raise_for_status()
            Logger.debug("获取节点配置响应成功", node_name=node_name, response=response.text)
            
        except requests.exceptions.Timeout as e:
            Logger.debug("获取节点配置超时", node_name=node_name, timeout=self.timeout)
            raise NetworkError(f"获取节点配置超时: 节点名称 '{node_name}', 超时时间: {self.timeout}秒", url=request_url, original_error=e)
        except requests.exceptions.ConnectionError as e:
            Logger.debug("获取节点配置连接失败", node_name=node_name, url=request_url)
            raise NetworkError(f"获取节点配置连接失败: 节点名称 '{node_name}', 无法连接到服务器", url=request_url, original_error=e)
        except requests.exceptions.HTTPError as e:
            Logger.debug("获取节点配置HTTP错误", node_name=node_name, status_code=response.status_code, url=request_url)
            raise NetworkError(f"获取节点配置HTTP错误: 节点名称 '{node_name}', HTTP状态码: {response.status_code}", url=request_url, status_code=response.status_code, original_error=e)
        except requests.exceptions.RequestException as e:
            Logger.debug("获取节点配置网络请求失败", node_name=node_name, url=request_url)
            raise NetworkError(f"获取节点配置网络请求失败: 节点名称 '{node_name}'", url=request_url, original_error=e)
        
        # 第三步：解析响应体
        try:
            # 获取响应文本
            response_text = response.text
            # 解析JSON响应
            response_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            Logger.debug("节点配置响应JSON解析失败", node_name=node_name, response_preview=response_text[:200] if response_text else None)
            raise ParseError(f"解析节点配置响应失败: 节点名称 '{node_name}', 响应不是有效的JSON格式", raw_data=response_text[:500] if response_text else None, original_error=e)
        except Exception as e:
            Logger.debug("节点配置响应解析未知错误", node_name=node_name, error=str(e))
            raise ParseError(f"解析节点配置响应时发生未知错误: 节点名称 '{node_name}'", original_error=e)

        # 检查API返回码，0表示成功，非0表示失败
        api_code = response_data.get('code')

        if api_code != 0:
            Logger.debug("获取节点配置API返回错误码", node_name=node_name, api_code=api_code, api_message=response_data.get('message'))
            raise NetworkError(f"获取节点配置API返回错误码: 节点名称 '{node_name}', API返回错误码: {api_code}", url=request_url, status_code=response.status_code, original_error=None)

        # 提取响应数据部分
        data = response_data.get('data', {})

        # 检查是否找到数据
        if not data:
            Logger.debug("获取节点配置未找到数据", node_name=node_name)
            raise ParseError(f"获取节点配置未找到数据: 节点名称 '{node_name}', 未找到数据", raw_data=response_text[:500] if response_text else None, original_error=None)

        # 获取节点列表
        node_list = data.get('list', [])

        # 检查是否找到匹配的节点
        if not node_list:
            Logger.debug("获取节点配置未找到匹配节点", node_name=node_name)
            raise ParseError(f"获取节点配置未找到匹配节点: 节点名称 '{node_name}', 未找到匹配的节点", raw_data=response_text[:500] if response_text else None, original_error=None)

        # 创建节点配置对象（使用第一个匹配的节点）
        node_config = node_list[0]
        
        # 检查节点ID是否存在，如果存在则设置到self.node_id
        if node_config.get('node_id', None):
            self.node_id = node_config.get('node_id', None)
        else:
            # 如果节点ID为空，说明节点可能不在线
            Logger.debug("获取节点配置节点ID失败", node_name=node_name)
            raise NetworkError(f"获取节点配置节点ID失败: 节点名称 '{node_name}', 节点可能不在线", url=request_url, status_code=response.status_code, original_error=None)

    @retry_on_error(max_retries=3, delay=3)
    def _execute_cdp_command(self, cdp_command: CdpCommand) -> dict:
        """
        执行CDP命令（完整的HTTP API调用流程）
        
        此方法执行完整的CDP命令调用流程：
        1. 准备请求参数（URL、请求头、请求体）
        2. 执行HTTP POST请求
        3. 解析响应并提取结果
        
        Args:
            cdp_command (CdpCommand): 要执行的CDP命令对象
        
        Returns:
            dict: CDP命令执行结果，已通过命令的parse_response方法解析
        
        Raises:
            NetworkError: 如果网络请求失败（连接错误、超时、HTTP错误等）
            ParseError: 如果响应解析失败（JSON解析错误等）
            BusinessError: 如果API返回业务错误码
            Exception: 如果命令执行失败
        
        API请求格式：
            请求URL: {node_api_base_url}/cdp/{node_id}
            请求方法: POST
            请求头:
                Authorization: Bearer {auth_token}
                Content-Type: application/json
            请求体示例:
                {
                    "type": "list_targets",
                    "id": "cdp_id_1",
                    "data": {}
                }
        
        API响应格式：
            {
                "code": 0,              # 0表示成功，非0表示失败
                "message": "OK",         # 响应消息
                "data": {                # 响应数据
                    "type": "list_targets",
                    "id": "cdp_id_1",
                    "success": true,     # 命令是否成功执行
                    "data": [...]        # 命令执行结果
                }
            }
        
        Example:
            command = ListTargetsCommand()
            result = browser._execute_cdp_command(command)
            # result: {"list": [{"tabId": 1, "tabIndex": 0, "url": "..."}, ...]}
        """
        # 第一步：准备请求参数
        # 构建API端点URL：{base_url}/cdp/{node_id}
        request_url = f"{self.node_api_base_url}/cdp/{self.node_id}"

        # 设置请求头，包括认证信息和内容类型
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        # 将CDP命令对象转换为字典格式
        request_body = cdp_command.to_dict()

        try:
            Logger.info("准备执行CDP命令", command_type=cdp_command.type, command_id=cdp_command.id, body=request_body)
            # 第二步：执行HTTP POST请求
            response = requests.post(url = request_url, headers = headers, json = request_body, timeout = self.timeout)

            # 检查HTTP状态码，如果不是2xx则抛出异常
            response.raise_for_status()
            Logger.debug("执行CDP命令响应成功", command_type=cdp_command.type, command_id=cdp_command.id, response=response.text)
            
        except requests.exceptions.Timeout as e:
            Logger.debug("执行CDP命令超时", command_type=cdp_command.type, command_id=cdp_command.id, timeout=self.timeout)
            raise NetworkError(f"执行CDP命令超时: {cdp_command.type} (ID: {cdp_command.id}), 超时时间: {self.timeout}秒", url=request_url, original_error=e)
        except requests.exceptions.ConnectionError as e:
            Logger.debug("执行CDP命令连接失败", command_type=cdp_command.type, command_id=cdp_command.id, url=request_url)
            raise NetworkError(f"执行CDP命令连接失败: {cdp_command.type} (ID: {cdp_command.id}), 无法连接到服务器", url=request_url, original_error=e)
        except requests.exceptions.HTTPError as e:
            Logger.debug("执行CDP命令HTTP错误", command_type=cdp_command.type, command_id=cdp_command.id, status_code=response.status_code, url=request_url)
            raise NetworkError(f"执行CDP命令HTTP错误: {cdp_command.type} (ID: {cdp_command.id}), HTTP状态码: {response.status_code}", url=request_url, status_code=response.status_code, original_error=e)
        except requests.exceptions.RequestException as e:
            Logger.debug("执行CDP命令网络请求失败", command_type=cdp_command.type, command_id=cdp_command.id, url=request_url)
            raise NetworkError(f"执行CDP命令网络请求失败: {cdp_command.type} (ID: {cdp_command.id})", url=request_url, original_error=e)
        except Exception as e:
            Logger.debug("执行CDP命令未知错误", command_type=cdp_command.type, command_id=cdp_command.id, error=str(e))
            raise NetworkError(f"执行CDP命令时发生未知错误: {cdp_command.type} (ID: {cdp_command.id})", original_error=e)
        
        # 第三步：解析响应体
        try:
            # 获取响应文本
            response_text = response.text
            # 解析JSON响应
            response_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            Logger.debug("执行CDP命令响应JSON解析失败", command_type=cdp_command.type, command_id=cdp_command.id, response_preview=response_text[:200] if response_text else None)
            raise ParseError(f"解析执行CDP命令响应失败: {cdp_command.type} (ID: {cdp_command.id}), 响应不是有效的JSON格式", raw_data=response_text[:500] if response_text else None, original_error=e)
        except Exception as e:
            Logger.debug("执行CDP命令响应解析未知错误", command_type=cdp_command.type, command_id=cdp_command.id, error=str(e))
            raise ParseError(f"执行CDP命令响应解析未知错误: {cdp_command.type} (ID: {cdp_command.id})", original_error=e)

        # 检查API返回码，0表示成功，非0表示失败
        api_code = response_data.get('code')

        if api_code != 0:
            Logger.debug("执行CDP命令API返回错误码", command_type=cdp_command.type, command_id=cdp_command.id, api_code=api_code, api_message=response_data.get('message'))
            raise NetworkError(f"执行CDP命令API返回错误码: {cdp_command.type} (ID: {cdp_command.id}), API返回错误码: {api_code}", url=request_url, status_code=response.status_code, original_error=None)

        return response_data.get('data', {})
    
    @retry_on_error(max_retries=3, delay=3)
    def _execute_instruction(self, instructions: list[Instruction]) -> dict:
        """
        执行指令列表（完整的HTTP API调用流程）
        
        此方法执行一个或多个指令，支持批量执行。指令是比CDP命令更高级的浏览器操作抽象。
        
        Args:
            instructions (list[Instruction]): 要执行的指令对象列表
        
        Returns:
            dict: 指令执行结果，格式为：
                {
                    "results": [
                        {
                            "instructionID": str,
                            "success": bool,
                            "duration": int,
                            "error": str,      # 仅在失败时存在
                            "data": dict       # 仅在成功时存在
                        },
                        ...
                    ]
                }
        
        Raises:
            NetworkError: 如果网络请求失败（连接错误、超时、HTTP错误等）
            ParseError: 如果响应解析失败（JSON解析错误等）
            BusinessError: 如果API返回业务错误码
        
        API请求格式：
            请求URL: {node_api_base_url}/instruction/{node_id}
            请求方法: POST
            请求头:
                Authorization: Bearer {auth_token}
                Content-Type: application/json
            请求体:
                {
                    "instructions": [
                        {
                            "tabId": int,
                            "type": str,
                            "instructionID": str,
                            "params": dict,
                            ...
                        },
                        ...
                    ]
                }
        
        Note:
            - 指令会按顺序执行
            - 每个指令的执行结果都会包含在返回的results数组中
            - 超时时间为所有指令超时时间的总和，如果总和为0则使用默认超时时间（180秒）
        
        Example:
            instructions = [
                NavigateInstruction(tab_id=1, url="https://example.com"),
                FindElementInstruction(tab_id=1, element=element)
            ]
            result = browser._execute_instruction(instructions)
        """
        # 第一步：准备请求参数
        # 构建API端点URL：{base_url}/instruction/{node_id}
        request_url = f"{self.node_api_base_url}/instruction/{self.node_id}"

        # 设置请求头，包括认证信息和内容类型
        headers = {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"}
        
        # 将指令对象列表转换为字典格式
        instruction_dicts = [instruction.to_dict() for instruction in instructions]
        request_body = {"instructions": instruction_dicts}

        # 获取指令信息用于日志（取第一个指令的信息）
        instruction_types = [inst.type for inst in instructions]
        instruction_ids = [inst.instructionID for inst in instructions]

        try:
            Logger.info("准备执行指令列表", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), body=request_body)
            # 第二步：执行HTTP POST请求
            # 指令执行的超时时间为所有指令超时时间的总和
            response = requests.post(url = request_url, headers = headers, json = request_body, timeout = self.timeout)

            # 检查HTTP状态码，如果不是2xx则抛出异常
            response.raise_for_status()
            Logger.debug("执行指令列表响应成功", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), response=response.text)
            
        except requests.exceptions.Timeout as e:
            Logger.debug("指令执行超时", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions))
            raise BusinessError(f"执行指令超时: {instruction_types}, 超时时间: {self.timeout}秒", code=1001, data={"instructions": instruction_dicts, "timeout": self.timeout})
        except requests.exceptions.ConnectionError as e:
            Logger.debug("指令连接失败", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), url=request_url)
            raise NetworkError(f"执行指令连接失败: {instruction_types}, 无法连接到服务器", url=request_url, original_error=e)
        except requests.exceptions.HTTPError as e:
            Logger.debug("指令HTTP错误", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), status_code=response.status_code, url=request_url)
            raise NetworkError(f"执行指令HTTP错误: {instruction_types}, HTTP状态码: {response.status_code}", url=request_url, status_code=response.status_code, original_error=e)
        except requests.exceptions.RequestException as e:
            Logger.debug("指令网络请求失败", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), url=request_url)
            raise NetworkError(f"执行指令网络请求失败: {instruction_types}", url=request_url, original_error=e)
        
        # 第三步：解析响应体
        try:
            # 获取响应文本
            response_text = response.text
            # 解析JSON响应
            response_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            Logger.debug("指令响应JSON解析失败", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), response_preview=response_text[:200] if response_text else None)
            raise ParseError(f"解析指令响应失败: {instruction_types}, 响应不是有效的JSON格式", raw_data=response_text[:500] if response_text else None, original_error=e)
        except Exception as e:
            Logger.debug("指令响应解析未知错误", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), error=str(e))
            raise ParseError(f"指令响应解析未知错误: {instruction_types}", original_error=e)

        # 检查API返回码，0表示成功，非0表示失败
        api_code = response_data.get('code')

        if api_code != 0:
            Logger.debug("指令API返回错误码", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions), api_code=api_code, api_message=response_data.get('message'))
            raise NetworkError(f"指令API返回错误码: {instruction_types}, API返回错误码: {api_code}", url=request_url, status_code=response.status_code, original_error=None)

        # 返回响应数据部分
        Logger.info("执行指令成功", instruction_types=instruction_types, instruction_ids=instruction_ids, instruction_count=len(instructions))
        return response_data.get('data', {})

    @retry_on_error(max_retries=3, delay=3)
    def _execute_http_command(self, http_command: HttpCommand) -> dict:
        """
        执行HTTP命令的核心方法
        
        功能说明：
        这是Browser类中执行HTTP命令的核心方法，负责将HttpCommand对象转换为实际的HTTP请求，
        发送到浏览器节点服务，并解析响应结果。该方法处理了完整的请求生命周期，包括：
        1. 构建请求URL和请求头
        2. 发送HTTP请求
        3. 处理各种异常情况（超时、连接错误、HTTP错误等）
        4. 解析响应数据
        
        设计模式：
        采用命令模式（Command Pattern），将HTTP请求封装为HttpCommand对象，通过统一接口执行。
        这样可以：
        - 解耦请求构建和执行逻辑
        - 支持回调机制（before_callback、after_callback）
        - 统一错误处理
        
        数据流转：
        1. HttpCommand对象（包含请求参数） 
        2. -> 构建HTTP请求（URL、Headers、Body）
        3. -> 发送请求到节点API
        4. -> 接收响应文本
        5. -> 调用http_command.parse_response()解析响应
        6. -> 返回标准格式的结果字典
        
        Args:
            http_command (HttpCommand): HTTP命令对象
                - 必须包含有效的url、method、headers、body、timeout等属性
                - 必须实现parse_response方法来解析响应
        
        Returns:
            dict: HTTP命令执行结果，标准格式如下：
            {
                "data": any,        # 解析后的数据（由parse_response方法决定）
                "success": bool,    # 操作是否成功
                "code": int,        # 状态码（0表示成功）
                "message": str      # 结果消息
            }
        
        Raises:
            NetworkError: 网络相关错误（超时、连接失败、HTTP错误等）
                - Timeout: 请求超时
                - ConnectionError: 无法连接到服务器
                - HTTPError: HTTP状态码错误（非2xx）
                - RequestException: 其他请求异常
            
            BusinessError: 业务逻辑错误（响应解析失败、命令执行失败等）
                - 当parse_response方法抛出异常时
                - 当响应解析失败时
        
        请求URL构建：
        URL格式：{node_api_base_url}/http/{node_id}{http_command.url}
        示例：http://api.example.com/http/node123/browser/open
        
        请求头处理：
        - 自动添加Authorization头（Bearer Token认证）
        - 合并http_command.headers中的其他请求头
        - 如果http_command.headers中包含Authorization，会被忽略（使用API Token）
        
        异常处理策略：
        - Timeout: 请求超时，返回None状态码
        - ConnectionError: 连接失败，返回None状态码
        - HTTPError: HTTP错误，从异常对象中提取状态码
        - RequestException: 其他异常，尝试提取状态码（如果存在）
        
        使用场景：
        - 在工作流中执行HTTP命令步骤（通过HttpStep调用）
        - 直接调用执行浏览器管理操作（打开、关闭、列表查询等）
        - 批量执行HTTP命令
        
        示例：
        ```python
        # 创建打开浏览器命令
        command = HttpBitBrowserOpenCommand(id="browser123")
        
        # 执行命令
        result = browser._execute_http_command(command)
        
        # 处理结果
        if result['success']:
            browser_info = result['data']
            print(f"浏览器已打开: {browser_info['seq']}")
        ```
        """
        # 第一步：准备请求参数
        # 构建完整的请求URL：基础URL + /http/ + 节点ID + 命令的相对路径
        # 示例：http://api.example.com/http/node123/browser/open
        request_url = self.node_api_base_url + "/http/" + self.node_id + http_command.url
        
        # 初始化请求头：添加API认证Token
        # 使用Bearer Token认证方式
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
        }

        # 合并命令对象中的请求头
        # 如果命令的请求头中包含Authorization，会被忽略（使用API Token）
        for key, value in http_command.headers.items():
            if key.lower() == "authorization":
                continue  # 跳过Authorization头，使用API Token
            headers[key] = value

        timeout = http_command.timeout if http_command.timeout is not None else self.timeout

        # 获取HTTP命令的字典表示
        http_command_dict = http_command.to_dict()

        try:
            Logger.info("准备执行HTTP命令", command_type=http_command.type, command_id=http_command.id, body=http_command.body)
            # 第二步：执行HTTP POST请求
            response = requests.request(method = http_command.method, url = request_url, headers = headers, json = http_command.body, timeout = timeout)

            # 检查HTTP状态码，如果不是2xx则抛出异常
            response.raise_for_status()
            Logger.debug("HTTP命令响应成功", command_type=http_command.type, command_id=http_command.id, response=response.text)
            
        except requests.exceptions.Timeout as e:
            Logger.debug("HTTP命令执行超时", command_type=http_command.type, command_id=http_command.id, timeout=timeout)
            raise NetworkError(f"执行HTTP命令超时: {http_command.type} (ID: {http_command.id}), 超时时间: {http_command.timeout}秒", url=request_url, status_code=None, original_error=e)
        except requests.exceptions.ConnectionError as e:
            Logger.debug("HTTP命令连接失败", command_type=http_command.type, command_id=http_command.id, url=request_url)
            raise NetworkError(f"执行HTTP命令连接失败: {http_command.type} (ID: {http_command.id}), 无法连接到服务器", url=request_url, status_code=None, original_error=e)
        except requests.exceptions.HTTPError as e:
            # HTTPError 异常时，response 对象存在于异常对象中
            status_code = None
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code if hasattr(e.response, 'status_code') else None
            Logger.debug("HTTP命令HTTP错误", command_type=http_command.type, command_id=http_command.id, status_code=status_code, url=request_url)
            raise NetworkError(f"执行HTTP命令HTTP错误: {http_command.type} (ID: {http_command.id}), HTTP状态码: {status_code}", url=request_url, status_code=status_code, original_error=e)
        except requests.exceptions.RequestException as e:
            # RequestException 是其他所有异常的基类，response 可能不存在
            status_code = None
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code if hasattr(e.response, 'status_code') else None
            Logger.debug("HTTP命令网络请求失败", command_type=http_command.type, command_id=http_command.id, url=request_url)
            raise NetworkError(f"执行HTTP命令网络请求失败: {http_command.type} (ID: {http_command.id})", url=request_url, status_code=status_code, original_error=e)

        # 第三步：解析响应体

        # 返回响应文本
        return response.text

# ==================== CDP命令子类 ========================

class CdpConnectCommand(CdpCommand):
    """
    连接CDP命令类
    
    用于建立与指定标签页的Chrome DevTools Protocol连接。
    在执行其他CDP命令之前，通常需要先建立CDP连接。
    
    Attributes:
        type (str): 命令类型，固定为 "cdp_connect"
    
    Args:
        tab_id (int): 要连接的标签页ID
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Example:
        command = CdpConnectCommand(tab_id=1482755452)
        result = browser._execute_cdp_command(command)
        # result: {"tabId": 1482755452}
    """
    # 命令类型标识符
    type = "cdp_connect"
    
    def __init__(self, tab_id: int, id: str = "", ignore_error: bool = False):
        """
        初始化连接CDP命令
        
        Args:
            tab_id (int): 要连接的标签页ID
            id (str): 可选，命令ID。如果不提供，会自动生成
            ignore_error (bool): 可选，是否忽略错误，默认为False
        """
        super().__init__(ignore_error)
        # 如果未提供ID，自动生成一个基于类型和UUID的唯一ID
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 命令数据：包含要连接的标签页ID
        self.data = {
            "tabId": tab_id
        }


class CdpDisconnectCommand(CdpCommand):
    """
    断开CDP连接命令类
    
    功能说明：
    用于断开与指定标签页的Chrome DevTools Protocol连接。
    在执行完CDP操作后，通常需要断开连接以释放资源。
    
    Attributes:
        type (str): 命令类型，固定为 "cdp_disconnect"
    
    Args:
        tab_id (int): 要断开连接的标签页ID
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Example:
        command = CdpDisconnectCommand(tab_id=1482755452)
        result = browser._execute_cdp_command(command)
    """
    # 命令类型标识符，固定为 "cdp_disconnect"
    type = "cdp_disconnect"
    
    def __init__(self, tab_id: int, id: str = "", ignore_error: bool = False):
        """
        初始化断开CDP连接命令
        
        Args:
            tab_id (int): 要断开连接的标签页ID
            id (str): 可选，命令ID。如果不提供，会自动生成
            ignore_error (bool): 可选，是否忽略错误，默认为False
        """
        super().__init__(ignore_error)
        # 如果未提供ID，自动生成一个基于类型和UUID的唯一ID
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 命令数据：包含要断开连接的标签页ID
        self.data = {
            "tabId": tab_id
        }


class ListTargetsCommand(CdpCommand):
    """
    列出所有标签页命令类
    
    功能说明：
    用于获取当前浏览器节点的所有标签页列表。返回的列表包含每个标签页的详细信息，
    如标签页ID、索引、URL等。此命令通常用于查找特定域名的标签页或获取所有打开的标签页。
    
    Attributes:
        type (str): 命令类型，固定为 "list_targets"
    
    Args:
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含标签页列表，格式为：
            {
                "success": bool,
                "data": [
                    {
                        "tabId": int,
                        "tabIndex": int,
                        "url": str,
                        ...
                    },
                    ...
                ]
            }
    
    Example:
        command = ListTargetsCommand()
        result = browser._execute_cdp_command(command)
        tabs = result.get('data', [])
        for tab in tabs:
            print(f"标签页 {tab['tabId']}: {tab['url']}")
    """
    # 命令类型标识符，固定为 "list_targets"
    type = "list_targets"
    
    def __init__(self, id: str = "", ignore_error: bool = False):
        """
        初始化列出所有标签页命令
        
        Args:
            id (str): 可选，命令ID。如果不提供，会自动生成
            ignore_error (bool): 可选，是否忽略错误，默认为False
        """
        super().__init__(ignore_error)
        # 如果未提供ID，自动生成一个基于类型和UUID的唯一ID
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 命令数据：此命令不需要额外参数，使用空字典
        self.data = {}


class ExecuteJavascriptCommand(CdpCommand):
    """
    执行JavaScript代码命令类
    
    功能说明：
    用于在指定标签页中执行JavaScript代码。此命令通过CDP的Runtime.evaluate方法
    执行JavaScript代码，并返回执行结果。可以执行任意JavaScript代码，包括函数调用、
    变量访问、DOM操作等。
    
    Attributes:
        type (str): 命令类型，固定为 "execute_javascript"
    
    Args:
        tab_id (int): 要执行JavaScript的标签页ID
        params (dict): CDP方法Runtime.evaluate的参数，格式为：
            {
                "expression": str,      # 要执行的JavaScript代码
                "returnByValue": bool,   # 可选，是否返回值
                "awaitPromise": bool,    # 可选，是否等待Promise
                ...
            }
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含JavaScript执行结果，格式为：
            {
                "success": bool,
                "data": {
                    "result": any,      # JavaScript执行结果
                    "exceptionDetails": dict  # 如果有异常，包含异常详情
                }
            }
    
    Example:
        command = ExecuteJavascriptCommand(
            tab_id=1482755452,
            params={
                "expression": "document.title",
                "returnByValue": True
            }
        )
        result = browser._execute_cdp_command(command)
        title = result.get('data', {}).get('result', {}).get('value')
    """
    # 命令类型标识符，固定为 "execute_javascript"
    type = "execute_javascript"
    
    def __init__(self, tab_id: int, params: dict, id: str = "", ignore_error: bool = False):
        """
        初始化执行JavaScript代码命令
        
        Args:
            tab_id (int): 要执行JavaScript的标签页ID
            params (dict): CDP方法Runtime.evaluate的参数
            id (str): 可选，命令ID。如果不提供，会自动生成
            ignore_error (bool): 可选，是否忽略错误，默认为False
        """
        super().__init__(ignore_error)
        # 如果未提供ID，自动生成一个基于类型和UUID的唯一ID
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 命令数据：包含标签页ID和JavaScript执行参数
        self.data = {
            "tabId": tab_id,
            "params": params
        }


class TakeElementScreenshotCommand(CdpCommand):
    """
    截取元素截图命令类
    
    功能说明：
    用于截取指定HTML元素的截图。此命令会先定位元素，然后截取该元素的可见区域，
    返回截图的base64编码数据。常用于验证元素显示、调试元素定位等场景。
    
    Attributes:
        type (str): 命令类型，固定为 "take_element_screenshot"
    
    Args:
        tab_id (int): 要截图的标签页ID
        selector (str): 元素选择器，用于定位要截图的元素
        selector_type (str): 可选，选择器类型，可选值：
            - "css": CSS选择器（默认）
            - "id": ID选择器
            - "tag": 标签名选择器
            - "text": 文本内容选择器
            默认为 "css"
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含截图数据，格式为：
            {
                "success": bool,
                "data": {
                    "dataUrl": str  # 截图的data URL，格式为 "data:image/png;base64,..."
                }
            }
    
    Example:
        command = TakeElementScreenshotCommand(
            tab_id=1482755452,
            selector="button.login",
            selector_type="css"
        )
        result = browser._execute_cdp_command(command)
        screenshot_data = result.get('data', {}).get('dataUrl')
    """
    # 命令类型标识符，固定为 "take_element_screenshot"
    type = "take_element_screenshot"
    def __init__(self, tab_id: int, selector: str, selector_type: str = "css", id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
            "selector": selector,
            "selectorType": selector_type
        }


class SendCommandCommand(CdpCommand):
    """
    执行CDP命令类
    
    功能说明：
    用于执行任意的Chrome DevTools Protocol命令。这是一个通用的CDP命令包装器，
    可以执行任何CDP方法，如Runtime.evaluate、Page.navigate、Network.enable等。
    提供了最大的灵活性，但需要手动构造CDP方法参数。
    
    Attributes:
        type (str): 命令类型，固定为 "send_command"
    
    Args:
        tab_id (int): 要执行CDP命令的标签页ID
        method (str): CDP方法名称，如 "Runtime.evaluate"、"Page.navigate"等
        params (dict|None): 可选，CDP方法的参数字典。不同的方法需要不同的参数
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含CDP方法的返回数据，格式为：
            {
                "success": bool,
                "data": any  # CDP方法的返回结果，格式取决于具体的方法
            }
    
    Example:
        # 执行Runtime.evaluate方法
        command = SendCommandCommand(
            tab_id=1482755452,
            method="Runtime.evaluate",
            params={
                "expression": "document.title",
                "returnByValue": True
            }
        )
        result = browser._execute_cdp_command(command)
        
        # 执行Page.navigate方法
        command = SendCommandCommand(
            tab_id=1482755452,
            method="Page.navigate",
            params={"url": "https://example.com"}
        )
        result = browser._execute_cdp_command(command)
    """
    # 命令类型标识符，固定为 "send_command"
    type = "send_command"
    def __init__(self, tab_id: int, method: str, params: dict = None, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
            "method": method,
            "params": params
        }


class GrepSourceCommand(CdpCommand):
    """
    源码搜索命令类
    
    功能说明：
    用于在指定标签页的页面源码中搜索指定的文本模式。支持正则表达式搜索，
    可以搜索HTML源码、JavaScript源码等。常用于查找特定的代码片段、验证页面内容等。
    
    Attributes:
        type (str): 命令类型，固定为 "grep_source"
    
    Args:
        tab_id (int): 要搜索的标签页ID
        pattern (str): 搜索模式，可以是普通文本或正则表达式
        case_sensitive (bool): 可选，是否区分大小写，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含匹配结果，格式为：
            {
                "success": bool,
                "data": {
                    "matches": [  # 匹配结果列表
                        {
                            "line": int,      # 行号
                            "content": str,    # 匹配的行内容
                            ...
                        },
                        ...
                    ]
                }
            }
    
    Example:
        # 搜索包含"login"的代码
        command = GrepSourceCommand(
            tab_id=1482755452,
            pattern="login",
            case_sensitive=False
        )
        result = browser._execute_cdp_command(command)
        matches = result.get('data', {}).get('matches', [])
    """
    # 命令类型标识符，固定为 "grep_source"
    type = "grep_source"
    def __init__(self, tab_id: int, pattern: str, case_sensitive: bool = False, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
            "pattern": pattern,
            "caseSensitive": case_sensitive
        }


class GetNetworkLogsCommand(CdpCommand):
    """
    获取网络日志命令类
    
    功能说明：
    用于获取指定标签页的网络请求日志。可以获取所有网络请求的详细信息，包括
    请求URL、请求方法、响应状态码、请求头、响应头等。支持过滤、分页、分组等功能。
    常用于网络请求分析、API调用追踪、性能分析等场景。
    
    注意：在执行此命令前，通常需要先调用InitNetworkLogsCommand初始化网络日志收集。
    
    Attributes:
        type (str): 命令类型，固定为 "get_network_logs"
    
    Args:
        tab_id (int): 要获取网络日志的标签页ID
        clear (bool): 可选，获取后是否清空日志，默认为False
        filter (dict|None): 可选，过滤条件字典，用于筛选网络请求
        limit (int|None): 可选，返回的最大记录数，用于限制结果数量
        offset (int|None): 可选，偏移量，用于分页查询
        request_id (str|None): 可选，请求ID，用于获取特定请求的日志
        group_by_request (bool): 可选，是否按请求分组，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含网络日志列表，格式为：
            {
                "success": bool,
                "data": [
                    {
                        "requestId": str,      # 请求ID
                        "url": str,            # 请求URL
                        "method": str,         # 请求方法
                        "status": int,         # 响应状态码
                        "requestHeaders": dict, # 请求头
                        "responseHeaders": dict, # 响应头
                        ...
                    },
                    ...
                ]
            }
    
    Example:
        # 先初始化网络日志收集
        init_cmd = InitNetworkLogsCommand(tab_id=1482755452)
        browser._execute_cdp_command(init_cmd)
        
        # 执行一些网络请求...
        
        # 获取网络日志
        command = GetNetworkLogsCommand(
            tab_id=1482755452,
            filter={"status": 200},  # 只获取状态码为200的请求
            limit=100
        )
        result = browser._execute_cdp_command(command)
        logs = result.get('data', [])
    """
    # 命令类型标识符，固定为 "get_network_logs"
    type = "get_network_logs"
    def __init__(self, tab_id: int, clear: bool = False, filter: dict = None, limit: int = None, 
                 offset: int = None, request_id: str = None, group_by_request: bool = False, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
        }
        if clear:
            self.data["clear"] = clear
        if filter:
            self.data["filter"] = filter
        if limit is not None:
            self.data["limit"] = limit
        if offset is not None:
            self.data["offset"] = offset
        if request_id:
            self.data["requestId"] = request_id
        if group_by_request:
            self.data["groupByRequest"] = group_by_request


class InitNetworkLogsCommand(CdpCommand):
    """
    初始化网络日志收集命令类
    
    功能说明：
    用于初始化指定标签页的网络日志收集功能。调用此命令后，浏览器会开始记录
    该标签页的所有网络请求和响应。之后可以通过GetNetworkLogsCommand获取这些日志。
    
    注意：此命令需要在获取网络日志之前调用，否则无法获取到网络请求信息。
    
    Attributes:
        type (str): 命令类型，固定为 "init_network_logs"
    
    Args:
        tab_id (int): 要初始化网络日志收集的标签页ID
        clear (bool): 可选，是否清空之前的日志，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，格式为：
            {
                "success": bool,
                "data": dict  # 初始化结果
            }
    
    Example:
        # 初始化网络日志收集
        command = InitNetworkLogsCommand(tab_id=1482755452, clear=True)
        result = browser._execute_cdp_command(command)
        
        # 执行一些操作，产生网络请求...
        
        # 获取网络日志
        get_logs_cmd = GetNetworkLogsCommand(tab_id=1482755452)
        logs = browser._execute_cdp_command(get_logs_cmd)
    """
    # 命令类型标识符，固定为 "init_network_logs"
    type = "init_network_logs"
    def __init__(self, tab_id: int, clear: bool = False, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
        }
        if clear:
            self.data["clear"] = clear


class CloseNetworkLogsCommand(CdpCommand):
    """
    关闭网络日志收集命令类
    
    功能说明：
    用于关闭指定标签页的网络日志收集功能。调用此命令后，浏览器会停止记录
    该标签页的网络请求和响应。通常在获取完网络日志后调用，以释放资源。
    
    注意：关闭后仍可以通过GetNetworkLogsCommand获取之前已收集的日志（如果未清空）。
    
    Attributes:
        type (str): 命令类型，固定为 "close_network_logs"
    
    Args:
        tab_id (int): 要关闭网络日志收集的标签页ID
        clear (bool): 可选，关闭时是否清空已收集的日志，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，格式为：
            {
                "success": bool,
                "data": dict  # 关闭结果
            }
    
    Example:
        # 初始化网络日志收集
        init_cmd = InitNetworkLogsCommand(tab_id=1482755452)
        browser._execute_cdp_command(init_cmd)
        
        # 执行操作并获取日志...
        
        # 关闭网络日志收集
        close_cmd = CloseNetworkLogsCommand(tab_id=1482755452, clear=True)
        browser._execute_cdp_command(close_cmd)
    """
    # 命令类型标识符，固定为 "close_network_logs"
    type = "close_network_logs"
    def __init__(self, tab_id: int, clear: bool = False, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
        }
        if clear:
            self.data["clear"] = clear


class GetConsoleLogsCommand(CdpCommand):
    """
    获取控制台日志命令类
    
    功能说明：
    用于获取指定标签页的浏览器控制台日志。可以获取JavaScript的console.log、
    console.error、console.warn等输出，以及JavaScript运行时错误信息。
    常用于调试JavaScript代码、追踪页面错误等场景。
    
    注意：在执行此命令前，通常需要先调用InitConsoleLogsCommand初始化控制台日志收集。
    
    Attributes:
        type (str): 命令类型，固定为 "get_console_logs"
    
    Args:
        tab_id (int): 要获取控制台日志的标签页ID
        clear (bool): 可选，获取后是否清空日志，默认为False
        filter (dict|None): 可选，过滤条件字典，用于筛选日志
        limit (int|None): 可选，返回的最大记录数，用于限制结果数量
        offset (int|None): 可选，偏移量，用于分页查询
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含控制台日志列表，格式为：
            {
                "success": bool,
                "data": [
                    {
                        "level": str,      # 日志级别：log、error、warning等
                        "text": str,       # 日志内容
                        "timestamp": int,  # 时间戳
                        "url": str,        # 产生日志的URL
                        ...
                    },
                    ...
                ]
            }
    
    Example:
        # 先初始化控制台日志收集
        init_cmd = InitConsoleLogsCommand(tab_id=1482755452)
        browser._execute_cdp_command(init_cmd)
        
        # 执行一些操作，产生控制台输出...
        
        # 获取控制台日志
        command = GetConsoleLogsCommand(
            tab_id=1482755452,
            filter={"level": "error"},  # 只获取错误日志
            limit=50
        )
        result = browser._execute_cdp_command(command)
        logs = result.get('data', [])
    """
    # 命令类型标识符，固定为 "get_console_logs"
    type = "get_console_logs"
    def __init__(self, tab_id: int, clear: bool = False, filter: dict = None, 
                 limit: int = None, offset: int = None, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
        }
        if clear:
            self.data["clear"] = clear
        if filter:
            self.data["filter"] = filter
        if limit is not None:
            self.data["limit"] = limit
        if offset is not None:
            self.data["offset"] = offset


class InitConsoleLogsCommand(CdpCommand):
    """
    初始化控制台日志收集命令类
    
    功能说明：
    用于初始化指定标签页的控制台日志收集功能。调用此命令后，浏览器会开始记录
    该标签页的所有控制台输出（console.log、console.error等）和JavaScript运行时错误。
    之后可以通过GetConsoleLogsCommand获取这些日志。
    
    注意：此命令需要在获取控制台日志之前调用，否则无法获取到控制台输出信息。
    
    Attributes:
        type (str): 命令类型，固定为 "init_console_logs"
    
    Args:
        tab_id (int): 要初始化控制台日志收集的标签页ID
        clear (bool): 可选，是否清空之前的日志，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，格式为：
            {
                "success": bool,
                "data": dict  # 初始化结果
            }
    
    Example:
        # 初始化控制台日志收集
        command = InitConsoleLogsCommand(tab_id=1482755452, clear=True)
        result = browser._execute_cdp_command(command)
        
        # 执行一些操作，产生控制台输出...
        
        # 获取控制台日志
        get_logs_cmd = GetConsoleLogsCommand(tab_id=1482755452)
        logs = browser._execute_cdp_command(get_logs_cmd)
    """
    # 命令类型标识符，固定为 "init_console_logs"
    type = "init_console_logs"
    def __init__(self, tab_id: int, clear: bool = False, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
        }
        if clear:
            self.data["clear"] = clear


class CloseConsoleLogsCommand(CdpCommand):
    """
    关闭控制台日志收集命令类
    
    功能说明：
    用于关闭指定标签页的控制台日志收集功能。调用此命令后，浏览器会停止记录
    该标签页的控制台输出和JavaScript运行时错误。通常在获取完控制台日志后调用，以释放资源。
    
    注意：关闭后仍可以通过GetConsoleLogsCommand获取之前已收集的日志（如果未清空）。
    
    Attributes:
        type (str): 命令类型，固定为 "close_console_logs"
    
    Args:
        tab_id (int): 要关闭控制台日志收集的标签页ID
        clear (bool): 可选，关闭时是否清空已收集的日志，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，格式为：
            {
                "success": bool,
                "data": dict  # 关闭结果
            }
    
    Example:
        # 初始化控制台日志收集
        init_cmd = InitConsoleLogsCommand(tab_id=1482755452)
        browser._execute_cdp_command(init_cmd)
        
        # 执行操作并获取日志...
        
        # 关闭控制台日志收集
        close_cmd = CloseConsoleLogsCommand(tab_id=1482755452, clear=True)
        browser._execute_cdp_command(close_cmd)
    """
    # 命令类型标识符，固定为 "close_console_logs"
    type = "close_console_logs"
    def __init__(self, tab_id: int, clear: bool = False, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id,
        }
        if clear:
            self.data["clear"] = clear


class CreateTabAndNavigateCommand(CdpCommand):
    """
    创建新标签页并导航命令类
    
    功能说明：
    用于创建一个新的浏览器标签页并导航到指定的URL。这是一个组合命令，相当于
    先创建标签页，然后导航到URL。返回新创建的标签页信息（ID、索引、URL等）。
    
    Attributes:
        type (str): 命令类型，固定为 "create_tab_and_navigate"
    
    Args:
        url (str): 要导航的URL地址
        active (bool): 可选，是否激活新标签页（使其成为当前活动标签页），默认为True
        new_window (bool): 可选，是否在新窗口中创建标签页，默认为False
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，包含新标签页信息，格式为：
            {
                "success": bool,
                "data": {
                    "tabId": int,      # 新标签页的ID
                    "tabIndex": int,    # 新标签页的索引
                    "url": str          # 导航后的URL
                }
            }
    
    Example:
        command = CreateTabAndNavigateCommand(
            url="https://example.com",
            active=True,
            new_window=False
        )
        result = browser._execute_cdp_command(command)
        tab_id = result.get('data', {}).get('tabId')
    """
    # 命令类型标识符，固定为 "create_tab_and_navigate"
    type = "create_tab_and_navigate"
    def __init__(self, url: str, id: str = "", active: bool = True, new_window: bool = False, ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "url": url,
        }
        if active:
            self.data["active"] = active
        if new_window:
            self.data["newWindow"] = new_window


class UpdateNodeNameCommand(CdpCommand):
    """
    更新节点名称命令类
    
    功能说明：
    用于更新浏览器节点的名称。节点名称用于标识和管理浏览器节点，可以通过
    节点名称查找和操作节点。此命令会修改节点的显示名称，不影响节点的功能。
    
    Attributes:
        type (str): 命令类型，固定为 "update_node_name"
    
    Args:
        node_name (str): 新的节点名称
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，格式为：
            {
                "success": bool,
                "data": dict  # 更新结果
            }
    
    Example:
        command = UpdateNodeNameCommand(node_name="My Browser Node")
        result = browser._execute_cdp_command(command)
    """
    # 命令类型标识符，固定为 "update_node_name"
    type = "update_node_name"
    def __init__(self, node_name: str, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "node_name": node_name
        }


class CloseTabCommand(CdpCommand):
    """
    关闭标签页命令类
    
    功能说明：
    用于关闭指定的浏览器标签页。关闭后，该标签页的所有资源会被释放，
    无法再对该标签页执行任何操作。常用于清理不再使用的标签页。
    
    Attributes:
        type (str): 命令类型，固定为 "close_tab"
    
    Args:
        tab_id (int): 要关闭的标签页ID
        id (str): 可选，命令ID。如果不提供，会自动生成一个唯一ID
        ignore_error (bool): 可选，是否忽略错误，默认为False
    
    Returns:
        dict: 命令执行结果，格式为：
            {
                "success": bool,
                "data": dict  # 关闭结果
            }
    
    Example:
        command = CloseTabCommand(tab_id=1482755452)
        result = browser._execute_cdp_command(command)
    """
    # 命令类型标识符，固定为 "close_tab"
    type = "close_tab"
    def __init__(self, tab_id: int, id: str = "", ignore_error: bool = False):
        super().__init__(ignore_error)
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.data = {
            "tabId": tab_id
        }


# ==================== Instruction指令子类 ========================

class ElementClass:
    """
    HTML元素封装类
    
    用于封装网页中的HTML元素信息，包括元素的选择器、类型、位置关系等。
    此类用于在指令系统中定位和操作网页元素。
    
    Attributes:
        tabId (int): 元素所在的标签页ID
        name (str): 元素的唯一名称，用于在指令中引用该元素
        selector (str): 元素选择器，用于定位元素
        selectorType (str): 选择器类型，可选值：
            - "css": CSS选择器（如 "div.class"、"#id" 等）
            - "id": ID选择器
            - "tag": 标签名选择器
            - "text": 文本内容选择器
        description (str|None): 元素的描述信息，用于文档和调试
        backup (str|None): 元素的备注信息
        text (str|None): 元素的文本内容（当selectorType为"text"时使用）
        parentName (str|None): 父元素的名称（用于CSS选择器类型的相对定位）
        childrenName (str|None): 子元素的名称（用于CSS选择器类型的相对定位）
        siblingName (str|None): 兄弟元素的名称（用于CSS选择器类型的相对定位）
        siblingOffset (int|None): 兄弟元素的偏移量（用于CSS选择器类型的相对定位）
    
    Args:
        tab_id (int): 元素所在的标签页ID
        name (str): 元素的唯一名称
        selector (str): 元素选择器
        selectorType (str): 选择器类型，可选值：css, id, tag, text
        description (str|None): 可选，元素描述
        backup (str|None): 可选，元素备注
        text (str|None): 可选，元素文本（text选择器类型时使用）
        parentName (str|None): 可选，父元素名称（css选择器类型时使用）
        childrenName (str|None): 可选，子元素名称（css选择器类型时使用）
        siblingName (str|None): 可选，兄弟元素名称（css选择器类型时使用）
        siblingOffset (int|None): 可选，兄弟元素偏移量（css选择器类型时使用）
    
    Example:
        # CSS选择器
        element = ElementClass(
            tab_id=1,
            name="login_button",
            selector="button.login-btn",
            selectorType="css",
            description="登录按钮"
        )
        
        # 文本选择器（带父元素）
        element = ElementClass(
            tab_id=1,
            name="submit_btn",
            selector="span",
            selectorType="text",
            text="Submit",
            parentName="form_container"
        )
    """
    def __init__(self, tab_id: int, name: str, selector: str, selectorType: str, description: str = None, backup: str = None, 
                text: str = None, parentName: str = None, childrenName: str = None, siblingName: str = None, siblingOffset: int = None):
        """
        初始化HTML元素对象
        
        Args:
            tab_id (int): 元素所在的标签页ID
            name (str): 元素的唯一名称
            selector (str): 元素选择器
            selectorType (str): 选择器类型
            description (str|None): 可选，元素描述
            backup (str|None): 可选，元素备注
            text (str|None): 可选，元素文本
            parentName (str|None): 可选，父元素名称
            childrenName (str|None): 可选，子元素名称
            siblingName (str|None): 可选，兄弟元素名称
            siblingOffset (int|None): 可选，兄弟元素偏移量
        """
        # 元素所在的标签页ID
        self.tabId = tab_id
        # 元素的唯一名称，用于在指令中引用该元素
        self.name = name
        # 元素的描述信息，用于文档和调试
        self.description = description
        # 元素的备注信息
        self.backup = backup
        # 元素的文本内容（当selectorType为"text"时使用）
        self.text = text
        # 元素选择器，用于定位元素
        self.selector = selector
        # 选择器类型：css, id, tag, text
        self.selectorType = selectorType
        # 父元素的名称（用于CSS选择器类型的相对定位）
        self.parentName = parentName
        # 子元素的名称（用于CSS选择器类型的相对定位）
        self.childrenName = childrenName
        # 兄弟元素的名称（用于CSS选择器类型的相对定位）
        self.siblingName = siblingName
        # 兄弟元素的偏移量（用于CSS选择器类型的相对定位）
        self.siblingOffset = siblingOffset

    def to_dict(self) -> dict:
        """
        将元素对象转换为字典格式，用于API请求
        
        功能说明：
        将ElementClass对象的所有属性转换为字典格式，便于序列化和API传输。
        只有非None的属性会被包含在返回的字典中。
        
        Returns:
            dict: 包含元素所有属性的字典，格式为：
                {
                    "tabId": int,              # 元素所在的标签页ID（必需）
                    "name": str,               # 元素的唯一名称（必需）
                    "selector": str,           # 元素选择器（必需）
                    "selectorType": str,       # 选择器类型（必需）
                    "description": str,        # 可选，元素描述
                    "backup": str,            # 可选，元素备注
                    "text": str,              # 可选，元素文本（text选择器类型时使用）
                    "parentName": str,        # 可选，父元素名称（css选择器类型时使用）
                    "childrenName": str,      # 可选，子元素名称（css选择器类型时使用）
                    "siblingName": str,       # 可选，兄弟元素名称（css选择器类型时使用）
                    "siblingOffset": int      # 可选，兄弟元素偏移量（css选择器类型时使用）
                }
        
        Note:
            - 只有非None的属性会被包含在返回的字典中
            - 必需属性（tabId, name, selector, selectorType）总是会被包含
            - 可选属性只有在有值时才被包含
        
        Example:
            element = ElementClass(
                tab_id=1,
                name="login_button",
                selector="button.login",
                selectorType="css",
                description="登录按钮"
            )
            element_dict = element.to_dict()
            # 返回: {
            #     "tabId": 1,
            #     "name": "login_button",
            #     "selector": "button.login",
            #     "selectorType": "css",
            #     "description": "登录按钮"
            # }
        """
        # 构建基础结果字典，包含必需属性
        result = {
            "tabId": self.tabId,
            "name": self.name,
            "selector": self.selector,
            "selectorType": self.selectorType,
        }
        # 如果description不为None，添加到结果中
        if self.description:
            result["description"] = self.description
        # 如果backup不为None，添加到结果中
        if self.backup:
            result["backup"] = self.backup
        # 如果text不为None，添加到结果中（text选择器类型时使用）
        if self.text:
            result["text"] = self.text
        # 如果parentName不为None，添加到结果中（用于相对定位）
        if self.parentName:
            result["parentName"] = self.parentName
        # 如果childrenName不为None，添加到结果中（用于相对定位）
        if self.childrenName:
            result["childrenName"] = self.childrenName
        # 如果siblingName不为None，添加到结果中（用于相对定位）
        if self.siblingName:
            result["siblingName"] = self.siblingName
        # 如果siblingOffset不为None，添加到结果中（用于相对定位）
        if self.siblingOffset:
            result["siblingOffset"] = self.siblingOffset
        return result


class NavigateInstruction(Instruction):
    """
    页面导航指令类
    
    功能说明：
    用于在指定标签页中导航到指定的URL。此指令会加载目标URL的页面内容，
    等待页面加载完成（load事件），然后返回导航后的URL。支持相对URL和绝对URL。
    
    Attributes:
        type (str): 指令类型，固定为 "navigate"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        url (str): 要导航的URL地址，可以是绝对URL（如"https://example.com"）或相对URL
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0。导航前会等待此时间
        retry (int): 可选，重试次数，默认为0。如果导航失败，会重试指定次数
        timeout (int): 可选，超时时间（秒），默认为150。如果页面加载超过此时间，会超时失败
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "url": str      # 导航后的URL
                }
            }
    
    Example:
        instruction = NavigateInstruction(
            tab_id=1,
            url="https://example.com",
            delay=2,  # 导航前等待2秒
            timeout=60  # 超时时间60秒
        )
        result = browser._execute_instruction([instruction])
        navigated_url = result.get('data', {}).get('url')
    """
    # 指令类型标识符，固定为 "navigate"
    type = "navigate"
    def __init__(self, tab_id: int, url: str, instruction_id: str = "", delay: int = 0, 
                 retry: int = 0, timeout: int = 150, ignore_error: bool = False, created_at: int = 0):
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.params = {"url": url}


class ExecuteScriptInstruction(Instruction):
    """
    页面JavaScript执行指令类
    
    功能说明：
    用于在指定标签页中执行JavaScript代码。此指令通过CDP的Runtime.evaluate方法
    执行JavaScript代码，并返回执行结果。可以执行任意JavaScript代码，包括函数调用、
    变量访问、DOM操作、异步操作（Promise）等。
    
    Attributes:
        type (str): 指令类型，固定为 "execute_script"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        params (dict): CDP方法Runtime.evaluate的参数，格式为：
            {
                "expression": str,        # 必需，要执行的JavaScript代码
                "returnByValue": bool,     # 可选，是否返回值，默认为False
                "awaitPromise": bool,      # 可选，是否等待Promise，默认为False
                "generatePreview": bool,   # 可选，是否生成预览，默认为False
                "userGesture": bool,       # 可选，是否模拟用户手势，默认为False
                ...
            }
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "results": any  # JavaScript执行结果
                }
            }
    
    Example:
        # 执行简单的JavaScript代码
        instruction = ExecuteScriptInstruction(
            tab_id=1,
            params={
                "expression": "document.title",
                "returnByValue": True
            }
        )
        result = browser._execute_instruction([instruction])
        title = result.get('data', {}).get('results', {}).get('value')
        
        # 执行异步操作
        instruction = ExecuteScriptInstruction(
            tab_id=1,
            params={
                "expression": "fetch('/api/data').then(r => r.json())",
                "awaitPromise": True,
                "returnByValue": True
            }
        )
        result = browser._execute_instruction([instruction])
    """
    # 指令类型标识符，固定为 "execute_script"
    type = "execute_script"
    def __init__(self, tab_id: int, params: dict, instruction_id: str = "", delay: int = 0, 
                 retry: int = 0, timeout: int = 150, ignore_error: bool = False, created_at: int = 0):
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.params = params


class FindElementInstruction(Instruction):
    """
    元素定位指令类
    
    功能说明：
    用于在指定标签页中定位HTML元素。此指令会根据ElementClass对象中定义的选择器
    和定位方式查找元素，如果找到元素，会将元素信息保存到变量中，并返回元素的详细信息。
    支持多种选择器类型（CSS、ID、标签名、文本内容）和相对定位（父元素、子元素、兄弟元素）。
    
    Attributes:
        type (str): 指令类型，固定为 "find_element"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        element (ElementClass): ElementClass对象，包含元素的定位信息（选择器、类型等）
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0。如果元素未找到，会重试指定次数
        timeout (int): 可选，超时时间（秒），默认为150。如果元素查找超过此时间，会超时失败
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "elementData": {
                        "name": str,      # 元素名称
                        "nodeId": int,    # 元素的节点ID
                        "tag": str,       # 元素标签名
                        ...
                    }
                }
            }
    
    Note:
        - 如果元素找到，会将元素名称保存到变量中，变量值为True
        - 元素名称由ElementClass对象的name属性定义
        - 支持相对定位：可以通过parentName、childrenName、siblingName等属性进行相对定位
    
    Example:
        # 使用CSS选择器定位元素
        element = ElementClass(
            tab_id=1,
            name="login_button",
            selector="button.login-btn",
            selectorType="css",
            description="登录按钮"
        )
        instruction = FindElementInstruction(
            tab_id=1,
            element=element,
            timeout=30
        )
        result = browser._execute_instruction([instruction])
        
        # 使用文本内容定位元素（带父元素）
        element = ElementClass(
            tab_id=1,
            name="submit_btn",
            selector="span",
            selectorType="text",
            text="Submit",
            parentName="form_container"
        )
        instruction = FindElementInstruction(tab_id=1, element=element)
        result = browser._execute_instruction([instruction])
    """
    # 指令类型标识符，固定为 "find_element"
    type = "find_element"
    def __init__(self, tab_id: int, element: ElementClass, instruction_id: str = "", delay: int = 0, 
                 retry: int = 0, timeout: int = 15, ignore_error: bool = False, created_at: int = 0):
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.params = {"element": element.to_dict()}


class InputInstruction(Instruction):
    """
    文本输入指令类
    
    功能说明：
    用于在指定的输入元素中输入文本。此指令会先定位元素，然后在元素中输入指定的文本。
    支持在输入前清空输入框（通过clear参数控制）。
    
    Attributes:
        type (str): 指令类型，固定为 "input"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        element_name (str): 元素名称，必须是之前通过FindElementInstruction找到的元素名称
        text (str): 要输入的文本内容
        clear (bool): 可选，是否在输入前先清空输入框，默认为False
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "text": str     # 实际输入的文本
                }
            }
    
    Example:
        # 先查找输入框元素
        element = ElementClass(tab_id=1, name="username_input", selector="#username", selectorType="css")
        find_instruction = FindElementInstruction(tab_id=1, element=element)
        
        # 然后输入文本
        input_instruction = InputInstruction(
            tab_id=1,
            element_name="username_input",
            text="my_username",
            clear=True  # 先清空再输入
        )
        result = browser._execute_instruction([input_instruction])
    """
    # 指令类型标识符，固定为 "input"
    type = "input"
    
    def __init__(self, tab_id: int, element_name: str, text: str, clear: bool = False,   
                 instruction_id: str = "", delay: int = 0, retry: int = 0, timeout: int = 30, 
                 ignore_error: bool = False, created_at: int = 0):
        """
        初始化文本输入指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            element_name (str): 元素名称
            text (str): 要输入的文本内容
            clear (bool): 可选，是否在输入前先清空输入框
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 指令参数：包含元素名称和要输入的文本
        self.params = {
            "elementName": element_name,
            "text": text
        }
        # 如果clear为True，添加clear参数
        if clear:
            self.params["clear"] = clear


class KeyboardInstruction(Instruction):
    """
    键盘操作指令类
    
    功能说明：
    用于模拟键盘操作，如按键、输入文本等。支持多种键盘操作类型，可以在指定元素上
    执行键盘操作，也可以在整个页面上执行键盘操作。
    
    Attributes:
        type (str): 指令类型，固定为 "keyboard"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        action (str): 键盘操作类型，可选值：
            - "press": 按下并释放按键（模拟按键操作）
            - "type": 输入文本（模拟打字）
            - "keydown": 按下按键（不释放）
            - "keyup": 释放按键
        key (str): 可选，单字符输入按键名称，主要用于特殊按键，如 "Enter", "Tab", "Escape"等
        text (str): 可选，多字符输入文本内容
        element_name (str): 可选，元素名称。如果提供，键盘操作会在指定元素上执行
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为30
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Note:
        key 和 text 参数至少需要提供一个。如果两者都提供，优先使用 key 参数。
        - key: 用于单字符输入按键，主要用于特殊按键（如 Enter, Tab, Escape 等）
        - text: 用于多字符输入文本，会逐个字符输入
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": dict       # 仅在成功时存在，包含 key/text 和 action
            }
    
    Example:
        # 在输入框中按Enter键（使用key参数）
        keyboard_instruction = KeyboardInstruction(
            tab_id=1,
            action="press",
            key="Enter",
            element_name="search_input"
        )
        
        # 输入文本（使用text参数）
        keyboard_instruction = KeyboardInstruction(
            tab_id=1,
            action="type",
            text="Hello World"
        )
        
        # 按下单个字符按键（使用key参数）
        keyboard_instruction = KeyboardInstruction(
            tab_id=1,
            action="press",
            key="a"
        )
    """
    # 指令类型标识符，固定为 "keyboard"
    type = "keyboard"
    
    def __init__(self, tab_id: int, action: str, key: str = None, text: str = None, 
                 element_name: str = None, instruction_id: str = "", delay: int = 1, 
                 retry: int = 0, timeout: int = 30, ignore_error: bool = False, created_at: int = 0):
        """
        初始化键盘操作指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            action (str): 键盘操作类型
            key (str): 可选，单字符输入按键名称，主要用于特殊按键
            text (str): 可选，多字符输入文本内容
            element_name (str): 可选，元素名称
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        
        Raises:
            ValueError: 如果 key 和 text 都未提供
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 指令参数：包含操作类型
        self.params = {"action": action}
        # 如果提供了 key 参数，添加到参数中
        if key is not None and key != "":
            self.params["key"] = key
        # 如果提供了 text 参数，添加到参数中
        if text is not None and text != "":
            self.params["text"] = text
        # 如果提供了元素名称，添加到参数中
        if element_name:
            self.params["elementName"] = element_name
        # 验证至少提供了 key 或 text 之一
        if "key" not in self.params and "text" not in self.params:
            raise ValueError("Either 'key' or 'text' parameter must be provided")


class MouseInstruction(Instruction):
    """
    鼠标操作指令类
    
    功能说明：
    用于模拟鼠标操作，如点击、双击、右键点击、悬停、移动等。支持在指定元素上
    执行鼠标操作，也可以在整个页面上执行鼠标操作（通过坐标）。支持多种模拟方式，
    可以模拟真实的鼠标移动轨迹，也可以直接执行操作。
    
    Attributes:
        type (str): 指令类型，固定为 "mouse"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        action (str): 鼠标操作类型，可选值：
            - "click": 左键单击
            - "dblclick": 左键双击
            - "rightclick": 右键单击
            - "hover": 鼠标悬停
            - "left_mousedown": 左键按下（不释放）
            - "left_mouseup": 左键释放
            - "right_mousedown": 右键按下（不释放）
            - "right_mouseup": 右键释放
            - "move_to": 移动鼠标到指定坐标
        element_name (str): 可选，元素名称。如果提供，鼠标操作会在指定元素上执行
        simulate (str): 可选，模拟方式，可选值：
            - "calculated": 计算鼠标移动轨迹，模拟真实鼠标移动（默认）
            - "simulated": 简化模拟，快速移动到目标位置
            - "none": 不模拟移动，直接执行操作
        x (int): 可选，X坐标（像素）。当action为"move_to"时使用，或当element_name未提供时使用
        y (int): 可选，Y坐标（像素）。当action为"move_to"时使用，或当element_name未提供时使用
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为3。操作后等待此时间，确保操作完成
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": dict       # 仅在成功时存在
            }
    
    Example:
        # 点击元素
        instruction = MouseInstruction(
            tab_id=1,
            action="click",
            element_name="login_button",
            simulate="calculated"  # 模拟真实鼠标移动
        )
        
        # 双击元素
        instruction = MouseInstruction(
            tab_id=1,
            action="dblclick",
            element_name="item",
            delay=1
        )
        
        # 移动到指定坐标
        instruction = MouseInstruction(
            tab_id=1,
            action="move_to",
            x=100,
            y=200
        )
        
        # 右键点击
        instruction = MouseInstruction(
            tab_id=1,
            action="rightclick",
            element_name="menu_item"
        )
    """
    # 指令类型标识符，固定为 "mouse"
    type = "mouse"
    def __init__(self, tab_id: int, action: str, element_name: str = None, simulate: str = None, 
                 x: int = None, y: int = None, instruction_id: str = "", delay: int = 3, 
                 retry: int = 0, timeout: int = 30, ignore_error: bool = False, created_at: int = 0):
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        self.params = {"action": action}
        if element_name:
            self.params["elementName"] = element_name
        if simulate:
            self.params["simulate"] = simulate
        if x is not None:
            self.params["x"] = x
        if y is not None:
            self.params["y"] = y


class GetAttributeInstruction(Instruction):
    """
    获取元素属性指令类
    
    功能说明：
    用于获取指定元素的属性值。此指令会先定位元素，然后获取指定属性的值。
    支持将属性值保存到变量中（通过usage参数控制）。
    
    Attributes:
        type (str): 指令类型，固定为 "get_attribute"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        element_name (str): 元素名称，必须是之前通过FindElementInstruction找到的元素名称
        attribute (str): 要获取的属性名称，如 "href", "value", "class", "aria-disabled"等
        usage (str): 可选，使用方式，可选值：
            - "variable": 将属性值保存到变量中，变量名为 "{element_name}.{attribute}"
            - "data": 仅返回属性值，不保存到变量
            - "none": 不保存也不返回（通常不使用）
            默认为None，表示不设置usage参数
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "value": str   # 属性值
                }
            }
    
    Example:
        # 先查找元素
        element = ElementClass(tab_id=1, name="link", selector="a.link", selectorType="css")
        find_instruction = FindElementInstruction(tab_id=1, element=element)
        
        # 获取href属性并保存到变量
        get_attr_instruction = GetAttributeInstruction(
            tab_id=1,
            element_name="link",
            attribute="href",
            usage="variable"  # 保存到变量 "link.href"
        )
        result = browser._execute_instruction([get_attr_instruction])
        href_value = result.get('data', {}).get('value')
    """
    # 指令类型标识符，固定为 "get_attribute"
    type = "get_attribute"
    
    def __init__(self, tab_id: int, element_name: str, attribute: str, usage: str = None, 
                 instruction_id: str = "", delay: int = 0, retry: int = 0, timeout: int = 10, 
                 ignore_error: bool = False, created_at: int = 0):
        """
        初始化获取元素属性指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            element_name (str): 元素名称
            attribute (str): 要获取的属性名称
            usage (str): 可选，使用方式
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 指令参数：包含元素名称和属性名称
        self.params = {"elementName": element_name, "attribute": attribute}
        # 如果提供了usage参数，添加到参数中
        if usage:
            self.params["usage"] = usage


class SetAttributeInstruction(Instruction):
    """
    设置元素属性指令类
    
    功能说明：
    用于设置指定元素的属性值。此指令会先定位元素，然后设置指定属性的值。
    常用于动态修改元素的属性，如设置input的value、修改元素的class等。
    
    Attributes:
        type (str): 指令类型，固定为 "set_attribute"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        element_name (str): 元素名称，必须是之前通过FindElementInstruction找到的元素名称
        attribute (str): 要设置的属性名称，如 "value", "class", "disabled"等
        value (str): 要设置的属性值
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": dict       # 仅在成功时存在
            }
    
    Example:
        # 先查找元素
        element = ElementClass(tab_id=1, name="input", selector="#username", selectorType="css")
        find_instruction = FindElementInstruction(tab_id=1, element=element)
        
        # 设置value属性
        set_attr_instruction = SetAttributeInstruction(
            tab_id=1,
            element_name="input",
            attribute="value",
            value="new_value"
        )
        result = browser._execute_instruction([set_attr_instruction])
    """
    # 指令类型标识符，固定为 "set_attribute"
    type = "set_attribute"
    
    def __init__(self, tab_id: int, element_name: str, attribute: str, value: str, 
                 instruction_id: str = "", delay: int = 0, retry: int = 0, timeout: int = 10, 
                 ignore_error: bool = False, created_at: int = 0):
        """
        初始化设置元素属性指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            element_name (str): 元素名称
            attribute (str): 要设置的属性名称
            value (str): 要设置的属性值
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 指令参数：包含元素名称、属性名称和属性值
        self.params = {"elementName": element_name, "attribute": attribute, "value": value}


class ScreenshotInstruction(Instruction):
    """
    页面截图指令类
    
    功能说明：
    用于截取指定标签页的截图。支持多种图片格式和截图选项，可以截取当前可见区域
    或整个页面（包括滚动区域）。截图结果以data URL格式返回。
    
    Attributes:
        type (str): 指令类型，固定为 "screenshot"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        format (str): 可选，图片格式，可选值：
            - "png": PNG格式（无损压缩，支持透明）
            - "jpeg": JPEG格式（有损压缩，不支持透明）
            默认为 "png"
        quality (int): 可选，图片质量（0-100），仅对jpeg格式有效，默认为None
            - 值越大，质量越好，文件越大
            - 通常建议设置为80-90
        full_page (bool): 可选，是否截取整个页面（包括滚动区域），默认为False
            - True: 截取整个页面，包括需要滚动才能看到的部分
            - False: 仅截取当前可见区域
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "dataUrl": str  # 截图的data URL，格式为 "data:image/png;base64,..."
                }
            }
    
    Example:
        # 截取当前可见区域（PNG格式）
        screenshot_instruction = ScreenshotInstruction(
            tab_id=1,
            format="png",
            full_page=False
        )
        
        # 截取整个页面（JPEG格式，质量90）
        screenshot_instruction = ScreenshotInstruction(
            tab_id=1,
            format="jpeg",
            quality=90,
            full_page=True
        )
        result = browser._execute_instruction([screenshot_instruction])
        data_url = result.get('data', {}).get('dataUrl')
    """
    # 指令类型标识符，固定为 "screenshot"
    type = "screenshot"
    
    def __init__(self, tab_id: int, format: str = "png", quality: int = None, full_page: bool = False, 
                 instruction_id: str = "", delay: int = 0, retry: int = 0, timeout: int = 15, 
                 ignore_error: bool = False, created_at: int = 0):
        """
        初始化页面截图指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            format (str): 可选，图片格式
            quality (int): 可选，图片质量（0-100）
            full_page (bool): 可选，是否截取整个页面
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 指令参数：根据提供的参数动态构建
        self.params = {}
        # 如果提供了format参数，添加到参数中
        if format:
            self.params["format"] = format
        # 如果提供了quality参数，添加到参数中
        if quality is not None:
            self.params["quality"] = quality
        # 如果full_page为True，添加到参数中
        if full_page:
            self.params["fullPage"] = full_page


class WaitInstruction(Instruction):
    """
    等待指令类
    
    功能说明：
    用于等待特定条件满足后再继续执行。支持多种等待类型，如等待标题包含文本、
    等待元素存在、等待元素可见、等待属性包含文本等。此指令常用于页面加载后
    等待特定元素出现或状态变化。
    
    Attributes:
        type (str): 指令类型，固定为 "wait"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        wait_type (str): 等待类型，可选值：
            - "wait_title_contains": 等待页面标题包含指定文本
            - "wait_element_exists": 等待元素存在于DOM中（不一定可见）
            - "wait_element_visible": 等待元素可见（存在于DOM且可见）
            - "wait_attribute_contains": 等待元素属性包含指定文本
        title_text (str): 可选，等待标题包含的文本（wait_type为"wait_title_contains"时使用）
        element (ElementClass): 可选，ElementClass对象（wait_type为"wait_element_exists"或"wait_element_visible"时使用）
        element_name (str): 可选，元素名称（wait_type为"wait_element_exists"、"wait_element_visible"、"wait_attribute_contains" 或 "wait_page_load"时使用）
        attribute (str): 可选，属性名称（wait_type为"wait_attribute_contains"时使用）
        attribute_text (str): 可选，属性值文本（wait_type为"wait_attribute_contains"时使用）
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为150。注意：这是等待的最大时间
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "elementName": str  # 如果等待的是元素，返回元素名称
                }
            }
    
    Example:
        # 等待元素可见
        element = ElementClass(tab_id=1, name="login_button", selector="button.login", selectorType="css")
        wait_instruction = WaitInstruction(
            tab_id=1,
            wait_type="wait_element_visible",
            element=element,
            timeout=30
        )
        
        # 等待标题包含文本
        wait_instruction = WaitInstruction(
            tab_id=1,
            wait_type="wait_title_contains",
            title_text="登录"
        )
        
        # 等待属性包含文本
        wait_instruction = WaitInstruction(
            tab_id=1,
            wait_type="wait_attribute_contains",
            element_name="status",
            attribute="class",
            attribute_text="active"
        )
    """
    # 指令类型标识符，固定为 "wait"
    type = "wait"
    
    def __init__(self, tab_id: int, wait_type: str, title_text: str = None, element: ElementClass = None, 
                 element_name: str = None, attribute: str = None, attribute_text: str = None, 
                 instruction_id: str = "", delay: int = 0, retry: int = 0, timeout: int = 150, 
                 ignore_error: bool = False, created_at: int = 0):
        """
        初始化等待指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            wait_type (str): 等待类型
            title_text (str): 可选，等待标题包含的文本
            element (ElementClass): 可选，ElementClass对象
            element_name (str): 可选，元素名称
            attribute (str): 可选，属性名称
            attribute_text (str): 可选，属性值文本
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 指令参数：根据等待类型动态构建
        self.params = {
            "waitType": wait_type
        }
        # 根据等待类型添加相应的参数
        if title_text:
            self.params["titleText"] = title_text
        if element:
            self.params["element"] = element.to_dict()
        if element_name:
            self.params["elementName"] = element_name
        if attribute:
            self.params["attribute"] = attribute
        if attribute_text:
            self.params["attributeText"] = attribute_text


class GetUrlInstruction(Instruction):
    """
    获取当前标签页URL指令类
    
    功能说明：
    用于获取指定标签页的当前URL。此指令会返回标签页当前显示的完整URL地址。
    支持将URL保存到变量中（通过usage参数控制）。
    
    Attributes:
        type (str): 指令类型，固定为 "get_url"
    
    Args:
        tab_id (int): 指令执行的标签页ID
        usage (str): 可选，使用方式，可选值：
            - "variable": 将URL保存到变量中，变量名为 "tab_url"
            - "data": 仅返回URL，不保存到变量
            - "none": 不保存也不返回（通常不使用）
            默认为 "data"
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为0
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为180
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": {          # 仅在成功时存在
                    "url": str      # 当前标签页的URL
                }
            }
    
    Example:
        # 获取URL并保存到变量
        get_url_instruction = GetUrlInstruction(
            tab_id=1,
            usage="variable"  # 保存到变量 "tab_url"
        )
        result = browser._execute_instruction([get_url_instruction])
        url = result.get('data', {}).get('url')
    """
    # 指令类型标识符，固定为 "get_url"
    type = "get_url"
    
    def __init__(self, tab_id: int, usage: str = "data", instruction_id: str = "", delay: int = 0, 
                 retry: int = 0, timeout: int = 15, ignore_error: bool = False, created_at: int = 0):
        """
        初始化获取当前标签页URL指令
        
        Args:
            tab_id (int): 指令执行的标签页ID
            usage (str): 可选，使用方式
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        # 总是设置 usage 参数（默认值为 "data"）
        self.params["usage"] = usage


class ActivateTabInstruction(Instruction):
    """
    激活标签页指令类
    
    功能说明：
    用于激活（切换到）指定的标签页。此指令会将浏览器焦点切换到指定的标签页，
    使其成为当前活动的标签页。激活标签页后，后续的指令操作都会在该标签页上执行。
    
    Attributes:
        type (str): 指令类型，固定为 "activate_tab"
    
    Args:
        tab_id (int): 要激活的标签页ID
        instruction_id (str): 可选，指令ID。如果不提供，会自动生成一个唯一ID
        delay (int): 可选，延迟时间（秒），默认为3。激活标签页后通常需要等待页面加载
        retry (int): 可选，重试次数，默认为0
        timeout (int): 可选，超时时间（秒），默认为30。激活操作通常很快完成
        ignore_error (bool): 可选，是否忽略错误，默认为False
        created_at (int): 可选，创建时间戳，默认为0
    
    Returns:
        dict: 指令执行结果，格式为：
            {
                "instructionID": str,
                "success": bool,
                "duration": int,
                "error": str,      # 仅在失败时存在
                "data": dict       # 仅在成功时存在
            }
    
    Example:
        # 激活标签页
        activate_instruction = ActivateTabInstruction(
            tab_id=1482755452,
            delay=3  # 激活后等待3秒
        )
        result = browser._execute_instruction([activate_instruction])
    """
    # 指令类型标识符，固定为 "activate_tab"
    type = "activate_tab"
    
    def __init__(self, tab_id: int, instruction_id: str = "", delay: int = 3, retry: int = 0, 
                 timeout: int = 30, ignore_error: bool = False, created_at: int = 0):
        """
        初始化激活标签页指令
        
        Args:
            tab_id (int): 要激活的标签页ID
            instruction_id (str): 可选，指令ID
            delay (int): 可选，延迟时间（秒）
            retry (int): 可选，重试次数
            timeout (int): 可选，超时时间（秒）
            ignore_error (bool): 可选，是否忽略错误
            created_at (int): 可选，创建时间戳
        """
        super().__init__(tab_id, instruction_id, delay, retry, timeout, ignore_error, created_at)
        # 如果未提供指令ID，自动生成一个基于类型和UUID的唯一ID
        self.instructionID = instruction_id if instruction_id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"


# ==================== Http命令子类 ========================


class HttpBitBrowserOpenCommand(HttpCommand):
    """
    HTTP代理打开浏览器命令类
    
    功能说明：
    用于通过HTTP API打开BitBrowser浏览器实例。这个命令会向浏览器节点服务发送请求，
    启动指定的浏览器实例，并返回浏览器的连接信息（WebSocket地址、HTTP地址等）。
    
    使用场景：
    - 在工作流开始时打开浏览器
    - 批量创建浏览器实例
    - 自动化测试中初始化浏览器环境
    
    请求流程：
    1. 构造命令对象（设置浏览器ID、启动参数等）
    2. 通过before_callback设置实际的浏览器ID（如果ID为0）
    3. 发送POST请求到 /browser/open 端点
    4. 解析响应获取浏览器连接信息
    5. 通过after_callback处理浏览器信息（如保存WebSocket地址）
    
    响应数据：
    成功时返回浏览器实例的详细信息，包括：
    - ws: WebSocket连接地址（用于CDP通信）
    - http: HTTP代理地址
    - seq: 浏览器序号
    - name: 浏览器名称
    - 其他浏览器配置信息
    """ 
    # 命令类型标识：http_request 表示这是一个HTTP请求类型的命令
    type = "http_request"
    
    def __init__(self, id: str, args: list = [], queue: bool = True, timeout: int = 180, ignore_error: bool = False):
        """
        初始化打开浏览器命令对象
        
        Args:
            id (str): 浏览器ID
                - 如果提供非空ID，则使用该ID打开指定的浏览器
                - 如果为空字符串或None，则自动生成一个临时ID
                - 如果为"0"，通常表示需要通过before_callback动态设置浏览器ID
                - 用途：标识要打开的浏览器实例
        
            args (list, optional): 浏览器启动参数列表，默认为空列表
                - 格式：列表，包含浏览器启动时的命令行参数
                - 示例：['--disable-blink-features=AutomationControlled', '--no-sandbox']
                - 用途：自定义浏览器启动行为（如禁用自动化检测、设置代理等）
                - 注意：如果传入None，会自动转换为空列表
        
            queue (bool, optional): 是否排队执行，默认为True
                - True: 如果浏览器正在被其他进程使用，则排队等待
                - False: 如果浏览器正在使用，则立即返回错误
                - 用途：控制并发打开浏览器的行为
        
            timeout (int, optional): 请求超时时间（秒），默认为180秒
                - 用途：设置HTTP请求的最大等待时间
                - 注意：打开浏览器可能需要较长时间，建议设置较大的超时值
        
            ignore_error (bool, optional): 是否忽略错误，默认为False
        
        请求体结构：
        {
            "id": str,      # 浏览器ID
            "args": list,   # 启动参数列表
            "queue": bool   # 是否排队
        }
        """
        # 调用父类初始化方法，设置错误处理选项
        super().__init__(ignore_error)
        
        # 设置命令ID：如果未提供ID，则自动生成一个唯一ID
        # ID格式：http_request_<16位十六进制字符串>
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        
        # 设置HTTP请求参数
        self.url = '/browser/open'  # 浏览器节点API的打开浏览器端点
        self.method = "POST"  # 使用POST方法发送请求
        
        # 设置请求头：指定内容类型为JSON
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # 确保 args 不是 None，如果是 None 则转换为空列表
        # 这是防御性编程，避免后续处理时出现NoneType错误
        if args is None:
            args = []
        
        # 构造请求体：包含浏览器ID、启动参数和排队选项
        self.body = {
            "id": self.id,      # 浏览器ID，可能通过before_callback修改
            "args": args,        # 浏览器启动参数
            "queue": queue       # 是否排队执行
        }
        
        # 设置请求超时时间
        self.timeout = timeout


class HttpBitBrowserCloseCommand(HttpCommand):
    """
    HTTP代理关闭浏览器命令类
    
    功能说明：
    用于通过HTTP API关闭指定的BitBrowser浏览器实例。这个命令会向浏览器节点服务发送请求，
    关闭指定ID的浏览器进程，释放相关资源。
    
    使用场景：
    - 在工作流结束时关闭浏览器
    - 批量关闭多个浏览器实例
    - 清理不再使用的浏览器资源
    - 自动化测试后清理环境
    
    请求流程：
    1. 构造命令对象（设置浏览器ID）
    2. 通过before_callback设置实际的浏览器ID（如果ID为0）
    3. 发送POST请求到 /browser/close 端点
    4. 解析响应确认关闭操作是否成功
    5. 通过after_callback执行清理操作（如清除保存的浏览器ID）
    
    注意事项：
    - 关闭浏览器后，该浏览器的WebSocket连接将断开
    - 关闭浏览器后，无法再对该浏览器执行CDP命令
    - 建议在关闭前保存重要数据（如Cookie、会话信息等）
    """
    # 命令类型标识：http_request 表示这是一个HTTP请求类型的命令
    type = "http_request"

    def __init__(self, id: str, timeout: int = 180, ignore_error: bool = False):
        """
        初始化关闭浏览器命令对象
        
        Args:
            id (str): 要关闭的浏览器ID
                - 如果提供非空ID，则关闭指定的浏览器
                - 如果为空字符串或None，则自动生成一个临时ID（通常不推荐）
                - 用途：标识要关闭的浏览器实例
            
            timeout (int, optional): 请求超时时间（秒），默认为180秒
                - 用途：设置HTTP请求的最大等待时间
                - 注意：关闭浏览器通常很快完成，默认超时时间足够
            
            ignore_error (bool, optional): 是否忽略错误，默认为False
                - True: 即使关闭失败也不抛出异常（适用于批量关闭场景）
                - False: 关闭失败时抛出BusinessError异常
        
        请求体结构：
        {
            "id": str  # 浏览器ID
        }
        """
        # 调用父类初始化方法，设置错误处理选项
        super().__init__(ignore_error)
        
        # 设置命令ID：如果未提供ID，则自动生成一个唯一ID
        self.id = id
        
        # 设置HTTP请求参数
        self.url = '/browser/close'  # 浏览器节点API的关闭浏览器端点
        self.method = "POST"  # 使用POST方法发送请求
        
        # 设置请求头：指定内容类型为JSON
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # 构造请求体：只包含浏览器ID
        self.body = {
            "id": self.id  # 浏览器ID，可能通过before_callback修改
        }
        
        # 设置请求超时时间
        self.timeout = timeout


class HttpBitBrowserListCommand(HttpCommand):
    """
    HTTP代理查询浏览器列表命令类
    
    功能说明：
    用于通过HTTP API查询BitBrowser浏览器实例列表。这个命令支持分页查询和按序号筛选，
    可以获取浏览器实例的详细信息（ID、序号、名称、状态、配置等）。
    
    使用场景：
    - 通过浏览器序号查找对应的浏览器ID
    - 批量查询浏览器列表
    - 检查浏览器是否存在
    - 获取浏览器的详细配置信息
    
    请求流程：
    1. 构造命令对象（设置查询参数：序号、页码、每页数量）
    2. 发送POST请求到 /browser/list 端点
    3. 解析响应获取浏览器列表数据
    4. 通过after_callback处理列表数据（如根据序号查找浏览器ID）
    
    查询参数说明：
    - seq: 浏览器序号，用于筛选特定浏览器（0表示不过滤）
    - page: 页码，用于分页查询（从0开始）
    - pageSize: 每页数量，控制返回的浏览器数量
    
    响应数据：
    返回分页的浏览器列表，每个浏览器包含完整的配置信息和状态。
    """
    # 命令类型标识：http_request 表示这是一个HTTP请求类型的命令
    type = "http_request"
    
    def __init__(self, seq: int=0, page: int=0, pageSize: int=100, timeout: int = 180, ignore_error: bool = False):
        """
        初始化查询浏览器列表命令对象
        
        Args:
            seq (int, optional): 浏览器序号，用于筛选特定浏览器，默认为0
                - 0: 不过滤，返回所有浏览器
                - 非0: 只返回序号等于该值的浏览器
                - 用途：通过序号查找对应的浏览器ID
                - 示例：seq=55391 只返回序号为55391的浏览器
        
            page (int, optional): 页码，用于分页查询，默认为0
                - 从0开始计数
                - 用途：当浏览器数量很多时，分页获取数据
                - 示例：page=0 获取第一页，page=1 获取第二页
        
            pageSize (int, optional): 每页返回的浏览器数量，默认为100
                - 用途：控制单次查询返回的数据量
                - 注意：如果浏览器数量超过pageSize，需要多次查询
                - 示例：pageSize=100 每页返回100个浏览器
        
            timeout (int, optional): 请求超时时间（秒），默认为180秒
                - 用途：设置HTTP请求的最大等待时间
                - 注意：查询列表通常很快完成，默认超时时间足够
            
            ignore_error (bool, optional): 是否忽略错误，默认为False
        
        请求体结构：
        {
            "page": int,      # 页码
            "pageSize": int,  # 每页数量
            "seq": int        # 浏览器序号（0表示不过滤）
        }
        
        注意：
        - 命令ID会自动生成，不需要手动设置
        - 如果seq=0，返回所有浏览器；否则只返回匹配的浏览器
        """
        # 调用父类初始化方法，设置错误处理选项
        super().__init__(ignore_error)
        
        # 自动生成命令ID：格式为 http_request_<16位十六进制字符串>
        self.id = f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        
        # 设置HTTP请求参数
        self.url = '/browser/list'  # 浏览器节点API的查询列表端点
        self.method = "POST"  # 使用POST方法发送请求
        
        # 设置请求头：指定内容类型为JSON
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # 构造请求体：包含分页参数和筛选条件
        self.body = {
            "page": page,        # 页码
            "pageSize": pageSize, # 每页数量
            "seq": seq           # 浏览器序号（0表示不过滤）
        }
        
        # 设置请求超时时间
        self.timeout = timeout


class HttpBitBrowserResetCommand(HttpCommand):
    """
    HTTP代理重置浏览器命令类
    
    功能说明：
    用于通过HTTP API重置指定的BitBrowser浏览器实例。重置操作会清除浏览器的数据
    （如Cookie、缓存、历史记录等），但不会关闭浏览器进程。重置后浏览器会恢复到初始状态。
    
    使用场景：
    - 清除浏览器的所有数据，重新开始会话
    - 自动化测试中重置浏览器状态
    - 清理浏览器缓存和Cookie
    - 准备浏览器用于新的任务
    
    请求流程：
    1. 构造命令对象（设置浏览器ID）
    2. 通过before_callback设置实际的浏览器ID（如果ID为0）
    3. 发送POST请求到 /browser/closing/reset 端点
    4. 解析响应确认重置操作是否成功
    5. 通过after_callback执行后续操作（如重新登录）
    
    注意事项：
    - 重置操作会清除浏览器的所有数据，包括登录状态
    - 重置操作不会关闭浏览器，浏览器进程仍然运行
    - 重置后需要重新建立会话和登录
    - 建议在重置前保存重要数据
    """
    # 命令类型标识：http_request 表示这是一个HTTP请求类型的命令
    type = "http_request"
    
    def __init__(self, id: str, timeout: int = 180, ignore_error: bool = False):
        """
        初始化重置浏览器命令对象
        
        Args:
            id (str): 要重置的浏览器ID
                - 如果提供非空ID，则重置指定的浏览器
                - 如果为空字符串或None，则自动生成一个临时ID（通常不推荐）
                - 用途：标识要重置的浏览器实例
            
            timeout (int, optional): 请求超时时间（秒），默认为180秒
                - 用途：设置HTTP请求的最大等待时间
                - 注意：重置操作可能需要一些时间，建议保持默认值
            
            ignore_error (bool, optional): 是否忽略错误，默认为False
                - True: 即使重置失败也不抛出异常
                - False: 重置失败时抛出BusinessError异常
        
        请求体结构：
        {
            "id": str  # 浏览器ID
        }
        """
        # 调用父类初始化方法，设置错误处理选项
        super().__init__(ignore_error)
        
        # 设置命令ID：如果未提供ID，则自动生成一个唯一ID
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"
        
        # 设置HTTP请求参数
        self.url = '/browser/closing/reset'  # 浏览器节点API的重置浏览器端点
        self.method = "POST"  # 使用POST方法发送请求
        
        # 设置请求头：指定内容类型为JSON
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # 构造请求体：只包含浏览器ID
        self.body = {
            "id": self.id  # 浏览器ID，可能通过before_callback修改
        }
        
        # 设置请求超时时间
        self.timeout = timeout


class HttpBitBrowserAliveCommand(HttpCommand):
    """
    HTTP代理查询浏览器是否存活命令类
    
    功能说明：
    用于通过HTTP API查询指定的BitBrowser浏览器实例是否存活。这个命令会检查浏览器进程是否正在运行，
    并返回浏览器进程的PID（进程ID）。
    
    使用场景：
    - 检查浏览器是否正常运行
    - 在自动化测试中验证浏览器状态
    - 确认浏览器节点是否响应
    """
    type = "http_request"
    
    def __init__(self, id: str, timeout: int = 180, ignore_error: bool = False):
        """
        初始化查询浏览器是否存活命令对象
        
        Args:
            id (str): 要查询的浏览器ID
                - 如果提供非空ID，则查询指定的浏览器
                - 如果为空字符串或None，则自动生成一个临时ID（通常不推荐）
                - 用途：标识要查询的浏览器实例
            
            timeout (int, optional): 请求超时时间（秒），默认为180秒
                - 用途：设置HTTP请求的最大等待时间
                - 注意：查询操作通常很快完成，默认超时时间足够
            
            ignore_error (bool, optional): 是否忽略错误，默认为False
                - True: 即使查询失败也不抛出异常（适用于批量查询场景）
                - False: 查询失败时抛出BusinessError异常
        
        请求体结构：
        {
            "ids": [str]  # 浏览器ID数组（只包含一个ID）
        }
        
        Note:
            - 命令ID会自动生成，不需要手动设置
            - 请求体中的ids是数组格式，即使只查询一个浏览器
        """
        # 调用父类初始化方法，设置错误处理选项
        super().__init__(ignore_error)
        
        # 设置命令ID：如果未提供ID，则自动生成一个唯一ID
        self.id = id if id else f"{self.__class__.type}_{uuid.uuid4().hex[:16]}"

        # 设置HTTP请求参数
        self.url = '/browser/pids'  # 浏览器节点API的查询进程ID端点
        self.method = "POST"  # 使用POST方法发送请求

        # 设置请求头：指定内容类型为JSON
        self.headers = {
            "Content-Type": "application/json"
        }

        # 构造请求体：包含浏览器ID数组（即使只查询一个浏览器，也需要数组格式）
        self.body = {
            "ids": [self.id]  # 浏览器ID数组
        }

        # 设置请求超时时间
        self.timeout = timeout


# ==================== 网站抽象基类 ========================


class StepResult:
    """
    步骤执行结果类
    
    功能说明：
    用于封装步骤执行的结果信息。每个步骤执行后都会返回一个StepResult对象，
    包含执行是否成功、错误信息、错误类型、错误阶段、上下文等信息。
    便于在工作流中统一处理和传递步骤执行结果。
    
    Attributes:
        success (bool): 步骤是否成功执行
        error (AutoJSError|None): 错误对象，如果执行失败则包含错误信息
        error_type (str|None): 错误类型名称，如 "NetworkError"、"BusinessError"等
        error_stage (str|None): 错误发生的阶段，如步骤名称、方法名称等
        context (Context|None): 工作流上下文对象，包含步骤执行时的变量和状态
    
    使用场景：
    - 在工作流的各个步骤中返回执行结果
    - 根据结果决定后续操作流程
    - 错误处理和日志记录
    - 结果汇总和报告生成
    """
    def __init__(self, success: bool, error: AutoJSError = None, error_type: str = None, error_stage: str = None, context: Context = None):
        """
        初始化步骤执行结果对象
        
        Args:
            success (bool): 步骤是否成功执行
                - True: 步骤执行成功
                - False: 步骤执行失败
            error (AutoJSError|None): 可选，错误对象。如果执行失败，应传入错误对象
            error_type (str|None): 可选，错误类型名称，如 "NetworkError"、"BusinessError"等
            error_stage (str|None): 可选，错误发生的阶段，通常是步骤名称或方法名称
            context (Context|None): 可选，工作流上下文对象，包含步骤执行时的变量和状态
        """
        self.success: bool = success
        self.error: AutoJSError = error
        self.error_type: str = error_type
        self.error_stage: str = error_stage
        self.context: Context = context

    def to_dict(self) -> dict:
        """
        将步骤执行结果转换为字典格式
        
        功能说明：
        将StepResult对象的所有属性转换为字典格式，便于序列化、日志记录、API返回等。
        上下文变量会被复制到字典中，避免修改原始上下文。
        
        Returns:
            dict: 包含步骤执行结果的字典，格式为：
                {
                    "success": bool,           # 是否成功
                    "error": AutoJSError|None, # 错误对象（如果失败）
                    "error_type": str|None,    # 错误类型
                    "error_stage": str|None,   # 错误阶段
                    "context": dict            # 上下文变量字典
                }
        
        Example:
            result = StepResult(
                success=True,
                context=context
            )
            result_dict = result.to_dict()
            # 返回: {"success": True, "error": None, "error_type": None, "error_stage": None, "context": {...}}
        """
        return {
            "success": self.success,
            "error": self.error,
            "error_type": self.error_type,
            "error_stage": self.error_stage,
            # 复制上下文变量字典，避免修改原始上下文
            "context": self.context.var.copy() if self.context else {}
        }


class WebSite(ABC):
    """
    网站抽象基类
    
    功能说明：
    这是所有网站操作类的抽象基类，定义了网站操作的标准接口和通用功能。
    每个具体的网站类（如Facebook、Onestream等）都继承自此类，实现网站特定的操作逻辑。
    
    核心功能：
    1. 封装网站的元素定义（通过返回ElementClass对象的方法）
    2. 封装网站的步骤执行（通过返回StepResult的方法）
    3. 提供通用的指令和命令执行方法（navigate_instruction、find_element_instruction等）
    4. 提供变量管理功能（get_variable、set_variable）
    5. 提供条件判断功能（condition_match_current_url_is等）
    
    设计模式：
    采用模板方法模式（Template Method Pattern），定义通用的操作流程，
    子类实现具体的元素定义和步骤逻辑。
    
    使用流程：
    1. 创建网站对象（传入Browser对象和域名）
    2. 调用步骤方法（如login_step、home_step等）
    3. 步骤方法内部调用指令方法（如navigate_instruction、find_element_instruction等）
    4. 指令方法执行浏览器操作并返回结果
    5. 步骤方法返回StepResult对象
    
    Attributes:
        browser (Browser): 浏览器操作对象，用于执行CDP命令和指令
        domain (str): 网站域名，如 "facebook.com"
        name (str): 网站名称，由子类设置
        home_url (str): 网站首页URL，由子类设置
        login_url (str): 网站登录URL，由子类设置
        variables (dict): 网站变量字典，用于存储网站相关的临时变量
            - 'tab_id' (int): 当前标签页ID，默认为-1
            - 'tab_url' (str): 当前标签页URL，默认为空字符串
            - 'tab_index' (int): 当前标签页索引，默认为-1
            - 其他自定义变量：可以在步骤中存储任意数据
    """
    def __init__(self, browser: Browser, domain: str):
        """
        初始化网站对象
        
        功能说明：
        创建网站对象，初始化浏览器操作对象、域名、URL、变量等基础信息。
        子类应该在初始化后设置name、home_url、login_url等属性。
        
        Args:
            browser (Browser): 浏览器操作对象，用于执行CDP命令和指令
            domain (str): 网站域名，如 "facebook.com"、"onestream.live"等
        """
        # 浏览器对象
        self.browser = browser
        # 网站域名，如 "facebook.com"
        self.domain = domain
        # 网站名称，由子类设置
        self.name = ""

        # 网站基础信息
        # 网站首页URL，由子类设置，必须以/结尾
        self.home_url = ""
        # 网站登录URL，由子类设置，必须以/结尾
        self.login_url = ""

        # 保存临时变量 - 跟当前网站相关的临时变量
        self.variables = dict()
        # 标签页ID，默认为-1表示未设置
        self.variables['tab_id'] = -1
        # 标签页URL，默认为空字符串
        self.variables['tab_url'] = ''
        # 标签页索引，默认为-1表示未设置
        self.variables['tab_index'] = -1

    def get_variable(self, key: str, value: any = None) -> any:
        """
        获取网站变量
        
        功能说明：
        从网站对象的变量字典中获取指定名称的变量值。如果变量不存在，返回默认值。
        网站变量用于在步骤之间传递数据和状态信息。
        
        Args:
            key (str): 变量名称，如 "tab_id"、"tab_url"、"browser_id"等
            value (any): 可选，如果变量不存在时返回的默认值，默认为None
        
        Returns:
            any: 变量的值，如果变量不存在则返回默认值
        
        Example:
            tab_id = website.get_variable('tab_id', -1)  # 获取标签页ID，不存在则返回-1
            browser_id = website.get_variable('browser_id')  # 获取浏览器ID，不存在则返回None
        """
        return self.variables.get(key, value)

    def set_variable(self, key: str, value: any) -> None:
        """
        设置网站变量
        
        功能说明：
        在网站对象的变量字典中设置指定名称的变量值。如果变量已存在，会被覆盖。
        网站变量用于在步骤之间传递数据和状态信息。
        
        Args:
            key (str): 变量名称，如 "tab_id"、"tab_url"、"browser_id"等
            value (any): 变量的值，可以是任意类型（int、str、dict、list等）
        
        Example:
            website.set_variable('tab_id', 1482755452)  # 设置标签页ID
            website.set_variable('browser_id', 'browser_123')  # 设置浏览器ID
            website.set_variable('data', {'key': 'value'})  # 设置复杂数据
        """
        self.variables[key] = value

    def stop_decorator(func: Callable):
        """
        Python装饰器函数 - 停止标志检查装饰器
        
        功能说明：
        用于在命令或指令执行前检查工作流上下文的stop标记。如果stop为True，
        则跳过函数执行，直接返回None。用于实现工作流的提前终止功能。
        
        使用场景：
        - 当某个步骤失败且需要停止整个工作流时
        - 当满足某个条件需要提前退出时
        - 在错误处理中设置stop标志，跳过后续步骤
        
        工作原理：
        1. 从函数参数中获取context对象
        2. 检查context.is_stop()的返回值
        3. 如果为True，直接返回None，不执行函数
        4. 如果为False，正常执行函数
        
        Args:
            func (Callable): 要装饰的函数，通常是WebSite类的方法
        
        Returns:
            Callable: 装饰后的函数，增加了停止标志检查功能
        
        Example:
            @stop_decorator
            def some_step(self, context: Context):
                # 如果context.is_stop()为True，此函数不会执行
                pass
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从参数中获取context对象
            context: Context = kwargs.get('context', Context())
            
            if context.is_stop():
                return

            return func(*args, **kwargs)
        return wrapper

    def ignore_error_decorator(default_value: any = None):
        """
        Python装饰器函数 - 错误忽略装饰器
        
        功能说明：
        用于在命令或指令执行时处理错误。如果ignore_error参数为True，
        则捕获所有异常，不抛出异常，而是返回默认值。用于实现可选的错误忽略功能。
        
        使用场景：
        - 某些步骤失败时不影响整个工作流继续执行
        - 可选的操作，失败时使用默认值
        - 在测试或调试时忽略某些错误
        
        工作原理：
        1. 从函数参数中获取ignore_error参数
        2. 执行函数，捕获所有异常
        3. 如果ignore_error为True，记录警告日志并返回default_value
        4. 如果ignore_error为False，重新抛出异常
        
        Args:
            default_value (any): 如果ignore_error为True时返回的默认值，默认为None
        
        Returns:
            Callable: 装饰器函数，返回装饰后的函数
        
        Example:
            @ignore_error_decorator(default_value='')
            def get_url(self, context: Context, ignore_error: bool = False):
                # 如果ignore_error为True且发生异常，返回空字符串而不是抛出异常
                pass
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 从参数中获取ignore_error参数
                ignore_error: bool = kwargs.get('ignore_error', False)
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if ignore_error:
                        Logger.warning(f"指令执行失败: {e}, 忽略错误")
                        return default_value
                    else:
                        raise e
            return wrapper
        return decorator

    def condition_match_current_url_is(self, url: str) -> bool:
        """
        条件判断方法 - 检查当前标签页URL是否完全匹配指定URL
        
        功能说明：
        用于判断当前标签页的URL是否与指定的URL完全匹配。会进行URL标准化处理，
        忽略查询参数、锚点等，只比较协议、域名和路径部分。
        
        URL标准化规则：
        1. 解析URL，提取协议、域名、路径
        2. 如果路径不以'/'结尾，自动添加'/'
        3. 转换为小写进行比较
        4. 忽略查询参数（?后面的部分）和锚点（#后面的部分）
        
        Args:
            url (str): 需要判断的URL，如 "https://facebook.com/login/"
        
        Returns:
            bool: 
                - True: 当前标签页URL与指定URL完全匹配
                - False: 不匹配，或当前标签页URL为空，或URL解析失败
        
        Example:
            # 检查是否在登录页面
            if website.condition_match_current_url_is("https://facebook.com/login/"):
                # 执行登录操作
                pass
            
            # 检查是否在首页
            if website.condition_match_current_url_is(website.home_url):
                # 执行首页操作
                pass
        """
        current_url = self.get_variable('tab_url')

        if not current_url:
            return False

        try:
            parsed = urlparse(current_url)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if not normalized_url.endswith('/'):
                normalized_url += '/'
            
            return normalized_url.lower() == url.lower()
        except Exception:
            return False

    def condition_include_current_url_is(self, url: str) -> bool:
        """
        条件判断方法 - 检查当前标签页URL是否包含指定URL
        
        功能说明：
        用于判断当前标签页的URL是否包含指定的URL字符串。会进行URL标准化处理，
        忽略查询参数、锚点等，只比较协议、域名和路径部分。支持部分匹配。
        
        URL标准化规则：
        1. 解析URL，提取协议、域名、路径
        2. 如果路径不以'/'结尾，自动添加'/'
        3. 转换为小写进行比较
        4. 使用字符串包含判断（in操作符）
        
        Args:
            url (str): 需要判断的URL字符串，如 "/login/"、"facebook.com"等
        
        Returns:
            bool:
                - True: 当前标签页URL包含指定URL字符串
                - False: 不包含，或当前标签页URL为空，或URL解析失败
        
        Example:
            # 检查URL是否包含登录路径
            if website.condition_include_current_url_is("/login/"):
                # 执行登录相关操作
                pass
            
            # 检查URL是否包含特定域名
            if website.condition_include_current_url_is("facebook.com"):
                # 执行Facebook相关操作
                pass
        """
        # 如果url为空, 则返回False
        if not url:
            return False

        # 获取当前标签页URL
        current_url = self.get_variable('tab_url')

        # 如果当前标签页URL为空, 则返回False
        if not current_url:
            return False

        try:
            parsed = urlparse(current_url)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if not normalized_url.endswith('/'):
                normalized_url += '/'
            
            return url.lower() in normalized_url.lower()
        except Exception:
            return False

    # begin ---------------------------Cdp命令模块(命令)-----------------------------------------------------

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def list_targets_command(self, context: Context, ignore_error: bool = False) -> None:
        """
        列出当前浏览器节点的所有标签页命令
        Args:
            context: 上下文
            ignore_error: 是否忽略错误
        """
        command = ListTargetsCommand(ignore_error=ignore_error)

        result = self.browser._execute_cdp_command(command)

        if not result.get('success'):
            raise BusinessError(
                f"列出当前浏览器节点的所有标签页命令失败: {command.id}",
                data={"url": self.browser.node_api_base_url, "status_code": result.get('status_code', 0), "command_id": command.id}
            )

        for tab in result.get('data', []):
            url = tab.get('url', '')
            parsed = urlparse(url)
            if self.domain.lower() in parsed.netloc.lower():
                self.set_variable('tab_id', tab.get('tabId', -1))
                self.set_variable('tab_index', tab.get('tabIndex', -1))
                self.set_variable('tab_url', tab.get('url', ''))

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def create_tab_and_navigate_command(self, context: Context, url: str, active: bool = True, new_window: bool = False, ignore_error: bool = False) -> None:
        """
        创建标签页并导航到首页命令
        Args:
            context: 上下文
            url: 要导航的URL
            active: 是否激活标签页
            ignore_error: 是否忽略错误
        """
        command = CreateTabAndNavigateCommand(url=url, active=active, new_window=new_window, ignore_error=ignore_error)

        result = self.browser._execute_cdp_command(command)

        if not result.get('success'):
            raise BusinessError(
                f"创建标签页并导航到首页命令失败: {command.id}",
                data={"url": self.browser.node_api_base_url, "status_code": result.get('status_code', 0), "command_id": command.id}
            )

        data = result.get('data', {})

        self.set_variable('tab_id', data.get('tabId', -1))
        self.set_variable('tab_index', data.get('tabIndex', -1))
        self.set_variable('tab_url', data.get('url', ''))

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def update_node_name_command(self, context: Context, node_name: str, ignore_error: bool = False) -> None:
        """
        更新节点名称命令
        Args:
            context: 上下文
            node_name: 节点名称
            ignore_error: 是否忽略错误
        """
        command = UpdateNodeNameCommand(node_name=node_name, ignore_error=ignore_error)

        result = self.browser._execute_cdp_command(command)

        if not result.get('success'):
            raise BusinessError(f"更新节点名称命令失败: {command.id}",data={"url": self.browser.node_api_base_url, "status_code": result.get('status_code', 0), "command_id": command.id})

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def close_tab_command(self, context: Context, ignore_error: bool = False) -> None:
        """
        关闭标签页命令
        Args:
            context: 上下文
            tab_id: 标签页ID

            ignore_error: 是否忽略错误
        """
        command = CloseTabCommand(
            tab_id=self.get_variable('tab_id', -1),
            ignore_error=ignore_error
        )

        result = self.browser._execute_cdp_command(command)

        if not result.get('success'):
            raise BusinessError(f"关闭标签页命令失败: {command.id}", data={"url": self.browser.node_api_base_url, "status_code": result.get('status_code', 0), "command_id": command.id})

    # end   ---------------------------Cdp命令模块(命令)-----------------------------------------------------

    # begin ---------------------------Instruction命令模块(命令)---------------------------------------------

    @stop_decorator
    @ignore_error_decorator(default_value=False)
    def activate_tab_instruction(self, context: Context, delay: int = 0, retry: int = 0, timeout: int = 30, ignore_error: bool = False) -> bool:
        """
        激活标签页指令
        Args:
            context: 上下文
            delay: 延迟时间（秒），默认为3
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为30
            ignore_error: 是否忽略错误，默认为False
        Returns:
            bool: 是否成功
        """
        instruction = ActivateTabInstruction(
            tab_id=self.get_variable('tab_id', -1),
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )
        
        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"激活标签页指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"激活标签页指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        return True

    @stop_decorator
    @ignore_error_decorator(default_value='')
    def get_tab_url_instruction(self, context: Context, usage: str = "variable", delay: int = 0, retry: int = 0, timeout: int = 15, ignore_error: bool = False) -> str:
        """
        获取标签页URL指令
        Args:
            context: 上下文
            usage: 使用方式，可选值: "variable", "data", "none"，默认为"variable"
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为15
            ignore_error: 是否忽略错误，默认为False
        Returns:
            str: 标签页URL
        """
        instruction = GetUrlInstruction(
            tab_id=self.get_variable('tab_id', -1),
            usage=usage,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"获取标签页URL指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"获取标签页URL指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})
        url = data.get('url', '')

        if usage == "variable":
            self.set_variable('tab_url', url)

        return url

    @stop_decorator
    @ignore_error_decorator(default_value='')
    def navigate_instruction(self, context: Context, url: str, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> str:
        """
        页面导航指令
        Args:
            context: 上下文
            url: 要导航的URL
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为150
            ignore_error: 是否忽略错误，默认为False
        Returns:
            str: 导航后的URL
        """
        instruction = NavigateInstruction(
            tab_id=self.get_variable('tab_id', -1),
            url=url,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"页面导航指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"页面导航指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})
        navigated_url = data.get('url', url)

        self.set_variable('tab_url', navigated_url)

        return navigated_url

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def execute_script_instruction(self, context: Context, params: dict, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> any:
        """
        页面JavaScript执行指令
        Args:
            context: 上下文
            params: CDP方法 Runtime.evaluate 的参数
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为150
            ignore_error: 是否忽略错误，默认为False
        Returns:
            any: JavaScript执行结果
        """
        instruction = ExecuteScriptInstruction(
            tab_id=self.get_variable('tab_id', -1),
            params=params,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"执行脚本指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"执行脚本指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})
        results = data.get('results', None)

        return results

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def find_element_instruction(self, context: Context, element: ElementClass, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> dict:
        """
        元素定位指令
        Args:
            context: 上下文
            element: ElementClass对象，包含元素的定位信息
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为150
            ignore_error: 是否忽略错误，默认为False
        Returns:
            dict: 元素数据，包含nodeId、tag等信息
        """
        instruction = FindElementInstruction(
            tab_id=self.get_variable('tab_id', -1),
            element=element,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"查找元素指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"查找元素指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})

        elementData = data.get('elementData', {})
        name = elementData.get('name', '')

        if name:
            self.set_variable(name, True)

        return element
    
    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def wait_instruction(self, context: Context, wait_type: str, title_text: str = None, element: ElementClass = None, element_name: str = None, attribute: str = None, attribute_text: str = None, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> dict:
        """
        等待指令
        Args:
            context: 上下文
            wait_type: 等待类型，可选值: "wait_title_contains", "wait_element_exists", "wait_element_visible", "wait_attribute_contains"
            title_text: 等待标题包含的文本（wait_type为"wait_title_contains"时使用）
            element: ElementClass对象（wait_type为"wait_element_exists"或"wait_element_visible"时使用）
            element_name: 元素名称（wait_type为"wait_element_exists"、"wait_element_visible"或"wait_attribute_contains"时使用）
            attribute: 属性名称（wait_type为"wait_attribute_contains"时使用）
            attribute_text: 属性值文本（wait_type为"wait_attribute_contains"时使用）
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为150
            ignore_error: 是否忽略错误，默认为False
        Returns:
            dict: 等待结果
        """
        instruction = WaitInstruction(
            tab_id=self.get_variable('tab_id', -1),
            wait_type=wait_type,
            title_text=title_text,
            element=element,
            element_name=element_name,
            attribute=attribute,
            attribute_text=attribute_text,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"等待指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        
        if not instruction_result.get('success'):
            return None

        data = instruction_result.get('data', {})
        elementName = data.get('elementName', '')

        if elementName:
            self.set_variable(elementName, True)

        return data

    @stop_decorator
    @ignore_error_decorator(default_value='')
    def input_instruction(self, context: Context, element_name: str, text: str, clear: bool = False, delay: int = 0.2, retry: int = 0, timeout: int = 30, ignore_error: bool = False) -> str:
        """
        文本输入指令
        Args:
            context: 上下文
            element_name: 元素名称
            text: 要输入的文本
            clear: 是否先清空输入框，默认为False
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为30
            ignore_error: 是否忽略错误，默认为False
        Returns:
            str: 输入的文本
        """
        instruction = InputInstruction(
            tab_id=self.get_variable('tab_id', -1),
            element_name=element_name,
            text=text,
            clear=clear,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"文本输入指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"文本输入指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})
        input_text = data.get('text', text)

        return input_text

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def keyboard_instruction(self, context: Context, action: str, key: str = None, text: str = None, element_name: str = None, delay: int = 1, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> dict:
        """
        键盘操作指令
        Args:
            context: 上下文
            action: 键盘操作类型，可选值: "press", "type", "keydown", "keyup"
            key: 按键名称或文本
            element_name: 可选，元素名称（如果需要在特定元素上操作）
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为150
            ignore_error: 是否忽略错误，默认为False
        Returns:
            dict: 操作结果
        """
        instruction = KeyboardInstruction(
            tab_id=self.get_variable('tab_id', -1),
            action=action,
            key=key,
            text=text,
            element_name=element_name,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"键盘操作指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"键盘操作指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})

        return data

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def mouse_instruction(self, context: Context, action: str, element_name: str = None, simulate: str = None, x: int = None, y: int = None, delay: int = 1, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> dict:
        """
        鼠标操作指令
        Args:
            context: 上下文
            action: 鼠标操作类型，可选值: "click", "dblclick", "rightclick", "hover", "left_mousedown", "left_mouseup", "right_mousedown", "right_mouseup", "move_to"
            element_name: 可选，元素名称（如果需要在特定元素上操作）
            simulate: 可选，模拟方式，可选值: "calculated", "simulated", "none"
            x: 可选，X坐标（当action为"move_to"时使用）
            y: 可选，Y坐标（当action为"move_to"时使用）
            delay: 延迟时间（秒），默认为3
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为150
            ignore_error: 是否忽略错误，默认为False
        Returns:
            dict: 操作结果
        """
        instruction = MouseInstruction(
            tab_id=self.get_variable('tab_id', -1),
            action=action,
            element_name=element_name,
            simulate=simulate,
            x=x,
            y=y,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"鼠标操作指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"鼠标操作指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})

        return data

    @stop_decorator
    @ignore_error_decorator(default_value='')
    def get_attribute_instruction(self, context: Context, element_name: str, attribute: str, usage: str = "variable", delay: int = 0, retry: int = 0, timeout: int = 10, ignore_error: bool = False) -> str:
        """
        获取元素属性指令
        Args:
            context: 上下文
            element_name: 元素名称
            attribute: 属性名称
            usage: 使用方式，可选值: "variable", "data", "none"，默认为"variable"
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为10
            ignore_error: 是否忽略错误，默认为False
        Returns:
            str: 属性值
        """
        instruction = GetAttributeInstruction(
            tab_id=self.get_variable('tab_id', -1),
            element_name=element_name,
            attribute=attribute,
            usage=usage,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"获取元素属性指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]

        if not instruction_result.get('success'):
            return ''

        data = instruction_result.get('data', {})
        value = data.get('value', '')

        if usage == "variable":
            variable_name = f"{element_name}.{attribute}"
            self.set_variable(variable_name, value)

        return value

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def set_attribute_instruction(self, context: Context, element_name: str, attribute: str, value: str, delay: int = 0, retry: int = 0, timeout: int = 10, ignore_error: bool = False) -> dict:
        """
        设置元素属性指令
        Args:
            context: 上下文
            element_name: 元素名称
            attribute: 属性名称
            value: 属性值
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为10
            ignore_error: 是否忽略错误，默认为False
        Returns:
            dict: 操作结果
        """
        instruction = SetAttributeInstruction(
            tab_id=self.get_variable('tab_id', -1),
            element_name=element_name,
            attribute=attribute,
            value=value,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"设置元素属性指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"设置元素属性指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})

        return data

    @stop_decorator
    @ignore_error_decorator(default_value='')
    def screenshot_instruction(self, context: Context, format: str = "png", quality: int = None, full_page: bool = False, delay: int = 0, retry: int = 0, timeout: int = 15, ignore_error: bool = False) -> str:
        """
        页面截图指令
        Args:
            context: 上下文
            format: 图片格式，可选值: "png", "jpeg"，默认为"png"
            quality: 图片质量（0-100，仅对jpeg格式有效），默认为None
            full_page: 是否截取整个页面，默认为False
            delay: 延迟时间（秒），默认为0
            retry: 重试次数，默认为0
            timeout: 超时时间（秒），默认为15
            ignore_error: 是否忽略错误，默认为False
        Returns:
            str: 截图的dataUrl
        """
        instruction = ScreenshotInstruction(
            tab_id=self.get_variable('tab_id', -1),
            format=format,
            quality=quality,
            full_page=full_page,
            delay=delay,
            retry=retry,
            timeout=timeout,
            ignore_error=ignore_error
        )

        result = self.browser._execute_instruction([instruction])

        if not result.get('results') or len(result.get('results', [])) == 0:
            raise BusinessError(
                f"页面截图指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID}
            )

        instruction_result = result.get('results', [])[0]
        if not instruction_result.get('success'):
            raise BusinessError(
                f"页面截图指令失败: {instruction.instructionID}",
                data={"url": self.browser.node_api_base_url, "instruction_id": instruction.instructionID, "error": instruction_result.get('error')}
            )

        data = instruction_result.get('data', {})
        data_url = data.get('dataUrl', '')

        return data_url

    # end   ---------------------------Instruction命令模块(命令)---------------------------------------------

    # begin ---------------------------Http命令模块(命令和对应的回调函数)-------------------------------------

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def bit_browser_list_command(self, context: Context, browser_seq: int, page: int=0, pageSize: int=100, timeout: int = 180, ignoreError: bool = False):
        """
        创建Bit浏览器列表查询命令 - 通过浏览器序号查找浏览器ID
        
        功能说明：
        创建一个HttpBitBrowserListCommand命令对象，用于查询浏览器列表。
        ```
        """

        command = HttpBitBrowserListCommand(seq=browser_seq, page=page, pageSize=pageSize, timeout=timeout, ignore_error=ignoreError)

        response = self.browser._execute_http_command(http_command=command)

        result = json.loads(response)

        if not result.get('success'):
            raise BusinessError(
                f"没有这个序列号的比特浏览器窗口，比特浏览器序号: {browser_seq}",
                data={"url": self.browser.node_api_base_url, "command_id": command.id, "error": result.get('msg')}
            )

        # 从HTTP命令执行结果中提取数据
        # result['data']包含分页信息和浏览器列表
        data = result.get('data', {})

        if not data.get('list'):
            raise BusinessError(
                f"没有这个序列号的比特浏览器窗口，比特浏览器序号: {browser_seq}",
                data={"url": self.browser.node_api_base_url, "command_id": command.id, "error": "未找到浏览器列表"}
            )

        # 遍历浏览器列表，查找序号匹配的浏览器
        # data['list']是浏览器对象数组，每个对象包含浏览器的详细信息
        for browser in data.get('list', []):
            # 检查当前浏览器的序号是否与目标序号匹配
            if browser.get('seq') == browser_seq:
                # 找到匹配的浏览器，保存其ID到网站变量
                # browser_id将用于后续的打开、关闭、重置等操作
                self.set_variable(key='browser_id', value=browser.get('id'))
                # 返回成功结果，包含浏览器ID和消息
                return { 'success': True, 'browser_id': browser.get('id') }

        # 未找到匹配的浏览器，返回失败结果
        raise BusinessError(
            f"浏览器序号不存在: {browser_seq}",
            data={"url": self.browser.node_api_base_url, "browser_seq": browser_seq}
        )

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def bit_browser_open_command(self, context: Context, browser_id: str, args: list = [], queue: bool = True, timeout: int = 180, ignoreError: bool = False):
        """
        创建Bit浏览器打开命令 - 通过浏览器ID并打开

        """
        # 创建并执行打开浏览器命令
        command = HttpBitBrowserOpenCommand(id=browser_id, args=args, queue=queue, timeout=timeout, ignore_error=ignoreError)
        response = self.browser._execute_http_command(http_command=command)

        result = json.loads(response)
        
        if not result.get('success'):
            raise BusinessError(
                f"浏览器打开失败: {result.get('msg', '')}",
                data={"browser_id": browser_id, "error": result.get('msg')}
            )
        
        return result

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def bit_browser_close_command(self, context: Context, browser_id: str, timeout: int = 180, ignoreError: bool = False):
        """
        创建Bit浏览器关闭命令 - 通过浏览器ID并关闭
        
        功能说明：
        创建一个HttpBitBrowserCloseCommand命令对象，用于关闭指定的BitBrowser浏览器实例。
        
        Args:
            browser_id (str): 浏览器ID，用于标识要关闭的浏览器实例
            timeout (int, optional): 请求超时时间（秒），默认为180
            ignoreError (bool, optional): 是否忽略错误，默认为False
        
        Returns:
            dict: HTTP命令执行结果
        """
        # 创建并执行关闭浏览器命令
        command = HttpBitBrowserCloseCommand(id=browser_id, timeout=timeout, ignore_error=ignoreError)
        response = self.browser._execute_http_command(http_command=command)
        result = json.loads(response)
        
        if not result.get('success'):
            raise BusinessError(
                f"浏览器关闭失败: {result.get('msg', '')}",
                data={"browser_id": browser_id, "error": result.get('msg')}
            )
        
        return result

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def bit_browser_reset_command(self, context: Context, browser_id: str, timeout: int = 180, ignoreError: bool = False):
        """
        创建Bit浏览器重置命令 - 通过浏览器ID并重置
        
        功能说明：
        创建一个HttpBitBrowserResetCommand命令对象，用于重置指定的BitBrowser浏览器实例。
        
        Args:
            browser_id (str): 浏览器ID，用于标识要重置的浏览器实例
            timeout (int, optional): 请求超时时间（秒），默认为180
            ignoreError (bool, optional): 是否忽略错误，默认为False
        
        Returns:
            dict: HTTP命令执行结果
        """
        # 创建并执行重置浏览器命令
        command = HttpBitBrowserResetCommand(id=browser_id, timeout=timeout, ignore_error=ignoreError)
        response = self.browser._execute_http_command(http_command=command)
        result = json.loads(response)
        
        if not result.get('success'):
            raise BusinessError(
                f"浏览器重置失败: {result.get('msg', '')}",
                data={"browser_id": browser_id, "error": result.get('msg')}
            )
        
        return result

    @stop_decorator
    @ignore_error_decorator(default_value=None)
    def bit_browser_alive_command(self, context: Context, browser_id: str, timeout: int = 180, ignoreError: bool = False):
        """
        创建Bit浏览器存活查询命令 - 通过浏览器ID并查询是否存活
        """
        command = HttpBitBrowserAliveCommand(id=browser_id, timeout=timeout, ignore_error=ignoreError)
        response = self.browser._execute_http_command(http_command=command)
        result = json.loads(response)

        if not result.get('success'):
            raise BusinessError(f"浏览器存活查询失败: {result.get('msg', '')}", data={"browser_id": browser_id, "error": result.get('msg')})

        data = result.get('data', {})

        pid = data.get(browser_id, None)

        return { 'success': True, 'pid': pid }

    # end   ---------------------------Http命令模块(命令和对应的回调函数)-------------------------------------

    # begin ---------------------------步骤执行模块-------------------------------------------

    def create_tab_step(self, context: Context, url: str, active: bool = True, new_window: bool = False, ignore_error: bool = False) -> StepResult:
        """
        创建标签页步骤
        Args:
            context: 上下文
            url: 要导航的URL
            active: 是否激活标签页
            ignore_error: 是否忽略错误
        """
        try:
            self.create_tab_and_navigate_command(context=context, url=url, active=active, new_window=new_window, ignore_error=ignore_error)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)
        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_tab_step", context=context)
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_tab_step", context=context)

    def create_tab_and_navigate_step(self, context: Context, url: str, active: bool = True, ignore_error: bool = False) -> StepResult:
        """
        创建标签页并导航到首页步骤
        Args:
            context: 上下文
            url: 要导航的URL
            active: 是否激活标签页
            ignore_error: 是否忽略错误
        """

        try:
            self.list_targets_command(context=context, ignore_error=ignore_error)

            if self.get_variable('tab_id', -1) == -1:
                self.create_tab_and_navigate_command(context=context, url=url, active=active, ignore_error=ignore_error)
        
            self.activate_tab_instruction(context=context, ignore_error=ignore_error)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_tab_and_navigate_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_tab_and_navigate_step", context=context)

    def update_node_name_step(self, context: Context, node_name: str, ignore_error: bool = False) -> StepResult:
        """
        更新节点名称步骤
        Args:
            context: 上下文
            node_name: 节点名称
            ignore_error: 是否忽略错误
        """
        try:
            self.update_node_name_command(context=context, node_name=node_name, ignore_error=ignore_error)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)
        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="update_node_name_step", context=context)
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="update_node_name_step", context=context)

    # end   ---------------------------步骤执行模块-------------------------------------------


class Facebook(WebSite):
    """
    Facebook网站类
    Args:
        browser: 浏览器对象(用于执行Cdp命令)
    """

    def __init__(self, browser: Browser, post_title: str = None, post_description: str = None):
        super().__init__(browser=browser, domain="facebook.com")

        self.name = "facebook"

        self.home_url = "https://www.facebook.com/"
        self.login_url = "https://www.facebook.com/login/"
        self.check_url = "https://www.facebook.com/checkpoint/"

        self.set_variable('post_title', post_title)
        self.set_variable('post_description', post_description)

    # begin ---------------------------Html标签元素模块------------------------------------- 

    def royal_login_button(self) -> ElementClass:
        """
        facebook皇家登录按钮元素 data-testid="royal-login-button"
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_royal_login_button',
            selector='button[data-testid="royal-login-button"]',
            selectorType='css',
            description='Login.皇家登录按钮',
        )

    def home_button(self) -> ElementClass:
        """
        facebook首页按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_home_button',
            selector='a[aria-label="Facebook"][href="/"]',
            selectorType='css',
            description='All.首页按钮',
        )

    def back_button(self) -> ElementClass:
        """
        facebook后退按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_back_button',
            selector='div[aria-label="Back"]',
            selectorType='css',
            description='All.后退按钮',
        )

    def live_video_button(self) -> ElementClass:
        """
        facebook直播视频按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_live_video_button',
            selector='div[aria-label="Live video"]',
            selectorType='css',
            description='Home.直播视频按钮',
        )

    def go_live_button(self) -> ElementClass:
        """
        facebook直播按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button',
            selector='div[aria-label="Go live"]', 
            selectorType='css', 
            description='Live Producer.直播按钮', 
        )

    def go_live_button_duplicate_start_set_up(self) -> ElementClass:
        """
        facebook直播按钮元素 duplicate start set up
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button',
            selector='div[aria-label="Start set up"]',
            selectorType='css',
            description='Live Producer.直播按钮 duplicate start set up',
        )

    def go_live_button_duplicate_set_up_live_video(self) -> ElementClass:
        """
        facebook直播按钮元素 duplicate set up live video
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button',
            selector='div[aria-label="Set up live video"]',
            selectorType='css',
            description='Live Producer.直播按钮 duplicate set up live video',
        )
    
    def go_live_button_duplicate_start_setup(self) -> ElementClass:
        """
        facebook直播按钮元素 duplicate start setup
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button',
            selector='div[aria-label="Start setup"]',
            selectorType='css',
            description='Live Producer.直播按钮 duplicate start setup',
        )

    def streaming_software_button(self) -> ElementClass:
        """
        facebook软件流按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_streaming_software_button',
            selector='div[aria-label="Streaming software"]', 
            selectorType='css', 
            description='Live Producer.软件流按钮', 
        )

    def stream_key_input(self) -> ElementClass:
        """
        facebook直播密钥输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_stream_key_input',
            selector='input[aria-label="Stream key"]', 
            selectorType='css', 
            description='Live Producer.直播密钥输入框', 
        )

    def go_live_button_finally(self) -> ElementClass:
        """
        facebook最终直播按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button_finally',
            selector='div[aria-label="Go live"][tabindex="-1"]', 
            selectorType='css', 
            description='Live Producer.最终直播按钮',
        )

    def go_live_button_finally_duplicate(self) -> ElementClass:
        """
        facebook最终直播按钮元素 duplicate
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button_finally',
            selector='div[aria-label="Go Live"][tabindex="-1"]', 
            selectorType='css', 
            description='Live Producer.最终直播按钮 duplicate',
        )

    def go_live_button_without_current(self) -> ElementClass:
        """
        facebook当前直播按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button_without_current',
            selector='div[aria-label="Go live"]:not([aria-current])',
            selectorType='css',
            description='Live Producer.当前直播按钮',
        )

    def go_live_button_without_current_duplicate(self) -> ElementClass:
        """
        facebook当前直播按钮元素 duplicate
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button_without_current',
            selector='div[aria-label="Go Live"]',
            selectorType='css',
            description='Live Producer.当前直播按钮 duplicate',
        )

    def add_title_dialog(self) -> ElementClass:
        """
        facebook添加标题对话框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_add_title_dialog',
            selector='div[aria-label="Add a title"][role="dialog"]', 
            selectorType='css', 
            description='Popup.添加标题对话框', 
        )

    def go_live_button_of_add_title_dialog(self) -> ElementClass:
        """
        facebook添加标题对话框中的直播按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button_of_add_title_dialog',
            selector='div[aria-label="Go live"]', 
            selectorType='css', 
            description='Popup.添加标题对话框中的直播按钮', 
            parentName=f'{self.name}_add_title_dialog',
        )

    def go_live_button_of_add_title_dialog_duplicate(self) -> ElementClass:
        """
        facebook添加标题对话框中的直播按钮元素 duplicate
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button_of_add_title_dialog',
            selector='div[aria-label="Go Live"]',
            selectorType='css',
            description='Popup.添加标题对话框中的直播按钮 duplicate',
        )

    def post_description_div(self) -> ElementClass:
        """
        facebook发布描述div元素 div[aria-label="Description"]
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_post_description_div',
            selector='div[aria-label="Description"]',
            selectorType='css',
            description='Popup.发布描述div',
        )

    def edit_post_details_button(self) -> ElementClass:
        """
        facebook编辑贴文详情按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_edit_post_details_button',
            selector='div[aria-label="Edit Post Details"]',
            selectorType='css',
            description='Post.编辑贴文详情按钮',
        )

    def create_post_display(self) -> ElementClass:
        """
        facebook创建贴文显示框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_create_post_display',
            selector='div[aria-label="Create post"]',
            selectorType='css',
            description='Post.创建贴文显示框',
        )

    def post_title_input_field(self) -> ElementClass:
        """
        facebook贴文标题输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_post_title_input_field',
            selector='input[maxlength="250"]',
            selectorType='css',
            description='Post.贴文标题输入框',
        )

    def post_description_input_field(self) -> ElementClass:
        """
        facebook贴文描述输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_post_description_input_field',
            selector='div[role="textbox"][contenteditable="true"]',
            selectorType='css',
            description='Post.贴文描述输入框',
        )

    def post_save_button(self) -> ElementClass:
        """
        facebook贴文保存按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_post_save_button',
            selector='div[aria-label="Save"]',
            selectorType='css',
            description='Post.贴文保存按钮',
        )

    def end_live_button(self) -> ElementClass:
        """
        facebook结束直播按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_end_live_button',
            selector='div[aria-label="End live video"]',
            selectorType='css',
            description='Live.结束直播按钮',
        )

    def end_live_button_duplicate(self) -> ElementClass:
        """
        facebook结束直播按钮元素 duplicate
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_end_live_button',
            selector='div[aria-label="End Live Video"]',
            selectorType='css',
            description='Live.结束直播按钮 duplicate',
        )

    def enabled_button(self) -> ElementClass:
        """
        facebook启用按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_enabled_button',
            selector='input[aria-label="Enabled"]',
            selectorType='css',
            description='Live.启用按钮',
        )

    def feeling_activity_button(self) -> ElementClass:
        """
        facebook感受/活动按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_feeling_activity_button',
            selector='div[aria-label="Feeling/activity"]',
            selectorType='css',
            description='Live.感受/活动按钮',
        )

    def lovely_button(self) -> ElementClass:
        """
        facebook可爱按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_lovely_button',
            selector='div[aria-label="lovely"]',
            selectorType='css',
            description='Live.可爱按钮',
        )

    # end ---------------------------Html标签元素模块-------------------------------------

    # begin ---------------------------Instruction命令模块(命令)---------------------------------------------

    @WebSite.stop_decorator
    @WebSite.ignore_error_decorator(default_value=False)
    def wait_and_click_immediately_button(self, context: Context, wait_type: str, title_text: str = None, element: ElementClass = None, element_name: str = None, attribute: str = None, attribute_text: str = None, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False) -> bool:
        """
        facebook等待并立即点击元素指令
        Args:
            context: 上下文
            element: 元素
            timeout: 超时时间
            ignore_error: 是否忽略错误
        Returns:
            bool: 是否成功
        """
        # 先等待元素存在
        wait_instruction = WaitInstruction(
            tab_id=self.get_variable('tab_id'),
            wait_type=wait_type, 
            title_text=title_text, 
            element=element, 
            element_name=element_name, 
            attribute=attribute, 
            attribute_text=attribute_text, 
            delay=delay, 
            retry=retry, 
            timeout=timeout, 
            ignore_error=ignore_error
        )

        # 等待成功后，执行点击操作
        element_name = element_name if element_name else element.name
        mouse_instruction = MouseInstruction(
            tab_id=self.get_variable('tab_id'),
            action="click", 
            element_name=element_name, 
            simulate="simulated", 
            ignore_error=ignore_error
        )
        
        # 执行命令
        result = self.browser._execute_instruction([wait_instruction, mouse_instruction])

        for instruction_result in result.get('results', []):
            if instruction_result.get('success'):
                data = instruction_result.get('data', {})
                elementName = data.get('elementName', '')
                if elementName:
                    self.set_variable(elementName, True)
                    return True

        return False

    # end ---------------------------Instruction命令模块(命令)---------------------------------------------

    # begin ---------------------------步骤执行模块-------------------------------------------

    def home_step(self, context: Context) -> StepResult:
        """
        点击首页按钮步骤
        """
        try:
            # 如果当前tab_id不存在, 则创建标签页并导航到登录页面步骤
            if self.get_variable("tab_id", -1) == -1:
                result = self.create_tab_step(context=context, url=self.home_url, active=True, new_window=False, ignore_error=False)
                if not result.success:
                    return result

            # 判断皇家登录按钮是否存在
            self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.royal_login_button(), timeout=5, ignore_error=True)
            if self.get_variable(self.royal_login_button().name, None) is not None:
                raise LoginError("皇家登录按钮存在, 请先登录皇家账号")

            # 判断当前URL是否包含 check_url
            if self.condition_include_current_url_is(url=self.check_url):
                raise BusinessError("Facebook账号需要验证, 请先验证账号")

            # 判断当前域名的tab是否在首页, 如果不在首页, 则查找并点击首页按钮步骤
            if not self.condition_match_current_url_is(url=self.home_url):
                self.find_element_instruction(context=context, element=self.home_button(), ignore_error=False)
                if self.get_variable(self.home_button().name, None) is None:
                    raise BusinessError("Facebook首页按钮不存在, 请检查Facebook首页按钮状态")
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.home_button().name, ignore_error=False)
                time.sleep(3.1)

        # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="home_step", context=context)
            
        except Exception as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="home_step", context=context)

    def live_stream_step(self, context: Context) -> StepResult:
        """
        直播推流步骤
        """
        try:
            # 如果当前tab_id不存在, 则创建标签页并导航到首页步骤
            if self.get_variable("tab_id", -1) == -1:
                result = self.home_step(context=context)
                if not result.success:
                    return result

            # 点击直播视频按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.live_video_button(), ignore_error=False)
            if self.get_variable(self.live_video_button().name, None) is None:
                raise BusinessError("网络出现问题，超时60秒, 未找到Facebook直播视频按钮")
            self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.live_video_button().name, ignore_error=False)

            # 等待并立即点击直播按钮元素
            self.wait_and_click_immediately_button(context=context, wait_type="wait_element_exists", element=self.go_live_button(), timeout=60, ignore_error=True)
            if self.get_variable(self.go_live_button().name, None) is None:
                # 点击开始设置按钮步骤
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button_duplicate_start_set_up(), timeout=3, ignore_error=False)
                if self.get_variable(self.go_live_button_duplicate_start_set_up().name, None) is None:
                    # 点击设置直播视频按钮步骤
                    self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button_duplicate_set_up_live_video(), timeout=3, ignore_error=False)
                    if self.get_variable(self.go_live_button_duplicate_set_up_live_video().name, None) is None:
                        # 点击开始设置按钮步骤
                        self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button_duplicate_start_setup(), timeout=3, ignore_error=False)
                        if self.get_variable(self.go_live_button_duplicate_start_setup().name, None) is None:
                            raise BusinessError("facebook直播按钮不可用, 请检查Live Producer.直播按钮")
                
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.go_live_button().name, ignore_error=False)

            time.sleep(3.1)

            # 点击软件流按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.streaming_software_button(), ignore_error=False)
            if self.get_variable(self.streaming_software_button().name, None) is None:
                raise BusinessError("软件流按钮不可用, 请检查软件流按钮状态")
            self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.streaming_software_button().name, ignore_error=False)
            time.sleep(1.1)

            # 获取直播密钥输入框属性 value, 其它WebSite对象需要使用此变量, 所以需要设置为上下文变量
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.stream_key_input(), ignore_error=False)
            if self.get_variable(self.stream_key_input().name, None) is None:
                raise BusinessError("直播密钥输入框不可用, 请检查直播密钥输入框状态")
            stream_key_input_attribute = self.get_attribute_instruction(context=context, attribute="value", element_name=self.stream_key_input().name, ignore_error=False)
            context.set_var('stream_key', stream_key_input_attribute)
            time.sleep(0.3)

            # 查找 go_live_button_finally 元素
            self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.go_live_button_finally(), timeout=10, ignore_error=False)
            if self.get_variable(self.go_live_button_finally().name, None) is None:
                # 查找 go_live_button_finally_duplicate 元素
                self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.go_live_button_finally_duplicate(), timeout=10, ignore_error=False)
                if self.get_variable(self.go_live_button_finally_duplicate().name, None) is None:
                    raise BusinessError("facebook最终直播按钮不存在, 请检查Live Producer.最终直播按钮")

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="live_stream_step", context=context)
            
        except Exception as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="live_stream_step", context=context)

    def go_live_step(self, context: Context, post_title: str = None, post_description: str = None):
        """
        直播按钮步骤
        """
        try:
            # 如果当前tab_id不存在, 则创建标签页并导航到首页步骤
            if self.get_variable("tab_id", -1) == -1:
                result = self.live_stream_step(context=context)
                if not result.success:
                    return result

            # 判断当前域名是否在后台按钮中
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.back_button(), timeout=60, ignore_error=False)
            if self.get_variable(self.back_button().name, None) is None:
                raise BusinessError("后台按钮不可用, 请检查后台按钮状态")

            # 判断有没有'启用按钮'按钮
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.enabled_button(), timeout=10, ignore_error=True)
            if self.get_variable(self.enabled_button().name, None) is None:
                # 判断最终直播按钮是否可点击
                for i in range(60):
                    go_live_button_finally_aria_disabled_attribute = self.get_attribute_instruction(context=context, attribute="aria-disabled", element_name=self.go_live_button_finally().name, ignore_error=False)
                    if go_live_button_finally_aria_disabled_attribute == "true":
                        time.sleep(3.1)
                    else:
                        break
                else:
                    raise BusinessError("最终直播按钮不可用, 请检查最终直播按钮状态")

                # 点击直播按钮步骤
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button_without_current(), timeout=5, ignore_error=False)
                if self.get_variable(self.go_live_button_without_current().name, None) is None:
                    # 查找 go_live_button_without_current_duplicate 元素
                    self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.go_live_button_without_current_duplicate(), timeout=3, ignore_error=False)
                    if self.get_variable(self.go_live_button_without_current_duplicate().name, None) is None:
                        raise BusinessError("facebook当前直播按钮不可用, 请检查Live Producer.当前直播按钮")
                
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.go_live_button_without_current().name, ignore_error=False)
                time.sleep(1.7)

                # 点击添加标题对话框中的直播按钮步骤
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.add_title_dialog(), timeout=120, ignore_error=False)
                if self.get_variable(self.add_title_dialog().name, None) is None:
                    raise BusinessError("添加标题对话框不可用, 请检查添加标题对话框状态")
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button_of_add_title_dialog(), timeout=3, ignore_error=False)
                if self.get_variable(self.go_live_button_of_add_title_dialog().name, None) is None:
                    # 查找 go_live_button_of_add_title_dialog_duplicate 元素
                    self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.go_live_button_of_add_title_dialog_duplicate(), timeout=3, ignore_error=False)
                    if self.get_variable(self.go_live_button_of_add_title_dialog_duplicate().name, None) is None:
                        raise BusinessError("facebook添加标题对话框中的直播按钮不可用, 请检查Popup.添加标题对话框中的直播按钮")
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.go_live_button_of_add_title_dialog().name, ignore_error=False)
                time.sleep(3.3)
            else:
                # 点击'感受/活动按钮'
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.feeling_activity_button(), timeout=10, ignore_error=False)
                if self.get_variable(self.feeling_activity_button().name, None) is None:
                    raise BusinessError("感受/活动按钮不可用, 请检查感受/活动按钮状态")
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.feeling_activity_button().name, ignore_error=False)
                time.sleep(2.7)

                # 点击'可爱按钮'
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.lovely_button(), timeout=10, ignore_error=False)
                if self.get_variable(self.lovely_button().name, None) is None:
                    raise BusinessError("可爱按钮不可用, 请检查可爱按钮状态")
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.lovely_button().name, ignore_error=False)
                time.sleep(1.7)

                # 判断有没有'创建贴文'显示
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.create_post_display(), timeout=10, ignore_error=True)
                if self.get_variable(self.create_post_display().name, None) is None:
                    raise BusinessError("创建贴文显示不可用, 请检查创建贴文显示状态")

                # 点击'贴文标题'输入框
                post_title = post_title if post_title else self.get_variable('post_title')
                if post_title:
                    self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.post_title_input_field(), ignore_error=False)
                    if self.get_variable(self.post_title_input_field().name, None) is None:
                        raise BusinessError("贴文标题输入框不可用, 请检查贴文标题输入框状态")
                    self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.post_title_input_field().name, ignore_error=False)
                    # 使用 keyboard_instruction 输入贴文标题
                    self.keyboard_instruction(context=context, action="press", text=post_title, delay=0.6, element_name=self.post_title_input_field().name, ignore_error=False)
                    time.sleep(1)
                    
                # 点击'贴文描述'输入框
                post_description = post_description if post_description else self.get_variable('post_description')
                if post_description:
                    self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.post_description_input_field(), ignore_error=False)
                    if self.get_variable(self.post_description_input_field().name, None) is None:
                        raise BusinessError("贴文描述输入框不可用, 请检查贴文描述输入框状态")
                    self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.post_description_input_field().name, ignore_error=False)
                    self.keyboard_instruction(context=context, action="press", text=post_description, delay=0.7, element_name=self.post_description_input_field().name, ignore_error=False)
                    time.sleep(1)

                # 点击'贴文保存'按钮
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.post_save_button(), ignore_error=False)
                if self.get_variable(self.post_save_button().name, None) is None:
                    raise BusinessError("贴文保存按钮不可用, 请检查贴文保存按钮状态")
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.post_save_button().name, ignore_error=False)
                time.sleep(3)

                # 判断最终直播按钮是否可点击
                for i in range(60):
                    go_live_button_finally_aria_disabled_attribute = self.get_attribute_instruction(context=context, attribute="aria-disabled", element_name=self.go_live_button_finally().name, ignore_error=False)
                    if go_live_button_finally_aria_disabled_attribute == "true":
                        time.sleep(3.1)
                    else:
                        break
                else:
                    raise BusinessError("最终直播按钮不可用, 请检查最终直播按钮状态")

                # 点击直播按钮步骤
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button_without_current(), timeout=3, ignore_error=False)
                if self.get_variable(self.go_live_button_without_current().name, None) is None:
                    # 查找 go_live_button_without_current_duplicate 元素
                    self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.go_live_button_without_current_duplicate(), timeout=3, ignore_error=False)
                    if self.get_variable(self.go_live_button_without_current_duplicate().name, None) is None:
                        raise BusinessError("facebook当前直播按钮不可用, 请检查Live Producer.当前直播按钮")
                
                self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.go_live_button_without_current().name, ignore_error=False)
                time.sleep(3.2)

            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.end_live_button(), timeout=60, ignore_error=False)
            if self.get_variable(self.end_live_button().name, None) is None:
                # 查找 end_live_button_duplicate 元素
                self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.end_live_button_duplicate(), timeout=3, ignore_error=False)
                if self.get_variable(self.end_live_button_duplicate().name, None) is None:
                    raise BusinessError("facebook结束直播按钮不可用, 请检查Live Producer.结束直播按钮")

            time.sleep(2.6)

            # 关闭当前标签页
            self.close_tab_command(context=context, ignore_error=False)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="go_live_step", context=context)

        except Exception as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="go_live_step", context=context)

    # end ---------------------------步骤执行模块---------------------------------------------


class Onestream(WebSite):
    """
    Onestream网站类
    Args:
        browser: 浏览器对象(用于执行Cdp命令)
        onestream_account: Onestream账号
        onestream_password: Onestream密码
        live_social_account: 直播社交平台账号
        video_name: 视频名称
    """
    def __init__(self, browser: Browser, onestream_account: str = None, onestream_password: str = None, live_social_account: str = None, video_name: str = None, stream_key: str = None):
        super().__init__(browser=browser, domain="onestream.live")

        self.name = "onestream"

        # 网站基础信息
        self.home_url = "https://app.onestream.live/"
        self.login_url = "https://app.onestream.live/login/"

        self.onestream_account = onestream_account
        self.onestream_password = onestream_password
        self.live_social_account = live_social_account
        self.video_name = video_name
        self.stream_key = stream_key

        # begin ---------------------------Html标签元素模块------------------------------------- 

    def login_email_input(self) -> ElementClass:
        """
        onestream登录邮箱输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_login_email_input',
            selector='#login_email_input',
            selectorType='css',
            description='Login.邮箱输入框',
        )

    def login_password_input(self) -> ElementClass:
        """
        onestream登录密码输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_login_password_input',
            selector='#login_password_input',
            selectorType='css',
            description='Login.密码输入框',
        )

    def login_button(self) -> ElementClass:
        """
        onestream登录按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_login_button',
            selector='#login_button',
            selectorType='css',
            description='Login.登录按钮',
        )

    def social_platforms_button(self) -> ElementClass:
        """
        onestream社交平台按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_social_platforms_button',
            selector='div[aria-label="Social Platforms"]',
            selectorType='css',
            description='Destinations.社交平台按钮',
        )

    def schedules_button(self) -> ElementClass:
        """
        onestream计划任务按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_schedules_button',
            selector='div[aria-label="Schedules"]',
            selectorType='css',
            description='Schedules.计划任务按钮',
        )

    def schedules_input(self) -> ElementClass:
        """
        onestream计划任务输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_schedules_input',
            selector='#os-3602',
            selectorType='css',
            description='Schedules.计划任务输入框',
        )

    def account_search_input(self) -> ElementClass:
        """
        onestream账号搜索输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_account_search_input',
            selector='input[aria-label="description"]',
            selectorType='css',
            description='Destinations.账号搜索输入框',
        )

    def rtmp_update_button(self) -> ElementClass:
        """
        onestreamRTMP更新按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_rtmp_update_button',
            selector='div[aria-label="Update RTMP destination"]',
            selectorType='css',
            description='Destinations.RTMP更新按钮',
        )

    def stream_key_input(self) -> ElementClass:
        """
        onestream直播密钥输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_stream_key_input',
            selector='#os-272',
            selectorType='css',
            description='Destinations.直播密钥输入框',
        )

    def update_button(self) -> ElementClass:
        """
        onestream更新按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_update_button',
            selector='#os-39',
            selectorType='css',
            description='Destinations.更新按钮',
        )

    def create_stream_button(self) -> ElementClass:
        """
        onestream创建流按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_create_stream_button',
            selector='#header-primary-btn1',
            selectorType='css',
            description='Stream.创建流按钮',
        )

    def single_video_button_container(self) -> ElementClass:
        """
        onestream单视频按钮容器元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_single_video_button_container',
            selector='#os-3606',
            selectorType='css',
            description='Stream.单视频按钮容器',
        )

    def single_video_button(self) -> ElementClass:
        """
        onestream单视频按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_single_video_button',
            text='Single Video',
            selector='span',
            selectorType='text',
            description='Stream.单视频按钮',
            parentName=f'{self.name}_single_video_button_container',
        )

    def onestream_storage_button(self) -> ElementClass:
        """
        onestream存储按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_onestream_storage_button',
            selector='svg[data-testid="ArrowForwardIosOutlinedIcon"]',
            selectorType='css',
            description='Stream.Onestream存储按钮',
        )

    def video_search_input(self) -> ElementClass:
        """
        onestream搜索视频输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_video_search_input',
            selector='input[placeholder="Search Videos"][aria-label="description"]',
            selectorType='css',
            description='Stream.直播视频搜索输入框',
        )

    def video_select_container(self) -> ElementClass:
        """
        onestream选择视频容器元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_video_select_container',
            selector='div[primarybuttontext="Select Video"]',
            selectorType='css',
            description='Stream.视频选择容器',
        )

    def video_select_button(self) -> ElementClass:
        """
        onestream选择视频按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_video_select_button',
            selector='button',
            selectorType='css',
            description='Stream.视频选择按钮',
            parentName=f'{self.name}_video_select_container',
        )

    def live_social_account_button(self, live_social_account: str = None) -> ElementClass:
        """
        onestream选择直播社交平台账号按钮元素
        """
        live_social_account = self.live_social_account if live_social_account is None else live_social_account

        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_live_social_account_button',
            selector=f'div[aria-label^="{ live_social_account }"]',
            selectorType='css',
            description='Stream.选择直播社交平台账号按钮',
        )

    def go_live_button(self) -> ElementClass:
        """
        onestream直播按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_go_live_button',
            selector='#os-160',
            selectorType='css',
            description='Stream.直播按钮',
        )

    def confirm_live_button(self) -> ElementClass:
        """
        onestream直播确认按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_confirm_live_button',
            selector='#os-256',
            selectorType='css',
            description='Stream.直播确认按钮',
        )

    def close_popup_button(self) -> ElementClass:
        """
        onestream关闭弹窗按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_close_popup_button',
            selector='svg[data-testid="CloseOutlinedIcon"]',
            selectorType='css',
            description='Stream.关闭弹窗按钮',
        )

    def video_name_span(self, video_name: str = None) -> ElementClass:
        """
        onestream视频名称span元素
        """
        video_name = self.video_name if video_name is None else video_name
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_video_name_span',
            text=video_name,
            selector=f'span',
            selectorType='text',
            description='Stream.视频名称',
        )

    def schedule_item_container(self) -> ElementClass:
        """
        onestream直播计划容器元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_schedule_item_container',
            selector='div.schedule-item-container',
            selectorType='css',
            description='Stream.直播计划容器',
            childrenName=f'{self.name}_video_name_span',
        )

    def schedule_item_buttons_container(self) -> ElementClass:
        """
        onestream直播计划按钮容器元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_schedule_item_buttons_container',
            selector='div.schedule-item-buttons-container',
            selectorType='css',
            description='Stream.直播计划按钮容器',
            parentName=f'{self.name}_schedule_item_container',
        )

    def stop_button_container(self) -> ElementClass:
        """
        onestream停止按钮容器元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_stop_button_container',
            selector='div.stop-button-container',
            selectorType='css',
            description='Stream.停止按钮容器',
            parentName=f'{self.name}_schedule_item_buttons_container',
        )

    def add_social_platform(self) -> ElementClass:
        """
        onestream添加社交平台按钮元素 os-239
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_add_social_platform',
            selector='#os-239',
            selectorType='css',
            description='destinations.添加社交平台按钮',
        )

    def custom_rtmp_button(self) -> ElementClass:
        """
        onestream自定义RTMP按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_custom_rtmp_button',
            selector='img[src$="rtmp.png"]',
            selectorType='css',
            description='destinations.自定义RTMP按钮',
        )

    def social_account_input(self) -> ElementClass:
        """
        onestream社交账号输入框元素 os-270
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_social_account_input',
            selector='#os-270',
            selectorType='css',
            description='destinations.社交账号输入框',
        )

    def choose_platform_container(self) -> ElementClass:
        """
        onestream选择平台容器元素 os-1112
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_choose_platform_container',
            selector='#os-1112',
            selectorType='css',
            description='destinations.选择平台容器元素',
        )

    def choose_platform_combobox(self) -> ElementClass:
        """
        onestream选择平台下拉框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_choose_platform_combobox',
            selector='div[aria-haspopup="listbox"]',
            selectorType='css',
            description='destinations.选择平台下拉框',
            parentName=f'{self.name}_choose_platform_container',
        )

    def choose_platform_facebook_button(self) -> ElementClass:
        """
        onestream选择平台Facebook按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_choose_platform_facebook_button',
            selector='li[data-value="Facebook"]',
            selectorType='css',
            description='destinations.选择平台Facebook按钮',
        )

    def server_url_right_arrow_button(self) -> ElementClass:
        """
        onestream服务器URL右侧箭头按钮元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_server_url_right_arrow_button',
            selector='svg[data-testid="ArrowDropDownIcon"]',
            selectorType='css',
            description='destinations.服务器URL右侧箭头按钮',
        )
    
    def server_facebook_url_input(self) -> ElementClass:
        """
        onestreamFacebook服务器URL输入框元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_server_facebook_url_input',
            selector='li[data-value="rtmps://live-api-s.facebook.com:443/rtmp/"]',
            selectorType='css',
            description='destinations.Facebook服务器URL输入框',
        )

    def connect_button(self) -> ElementClass:
        """
        onestream连接按钮元素 os-39
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_connect_button',
            selector='#os-39',
            selectorType='css',
            description='destinations.连接按钮',
        )

    def custom_rtmp_span(self) -> ElementClass:
        """
        onestream自定义RTMP span元素
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_custom_rtmp_span',
            text='Custom RTMP',
            selector='span.social-account',
            selectorType='text',
            description='destinations.自定义RTMP span',
        )

    def disconnect_button(self) -> ElementClass:
        """
        onestream断开按钮元素 os-900
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_disconnect_button',
            selector='#os-900',
            selectorType='css',
            description='destinations.社交账号断开按钮',
        )
    
    def disconnect_confirm_button(self) -> ElementClass:
        """
        onestream断开确认按钮元素 os-256
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_disconnect_confirm_button',
            selector='#os-256',
            selectorType='css',
            description='destinations.断开确认按钮',
        )

    def social_account_all_selected_button(self) -> ElementClass:
        """
        onestream社交账号全选按钮元素 os-3026
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_social_account_all_selected_button',
            selector='#os-3026',
            selectorType='css',
            description='destinations.社交账号全选按钮',
        )

    def social_account_all_disconnect_button(self) -> ElementClass:
        """
        onestream社交账号全部断开按钮元素 os-3027
        """
        return ElementClass(
            tab_id=self.get_variable('tab_id'),
            name= f'{self.name}_social_account_all_disconnect_button',
            selector='#os-3027',
            selectorType='css',
            description='destinations.社交账号全部断开按钮',
        )

    # end ---------------------------Html标签元素模块------------------------------------- 

    # begin ---------------------------步骤执行模块-------------------------------------------

    def login_onestream_step(self, context: Context, onestream_account: str = None, onestream_password: str = None) -> StepResult:
        """
        Onestream登录步骤
        
        Args:
            onestream_account: Onestream账号
            onestream_password: Onestream密码
        """
        try:
            # 如果当前tab_id不存在, 则创建标签页并导航到登录页面步骤
            if self.get_variable("tab_id", -1) == -1:
                result = self.create_tab_step(context=context, url=self.home_url, active=False, new_window=True, ignore_error=False)
                if not result.success:
                    return result

            self.get_tab_url_instruction(context=context)

            # 如果没有登录, 页面会自动跳转到登录页面, 所以需要判断当前域名的tab是否在登录页面, 如果在登录页面，则输入账号密码并登录
            if self.condition_match_current_url_is(url=self.login_url):
                onestream_account = self.onestream_account if onestream_account is None else onestream_account
                onestream_password = self.onestream_password if onestream_password is None else onestream_password
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.login_email_input(), ignore_error=False)
                self.input_instruction(context=context, text=onestream_account, element_name=self.login_email_input().name, ignore_error=False)
                time.sleep(1)
                self.find_element_instruction(context=context, element=self.login_password_input(), ignore_error=False)
                self.input_instruction(context=context, text=onestream_password, element_name=self.login_password_input().name, ignore_error=False)
                time.sleep(1)
                self.find_element_instruction(context=context, element=self.login_button(), ignore_error=False)
                self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.login_button().name, ignore_error=False)
                time.sleep(3)
        
            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="login_onestream_step", context=context)
            
        except Exception as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="login_onestream_step", context=context)

    def update_social_account_stream_key_step(self, context: Context, onestream_account: str = None, onestream_password: str = None, live_social_account: str = None, stream_key: str = None) -> StepResult:
        """
        Onestream更新社交账号直播密钥步骤
        """
        try:
            # 如果没有登录, 页面会自动跳转到登录页面, 所以需要判断当前域名的tab是否在登录页面, 如果在登录页面，则输入账号密码并登录
            result = self.login_onestream_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password)
            if not result.success:
                return result

            # 点击 Onestream社交平台页面按钮
            self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.social_platforms_button(), timeout=30, ignore_error=False)

            # 检测社交平台页面按钮是否可见
            if self.get_variable(self.social_platforms_button().name, None) is None:
                raise BusinessError(f"社交平台页面按钮不可见", data={"onestream_account": onestream_account})

            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.social_platforms_button().name, ignore_error=False)

            # 搜索直播社交平台账号（在Onestream社交平台页面搜索直播社交平台账号）
            live_social_account = self.live_social_account if live_social_account is None else live_social_account
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.account_search_input(), ignore_error=False)
            self.input_instruction(context=context, text=live_social_account, element_name=self.account_search_input().name, ignore_error=False)

            # 点击社交账号编辑按钮（在Onestream社交平台页面点击社交账号编辑按钮）
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.rtmp_update_button(), ignore_error=False)
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.rtmp_update_button().name, ignore_error=False)

            # 等待并输入直播密钥
            stream_key = self.stream_key if stream_key is None else stream_key
            stream_key = context.get_var('stream_key', None) if stream_key is None else stream_key
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.stream_key_input(), ignore_error=False)
            self.input_instruction(context=context, text=stream_key, element_name=self.stream_key_input().name, clear=True, ignore_error=False)

            # 查找并点击更新按钮
            self.find_element_instruction(context=context, element=self.update_button(), ignore_error=False)
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.update_button().name, ignore_error=False)

            time.sleep(7)

            # 关闭标签页
            self.close_tab_command(context=context, ignore_error=False)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="update_social_account_stream_key_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="update_social_account_stream_key_step", context=context)

    def delete_social_account_step(self, context: Context, onestream_account: str = None, onestream_password: str = None, live_social_account: str = None) -> StepResult:
        """
        Onestream删除社交账号步骤
        """
        try:
            # 如果没有登录, 页面会自动跳转到登录页面, 所以需要判断当前域名的tab是否在登录页面, 如果在登录页面，则输入账号密码并登录
            result = self.login_onestream_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password)
            if not result.success:
                return result

            # 点击 Onestream社交平台页面按钮
            self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.social_platforms_button(), ignore_error=False)

            # 检测社交平台页面按钮是否可见
            if self.get_variable(self.social_platforms_button().name, None) is None:
                raise BusinessError(f"社交平台页面按钮不可见", data={"onestream_account": onestream_account})

            self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.social_platforms_button().name, ignore_error=False)
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.custom_rtmp_span(), timeout=10, ignore_error=True)

            if self.get_variable(self.custom_rtmp_span().name, None) is not None:
                # 搜索直播社交平台账号（在Onestream社交平台页面搜索直播社交平台账号）
                live_social_account = self.live_social_account if live_social_account is None else live_social_account
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.account_search_input(), ignore_error=False)
                self.input_instruction(context=context, text=live_social_account, element_name=self.account_search_input().name, ignore_error=False)

                time.sleep(3)

                # 点击断开按钮（在Onestream社交平台页面点击断开按钮）
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.disconnect_button(), ignore_error=True)
                if self.get_variable(self.disconnect_button().name, None) is not None:
                    self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.disconnect_button().name, ignore_error=False)

                    time.sleep(1)
    
                    # 点击断开确认按钮（在Onestream社交平台页面点击断开确认按钮）
                    self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.disconnect_confirm_button(), ignore_error=True)
                    if self.get_variable(self.disconnect_confirm_button().name, None) is not None:
                        self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.disconnect_confirm_button().name, ignore_error=False)

            time.sleep(3)

            # 关闭标签页
            self.close_tab_command(context=context, ignore_error=False)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)
        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="delete_social_account_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="delete_social_account_step", context=context)

    def clear_all_social_accounts_step(self, context: Context, onestream_account: str = None, onestream_password: str = None) -> StepResult:
        """
        Onestream清除所有社交平台步骤
        """
        try:
            # 如果没有登录, 页面会自动跳转到登录页面, 所以需要判断当前域名的tab是否在登录页面, 如果在登录页面，则输入账号密码并登录
            result = self.login_onestream_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password)
            if not result.success:
                return result

            # 点击 Onestream社交平台页面按钮
            self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.social_platforms_button(), ignore_error=False)

            # 检测社交平台页面按钮是否可见
            if self.get_variable(self.social_platforms_button().name, None) is None:
                raise BusinessError(f"社交平台页面按钮不可见", data={"onestream_account": onestream_account})

            self.mouse_instruction(context=context, action="click", simulate="simulated", element_name=self.social_platforms_button().name, ignore_error=False)

            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.custom_rtmp_span(), timeout=10, ignore_error=True)

            if self.get_variable(self.custom_rtmp_span().name, None) is not None:
                self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.social_account_all_selected_button(), ignore_error=False)
                self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.social_account_all_selected_button().name, ignore_error=False)
                time.sleep(1)
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.social_account_all_disconnect_button(), ignore_error=False)
                self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.social_account_all_disconnect_button().name, ignore_error=False)
                time.sleep(1)
                self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.disconnect_confirm_button(), ignore_error=False)
                self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.disconnect_confirm_button().name, ignore_error=False)

            time.sleep(7)

            # 关闭标签页
            self.close_tab_command(context=context, ignore_error=False)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="clear_all_social_accounts_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="clear_all_social_accounts_step", context=context)

    def create_social_account_stream_key_step(self, context: Context, onestream_account: str = None, onestream_password: str = None, live_social_account: str = None, stream_key: str = None) -> StepResult:
        """
        Onestream创建社交账号和直播密钥步骤
        """
        try:
            # 如果没有登录, 页面会自动跳转到登录页面, 所以需要判断当前域名的tab是否在登录页面, 如果在登录页面，则输入账号密码并登录
            result = self.login_onestream_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password)
            if not result.success:
                self.close_tab_command(context=context, ignore_error=False)
                return result

            # 导航到Onestream社交平台页面步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.social_platforms_button(), timeout=120, ignore_error=False)
            # 检测社交平台页面按钮是否可见
            if self.get_variable(self.social_platforms_button().name, None) is None:
                raise BusinessError(f"社交平台页面按钮不可见", data={"onestream_account": onestream_account})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.social_platforms_button().name, timeout=60, ignore_error=False)

            time.sleep(1.7)

            # 点击 add_social_platform 按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.add_social_platform(), timeout=60, ignore_error=False)
            if self.get_variable(self.add_social_platform().name, None) is None:
                raise BusinessError(f"添加社交平台按钮不存在, 请检查Live Producer.添加社交平台按钮")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.add_social_platform().name, ignore_error=False)

            time.sleep(1.7)

            # 点击 custom_rtmp_button 按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.custom_rtmp_button(), timeout=60, ignore_error=False)
            if self.get_variable(self.custom_rtmp_button().name, None) is None:
                raise BusinessError(f"自定义RTMP按钮不存在, 请检查Live Producer.自定义RTMP按钮")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.custom_rtmp_button().name, ignore_error=False)

            time.sleep(1.2)

            # 点击 choose_platform_combobox 下拉框步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.choose_platform_container(), timeout=30, ignore_error=False)
            if self.get_variable(self.choose_platform_container().name, None) is None:
                raise BusinessError(f"选择平台容器按钮不存在, 请检查Live Producer.选择平台容器按钮")
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.choose_platform_combobox(), timeout=30, ignore_error=False)
            if self.get_variable(self.choose_platform_combobox().name, None) is None:
                raise BusinessError(f"选择平台下拉框按钮不存在, 请检查Live Producer.选择平台下拉框按钮")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.choose_platform_combobox().name, ignore_error=False)

            time.sleep(1.7)

            # 选择平台Facebook按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.choose_platform_facebook_button(), timeout=30, ignore_error=False)
            if self.get_variable(self.choose_platform_facebook_button().name, None) is None:
                raise BusinessError(f"选择平台Facebook按钮不存在, 请检查Live Producer.选择平台Facebook按钮")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.choose_platform_facebook_button().name, ignore_error=False)

            time.sleep(1.7)

            # 点击 server_url_right_arrow_button 右侧箭头按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.server_url_right_arrow_button(), timeout=30, ignore_error=False)
            if self.get_variable(self.server_url_right_arrow_button().name, None) is None:
                raise BusinessError(f"服务器URL右侧箭头按钮不存在, 请检查Live Producer.服务器URL右侧箭头按钮")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.server_url_right_arrow_button().name, ignore_error=False)

            time.sleep(1.7)

            # 点击 server_facebook_url_input 服务器URL输入框步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.server_facebook_url_input(), timeout=30, ignore_error=False)
            if self.get_variable(self.server_facebook_url_input().name, None) is None:
                raise BusinessError(f"服务器URL输入框不存在, 请检查Live Producer.服务器URL输入框")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.server_facebook_url_input().name, ignore_error=False)

            time.sleep(1.7)

            # 输入社交账号步骤
            live_social_account = self.live_social_account if live_social_account is None else live_social_account
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.social_account_input(), timeout=30, ignore_error=False)
            if self.get_variable(self.social_account_input().name, None) is None:
                raise BusinessError(f"社交账号输入框不存在, 请检查Live Producer.社交账号输入框")
            self.input_instruction(context=context, text=live_social_account, element_name=self.social_account_input().name, clear=True, ignore_error=False)

            time.sleep(1)

            # 输入直播密钥步骤
            stream_key = self.stream_key if stream_key is None else stream_key
            stream_key = context.get_var('stream_key', '') if stream_key is None else stream_key
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.stream_key_input(), timeout=30, ignore_error=False)
            if self.get_variable(self.stream_key_input().name, None) is None:
                raise BusinessError(f"直播密钥输入框不存在, 请检查Live Producer.直播密钥输入框")
            self.input_instruction(context=context, text=stream_key, element_name=self.stream_key_input().name, clear=True, ignore_error=False)

            time.sleep(1)

            # 点击 update_button 更新按钮步骤
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.update_button(), timeout=30, ignore_error=False)
            if self.get_variable(self.update_button().name, None) is None:
                raise BusinessError(f"更新按钮不存在, 请检查Live Producer.更新按钮")
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.update_button().name, ignore_error=False)

            time.sleep(7)
        
            # 关闭标签页
            self.close_tab_command(context=context, ignore_error=False)

            self.set_variable(key='tab_id', value=-1)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_social_account_stream_key_step", context=context)
            
        except Exception as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_social_account_stream_key_step", context=context)

    def create_video_stream_step(self, context: Context, onestream_account: str = None, onestream_password: str = None, live_social_account: str = None, video_name: str = None) -> StepResult:
        """
        Onestream创建视频流步骤
        
        Args:
            onestream_account: Onestream账号
            onestream_password: Onestream密码
            video_name: 视频名称
            live_social_account: 直播社交平台账号
            stream_key: 直播密钥
        """
        try:
            # 如果没有登录, 页面会自动跳转到登录页面, 所以需要判断当前域名的tab是否在登录页面, 如果在登录页面，则输入账号密码并登录
            result = self.login_onestream_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password)
            if not result.success:
                return result

            # 点击创建流按钮
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.create_stream_button(), timeout=30, ignore_error=False)
            # 检测创建流按钮是否可见
            if self.get_variable(self.create_stream_button().name, None) is None:
                raise BusinessError(f"创建流按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.create_stream_button().name, ignore_error=False)
            time.sleep(1)

            # 点击单视频按钮
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.single_video_button_container(), timeout=30, ignore_error=False)
            if self.get_variable(self.single_video_button_container().name, None) is None:
                raise BusinessError(f"单视频按钮容器不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.find_element_instruction(context=context, element=self.single_video_button(), ignore_error=False)
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.single_video_button().name, ignore_error=False)
            time.sleep(1)

            # 点击Onestream存储按钮
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.onestream_storage_button(), timeout=30, ignore_error=False)
            if self.get_variable(self.onestream_storage_button().name, None) is None:
                raise BusinessError(f"Onestream存储按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.onestream_storage_button().name, ignore_error=False)
            time.sleep(1)

            # 搜索直播视频
            video_name = self.video_name if video_name is None else video_name
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.video_search_input(), timeout=30, ignore_error=False)
            if self.get_variable(self.video_search_input().name, None) is None:
                raise BusinessError(f"直播视频搜索输入框不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.input_instruction(context=context, text=video_name, element_name=self.video_search_input().name, clear=True, ignore_error=False)
            time.sleep(7)

            # 选择视频
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.video_select_container(), timeout=30, ignore_error=False)
            if self.get_variable(self.video_select_container().name, None) is None:
                raise BusinessError(f"视频选择容器不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.find_element_instruction(context=context, element=self.video_select_button(), ignore_error=False)
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.video_select_button().name, ignore_error=False)
            
            time.sleep(5)
            
            # 选择直播社交平台账号（在Onestream社交平台页面选择直播社交平台账号）
            live_social_account = self.live_social_account if live_social_account is None else live_social_account
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.live_social_account_button(live_social_account=live_social_account), timeout=60, ignore_error=False)
            if self.get_variable(self.live_social_account_button(live_social_account=live_social_account).name, None) is None:
                raise BusinessError(f"选择直播社交平台账号按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name, "live_social_account": live_social_account})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.live_social_account_button(live_social_account=live_social_account).name, ignore_error=False)
            
            time.sleep(1)

            # 点击直播按钮（在Onestream社交平台页面点击直播按钮）
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.go_live_button(), timeout=30, ignore_error=False)
            if self.get_variable(self.go_live_button().name, None) is None:
                raise BusinessError(f"直播按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.go_live_button().name, ignore_error=False)
            
            time.sleep(2)
            
            # 点击直播确认按钮（在Onestream社交平台页面点击直播确认按钮）
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.confirm_live_button(), timeout=30, ignore_error=False)
            if self.get_variable(self.confirm_live_button().name, None) is None:
                raise BusinessError(f"直播确认按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.confirm_live_button().name, ignore_error=False)

            time.sleep(7)

            # 关闭弹窗按钮（在Onestream社交平台页面关闭弹窗按钮）
            self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.close_popup_button(), timeout=60, ignore_error=False)
            if self.get_variable(self.close_popup_button().name, None) is None:
                raise BusinessError(f"关闭弹窗按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.close_popup_button().name, ignore_error=False)
            # time.sleep(1)

            # # 点击计划任务按钮
            # self.wait_instruction(context=context, wait_type="wait_element_exists", element=self.schedules_button(), ignore_error=False)
            # if self.get_variable(self.schedules_button().name, None) is None:
            #     raise BusinessError(f"计划任务按钮不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            # self.mouse_instruction(context=context, action="click", simulate="none", element_name=self.schedules_button().name, ignore_error=False)
            # time.sleep(3)

            # # 输入计划任务
            # self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.schedules_input(), ignore_error=False)
            # if self.get_variable(self.schedules_input().name, None) is None:
            #     raise BusinessError(f"计划任务输入框不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            # self.input_instruction(context=context, text=video_name, element_name=self.schedules_input().name, clear=True, ignore_error=False)
            # time.sleep(5)

            # # 检测视频名称是否可见
            # self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.video_name_span(video_name=video_name), ignore_error=False)
            # if self.get_variable(self.video_name_span(video_name=video_name).name, None) is None:
            #     raise BusinessError(f"视频名称不可见", data={"onestream_account": onestream_account, "video_name": video_name})
            # self.find_element_instruction(context=context, element=self.schedule_item_container(), ignore_error=False)
            # self.find_element_instruction(context=context, element=self.schedule_item_buttons_container(), ignore_error=False)

            # time.sleep(2)

            # # 检测是否在准备中, 如果找到 stop_button_container, 则代表准备完成
            # for i in range(12):
            #     # 检测停止按钮是否可见
            #     self.wait_instruction(context=context, wait_type="wait_element_visible", element=self.stop_button_container(), timeout=5, ignore_error=True)
            #     if self.get_variable(self.stop_button_container().name, None) is not None:
            #         break

            time.sleep(7)

            # 关闭标签页
            self.close_tab_command(context=context, ignore_error=False)

            self.set_variable(key='tab_id', value=-1)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_video_stream_step", context=context)
            
        except Exception as e:
            try:
                if self.get_variable('tab_id', -1) != -1:
                    self.close_tab_command(context=context, ignore_error=False)
            except Exception as e:
                pass

            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="create_video_stream_step", context=context)

    # end ---------------------------步骤执行模块---------------------------------------------


class Bit(WebSite):
    """
    Bit浏览器类
    """
    # 类级别的锁，用于控制所有Bit实例的browser_open_step方法执行频率
    _open_step_lock = threading.Lock()
    # 记录上次执行browser_open_step的时间戳
    _last_open_step_time = None
    # 最小执行间隔（秒）
    _min_open_step_interval = 15

    def __init__(self, browser: Browser):
        super().__init__(browser=browser, domain="bitbrowser.cn")

        self.name = "bitbrowser"
        self.home_url = "https://console.bitbrowser.net"
        self.login_url = "https://console.bitbrowser.net/login"

        # 浏览器ID，默认为None表示未设置
        self.variables['browser_id'] = None
        # 浏览器序号，默认为None表示未设置
        self.variables['browser_seq'] = None

    # begin ---------------------------步骤执行模块---------------------------------------------

    def browser_open_step(self, context: Context, browser_seq: int, args: list = []) -> StepResult:
        """
        Bit浏览器打开步骤
        
        功能说明：
        通过浏览器序号打开指定的BitBrowser浏览器实例。
        该步骤会自动查询浏览器列表，找到匹配的浏览器ID，然后执行打开操作。
        注意：该方法具有全局限流机制，确保所有Bit实例之间执行间隔至少30秒。
        
        Args:
            context (Context): 上下文对象
            browser_seq (int): 浏览器序号，用于查找对应的浏览器ID
            args (list, optional): 浏览器启动参数列表，默认为空列表
        
        Returns:
            dict: HTTP命令执行结果，包含浏览器连接信息（ws、http、seq等）
        """
        # 获取类级别的锁，确保所有Bit实例串行执行
        Bit._open_step_lock.acquire()
        try:
            # 检查距离上次执行的时间间隔
            current_time = time.time()
            if Bit._last_open_step_time is not None:
                elapsed_time = current_time - Bit._last_open_step_time
                if elapsed_time < Bit._min_open_step_interval:
                    # 需要等待的时间
                    wait_time = Bit._min_open_step_interval - elapsed_time
                    time.sleep(wait_time)
                    current_time = time.time()  # 更新当前时间
            
            # 更新最后执行时间
            Bit._last_open_step_time = current_time
        finally:
            # 释放锁，允许下一个实例执行
            Bit._open_step_lock.release()
        
        try:
            # 先查询浏览器列表，查找匹配的浏览器ID
            list_result = self.bit_browser_list_command(context=context, browser_seq=browser_seq, timeout=180, ignoreError=False)
            browser_id = list_result.get('browser_id')
            
            if not browser_id:
                raise BusinessError(data={"url": self.browser.node_api_base_url, "browser_seq": browser_seq})

            # 查询浏览器是否存活
            alive_result = self.bit_browser_alive_command(context=context, browser_id=browser_id, timeout=180, ignoreError=False)

            if alive_result.get('pid', None):
                raise BusinessError(f"浏览器已存在: {browser_id}", data={"browser_id": browser_id, "pid": alive_result.get('pid')})

            # 调用打开命令
            result = self.bit_browser_open_command(context=context, browser_id=browser_id, args=args, queue=True, timeout=180, ignoreError=False)

            if not result.get('success'):
                raise BusinessError(f"浏览器打开失败: {result.get('msg', '')}", data={"browser_id": browser_id, "error": result.get('msg')})

            time.sleep(10)

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="bit_browser_open_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="bit_browser_open_step", context=context)


    def browser_close_step(self, context: Context, browser_seq: int) -> StepResult:
        """
        Bit浏览器关闭步骤
        
        功能说明：
        通过浏览器序号关闭指定的BitBrowser浏览器实例。
        该步骤会自动查询浏览器列表，找到匹配的浏览器ID，然后执行关闭操作。
        
        Args:
            context (Context): 上下文对象
            browser_seq (int): 浏览器序号，用于查找对应的浏览器ID
        
        Returns:
            dict: HTTP命令执行结果，包含关闭操作的结果数据
        """
        try:
            # 先查询浏览器列表，查找匹配的浏览器ID
            list_result = self.bit_browser_list_command(context=context, browser_seq=browser_seq, timeout=180, ignoreError=False)
            browser_id = list_result.get('browser_id')
            
            if not browser_id:
                raise BusinessError(
                    f"浏览器序号不存在: {browser_seq}",
                    data={"url": self.browser.node_api_base_url, "browser_seq": browser_seq}
                )
            
            # 调用关闭命令
            result = self.bit_browser_close_command(context=context, browser_id=browser_id, timeout=180, ignoreError=False)
            
            if not result.get('success'):
                raise BusinessError(f"浏览器关闭失败: {result.get('msg', '')}", data={"browser_id": browser_id, "error": result.get('msg')})
        
            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="bit_browser_close_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="bit_browser_close_step", context=context)


    def browser_reset_step(self, context: Context, browser_seq: int) -> StepResult:
        """
        Bit浏览器重置步骤
        
        功能说明：
        通过浏览器序号重置指定的BitBrowser浏览器实例。
        该步骤会自动查询浏览器列表，找到匹配的浏览器ID，然后执行重置操作。
        
        Args:
            context (Context): 上下文对象
            browser_seq (int): 浏览器序号，用于查找对应的浏览器ID
        
        Returns:
            dict: HTTP命令执行结果，包含重置操作的结果数据
        """
        try:
            # 先查询浏览器列表，查找匹配的浏览器ID
            list_result = self.bit_browser_list_command(context=context, browser_seq=browser_seq, timeout=180, ignoreError=False)
            browser_id = list_result.get('browser_id')
            
            if not browser_id:
                raise BusinessError(f"浏览器序号不存在: {browser_seq}", data={"url": self.browser.node_api_base_url, "browser_seq": browser_seq})
            
            # 调用重置命令
            result = self.bit_browser_reset_command(context=context, browser_id=browser_id, timeout=180, ignoreError=False)

            if not result.get('success'):
                raise BusinessError(f"浏览器重置失败: {result.get('msg', '')}", data={"browser_id": browser_id, "error": result.get('msg')})

            # ========== 成功完成 ==========
            context.set_var('success', True)
            return StepResult(success=True, error=None, error_type=None, error_stage="完成", context=context)

        except (NetworkError, ParseError, BusinessError) as e:
            # 捕获所有自定义异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="bit_browser_reset_step", context=context)
            
        except Exception as e:
            # 捕获所有其他未知异常
            context.set_var('success', False)
            return StepResult(success=False, error=e, error_type=type(e).__name__, error_stage="bit_browser_reset_step", context=context)

    # end   ---------------------------步骤执行模块---------------------------------------------


def onestream_clear_all_social_accounts_step(context: Context, onestream_account: str, onestream_password: str, node_name_onestream: str, node_api_base_url: str, auth_token: str) -> StepResult:
    """
    Onestream清除所有社交平台步骤函数
    
    功能说明：
    这是一个工作流步骤函数，用于在Onestream平台上清除所有已连接的社交平台账号。
    该函数会创建Browser对象和Onestream网站对象，然后执行清除所有社交平台的步骤。
    
    工作流程：
    1. 创建Browser对象（连接到浏览器节点API）
    2. 创建Onestream网站对象（封装Onestream操作）
    3. 登录Onestream（如果需要）
    4. 导航到社交平台管理页面
    5. 全选所有社交平台账号
    6. 点击断开连接按钮
    7. 确认断开操作
    8. 返回步骤执行结果
    
    Args:
        context (Context): 工作流执行上下文，用于传递状态和变量
        onestream_account (str): Onestream账号（邮箱）
        onestream_password (str): Onestream密码
        node_name_onestream (str): Onestream节点名称，用于创建Browser对象
        node_api_base_url (str): 节点API基础URL，如 "https://browser.autowave.dev/api"
        auth_token (str): 节点认证Token，用于API请求认证
    
    Returns:
        StepResult: 步骤执行结果对象，包含：
            - success: 是否成功清除所有社交平台
            - error: 错误对象（如果失败）
            - error_type: 错误类型
            - error_stage: 错误阶段
            - context: 更新后的上下文对象
    
    Note:
        - 此操作会断开所有已连接的社交平台账号
        - 需要确保已登录Onestream账号
    
    Example:
        context = Context()
        result = onestream_clear_all_social_accounts_step(
            context=context,
            onestream_account="user@example.com",
            onestream_password="password123",
            node_name_onestream="local",
            node_api_base_url="https://browser.autowave.dev/api",
            auth_token="node_token_qwer2wsx"
        )
        if result.success:
            print("所有社交平台已清除")
    """
    onestream = Onestream(browser=Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_onestream, timeout=180))
    result = onestream.clear_all_social_accounts_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password)
    return result


# ============================================================================
# 延迟执行队列系统 - 用于延迟删除社交账号
# ============================================================================

# 全局延迟删除队列（优先队列，按执行时间排序）
_delayed_delete_queue = []
_delayed_delete_queue_lock = threading.Lock()
_delayed_delete_worker_thread = None
_delayed_delete_worker_running = False

# 延迟时间（秒）：46分钟
DELAY_DELETE_SECONDS = 46 * 60


def _delayed_delete_worker():
    """
    延迟删除队列的后台工作线程（单线程）
    
    功能说明：
    使用一个工作线程定期检查队列中的任务，对于超过46分钟的任务执行删除操作。
    使用优先队列按执行时间排序，确保高效处理大量任务。
    
    工作流程：
    1. 从优先队列中取出执行时间最早的任务
    2. 检查当前时间是否已经超过任务的执行时间
    3. 如果超过，执行删除操作并移除任务
    4. 如果未超过，等待到执行时间或等待新任务加入
    5. 重复上述过程
    """
    global _delayed_delete_worker_running
    
    _delayed_delete_worker_running = True
    Logger.info("[延迟删除队列] 后台工作线程已启动")
    
    while _delayed_delete_worker_running:
        try:
            tasks_to_execute = []
            
            # 在锁内收集所有到期的任务
            with _delayed_delete_queue_lock:
                current_time = time.time()
                
                # 处理所有到期的任务
                while _delayed_delete_queue:
                    # 获取执行时间最早的任务（堆顶）
                    execute_time, task = _delayed_delete_queue[0]
                    
                    # 如果任务还没到执行时间，跳出循环
                    if execute_time > current_time:
                        break
                    
                    # 移除已到期的任务
                    heapq.heappop(_delayed_delete_queue)
                    tasks_to_execute.append(task)
                
                # 如果队列为空，等待一段时间后继续检查
                if not _delayed_delete_queue:
                    wait_time = 60  # 队列为空时，等待60秒后再次检查
                else:
                    # 计算下一个任务的等待时间
                    next_execute_time, _ = _delayed_delete_queue[0]
                    wait_time = max(1, min(60, next_execute_time - current_time))
                    # 如果下一个任务执行时间很近（小于60秒），等待到执行时间
                    # 如果下一个任务执行时间很远（大于60秒），等待60秒后再次检查（避免等待过久）
            
            # 在锁外执行删除操作，避免长时间持有锁
            for task in tasks_to_execute:
                _execute_delete_task(task)
            
            # 等待一段时间后继续检查
            time.sleep(wait_time)
            
        except Exception as e:
            Logger.info(f"[延迟删除队列] 工作线程异常: {str(e)}")
            time.sleep(5)  # 发生异常时等待5秒后重试
    
    Logger.info("[延迟删除队列] 后台工作线程已停止")


def _execute_delete_task(task: dict):
    """
    执行删除任务（在工作线程中直接执行）
    
    Args:
        task (dict): 任务字典，包含执行删除所需的所有参数
    """
    try:
        live_social_account = task.get('live_social_account')
        enqueue_time = task.get('enqueue_time', 0)
        elapsed_time = time.time() - enqueue_time
        
        Logger.info(f"[延迟删除] 开始执行删除操作: live_social_account={live_social_account}, 已等待 {elapsed_time:.1f} 秒")
        
        result = onestream_delete_social_account_step(
            context=task.get('context'),
            onestream_account=task.get('onestream_account'),
            onestream_password=task.get('onestream_password'),
            live_social_account=live_social_account,
            node_name_onestream=task.get('node_name_onestream'),
            node_api_base_url=task.get('node_api_base_url', 'https://browser.autowave.dev/api'),
            auth_token=task.get('auth_token', 'node_token_qwer2wsx')
        )
        
        if result.success:
            Logger.info(f"[延迟删除] 删除成功: live_social_account={live_social_account}")
        else:
            Logger.info(f"[延迟删除] 删除失败: live_social_account={live_social_account}, error={result.error}")
    except Exception as e:
        Logger.info(f"[延迟删除] 删除操作异常: live_social_account={task.get('live_social_account', 'unknown')}, error={str(e)}")


def _start_delayed_delete_worker():
    """
    启动延迟删除队列的后台工作线程
    
    功能说明：
    如果工作线程未启动，则创建并启动一个新的后台线程来处理延迟删除任务。
    使用线程锁确保只启动一个工作线程。
    注意：使用非daemon线程，确保程序退出前所有任务都能完成。
    """
    global _delayed_delete_worker_thread, _delayed_delete_worker_running
    
    if _delayed_delete_worker_thread is None or not _delayed_delete_worker_thread.is_alive():
        _delayed_delete_worker_running = False  # 确保旧线程停止
        # 使用非daemon线程，确保程序退出前所有任务都能完成
        _delayed_delete_worker_thread = threading.Thread(target=_delayed_delete_worker, daemon=False)
        _delayed_delete_worker_thread.start()


def wait_for_all_delayed_delete_tasks_complete(timeout: float = None):
    """
    等待所有延迟删除任务执行完成
    
    功能说明：
    阻塞当前线程，直到所有延迟删除任务都执行完成。
    如果指定了timeout，会在超时后返回，但不会停止工作线程。
    
    Args:
        timeout (float|None): 可选，超时时间（秒）。如果为None，会一直等待直到所有任务完成。
    
    Returns:
        bool: 如果所有任务都完成返回True，如果超时返回False
    
    Note:
        - 此函数会阻塞当前线程
        - 会定期检查队列状态，显示进度信息
        - 如果指定了timeout，超时后函数会返回，但工作线程会继续运行
        - 队列为空后，会等待一段时间确保没有新任务加入
    """
    global _delayed_delete_worker_thread, _delayed_delete_worker_running
    
    if _delayed_delete_worker_thread is None or not _delayed_delete_worker_thread.is_alive():
        Logger.info("[延迟删除队列] 工作线程未运行，无需等待")
        return True
    
    Logger.info("[延迟删除队列] 开始等待所有延迟删除任务完成...")
    start_time = time.time()
    empty_queue_count = 0  # 连续空队列次数
    
    while True:
        with _delayed_delete_queue_lock:
            queue_size = len(_delayed_delete_queue)
            
            if queue_size == 0:
                empty_queue_count += 1
                # 如果队列连续3次检查都为空（约30秒），认为所有任务已完成
                if empty_queue_count >= 3:
                    Logger.info("[延迟删除队列] 队列已连续为空，所有延迟删除任务已完成")
                    return True
            else:
                empty_queue_count = 0  # 重置计数器
                # 显示队列中最早任务的执行时间
                if _delayed_delete_queue:
                    next_execute_time, _ = _delayed_delete_queue[0]
                    current_time = time.time()
                    remaining_time = next_execute_time - current_time
                    Logger.info(f"[延迟删除队列] 等待中... 队列中还有 {queue_size} 个任务，最早任务还需等待 {remaining_time/60:.1f} 分钟")
        
        # 检查超时
        if timeout is not None:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                Logger.info(f"[延迟删除队列] 等待超时（{timeout}秒），仍有 {queue_size} 个任务未完成")
                return False
        
        # 等待10秒后再次检查
        time.sleep(10)


def stop_delayed_delete_worker():
    """
    停止延迟删除队列的工作线程
    
    功能说明：
    设置停止标志，等待工作线程完成当前任务后退出。
    注意：此函数不会等待队列中的所有任务完成，只是停止工作线程。
    如果需要等待所有任务完成，请先调用 wait_for_all_delayed_delete_tasks_complete()。
    """
    global _delayed_delete_worker_running, _delayed_delete_worker_thread
    
    if _delayed_delete_worker_thread is None or not _delayed_delete_worker_thread.is_alive():
        Logger.info("[延迟删除队列] 工作线程未运行，无需停止")
        return
    
    Logger.info("[延迟删除队列] 正在停止工作线程...")
    _delayed_delete_worker_running = False
    
    # 等待工作线程退出
    if _delayed_delete_worker_thread.is_alive():
        _delayed_delete_worker_thread.join(timeout=10)
        if _delayed_delete_worker_thread.is_alive():
            Logger.info("[延迟删除队列] 工作线程未能在10秒内退出")
        else:
            Logger.info("[延迟删除队列] 工作线程已停止")


def enqueue_delayed_delete(
    context: Context,
    onestream_account: str,
    onestream_password: str,
    live_social_account: str,
    node_name_onestream: str,
    node_api_base_url: str = 'https://browser.autowave.dev/api',
    auth_token: str = 'node_token_qwer2wsx'
):
    """
    将删除社交账号任务加入延迟执行队列
    
    功能说明：
    将删除社交账号的任务加入优先队列，记录入队时间，计算执行时间（入队时间 + 46分钟）。
    后台工作线程会定期检查队列，对于超过46分钟的任务执行删除操作。
    
    Args:
        context (Context): 工作流执行上下文
        onestream_account (str): Onestream账号（邮箱）
        onestream_password (str): Onestream密码
        live_social_account (str): 直播社交平台账号名称
        node_name_onestream (str): Onestream节点名称
        node_api_base_url (str): 节点API基础URL，默认为 'https://browser.autowave.dev/api'
        auth_token (str): 节点认证Token，默认为 'node_token_qwer2wsx'
    
    Note:
        - 使用单个工作线程处理所有任务，支持上万个任务
        - 每个任务记录入队时间，在入队后46分钟执行删除
        - 使用优先队列按执行时间排序，高效处理大量任务
        - 不会阻塞当前流程，异步执行
    """
    # 确保工作线程已启动
    _start_delayed_delete_worker()
    
    # 记录入队时间
    enqueue_time = time.time()
    execute_time = enqueue_time + DELAY_DELETE_SECONDS
    
    # 创建任务字典
    task = {
        'context': context,
        'onestream_account': onestream_account,
        'onestream_password': onestream_password,
        'live_social_account': live_social_account,
        'node_name_onestream': node_name_onestream,
        'node_api_base_url': node_api_base_url,
        'auth_token': auth_token,
        'enqueue_time': enqueue_time
    }
    
    # 将任务加入优先队列（按执行时间排序）
    with _delayed_delete_queue_lock:
        heapq.heappush(_delayed_delete_queue, (execute_time, task))
    
    Logger.info(f"[延迟删除队列] 任务已入队: live_social_account={live_social_account}, 入队时间={enqueue_time:.0f}, 执行时间={execute_time:.0f} (46分钟后), 队列大小={len(_delayed_delete_queue)}")


def onestream_delete_social_account_step(context: Context, onestream_account: str, onestream_password: str, live_social_account: str, node_name_onestream: str, node_api_base_url: str, auth_token: str) -> StepResult:
    """
    Onestream删除社交账号步骤函数
    """
    onestream = Onestream(browser=Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_onestream, timeout=180))
    result = onestream.delete_social_account_step(context=context, onestream_account=onestream_account, onestream_password=onestream_password, live_social_account=live_social_account)
    return result


def workflow(
    context: Context, 
    node_name_facebook: str, 
    onestream_account: str, 
    onestream_password: str, 
    live_social_account: str, 
    video_name: str, 
    node_name_onestream: str, 
    post_title: str = None, 
    post_description: str = None, 
    node_api_base_url: str = 'https://browser.autowave.dev/api', 
    auth_token: str = 'node_token_qwer2wsx'
) -> (StepResult, str | None):
    """
    完整工作流函数 - Facebook直播自动化流程
    
    功能说明：
    这是一个完整的工作流函数，实现了从打开浏览器到开始Facebook直播的完整自动化流程。
    该函数直接创建Browser对象和网站对象（Bit、Facebook、Onestream），并调用它们的步骤方法实现自动化任务。
    
    工作流程：
    1. 打开Facebook节点浏览器（通过浏览器序号）
    2. 获取Facebook直播推流密钥（创建直播推流）
    3. 创建Onestream社交账号直播密钥（将推流密钥配置到Onestream）
    4. 创建Onestream视频流（选择视频并开始推流）
    5. 点击Facebook开始直播按钮（启动直播）
    6. 等待15秒（确保直播已启动）
    7. 关闭Facebook节点浏览器
    8. 返回工作流执行结果
    
    错误处理：
    - 如果任何步骤失败，会记录错误日志
    - 如果步骤失败，会尝试关闭浏览器（清理资源）
    - 返回详细的错误信息和执行结果
    
    Args:
        context (Context): 工作流执行上下文，用于传递状态和变量
        node_name_facebook (str): Facebook节点名称（实际上是浏览器序号，会被转换为int）
        onestream_account (str): Onestream账号（邮箱）
        onestream_password (str): Onestream密码
        live_social_account (str): 直播社交平台账号名称，如 "Facebook Page Name"
        video_name (str): 视频名称，用于在Onestream中选择要直播的视频
        node_name_onestream (str): Onestream节点名称（实际上是浏览器序号）
        post_title (str|None): 可选，Facebook直播标题
        post_description (str|None): 可选，Facebook直播描述
        node_api_base_url (str): 节点API基础URL，默认为 "https://browser.autowave.dev/api"
        auth_token (str): 节点认证Token，默认为 "node_token_qwer2wsx"
    
    Returns:
        dict: 工作流执行结果字典，格式为：
            {
                "success": bool,      # 是否成功完成整个工作流
                "error": str|None,    # 错误信息（如果失败）
                "error_type": str|None,  # 错误类型
                "error_stage": str|None, # 错误阶段
                "context": dict       # 上下文变量字典
            }
    
    Note:
        - node_name_facebook和node_name_onestream实际上是浏览器序号（整数），会被转换为int
        - 推流密钥会在步骤之间通过context传递
        - 如果任何步骤失败，会立即返回错误结果，不会继续执行后续步骤
    
    Example:
        context = Context()
        result = workflow(
            context=context,
            node_name_facebook="55391",
            onestream_account="user@example.com",
            onestream_password="password123",
            live_social_account="My Facebook Page",
            video_name="my_video.mp4",
            node_name_onestream="55195",
            post_title="我的直播",
            post_description="这是一个测试直播"
        )
        if result.get('success'):
            print("工作流执行成功")
        else:
            print(f"工作流执行失败: {result.get('error')}")
    """

    bit = Bit(browser=Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_onestream, timeout=180))

    # 打开facebook节点浏览器
    result = bit.browser_open_step(context=context, browser_seq=int(node_name_facebook), args=[])
    if not result.success:
        return result, None

    facebook = Facebook(browser=Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_facebook, timeout=180))

    # 获取Facebook直播推流密钥
    result = facebook.live_stream_step(context=context)
    if not result.success:
        return result, node_name_facebook

    
    onestream = Onestream(
        browser=Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_onestream, timeout=180), 
        onestream_account=onestream_account, 
        onestream_password=onestream_password, 
        live_social_account=live_social_account, 
        video_name=video_name,
    )

    # 创建Onestream社交账号直播密钥
    result = onestream.create_social_account_stream_key_step(
        context=context, 
        onestream_account=onestream_account, 
        onestream_password=onestream_password, 
        live_social_account=live_social_account,
    )
    if not result.success:
        return result, node_name_facebook

    # 创建Onestream视频流
    result = onestream.create_video_stream_step(
        context=context, 
        onestream_account=onestream_account, 
        onestream_password=onestream_password, 
        live_social_account=live_social_account, 
        video_name=video_name
    )
    if not result.success:
        return result, node_name_facebook

    # 点击Facebook直播按钮
    result = facebook.go_live_step(context=context, post_title=post_title, post_description=post_description)

    return result, node_name_facebook


def read_xlsx_file(file_path: str) -> List[dict]:
    """
    读取Excel文件并返回所有数据
    
    功能说明：
    读取Excel文件（.xlsx格式），将每一行数据转换为字典格式，并返回所有行的列表。
    每个字典的键为列名，值为对应的单元格值。会自动添加'_row_index'字段表示行索引。
    
    必需列检查：
    函数会检查Excel文件是否包含以下必需列：
    - node_name_facebook: Facebook节点名称（浏览器序号）
    - live_social_account: 直播社交平台账号
    - video_name: 视频名称
    - post_title: 直播标题
    - post_description: 直播描述
    
    如果缺少任何必需列，会抛出ValueError异常。
    
    Args:
        file_path (str): Excel文件路径，如 "./data.xlsx"
        
    Returns:
        List[dict]: 所有行的数据列表，每个元素是一个字典，格式为：
            {
                "node_name_facebook": str,    # Facebook节点名称
                "live_social_account": str,   # 直播社交平台账号
                "video_name": str,            # 视频名称
                "post_title": str,            # 直播标题
                "post_description": str,      # 直播描述
                "_row_index": int,           # 行索引（从0开始）
                ...  # 其他列的数据
            }
    
    Raises:
        ValueError: 如果Excel文件缺少必需的列
    
    Example:
        rows_data = read_xlsx_file("./data.xlsx")
        for row in rows_data:
            print(f"行 {row['_row_index']}: {row['video_name']}")
    """
    df = pd.read_excel(file_path)
    
    # 定义需要的列名
    required_columns = ['node_name_facebook', 'live_social_account', 'video_name', 'post_title', 'post_description']
    
    # 检查列是否存在
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Excel文件 {file_path} 缺少必需的列: {missing_columns}")
    
    # 遍历每一行，将行数据转换为字典并添加到列表
    rows_data = []
    for index, row in df.iterrows():
        # 将Series转换为字典，并添加行索引
        row_dict = row.to_dict()
        row_dict['_row_index'] = index
        rows_data.append(row_dict)
    
    return rows_data


def write_xlsx_file(file_path: str, data: List[dict]) -> None:
    """
    将数据写入Excel文件
    
    功能说明：
    将字典列表数据写入Excel文件（.xlsx格式）。每个字典代表一行数据，
    字典的键作为列名，值作为对应的单元格值。如果数据中包含'_row_index'字段，
    该字段会被排除，不会写入Excel文件（因为它是内部使用的行索引）。
    
    Args:
        file_path (str): Excel文件路径，如 "./error.xlsx"
        data (List[dict]): 要写入的数据列表，每个元素是一个字典，格式为：
            {
                "node_name_facebook": str,    # Facebook节点名称
                "live_social_account": str,   # 直播社交平台账号
                "video_name": str,            # 视频名称
                "post_title": str,            # 直播标题
                "post_description": str,      # 直播描述
                ...  # 其他列的数据
            }
    
    Raises:
        ValueError: 如果数据列表为空
        Exception: 如果写入文件时发生错误
    
    Example:
        error_rows = [
            {
                "node_name_facebook": "1",
                "live_social_account": "test@example.com",
                "video_name": "test_video",
                "post_title": "Test Title",
                "post_description": "Test Description"
            }
        ]
        write_xlsx_file(file_path='./error.xlsx', data=error_rows)
    """
    if not data:
        raise ValueError("数据列表不能为空")
    
    # 将字典列表转换为DataFrame
    # 排除 '_row_index' 字段（如果存在），因为它是内部使用的行索引
    cleaned_data = []
    for row_dict in data:
        cleaned_row = {k: v for k, v in row_dict.items() if k != '_row_index'}
        cleaned_data.append(cleaned_row)
    
    df = pd.DataFrame(cleaned_data)
    
    # 写入Excel文件
    # 使用 index=False 避免写入行索引
    # 使用 engine='openpyxl' 确保写入 .xlsx 格式
    try:
        df.to_excel(file_path, index=False, engine='openpyxl')
        Logger.info(f"成功写入 {len(data)} 行数据到文件: {file_path}")
    except ImportError:
        # 如果 openpyxl 未安装，尝试使用默认引擎
        Logger.info("openpyxl 未安装，尝试使用默认引擎写入Excel文件")
        df.to_excel(file_path, index=False)
        Logger.info(f"成功写入 {len(data)} 行数据到文件: {file_path}")
    except Exception as e:
        Logger.error(f"写入Excel文件失败: {str(e)}")
        raise


def main(onestream_account: str = None, onestream_password: str = None, node_name_onestream: str = None, thread: int = None, file_path: str = None, clear_all_social_accounts: bool = True) -> dict:
    """
    主函数 - 批量执行工作流
    
    功能说明：
    这是程序的主入口函数，用于批量执行工作流。函数会读取Excel文件中的任务数据，
    然后使用单线程或多线程方式执行工作流。支持从命令行参数或Excel文件中读取配置。
    
    工作流程：
    1. 创建Onestream上下文
    2. 执行Onestream清除所有社交平台步骤（清理环境）
    3. 读取Excel文件，获取所有任务数据
    4. 根据thread参数决定使用单线程或多线程执行
    5. 对每一行数据执行workflow函数
    6. 收集所有执行结果
    7. 返回汇总结果
    
    参数优先级：
    - 如果命令行参数提供了值（如onestream_account），优先使用命令行参数
    - 如果命令行参数未提供，使用Excel文件中的值
    
    线程执行：
    - 如果thread=1或未指定，使用单线程顺序执行（保持原有逻辑）
    - 如果thread>1，使用ThreadPoolExecutor并发执行
    - 多线程执行时，结果会按行索引排序，保持原始顺序
    
    Args:
        onestream_account (str|None): 可选，Onestream账号（邮箱）。如果提供，会覆盖Excel中的值
        onestream_password (str|None): 可选，Onestream密码。如果提供，会覆盖Excel中的值
        node_name_onestream (str|None): 可选，Onestream节点名称。如果提供，会覆盖Excel中的值
        thread (int|None): 可选，线程数，用于并发执行任务。默认为None（单线程）
        file_path (str|None): 可选，Excel文件路径。默认为None
    
    Returns:
        dict: 批量执行结果字典，格式为：
            {
                "total_rows": int,      # 总任务数
                "threads_used": int,    # 使用的线程数
                "results": [            # 执行结果列表
                    {
                        "row_index": int,    # 行索引
                        "success": bool,     # 是否成功
                        "result": dict       # workflow函数的返回结果
                    },
                    ...
                ]
            }
    
    Note:
        - Excel文件必须包含必需的列（见read_xlsx_file函数说明）
        - 如果Excel文件读取失败，会返回错误结果
        - 如果Excel文件为空，会返回错误结果
        - 多线程执行时，每个任务使用独立的Context对象
    
    Example:
        # 单线程执行
        result = main(
            onestream_account="user@example.com",
            onestream_password="password123",
            node_name_onestream="55195",
            thread=1,
            file_path="./data.xlsx"
        )
        
        # 多线程执行（使用4个线程）
        result = main(
            thread=4,
            file_path="./data.xlsx"
        )
        
        print(f"总任务数: {result['total_rows']}")
        print(f"使用线程数: {result['threads_used']}")
        for item in result['results']:
            if item['success']:
                print(f"行 {item['row_index']}: 成功")
            else:
                print(f"行 {item['row_index']}: 失败")
    """
    
    node_api_base_url = 'https://browser.autowave.dev/api'
    auth_token = 'node_token_qwer2wsx'

    if clear_all_social_accounts:
        # 创建Onestream上下文
        onestream_context = Context()
        result = onestream_clear_all_social_accounts_step(context=onestream_context, onestream_account=onestream_account, onestream_password=onestream_password, node_name_onestream=node_name_onestream, node_api_base_url=node_api_base_url, auth_token=auth_token)        
        if not result.success:
            return {'success': False, 'message': 'Onestream清除所有社交平台失败', 'node_name_onestream': node_name_onestream, 'onestream_account': onestream_account, 'onestream_password': onestream_password}
        
    # 使用 read_xlsx_file 函数读取数据
    try:
        rows_data = read_xlsx_file(file_path)
        total_rows = len(rows_data)
    except Exception as e:
        return {'success': False, 'message': f'读取Excel文件失败: {str(e)}'}
    
    if total_rows == 0:
        return {'success': False, 'message': 'Excel文件中没有数据'}
    
    # 存储所有结果
    results = []

    # 存储因为执行错误需要保存到error.xlsx的row_dict
    error_rows = []

    # 定义处理单行数据的函数
    def process_row(row_dict: dict) -> dict:
        """处理单行数据的函数，用于多线程执行"""
        index = row_dict.get('_row_index', 0)
        context = Context()

        # 设置线程编号到context
        context.set_var('线程编号', index)
        
        # 从字典中获取数据，如果命令行参数提供了值，优先使用命令行参数
        node_name_facebook = str(row_dict.get('node_name_facebook', ''))
        live_social_account = str(row_dict.get('live_social_account', ''))
        video_name = str(row_dict.get('video_name', ''))
        post_title = str(row_dict.get('post_title', ''))
        post_description = str(row_dict.get('post_description', ''))

        context.set_var('log_facebook_node_name', node_name_facebook)
        context.set_var('log_onestream_account', onestream_account)
        
        # 如果命令行参数提供了值，优先使用命令行参数，否则使用Excel中的值
        current_node_name_onestream = node_name_onestream if node_name_onestream else str(row_dict.get('node_name_onestream', ''))
        current_onestream_account = onestream_account if onestream_account else str(row_dict.get('onestream_account', ''))
        current_onestream_password = onestream_password if onestream_password else str(row_dict.get('onestream_password', ''))
        
        Logger.info(f"[线程 {index}] 开始执行: node_name_facebook: {node_name_facebook}, node_name_onestream: {current_node_name_onestream}, onestream_account: {current_onestream_account}, onestream_password: {current_onestream_password}, live_social_account: {live_social_account}, video_name: {video_name}")
        
        # 调用workflow
        result, node_close = workflow(
            context=context, 
            node_name_facebook=node_name_facebook, 
            node_name_onestream=current_node_name_onestream, 
            onestream_account=current_onestream_account, 
            onestream_password=current_onestream_password, 
            live_social_account=live_social_account, 
            video_name=video_name, 
            post_title=post_title, 
            post_description=post_description,
            node_api_base_url=node_api_base_url,
            auth_token=auth_token
        )

        # 将删除社交账号任务加入延迟执行队列（46分钟后执行）
        try:
            enqueue_delayed_delete(
                context=Context(),
                onestream_account=current_onestream_account,
                onestream_password=current_onestream_password,
                live_social_account=live_social_account,
                node_name_onestream=current_node_name_onestream,
                node_api_base_url=node_api_base_url,
                auth_token=auth_token
            )
        except Exception as e:
            # 入队失败不影响主流程，只记录日志
            Logger.info(f"[workflow] 延迟删除任务入队失败: {str(e)}")

        try:
            if node_close:
                time.sleep(5)
                bit = Bit(browser=Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=current_node_name_onestream, timeout=180))
                bit.browser_close_step(context=context, browser_seq=int(node_close))
        except Exception as e:
            Logger.info(f"[线程 {index}] 关闭facebook节点浏览器失败: {str(e)}")

        Logger.info(message=result.to_dict())

        FileLogger.write_log("INFO", f"{node_name_facebook} {video_name} {live_social_account} {result.to_dict()}")

        if not result.success:
            error_rows.append(row_dict)

        return {'row_index': index, 'result': result.to_dict(), 'success': result.success}
    
    # 确定线程数，默认为1（单线程）
    max_workers = thread if thread and thread > 0 else 1
    
    # 使用线程池并发执行
    if max_workers == 1:
        # 单线程执行（保持原有逻辑）
        for row_dict in rows_data:
            result = process_row(row_dict)
            results.append(result)
    else:
        # 多线程执行
        Logger.info(f"使用 {max_workers} 个线程并发执行任务")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_row = {executor.submit(process_row, row_dict): row_dict for row_dict in rows_data}
            
            # 收集结果（按完成顺序）
            for future in as_completed(future_to_row):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    row_dict = future_to_row[future]
                    row_index = row_dict.get('_row_index', 0)
                    Logger.info(f"[线程 {row_index}] 任务执行异常: {str(e)}")
                    results.append({'row_index': row_index, 'result': {'success': False, 'error': str(e)}, 'success': False})
        
        # 按行索引排序结果，保持原始顺序
        results.sort(key=lambda x: x['row_index'])
    
    if error_rows:
        write_xlsx_file(file_path='./error.xlsx', data=error_rows)

    return {'total_rows': total_rows, 'results': results, 'threads_used': max_workers}


if __name__ == "__main__":
    # 设置Python输出为无缓冲模式，确保输出立即显示（解决Windows控制台需要按Enter的问题）
    import sys
    import os
    # 设置环境变量，使Python使用无缓冲输出
    os.environ['PYTHONUNBUFFERED'] = '1'
    # 重新配置stdout和stderr为行缓冲模式
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
    
    Logger.enable()
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='AutoJS Python SDK - 自动化浏览器操作框架')
    parser.add_argument('-f', '--file_path', type=str, default='./data.xlsx', help='Excel文件路径')
    parser.add_argument('-a', '--onestream_account', type=str, default="", help='OneStream账号')
    parser.add_argument('-p', '--onestream_password', type=str, default="", help='OneStream密码')
    parser.add_argument('-n', '--node_name_onestream', type=str, default="", help='OneStream节点名称')
    parser.add_argument('-t', '--thread', type=int, default=2, help='线程数（用于并发执行）')
    parser.add_argument('-c', '--clear_all_social_accounts', type=bool, default=False, help='清除所有社交平台')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    print(args, flush=True)
    
    # 调用main函数并传递参数
    result = main(
        onestream_account=args.onestream_account,
        onestream_password=args.onestream_password,
        node_name_onestream=args.node_name_onestream,
        thread=args.thread,
        file_path=args.file_path,
        clear_all_social_accounts=args.clear_all_social_accounts
    )
    print(result, flush=True)

    # 等待所有延迟删除任务完成后再退出程序
    Logger.info("[主程序] 主工作流已完成，等待所有延迟删除任务完成...")
    wait_for_all_delayed_delete_tasks_complete()
    
    # 停止工作线程
    stop_delayed_delete_worker()
    
    Logger.info("[主程序] 所有任务已完成，程序退出")
    Logger.disable()