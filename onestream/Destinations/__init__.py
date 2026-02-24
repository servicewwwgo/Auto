"""
onestream.Destinations 页面

提供 Page 子类：DestinationsPage。
提供 Element：account_search_input、add_social_platform、choose_platform_combobox、choose_platform_container、
  choose_platform_facebook_button、connect_button、custom_rtmp_button、custom_rtmp_span、
  disconnect_button、disconnect_confirm_button、rtmp_update_button、server_facebook_url_input、
  server_url_right_arrow_button、social_account_all_disconnect_button、social_account_all_selected_button、
  social_account_input、stream_key_input、update_button。
"""

from ._core import DestinationsPage, DisconnectAllSocialAccountPopupPage, DisconnectSocialAccountPopupPage
from .account_search_input import AccountSearchInput
from .add_social_platform import AddSocialPlatform
from .choose_platform_combobox import ChoosePlatformCombobox
from .choose_platform_facebook_button import ChoosePlatformFacebookButton
from .connect_button import ConnectButton
from .custom_rtmp_button import CustomRtmpButton
from .custom_rtmp_span import CustomRtmpSpan
from .disconnect_button import DisconnectButton
from .disconnect_confirm_button import DisconnectConfirmButton
from .rtmp_update_button import RtmpUpdateButton
from .server_facebook_url_input import ServerFacebookUrlInput
from .server_url_right_arrow_button import ServerUrlRightArrowButton
from .social_account_all_disconnect_button import SocialAccountAllDisconnectButton
from .social_account_all_selected_button import SocialAccountAllSelectedButton
from .social_account_input import SocialAccountInput
from .stream_key_input import StreamKeyInput
from .update_button import UpdateButton

__all__ = [
    "DestinationsPage",
    "DisconnectAllSocialAccountPopupPage",
    "DisconnectSocialAccountPopupPage",
    "AccountSearchInput",
    "AddSocialPlatform",
    "ChoosePlatformCombobox",
    "ChoosePlatformFacebookButton",
    "ConnectButton",
    "CustomRtmpButton",
    "CustomRtmpSpan",
    "DisconnectButton",
    "DisconnectConfirmButton",
    "RtmpUpdateButton",
    "ServerFacebookUrlInput",
    "ServerUrlRightArrowButton",
    "SocialAccountAllDisconnectButton",
    "SocialAccountAllSelectedButton",
    "SocialAccountInput",
    "StreamKeyInput",
    "UpdateButton",
]
