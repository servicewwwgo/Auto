"""
onestream.com 域实现

Domain 子类，封装 Onestream 站点相关的标签页与 CDP 操作。
"""

from AutoPy import Domain


class OnestreamDomain(Domain):
    """Onestream 站点域。参考 autojs.py 中 Onestream 类。"""

    HOME_URL = "https://app.onestream.live/"
    LOGIN_URL = "https://app.onestream.live/login/"

    def __init__(self, browser, node_name: str, **kwargs):
        kwargs.pop("domain", None)  # 避免与显式 domain="onestream.live" 冲突
        super().__init__(
            browser,
            node_name,
            domain="onestream.live",
            description=kwargs.pop("description", "Onestream"),
            language=kwargs.pop("language", "en-US"),
            start_url=kwargs.pop("start_url", self.HOME_URL),
            active=kwargs.pop("active", True),
            new_window=kwargs.pop("new_window", True),
            **kwargs,
        )
