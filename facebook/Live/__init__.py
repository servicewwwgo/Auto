"""
facebook.Live 页面

提供 Page 子类：LivePage。
提供 Element：add_title_dialog、connect_video_source、go_live_button_finally、go_live_button_finally_duplicate、
  go_live_button_of_add_title_dialog、go_live_button_of_add_title_dialog_duplicate、
  go_live_button_without_current、go_live_button_without_current_duplicate、
  stream_key_input、streaming_software_button。
"""

from ._core import LivePage
from .add_title_dialog import AddTitleDialog
from .connect_video_source import ConnectVideoSource
from .go_live_button_finally import GoLiveButtonFinally
from .go_live_button_finally_duplicate import GoLiveButtonFinallyDuplicate
from .go_live_button_of_add_title_dialog import GoLiveButtonOfAddTitleDialog
from .go_live_button_of_add_title_dialog_duplicate import GoLiveButtonOfAddTitleDialogDuplicate
from .go_live_button_without_current import GoLiveButtonWithoutCurrent
from .go_live_button_without_current_duplicate import GoLiveButtonWithoutCurrentDuplicate
from .stream_key_input import StreamKeyInput
from .streaming_software_button import StreamingSoftwareButton

__all__ = [
    "LivePage",
    "AddTitleDialog",
    "ConnectVideoSource",
    "GoLiveButtonFinally",
    "GoLiveButtonFinallyDuplicate",
    "GoLiveButtonOfAddTitleDialog",
    "GoLiveButtonOfAddTitleDialogDuplicate",
    "GoLiveButtonWithoutCurrent",
    "GoLiveButtonWithoutCurrentDuplicate",
    "StreamKeyInput",
    "StreamingSoftwareButton",
]
