import argparse
import heapq
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

import pandas as pd

from AutoPy import Browser, Domain
from AutoPy.bit import bit_browser_open, bit_browser_close
from AutoPy.error import LogicError
from AutoPy.page import Page, PopupPage
from AutoPy.element import Element

# 在 clear_all_social_accounts_step 中通过 CDP Network.getAllCookies 获取并设置，供后续步骤使用
onestream_cookies: list = []

def append_log(log_file: str, level: str, message: str, encoding: str = "utf-8") -> None:
    """将一行日志追加写入文件，格式：[YYYY-MM-DD HH:MM:SS.mmm] [LEVEL] message"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{timestamp}] [{level}] {message}\n"
        with open(log_file, "a", encoding=encoding) as f:
            f.write(line)
    except Exception as e:
        print(f"[append_log] 写入日志失败: {e}", flush=True)


def login_onestream_step(browser: Browser, node_name: str, onestream_account: str = None, onestream_password: str = None) -> bool:
    """
    Onestream 登录步骤：若无 tab 则创建并打开首页；若当前在登录页则输入账号密码并登录。
    """
    from onestream import OnestreamDomain
    from onestream.Login import LoginPage, LoginEmailInput, LoginPasswordInput, LoginButton

    if not onestream_account or not onestream_password:
        raise LogicError("当前在 Onestream 登录页，请提供 onestream_account 与 onestream_password")

    domain = OnestreamDomain(browser=browser, node_name=node_name)

    # 如果当前在登录页，则输入账号密码并登录
    login_page: Page = LoginPage(browser=browser, node_name=node_name, domain=domain)
    if not login_page.is_current_url():
        domain.close_tab()
        return True

    email_el: Element = LoginEmailInput(browser=browser, node_name=node_name, domain=domain, page=login_page)
    if not email_el.input(text=onestream_account):
        raise LogicError("Onestream 登录账号输入失败")
    time.sleep(1)

    pwd_el: Element = LoginPasswordInput(browser=browser, node_name=node_name, domain=domain, page=login_page)
    if not pwd_el.input(text=onestream_password):
        raise LogicError("Onestream 登录密码输入失败")
    time.sleep(1)
    
    btn_el: Element = LoginButton(browser=browser, node_name=node_name, domain=domain, page=login_page)
    if not btn_el.mouse(action="click"):
        raise LogicError("Onestream 登录按钮点击失败")
    time.sleep(3)
    
    domain.close_tab()
    return True


def delete_social_account_step(browser: Browser, node_name: str, live_social_account: str = None) -> bool:
    """
    Onestream 删除指定社交账号：先登录，进入社交平台页，若有 custom_rtmp 则搜索账号后断开并确认。
    """
    from onestream import OnestreamDomain
    from onestream.Destinations import (
        DestinationsPage,
        AccountSearchInput,
        DisconnectSocialAccountPopupPage,
        DisconnectConfirmButton,
    )

    if not live_social_account:
        raise LogicError("请提供 live_social_account")

    domain = OnestreamDomain(browser=browser, node_name=node_name)
    try:
        dest_page: Page = DestinationsPage(browser=browser, node_name=node_name, domain=domain)
        if not dest_page.go():
            raise LogicError("Onestream 社交平台页打开失败")

        account_search: Element = AccountSearchInput(browser=browser, node_name=node_name, domain=domain, page=dest_page)
        if not account_search.input(text=live_social_account, clear=True):
            raise LogicError("Onestream 社交平台账号搜索失败")
        time.sleep(3)

        disconnect_popup_page: PopupPage = DisconnectSocialAccountPopupPage(browser=browser, node_name=node_name, domain=domain)
        if not disconnect_popup_page.go():
            raise LogicError("Onestream 断开社交平台账号弹窗页打开失败")
        time.sleep(0.7)

        disconnect_confirm_button: Element = DisconnectConfirmButton(browser=browser, node_name=node_name, domain=domain, page=disconnect_popup_page)
        if not disconnect_confirm_button.mouse(action="click"):
            raise LogicError("Onestream 断开社交平台账号确认按钮点击失败")
        time.sleep(3)

        return True
    finally:
        try:
            domain.close_tab()
        except Exception:
            pass


def clear_all_social_accounts_step(browser: Browser, node_name: str) -> bool:
    """
    Onestream 清除所有社交平台连接：先登录，进入社交平台页，获取当前 cookies 并写入全局 onestream_cookies，若有账号则全选并全部断开后确认。
    """
    global onestream_cookies
    from onestream import OnestreamDomain
    from onestream.Destinations import (
        DestinationsPage,
        DisconnectAllSocialAccountPopupPage,
        SocialAccountAllSelectedButton,
        DisconnectConfirmButton,
    )

    domain = OnestreamDomain(browser=browser, node_name=node_name)
    try:
        # 进入社交平台页
        dest_page: Page = DestinationsPage(browser=browser, node_name=node_name, domain=domain)
        if not dest_page.go():
            raise LogicError("Onestream 社交平台页打开失败")

        # 获取当前 Onestream 站点的 cookies，设置为全局变量供后续步骤使用（仅保留域名含 onestream 的 cookie）
        result = domain.send_command("Network.getAllCookies", {})
        if result and isinstance(result.get("data"), dict):
            all_cookies = result["data"].get("cookies") or []
            onestream_cookies = [c for c in all_cookies if isinstance(c, dict) and "onestream" in (c.get("domain") or "").lower()]
        else:
            raise LogicError("Onestream 清除所有社交平台账号失败")

        # 全选所有社交平台账号
        all_sel: Element = SocialAccountAllSelectedButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
        if not all_sel.mouse(action="click"):
            return False
        time.sleep(1)

        # 进入断开所有社交平台账号弹窗页
        disconnect_all_popup_page: PopupPage = DisconnectAllSocialAccountPopupPage(browser=browser, node_name=node_name, domain=domain)
        if not disconnect_all_popup_page.go():
            raise LogicError("Onestream 断开所有社交平台账号弹窗页打开失败")
        time.sleep(1)

        # 确认断开所有社交平台账号
        confirm_btn: Element = DisconnectConfirmButton(browser=browser, node_name=node_name, domain=domain, page=disconnect_all_popup_page)
        if not confirm_btn.mouse(action="click"):
            return False
        time.sleep(7)

        return True
    finally:
        try:
            domain.close_tab()
        except Exception:
            pass


# ============================================================================
# 延迟执行队列系统 - 用于延迟删除社交账号
# ============================================================================

_delayed_delete_queue = []
_delayed_delete_queue_lock = threading.Lock()
_delayed_delete_worker_thread = None
_delayed_delete_worker_running = False
DELAY_DELETE_SECONDS = 46 * 60  # 46 分钟


def _execute_delayed_delete_task(task: dict) -> None:
    """执行延迟删除任务：创建 Browser → 登录 Onestream → 删除指定社交账号。"""
    try:
        node_name_onestream = task.get('node_name_onestream')
        live_social_account = task.get('live_social_account')
        node_api_base_url = task.get('node_api_base_url') or os.environ.get('NODE_API_BASE_URL') or 'https://browser.autowave.dev/api'
        auth_token = task.get('auth_token') or os.environ.get('AUTH_TOKEN')
        if not auth_token:
            print("[延迟删除] 跳过: 未配置 AUTH_TOKEN（环境变量或任务参数）", flush=True)
            return
        enqueue_time = task.get('enqueue_time', 0)
        elapsed = time.time() - enqueue_time
        print(f"[延迟删除] 开始: live_social_account={live_social_account}, 已等待 {elapsed:.1f}s", flush=True)
        browser = Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_onestream, timeout=180)
        delete_social_account_step(browser=browser, node_name=node_name_onestream, live_social_account=live_social_account)
        print(f"[延迟删除] 成功: live_social_account={live_social_account}", flush=True)
    except Exception as e:
        print(f"[延迟删除] 失败: live_social_account={task.get('live_social_account', 'unknown')}, error={e}", flush=True)


def _delayed_delete_worker() -> None:
    """延迟删除队列的后台工作线程：按执行时间从优先队列取任务，到期则执行删除。"""
    global _delayed_delete_worker_running
    _delayed_delete_worker_running = True
    print("[延迟删除队列] 后台工作线程已启动", flush=True)
    while _delayed_delete_worker_running:
        try:
            tasks_to_execute = []
            with _delayed_delete_queue_lock:
                current_time = time.time()
                while _delayed_delete_queue:
                    execute_time, task = _delayed_delete_queue[0]
                    if execute_time > current_time:
                        break
                    heapq.heappop(_delayed_delete_queue)
                    tasks_to_execute.append(task)
                if not _delayed_delete_queue:
                    wait_time = 60
                else:
                    next_execute_time, _ = _delayed_delete_queue[0]
                    wait_time = max(1, min(60, next_execute_time - current_time))
            for task in tasks_to_execute:
                _execute_delayed_delete_task(task)
            time.sleep(wait_time)
        except Exception as e:
            print(f"[延迟删除队列] 工作线程异常: {e}", flush=True)
            time.sleep(5)
    print("[延迟删除队列] 后台工作线程已停止", flush=True)


def _start_delayed_delete_worker() -> None:
    """启动延迟删除队列的后台工作线程（非 daemon）。"""
    global _delayed_delete_worker_thread, _delayed_delete_worker_running
    if _delayed_delete_worker_thread is None or not _delayed_delete_worker_thread.is_alive():
        _delayed_delete_worker_running = False
        _delayed_delete_worker_thread = threading.Thread(target=_delayed_delete_worker, daemon=False)
        _delayed_delete_worker_thread.start()


def wait_for_all_delayed_delete_tasks_complete(timeout: float = None) -> bool:
    """等待所有延迟删除任务执行完成。若指定 timeout 则超时后返回。"""
    global _delayed_delete_worker_thread
    if _delayed_delete_worker_thread is None or not _delayed_delete_worker_thread.is_alive():
        print("[延迟删除队列] 工作线程未运行，无需等待", flush=True)
        return True
    print("[延迟删除队列] 等待所有延迟删除任务完成...", flush=True)
    start_time = time.time()
    empty_count = 0
    while True:
        with _delayed_delete_queue_lock:
            queue_size = len(_delayed_delete_queue)
            if queue_size == 0:
                empty_count += 1
                if empty_count >= 3:
                    print("[延迟删除队列] 队列已连续为空，所有任务已完成", flush=True)
                    return True
            else:
                empty_count = 0
                if _delayed_delete_queue:
                    next_time, _ = _delayed_delete_queue[0]
                    remaining = next_time - time.time()
                    print(f"[延迟删除队列] 等待中... 剩余 {queue_size} 个任务，最早还需 {remaining/60:.1f} 分钟", flush=True)
        if timeout is not None and (time.time() - start_time) >= timeout:
            print(f"[延迟删除队列] 等待超时（{timeout}s）", flush=True)
            return False
        time.sleep(10)


def stop_delayed_delete_worker() -> None:
    """停止延迟删除工作线程。"""
    global _delayed_delete_worker_running, _delayed_delete_worker_thread
    if _delayed_delete_worker_thread is None or not _delayed_delete_worker_thread.is_alive():
        print("[延迟删除队列] 工作线程未运行，无需停止", flush=True)
        return
    print("[延迟删除队列] 正在停止工作线程...", flush=True)
    _delayed_delete_worker_running = False
    if _delayed_delete_worker_thread.is_alive():
        _delayed_delete_worker_thread.join(timeout=10)
        if _delayed_delete_worker_thread.is_alive():
            print("[延迟删除队列] 工作线程未能在 10 秒内退出", flush=True)
        else:
            print("[延迟删除队列] 工作线程已停止", flush=True)


def enqueue_delayed_delete(
    onestream_account: str,
    onestream_password: str,
    live_social_account: str,
    node_name_onestream: str,
    node_api_base_url: str,
    auth_token: str,
) -> None:
    """将删除社交账号任务加入延迟队列，46 分钟后执行。"""
    _start_delayed_delete_worker()
    enqueue_time = time.time()
    execute_time = enqueue_time + DELAY_DELETE_SECONDS
    task = {
        'onestream_account': onestream_account,
        'onestream_password': onestream_password,
        'live_social_account': live_social_account,
        'node_name_onestream': node_name_onestream,
        'node_api_base_url': node_api_base_url,
        'auth_token': auth_token,
        'enqueue_time': enqueue_time,
    }
    with _delayed_delete_queue_lock:
        heapq.heappush(_delayed_delete_queue, (execute_time, task))
    print(f"[延迟删除队列] 任务已入队: live_social_account={live_social_account}, 46分钟后执行, 队列大小={len(_delayed_delete_queue)}", flush=True)


def go_live_streamm_step(browser: Browser, node_facebook: str, node_onestream: str, onestream_account: str = None, onestream_password: str = None, post_title: str = None, post_description: str = None, live_social_account: str = None, video_name: str = None, node_api_base_url: str = None, auth_token: str = None) -> bool:
    """
    按顺序执行：live_stream（Facebook 获取 stream_key）→ create_social_account_stream_key（Onestream 创建社交账号并填密钥）→ create_video_stream（Onestream 创建视频流）→ go_live（Facebook 开播）。
    node_facebook：Facebook 节点名称；node_onestream：Onestream 节点名称。
    """
    node_api_base_url = node_api_base_url or os.environ.get('NODE_API_BASE_URL') or 'https://browser.autowave.dev/api'
    auth_token = auth_token or os.environ.get('AUTH_TOKEN')
    if not auth_token:
        raise LogicError("未配置 AUTH_TOKEN，请设置环境变量 AUTH_TOKEN 或传入参数")

    wait_close_facebook_domain : FacebookDomain = None
    wait_close_onestream_domain : OnestreamDomain = None

    try:

        # ---------- 步骤 1: live_stream_step ----------
        if not live_social_account or not video_name:
            raise LogicError("请提供 live_social_account 与 video_name")

        from facebook import FacebookDomain
        from facebook.Check import CheckPage
        from facebook.Login import LoginPage as FacebookLoginPage
        from facebook.Home import HomePage as FacebookHomePage
        from facebook.Live_Setup_and_Eligibility_Check_Page import LiveSetupAndEligibilityCheckPage
        from facebook.Live import (
            LivePage,
            StreamingSoftwareButton,
            StreamKeyInput,
        )

        fb_domain = FacebookDomain(browser=browser, node_name=node_facebook)
        wait_close_facebook_domain = fb_domain

        fb_domain.close_all_tabs()

        check_page: Page = CheckPage(browser=browser, node_name=node_facebook, domain=fb_domain)
        if check_page.is_current_url():
            raise LogicError("账户状态错误, 请先解决账户状态问题!", retry_task=False)

        login_page: Page = FacebookLoginPage(browser=browser, node_name=node_facebook, domain=fb_domain)
        if login_page.is_current_url():
            raise LogicError("登录按钮存在, 请先登录!")

        home_page: Page = FacebookHomePage(browser=browser, node_name=node_facebook, domain=fb_domain)
        if not home_page.is_current_url():
            home_page.go()

        live_setup_and_eligibility_check_page: Page = LiveSetupAndEligibilityCheckPage(browser=browser, node_name=node_facebook, domain=fb_domain)
        if not live_setup_and_eligibility_check_page.go():
            raise LogicError("直播设置和资格检查页打开失败")

        live_page: Page = LivePage(browser=browser, node_name=node_facebook, domain=fb_domain)
        if not live_page.go():
            raise LogicError("直播页打开失败")

        streaming_software_button: Element = StreamingSoftwareButton(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
        if not streaming_software_button.mouse(action="click", simulate="simulated"):
            raise LogicError("streaming software button 点击失败")

        time.sleep(0.7)

        stream_key_input: Element = StreamKeyInput(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
        stream_key = stream_key_input.get_attribute("value")
        if stream_key is None or stream_key == "":
            raise LogicError("stream_key_input 的 value 为空")
        time.sleep(0.3)

        # ---------- 步骤 2: create_social_account_stream_key_step ----------
        from onestream import OnestreamDomain
        from onestream.Destinations import (
            DestinationsPage,
            AddSocialPlatform,
            CustomRtmpButton,
            ChoosePlatformCombobox,
            ChoosePlatformFacebookButton,
            ServerUrlRightArrowButton,
            ServerFacebookUrlInput,
            SocialAccountInput,
            StreamKeyInput as OnestreamStreamKeyInput,
            UpdateButton,
        )

        # 使用 onestream_cookies 创建带 cookie 的 Onestream 标签页（先 about:blank + setCookies 再导航到 HOME_URL）
        onestream_domain = OnestreamDomain(browser=browser, node_name=node_onestream, new_window=True)
        wait_close_onestream_domain = onestream_domain

        dest_page: Page = DestinationsPage(browser=browser, node_name=node_onestream, domain=onestream_domain)
        if not dest_page.go():
            raise LogicError("Onestream 社交平台页打开失败")
        time.sleep(0.7)

        add_platform: Element = AddSocialPlatform(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not add_platform.mouse(action="click"):
            raise LogicError("Onestream 添加社交平台按钮点击失败")
        time.sleep(0.7)

        custom_rtmp: Element = CustomRtmpButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not custom_rtmp.mouse(action="click"):
            raise LogicError("Onestream 自定义 RTMP 按钮点击失败")
        time.sleep(0.2)

        choose_combobox: Element = ChoosePlatformCombobox(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not choose_combobox.mouse(action="click"):
            raise LogicError("Onestream 选择平台下拉框按钮点击失败")
        time.sleep(0.7)

        fb_btn: Element = ChoosePlatformFacebookButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not fb_btn.mouse(action="click"):
            raise LogicError("Onestream 选择 Facebook 按钮点击失败")
        time.sleep(0.7)

        arrow_btn: Element = ServerUrlRightArrowButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not arrow_btn.mouse(action="click"):
            raise LogicError("Onestream 服务器 URL 右箭头按钮点击失败")
        time.sleep(0.7)

        server_input: Element = ServerFacebookUrlInput(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not server_input.mouse(action="click"):
            raise LogicError("Onestream 服务器 URL 输入框点击失败")
        time.sleep(0.7)

        social_input: Element = SocialAccountInput(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not social_input.input(text=live_social_account, clear=True):
            raise LogicError("Onestream 社交平台账号输入失败")
        time.sleep(0.1)

        stream_key_el: Element = OnestreamStreamKeyInput(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not stream_key_el.input(text=stream_key, clear=True):
            raise LogicError("Onestream 直播密钥输入失败")
        time.sleep(0.1)

        update_btn: Element = UpdateButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=dest_page)
        if not update_btn.mouse(action="click"):
            raise LogicError("Onestream 更新按钮点击失败")
        time.sleep(7)

        # 删除社交平台账号 - 延迟任务（46 分钟后执行）
        try:
            enqueue_delayed_delete(
                onestream_account=onestream_account,
                onestream_password=onestream_password,
                live_social_account=live_social_account,
                node_name_onestream=node_onestream,
                node_api_base_url=node_api_base_url,
                auth_token=auth_token,
            )
        except Exception as e:
            print(f"[WARN] 延迟删除入队失败: {e}", flush=True)

        # ---------- 步骤 3: create_video_stream_step ----------
        from onestream.Home import (
            HomePage,
            CreateStreamButton,
            SingleVideoButton,
            OnestreamStorageButton,
            VideoSearchInput,
            VideoSelectButton,
            LiveSocialAccountButton,
            GoLiveButton as OnestreamGoLiveButton,
            ConfirmLiveButton,
            ClosePopupButton,
        )

        home_page_os: Page = HomePage(browser=browser, node_name=node_onestream, domain=onestream_domain)
        if not home_page_os.is_current_url():
            home_page_os.go()

        create_btn: Element = CreateStreamButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not create_btn.mouse(action="click"):
            raise LogicError("Onestream 创建流按钮点击失败")
        time.sleep(0.6)

        single_btn: Element = SingleVideoButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not single_btn.mouse(action="click"):
            raise LogicError("Onestream 单视频按钮点击失败")
        time.sleep(0.6)

        storage_btn: Element = OnestreamStorageButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not storage_btn.mouse(action="click"):
            raise LogicError("Onestream 存储按钮点击失败")
        time.sleep(0.6)

        video_search: Element = VideoSearchInput(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not video_search.input(text=video_name, clear=True):
            raise LogicError("Onestream 视频搜索输入失败")
        time.sleep(5)

        video_select_btn: Element = VideoSelectButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not video_select_btn.mouse(action="click"):
            raise LogicError("Onestream 视频选择按钮点击失败")
        time.sleep(5.1)

        live_account_btn: Element = LiveSocialAccountButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os, live_social_account=live_social_account)
        if not live_account_btn.mouse(action="click"):
            raise LogicError("Onestream 直播社交账号按钮点击失败")
        time.sleep(0.6)

        go_live_btn: Element = OnestreamGoLiveButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not go_live_btn.mouse(action="click"):
            raise LogicError("Onestream 开播按钮点击失败")
        time.sleep(0.6)

        confirm_btn: Element = ConfirmLiveButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not confirm_btn.mouse(action="click"):
            raise LogicError("Onestream 确认开播按钮点击失败")
        time.sleep(0.6)

        close_popup: Element = ClosePopupButton(browser=browser, node_name=node_onestream, domain=onestream_domain, page=home_page_os)
        if not close_popup.mouse(action="click"):
            raise LogicError("Onestream 关闭弹窗按钮点击失败")
        time.sleep(0.6)

        # ---------- 步骤 4: go_live_step ----------
        from AutoPy.element import PreInstruction
        from facebook.Live import (
            GoLiveButtonFinally,
            GoLiveButtonWithoutCurrent,
            GoLiveButtonOfAddTitleDialog,
            EnabledButton,
            FeelingActivityButton,
            LovelyButton,
            CreatePostDisplay,
            PostTitleInputField,
            PostDescriptionInputField,
            PostSaveButton,
            EndLiveButton,
        )

        # 重新激活 facebook 标签页（CDP Page.bringToFront 无参数，tab 由 send_command 的 tab_id 指定）
        # fb_domain.send_command("Page.bringToFront", {})

        enabled_btn: Element = EnabledButton(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
        has_enabled = enabled_btn.find_element()

        if has_enabled:
            feeling_btn: Element = FeelingActivityButton(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
            if not feeling_btn.mouse(action="click", simulate="simulated", pre=PreInstruction.FIND_ELEMENT):
                raise LogicError("感受/活动按钮不可用, 请检查感受/活动按钮状态")
            time.sleep(2.7)

            lovely_btn: Element = LovelyButton(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
            if not lovely_btn.mouse(action="click", simulate="simulated", pre=PreInstruction.WAIT):
                raise LogicError("可爱按钮不可用, 请检查可爱按钮状态")
            time.sleep(1.7)

            create_post_display: Element = CreatePostDisplay(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
            if not create_post_display.wait(timeout=60, ignore_error=True):
                raise LogicError("创建贴文显示不可用, 请检查创建贴文显示状态")

            if post_title:
                title_input: Element = PostTitleInputField(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
                if not title_input.keyboard(action="type", text=post_title, delay=0.6, pre=PreInstruction.WAIT):
                    raise LogicError("贴文标题输入框不可用, 请检查贴文标题输入框状态")
                time.sleep(1)

            if post_description:
                desc_input: Element = PostDescriptionInputField(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
                if not desc_input.keyboard(action="type", text=post_description, delay=0.7, pre=PreInstruction.WAIT):
                    raise LogicError("贴文描述输入框不可用, 请检查贴文描述输入框状态")
                time.sleep(1)

            save_btn: Element = PostSaveButton(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
            if not save_btn.mouse(action="click", simulate="simulated", pre=PreInstruction.WAIT):
                raise LogicError("贴文保存按钮不可用, 请检查贴文保存按钮状态")
            time.sleep(3)

        go_live_finally: Element = GoLiveButtonFinally(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
        for _ in range(18):
            if go_live_finally.get_attribute("aria-disabled", pre=PreInstruction.FIND_ELEMENT) != "true":
                break
            time.sleep(10)
        else:
            raise LogicError("facebook当前直播按钮没有点亮，不能点击")

        go_without: Element = GoLiveButtonWithoutCurrent(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
        if not go_without.mouse(action="click", simulate="simulated", pre=PreInstruction.FIND_ELEMENT):
            raise LogicError("facebook当前直播按钮没有点亮，不能点击")
        time.sleep(1.3)

        if not has_enabled:
            go_in_dialog = GoLiveButtonOfAddTitleDialog(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
            if not go_in_dialog.mouse(action="click", simulate="simulated"):
                raise LogicError("facebook添加标题对话框中的直播按钮不可用")
            time.sleep(3.3)

        end_live_button: Element = EndLiveButton(browser=browser, node_name=node_facebook, domain=fb_domain, page=live_page)
        if not end_live_button.wait():
            raise LogicError("facebook结束直播按钮不可用")
        time.sleep(2.6)

    except Exception:
        raise
    finally:
        try:
            if wait_close_facebook_domain is not None:
                wait_close_facebook_domain.close_tab()
            if wait_close_onestream_domain is not None:
                wait_close_onestream_domain.close_tab()
        except Exception:
            pass
    
    return True


def read_xlsx_file(file_path: str) -> List[dict]:
    """
    读取 Excel 文件并返回所有行数据。
    每行转为字典，并带 _row_index。必需列：node_name_facebook, live_social_account, video_name, post_title, post_description。
    """
    df = pd.read_excel(file_path)
    required_columns = ['node_name_facebook', 'live_social_account', 'video_name', 'post_title', 'post_description']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Excel 文件 {file_path} 缺少必需列: {missing_columns}")
    rows_data = []
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        row_dict['_row_index'] = index
        rows_data.append(row_dict)
    return rows_data


def write_xlsx_file(file_path: str, data: List[dict]) -> None:
    """将字典列表写入 Excel 文件，排除内部键 _row_index。"""
    if not data:
        raise ValueError("数据列表不能为空")
    cleaned_data = [{k: v for k, v in row_dict.items() if k != '_row_index'} for row_dict in data]
    df = pd.DataFrame(cleaned_data)
    df.to_excel(file_path, index=False, engine='openpyxl')


def main(
    onestream_account: str = None,
    onestream_password: str = None,
    node_name_onestream: str = None,
    thread: int = None,
    file_path: str = None,
    node_api_base_url: str = None,
    auth_token: str = None,
) -> dict:
    """
    批量执行工作流：读取 Excel 任务列表，先执行清除所有社交平台，再单/多线程执行 go_live_streamm_step。
    auth_token 与 node_api_base_url 未传入时从环境变量 AUTH_TOKEN、NODE_API_BASE_URL 读取。
    """
    auth_token = auth_token or os.environ.get('AUTH_TOKEN')
    if not auth_token:
        return {'success': False, 'message': '未配置 AUTH_TOKEN，请设置环境变量 AUTH_TOKEN'}
    node_api_base_url = node_api_base_url or os.environ.get('NODE_API_BASE_URL') or 'https://browser.autowave.dev/api'

    try:
        rows_data = read_xlsx_file(file_path)
        total_rows = len(rows_data)
    except Exception as e:
        return {'success': False, 'message': f'读取 Excel 失败: {str(e)}'}

    if total_rows == 0:
        return {'success': False, 'message': 'Excel 中无数据'}

    first_node = node_name_onestream or str(rows_data[0].get('node_name_onestream', ''))
    if first_node:
        try:
            browser = Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=first_node, timeout=180)
            clear_all_social_accounts_step(browser=browser, node_name=first_node)
        except Exception as e:
            return {'success': False, 'message': f'清除所有社交平台失败: {str(e)}'}

    results = []
    error_rows = []
    error_file_path = './error.xlsx'
    error_lock = threading.Lock()
    log_lock = threading.Lock()
    log_file_path = "auto.log"
    max_workers = thread if thread and thread > 0 else 1

    browser = Browser(node_api_base_url=node_api_base_url, auth_token=auth_token, node_name=node_name_onestream, timeout=180)

    def append_error_and_write(row_dict: dict) -> None:
        """追加失败行并实时写入 error.xlsx（多线程安全）"""
        with error_lock:
            error_rows.append(row_dict)
            try:
                write_xlsx_file(file_path=error_file_path, data=list(error_rows))
            except Exception as write_err:
                print(f"[append_error_and_write] 写入 {error_file_path} 失败: {write_err}", flush=True)

    def process_row(row_dict: dict) -> dict:
        index = row_dict.get('_row_index', 0)
        node_facebook = str(row_dict.get('node_name_facebook', ''))
        node_onestream = node_name_onestream or str(row_dict.get('node_name_onestream', ''))
        account = onestream_account or str(row_dict.get('onestream_account', ''))
        password = onestream_password or str(row_dict.get('onestream_password', ''))
        live_social_account = str(row_dict.get('live_social_account', ''))
        video_name = str(row_dict.get('video_name', ''))
        post_title = str(row_dict.get('post_title', ''))
        post_description = str(row_dict.get('post_description', ''))

        try:
            browser_seq = int(node_facebook)
        except (ValueError, TypeError):
            err_msg = "node_name_facebook 必须为可转换为整数的值"
            row_dict['error'] = err_msg
            append_error_and_write(row_dict)
            result = {'row_index': index, 'success': False, 'result': err_msg}
            with log_lock:
                append_log(log_file_path, "ERROR", f"{node_facebook} {result}")
            results.append(result)
            return result

        if index < thread:
            time.sleep(index)

        try:
            # 打开 Facebook 节点 Bit 浏览器（时机参考 autojs：流程开始前）
            bit_browser_open(browser=browser, node_name=node_onestream, browser_seq=browser_seq, args=[], queue=True, timeout=180)

            go_live_streamm_step(
                browser=browser,
                node_facebook=node_facebook,
                node_onestream=node_onestream,
                onestream_account=account,
                onestream_password=password,
                post_title=post_title or None,
                post_description=post_description or None,
                live_social_account=live_social_account,
                video_name=video_name,
                node_api_base_url=node_api_base_url,
                auth_token=auth_token,
            )
            result = {'row_index': index, 'success': True, 'result': 'ok'}
            with log_lock:
                append_log(log_file_path, "INFO", f"{node_facebook} {result}")
        except Exception as e:
            row_dict['error'] = str(e)
            append_error_and_write(row_dict)
            result = {'row_index': index, 'success': False, 'result': str(e)}
            with log_lock:
                append_log(log_file_path, "ERROR", f"{node_facebook} {result}")
        finally:
            # 关闭 Facebook 节点 Bit 浏览器（时机参考 autojs：单行任务结束后）
            try:
                time.sleep(5)
                bit_browser_close(browser=browser, node_name=node_onestream, browser_seq=browser_seq, timeout=180)
            except Exception:
                pass
        results.append(result)
        return result

    if max_workers == 1:
        for row_dict in rows_data:
            process_row(row_dict)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_row = {executor.submit(process_row, row_dict): row_dict for row_dict in rows_data}
            for future in as_completed(future_to_row):
                try:
                    future.result()
                except Exception as e:
                    row_dict = future_to_row[future]
                    row_dict['error'] = str(e)
                    index = row_dict.get('_row_index', 0)
                    results.append({'row_index': index, 'success': False, 'result': str(e)})
                    append_error_and_write(row_dict)
        results.sort(key=lambda x: x['row_index'])

    return {'total_rows': total_rows, 'threads_used': max_workers, 'results': results}


if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)

    auth_token = os.environ.get('AUTH_TOKEN')
    node_api_base_url = os.environ.get('NODE_API_BASE_URL') or 'https://browser.autowave.dev/api'
    if not auth_token:
        print("错误: 请设置环境变量 AUTH_TOKEN", file=sys.stderr, flush=True)
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Auto 批量开播 - 从 Excel 读取任务并执行')
    parser.add_argument('-f', '--file_path', type=str, default='./data.xlsx', help='Excel 文件路径')
    parser.add_argument('-a', '--onestream_account', type=str, default='', help='Onestream 账号')
    parser.add_argument('-p', '--onestream_password', type=str, default='', help='Onestream 密码')
    parser.add_argument('-n', '--node_name_onestream', type=str, default='', help='Onestream 节点名称')
    parser.add_argument('-t', '--thread', type=int, default=1, help='线程数')
    args = parser.parse_args()

    result = main(
        onestream_account=args.onestream_account or None,
        onestream_password=args.onestream_password or None,
        node_name_onestream=args.node_name_onestream or None,
        thread=args.thread,
        file_path=args.file_path,
        node_api_base_url=node_api_base_url,
        auth_token=auth_token,
    )
    print(result, flush=True)

    print("[主程序] 主工作流已完成，等待所有延迟删除任务完成...", flush=True)
    wait_for_all_delayed_delete_tasks_complete()
    stop_delayed_delete_worker()
    print("[主程序] 所有任务已完成，程序退出", flush=True)
    if sys.gettrace() is not None:
        input("调试结束，按 Enter 退出...")