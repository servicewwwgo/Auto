"""
facebook.Login 页面

提供 Page 子类：LoginPage。
提供 Element：email_input、password_input、royal_login_button。
"""

from ._core import LoginPage
from .email_input import EmailInput
from .password_input import PasswordInput
from .royal_login_button import RoyalLoginButton

__all__ = [
    "LoginPage",
    "EmailInput",
    "PasswordInput",
    "RoyalLoginButton",
]
