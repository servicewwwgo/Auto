"""
facebook.Login 页面

提供 Page 子类：LoginPage。
提供 Element：royal_login_button。
"""

from ._core import LoginPage
from .royal_login_button import RoyalLoginButton

__all__ = [
    "LoginPage",
    "RoyalLoginButton",
]
