"""
facebook.com 域实现

Domain 子类，封装 Facebook 站点相关的标签页与 CDP 操作。
"""

from AutoPy import Domain


class FacebookDomain(Domain):
    """Facebook 站点域。"""

    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description", "Facebook"),
            language=kwargs.pop("language", "en-US"),
            start_url=kwargs.pop("start_url", "https://www.facebook.com/"),
            active=kwargs.pop("active", True),
            new_window=kwargs.pop("new_window", False),
            **kwargs,
        )
 