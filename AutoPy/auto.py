"""
AutoPy 站点子类入口

根据 domain / page / element 参数动态导入并创建 Domain、Page、Element 子类实例。
从标准包入口导入（domain 包、{domain}.{Page} 包、{domain}.{Page}.{element} 模块），
类实现可在包内任意位置，只需在包入口导出约定命名的类即可。新增/删除包无需修改本文件。
"""

import sys
import importlib
from pathlib import Path

from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page
from AutoPy.element import Element

# 保证项目根目录（domain 包所在）可被导入
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _domain_class_name(domain: str) -> str:
    """domain → Domain 类名，如 'facebook' → 'FacebookDomain'。"""
    parts = domain.strip().replace("-", "_").split("_")
    return "".join(p.capitalize() for p in parts) + "Domain"


def _page_class_name(page: str) -> str:
    """page 包名 → Page 类名，如 'Home' → 'HomePage'，'Live_Setup_and_Eligibility_Check_Page' → 'LiveSetupAndEligibilityCheckPage'。"""
    parts = page.strip().replace("-", "_").split("_")
    base = "".join(p.capitalize() for p in parts)
    return base if base.endswith("Page") else base + "Page"


def _element_class_name(element: str) -> str:
    """element → Element 类名，如 'stream_key_input' → 'StreamKeyInput'。"""
    parts = element.strip().replace("-", "_").split("_")
    return "".join(p.capitalize() for p in parts)


def _to_package_name(s: str, lowercase: bool = False) -> str:
    """规范为包名：strip、'-'→'_'，可选小写。包名即调用名，无需映射。"""
    out = (s or "").strip().replace("-", "_")
    return out.lower() if lowercase else out


def get_domain(domain: str, browser: Browser, node_name: str, description: str = "", language: str = "en-US", start_url: str | None = None, active: bool = True, new_window: bool = False) -> Domain:
    """
    根据 domain 动态导入并创建 Domain 子类实例。

    - domain: 站点包名（与目录名一致），如 'facebook'。
    - browser: Browser 实例。
    - node_name: 节点名。
    - description: 基类 Domain 参数。
    - language: 基类 Domain 参数。
    - start_url: 基类 Domain 参数。
    - active: 基类 Domain 参数。
    - new_window: 基类 Domain 参数。

    Returns:
        Domain 子类实例，如 FacebookDomain、OnestreamDomain。
    """
    domain_mod = _to_package_name(domain, lowercase=True).split(".")[0] or "facebook"
    mod = importlib.import_module(domain_mod)
    cls = getattr(mod, _domain_class_name(domain_mod))
    return cls(browser=browser, node_name=node_name, description=description, language=language, start_url=start_url, active=active, new_window=new_window)


def get_page(domain: str, page: str, browser: Browser, node_name: str, domain_instance: Domain, description: str = "", language: str = "en-US") -> Page:
    """
    根据 domain、page 动态导入并创建 Page 子类实例。

    - domain: 站点包名（与目录名一致），如 'facebook'。
    - page: 页面包名（与目录名一致），如 'Home'、'Live'、'Live_Setup_and_Eligibility_Check_Page'。
    - browser: Browser 实例。
    - node_name: 节点名。
    - domain_instance: 已创建的 Domain 实例（如 FacebookDomain）。
    - description: 基类 Page 参数。
    - language: 基类 Page 参数。

    Returns:
        Page 子类实例，如 HomePage、LivePage。
    """
    domain_mod = _to_package_name(domain, lowercase=True).split(".")[0] or "facebook"
    page_mod = _to_package_name(page)
    mod = importlib.import_module(f"{domain_mod}.{page_mod}")
    cls = getattr(mod, _page_class_name(page_mod))
    return cls(browser=browser, node_name=node_name, domain=domain_instance, description=description, language=language)


def get_element(domain: str, page: str, element: str, browser: Browser, node_name: str, domain_instance: Domain, page_instance: Page, language: str = "en-US") -> Element:
    """
    根据 domain、page、element 动态导入并创建 Element 子类实例。

    - domain: 站点包名（与目录名一致），如 'facebook'。
    - page: 页面包名（与目录名一致），如 'Live'、'Live_Setup_and_Eligibility_Check_Page'。
    - element: 元素包名（与目录名一致），如 'stream_key_input'、'royal_login_button'。
    - browser: Browser 实例。
    - node_name: 节点名。
    - domain_instance: 已创建的 Domain 实例。
    - page_instance: 已创建的 Page 实例。
    - description: 基类 Element 参数。
    - language: 基类 Element 参数。

    Returns:
        Element 子类实例，如 StreamKeyInput。
    """
    domain_mod = _to_package_name(domain, lowercase=True).split(".")[0] or "facebook"
    page_mod = _to_package_name(page)
    element_mod = _to_package_name(element)
    mod = importlib.import_module(f"{domain_mod}.{page_mod}.{element_mod}")
    cls = getattr(mod, _element_class_name(element_mod))
    return cls(browser=browser, node_name=node_name, domain=domain_instance, page=page_instance, language=language)


__all__ = [
    "get_domain",
    "get_page",
    "get_element",
]
