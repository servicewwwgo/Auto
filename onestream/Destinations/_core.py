"""
onestream.live/Destinations 页面实现

Page 子类，表示 Onestream 目的地/社交平台管理页（侧栏或同应用内）。参考 autojs.py 中 Destinations 相关步骤。
"""

import json
from urllib.parse import urlparse

from AutoPy import Element, Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction
from AutoPy.page import PopupPage


class DestinationsPage(Page):
    """Onestream 目的地（社交平台）页。"""

    BASE_URL = "https://app.onestream.live/destinations"

    def __init__(self, **kwargs):
        kwargs.pop("url", None)
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """通过点击社交平台按钮进入 Destinations。"""
        from ..Home import HomePage
        from ..Home.social_platforms_button import SocialPlatformsButton
        home_page = HomePage.instance(browser=self._browser, node_name=self._node_name, domain=self.domain)
        social: Element = SocialPlatformsButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=home_page)
        if social.mouse(action="click"):
            return self.has_page_elements()
        return False

    def is_current_url(self) -> bool:
        """Destinations 与 Home 同域，通过当前 URL 判断是否在 /destinations。"""
        inst = GetUrlInstruction(tab_id=self.domain.tab_id)
        req = Instructions(node_name=self._node_name, instructions=[inst])
        resp = self._browser.request(req)
        try:
            body = resp.json()
        except json.JSONDecodeError:
            return False
        data = body.get("data") or {}
        results = data.get("results") or []
        if not results or not results[0].get("success"):
            return False
        url = (results[0].get("data") or {}).get("url") or results[0].get("value") or ""
        return self.BASE_URL in url.lower()

    def has_page_elements(self) -> bool:
        """判断是否存在 Destinations 页特有元素。"""
        from .add_social_platform import AddSocialPlatform
        add_btn: Element = AddSocialPlatform.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        return add_btn.wait()


class DisconnectAllSocialAccountPopupPage(PopupPage):
    """断开所有社交平台账号弹窗页。"""

    BASE_URL = "https://app.onestream.live/destinations"

    def __init__(self, **kwargs):
        kwargs.pop("url", None)
        super().__init__(url=self.BASE_URL, **kwargs)


    def go(self) -> bool:
        """通过点击断开所有社交平台账号按钮进入 DisconnectAllSocialAccountPopupPage。"""
        from .social_account_all_disconnect_button import SocialAccountAllDisconnectButton
        all_disconnect: Element = SocialAccountAllDisconnectButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        if all_disconnect.mouse(action="click"):
            return self.has_page_elements()
        return False

    def is_current_url(self) -> bool:
        """DisconnectAllSocialAccountPopupPage 与 Destinations 同域，通过当前 URL 判断是否在 /destinations/disconnect-all-social-accounts。"""
        raise NotImplementedError("DisconnectAllSocialAccountPopupPage 没有实现 is_current_url 方法")

    def has_page_elements(self) -> bool:
        """判断是否存在 DisconnectAllSocialAccountPopupPage 页特有元素。"""
        from .disconnect_confirm_button import DisconnectConfirmButton
        confirm_btn: Element = DisconnectConfirmButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        return confirm_btn.wait()

    def back(self) -> bool:
        """通过点击返回按钮返回 Destinations 页。"""
        from .disconnect_confirm_button import DisconnectConfirmButton
        back_btn: Element = DisconnectConfirmButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        if back_btn.mouse(action="click"):
            return True
        return False

class DisconnectSocialAccountPopupPage(PopupPage):

    BASE_URL = "https://app.onestream.live/destinations"

    def __init__(self, **kwargs):
        kwargs.pop("url", None)
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """通过点击断开社交平台账号按钮进入 DisconnectSocialAccountPopupPage。"""
        from .disconnect_button import DisconnectButton
        disconnect: Element = DisconnectButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        if disconnect.mouse(action="click"):
            return self.has_page_elements()
        return False

    def is_current_url(self) -> bool:
        """DisconnectSocialAccountPopupPage 与 Destinations 同域，通过当前 URL 判断是否在 /destinations/disconnect-social-accounts。"""
        raise NotImplementedError("DisconnectSocialAccountPopupPage 没有实现 is_current_url 方法")

    def has_page_elements(self) -> bool:
        """判断是否存在 DisconnectSocialAccountPopupPage 页特有元素。"""
        from .disconnect_confirm_button import DisconnectConfirmButton
        confirm_btn: Element = DisconnectConfirmButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        return confirm_btn.wait()

    def back(self) -> bool:
        """通过点击返回按钮返回 Destinations 页。"""
        from .disconnect_confirm_button import DisconnectConfirmButton
        back_btn: Element = DisconnectConfirmButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        if back_btn.mouse(action="click"):
            return True
        return False