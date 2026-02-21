"""
onestream.com 域实现

Domain 子类，封装 Onestream 站点相关的标签页与 CDP 操作。
"""

from AutoPy import Domain


class OnestreamDomain(Domain):
    """Onestream 站点域。"""

    def __init__(self, browser, node_name: str, **kwargs):
        super().__init__(
            browser,
            node_name,
            domain="onestream.com",
            description="Onestream",
            language=kwargs.pop("language", "en-US"),
            start_url=kwargs.pop("start_url", None),
            active=kwargs.pop("active", True),
            new_window=kwargs.pop("new_window", False),
            **kwargs,
        )
