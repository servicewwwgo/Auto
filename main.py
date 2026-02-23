import time
from AutoPy import Browser, Domain
from AutoPy.auto import get_domain, get_page, get_element
from AutoPy.page import Page
from AutoPy.element import Element


def live_stream_step(browser: Browser, node_name: str, domain: Domain):
    domain = get_domain(domain="facebook", browser=browser, node_name=node_name) if domain is None else domain

    # 检查页 - 是否自动跳转到检查页
    check_page: Page = get_page(domain="facebook", page="Check", browser=browser, node_name=node_name, domain_instance=domain)
    if check_page.is_current_url():
        raise Exception("账户状态错误, 请先解决账户状态问题!")
    
    # 登录按钮 - 是否自动跳转到
    login_page: Page = get_page(domain="facebook", page="Login", browser=browser, node_name=node_name, domain_instance=domain)
    if login_page.is_current_url():
        raise Exception("登录按钮存在, 请先登录!")

    # 首页
    home_page: Page = get_page(domain="facebook", page="Home", browser=browser, node_name=node_name, domain_instance=domain)
    if not home_page.is_current_url():
        home_page.go()

    # 直播设置和资格检查页
    live_setup_and_eligibility_check_page: Page = get_page(domain="facebook", page="Live_Setup_and_Eligibility_Check_Page", browser=browser, node_name=node_name, domain_instance=domain)
    live_setup_and_eligibility_check_page.go()

    # 直播页
    live_page: Page = get_page(domain="facebook", page="Live", browser=browser, node_name=node_name, domain_instance=domain)
    live_page.go()

    # 点击 streaming software button
    streaming_software_button: Element = get_element(domain="facebook", page="Live", element="streaming_software_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
    streaming_software_button.mouse(action="click", simulate="simulated")

    # 获取 stream_key_input 的 value
    stream_key_input: Element = get_element(domain="facebook", page="Live", element="stream_key_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
    stream_key_input_value = stream_key_input.get_attribute("value")
    print(stream_key_input_value)

    return stream_key_input_value


def go_live_step(browser: Browser, node_name: str, domain: Domain, post_title: str = None, post_description: str = None):
    """
    直播按钮步骤：在已具备直播设置的前提下点击开播。
    若未在直播页则先执行与 live_stream_step 相同的导航（检查/登录/首页/直播设置/直播页），
    然后等待最终直播按钮可用、点击当前直播按钮、在添加标题弹窗中点击开播。
    """
    domain = get_domain(domain="facebook", browser=browser, node_name=node_name) if domain is None else domain

    # 检查页 - 是否自动跳转到检查页
    check_page: Page = get_page(domain="facebook", page="Check", browser=browser, node_name=node_name, domain_instance=domain)
    if check_page.is_current_url():
        raise Exception("账户状态错误, 请先解决账户状态问题!")

    # 登录按钮 - 是否自动跳转到
    login_page: Page = get_page(domain="facebook", page="Login", browser=browser, node_name=node_name, domain_instance=domain)
    if login_page.is_current_url():
        raise Exception("登录按钮存在, 请先登录!")

    # 首页 -> 直播设置和资格检查页 -> 直播页（与 live_stream_step 一致，不取 stream_key）
    home_page: Page = get_page(domain="facebook", page="Home", browser=browser, node_name=node_name, domain_instance=domain)
    if not home_page.is_current_url():
        home_page.go()
    live_setup_page: Page = get_page(domain="facebook", page="Live_Setup_and_Eligibility_Check_Page", browser=browser, node_name=node_name, domain_instance=domain)
    live_setup_page.go()
    live_page: Page = get_page(domain="facebook", page="Live", browser=browser, node_name=node_name, domain_instance=domain)
    live_page.go()

    # 等待最终直播按钮可点击（aria-disabled != "true"）
    go_live_finally: Element = get_element(domain="facebook", page="Live", element="go_live_button_finally", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
    for _ in range(60):
        if go_live_finally.get_attribute("aria-disabled") != "true":
            break
        time.sleep(3.1)
    else:
        raise Exception("最终直播按钮不可用, 请检查最终直播按钮状态")

    # 点击当前直播按钮（不含 aria-current 的 Go live）
    go_without: Element = get_element(domain="facebook", page="Live", element="go_live_button_without_current", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
    if go_without.wait(wait_type="wait_element_visible", timeout=5):
        go_without.mouse(action="click", simulate="simulated")
    else:
        go_without_dup: Element = get_element(domain="facebook", page="Live", element="go_live_button_without_current_duplicate", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
        if not go_without_dup.wait(wait_type="wait_element_exists", timeout=3):
            raise Exception("facebook当前直播按钮不可用, 请检查Live Producer.当前直播按钮")
        go_without_dup.mouse(action="click", simulate="simulated")
    time.sleep(1.7)

    # 添加标题对话框中的直播按钮
    add_title: Element = get_element(domain="facebook", page="Live", element="add_title_dialog", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
    if not add_title.wait(wait_type="wait_element_visible", timeout=120):
        raise Exception("添加标题对话框不可用, 请检查添加标题对话框状态")
    go_in_dialog: Element = get_element(domain="facebook", page="Live", element="go_live_button_of_add_title_dialog", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
    if not go_in_dialog.wait(wait_type="wait_element_visible", timeout=3):
        go_in_dialog = get_element(domain="facebook", page="Live", element="go_live_button_of_add_title_dialog_duplicate", browser=browser, node_name=node_name, domain_instance=domain, page_instance=live_page)
        if not go_in_dialog.wait(wait_type="wait_element_exists", timeout=3):
            raise Exception("facebook添加标题对话框中的直播按钮不可用")
    go_in_dialog.mouse(action="click", simulate="simulated")
    time.sleep(3.3)

    # 等待结束直播按钮出现（当前仓库无 end_live_button 元素，短暂等待后结束）
    time.sleep(2.6)
    domain.close_tab()


ONESTREAM_HOME_URL = "https://app.onestream.live/"


def login_onestream_step(browser: Browser, node_name: str, domain: Domain = None, onestream_account: str = None, onestream_password: str = None):
    """
    Onestream 登录步骤：若无 tab 则创建并打开首页；若当前在登录页则输入账号密码并登录。
    """
    domain = get_domain(domain="onestream", browser=browser, node_name=node_name, start_url=ONESTREAM_HOME_URL, new_window=True) if domain is None else domain

    # 触发 tab 创建（访问 tab_id 时若未建表会先 create_tab）
    _ = domain.tab_id

    login_page: Page = get_page(domain="onestream", page="Login", browser=browser, node_name=node_name, domain_instance=domain)
    if not login_page.is_current_url():
        return

    if not onestream_account or not onestream_password:
        raise Exception("当前在 Onestream 登录页，请提供 onestream_account 与 onestream_password")

    email_el: Element = get_element(domain="onestream", page="Login", element="login_email_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=login_page)
    email_el.wait(wait_type="wait_element_visible", timeout=30)
    email_el.input(text=onestream_account)
    time.sleep(1)
    pwd_el: Element = get_element(domain="onestream", page="Login", element="login_password_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=login_page)
    pwd_el.find_element(timeout=30)
    pwd_el.input(text=onestream_password)
    time.sleep(1)
    btn_el: Element = get_element(domain="onestream", page="Login", element="login_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=login_page)
    btn_el.find_element(timeout=30)
    btn_el.mouse(action="click", simulate="none")
    time.sleep(3)


def update_social_account_stream_key_step(
    browser: Browser,
    node_name: str,
    domain: Domain = None,
    onestream_account: str = None,
    onestream_password: str = None,
    live_social_account: str = None,
    stream_key: str = None,
):
    """
    Onestream 更新社交账号直播密钥：先登录，进入社交平台页，搜索账号后点击更新 RTMP，输入 stream_key 并点击更新。
    """
    domain = get_domain(domain="onestream", browser=browser, node_name=node_name, start_url=ONESTREAM_HOME_URL) if domain is None else domain
    login_onestream_step(browser=browser, node_name=node_name, domain=domain, onestream_account=onestream_account, onestream_password=onestream_password)
    if not live_social_account or not stream_key:
        raise Exception("请提供 live_social_account 与 stream_key")

    home_page: Page = get_page(domain="onestream", page="Home", browser=browser, node_name=node_name, domain_instance=domain)
    dest_page: Page = get_page(domain="onestream", page="Destinations", browser=browser, node_name=node_name, domain_instance=domain)

    social_btn: Element = get_element(domain="onestream", page="Home", element="social_platforms_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    if not social_btn.wait(wait_type="wait_element_exists", timeout=30):
        raise Exception("社交平台页面按钮不可见")
    social_btn.mouse(action="click", simulate="none")

    account_search: Element = get_element(domain="onestream", page="Destinations", element="account_search_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    account_search.wait(wait_type="wait_element_visible", timeout=30)
    account_search.input(text=live_social_account)

    rtmp_btn: Element = get_element(domain="onestream", page="Destinations", element="rtmp_update_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    rtmp_btn.wait(wait_type="wait_element_visible", timeout=30)
    rtmp_btn.mouse(action="click", simulate="none")

    stream_key_el: Element = get_element(domain="onestream", page="Destinations", element="stream_key_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    stream_key_el.wait(wait_type="wait_element_visible", timeout=30)
    stream_key_el.input(text=stream_key, clear=True)

    update_btn: Element = get_element(domain="onestream", page="Destinations", element="update_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    update_btn.find_element(timeout=30)
    update_btn.mouse(action="click", simulate="none")
    time.sleep(7)
    domain.close_tab()


def delete_social_account_step(
    browser: Browser,
    node_name: str,
    domain: Domain = None,
    onestream_account: str = None,
    onestream_password: str = None,
    live_social_account: str = None,
):
    """
    Onestream 删除指定社交账号：先登录，进入社交平台页，若有 custom_rtmp 则搜索账号后断开并确认。
    """
    domain = get_domain(domain="onestream", browser=browser, node_name=node_name, start_url=ONESTREAM_HOME_URL) if domain is None else domain
    login_onestream_step(browser=browser, node_name=node_name, domain=domain, onestream_account=onestream_account, onestream_password=onestream_password)
    if not live_social_account:
        raise Exception("请提供 live_social_account")

    home_page: Page = get_page(domain="onestream", page="Home", browser=browser, node_name=node_name, domain_instance=domain)
    dest_page: Page = get_page(domain="onestream", page="Destinations", browser=browser, node_name=node_name, domain_instance=domain)

    social_btn: Element = get_element(domain="onestream", page="Home", element="social_platforms_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    social_btn.wait(wait_type="wait_element_exists", timeout=30)
    social_btn.mouse(action="click", simulate="simulated")
    custom_rtmp: Element = get_element(domain="onestream", page="Destinations", element="custom_rtmp_span", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    ok = custom_rtmp.wait(wait_type="wait_element_visible", timeout=10, ignore_error=True)
    if ok:
        account_search: Element = get_element(domain="onestream", page="Destinations", element="account_search_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
        account_search.wait(wait_type="wait_element_visible", timeout=30)
        account_search.input(text=live_social_account)
        time.sleep(3)
        disconnect_btn: Element = get_element(domain="onestream", page="Destinations", element="disconnect_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
        if disconnect_btn.wait(wait_type="wait_element_visible", timeout=10, ignore_error=True):
            disconnect_btn.mouse(action="click", simulate="none")
            time.sleep(1)
            confirm_btn: Element = get_element(domain="onestream", page="Destinations", element="disconnect_confirm_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
            if confirm_btn.wait(wait_type="wait_element_visible", timeout=10, ignore_error=True):
                confirm_btn.mouse(action="click", simulate="none")
    time.sleep(3)
    domain.close_tab()


def clear_all_social_accounts_step(
    browser: Browser,
    node_name: str,
    domain: Domain = None,
    onestream_account: str = None,
    onestream_password: str = None,
):
    """
    Onestream 清除所有社交平台连接：先登录，进入社交平台页，若有账号则全选并全部断开后确认。
    """
    domain = get_domain(domain="onestream", browser=browser, node_name=node_name, start_url=ONESTREAM_HOME_URL) if domain is None else domain
    login_onestream_step(browser=browser, node_name=node_name, domain=domain, onestream_account=onestream_account, onestream_password=onestream_password)

    home_page: Page = get_page(domain="onestream", page="Home", browser=browser, node_name=node_name, domain_instance=domain)
    dest_page: Page = get_page(domain="onestream", page="Destinations", browser=browser, node_name=node_name, domain_instance=domain)

    social_btn: Element = get_element(domain="onestream", page="Home", element="social_platforms_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    social_btn.wait(wait_type="wait_element_exists", timeout=30)
    social_btn.mouse(action="click", simulate="simulated")
    custom_rtmp: Element = get_element(domain="onestream", page="Destinations", element="custom_rtmp_span", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    if custom_rtmp.wait(wait_type="wait_element_visible", timeout=10, ignore_error=True):
        all_sel: Element = get_element(domain="onestream", page="Destinations", element="social_account_all_selected_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
        all_sel.wait(wait_type="wait_element_exists", timeout=30)
        all_sel.mouse(action="click", simulate="none")
        time.sleep(1)
        all_disconnect: Element = get_element(domain="onestream", page="Destinations", element="social_account_all_disconnect_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
        all_disconnect.wait(wait_type="wait_element_visible", timeout=30)
        all_disconnect.mouse(action="click", simulate="none")
        time.sleep(1)
        confirm_btn: Element = get_element(domain="onestream", page="Destinations", element="disconnect_confirm_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
        confirm_btn.wait(wait_type="wait_element_visible", timeout=30)
        confirm_btn.mouse(action="click", simulate="none")
    time.sleep(7)
    domain.close_tab()


def create_social_account_stream_key_step(
    browser: Browser,
    node_name: str,
    domain: Domain = None,
    onestream_account: str = None,
    onestream_password: str = None,
    live_social_account: str = None,
    stream_key: str = None,
):
    """
    Onestream 创建社交账号并设置直播密钥：登录后进入社交平台，添加自定义 RTMP，选 Facebook，填服务器 URL/账号/密钥后更新。
    """
    domain = get_domain(domain="onestream", browser=browser, node_name=node_name, start_url=ONESTREAM_HOME_URL) if domain is None else domain
    login_onestream_step(browser=browser, node_name=node_name, domain=domain, onestream_account=onestream_account, onestream_password=onestream_password)
    if not live_social_account or not stream_key:
        raise Exception("请提供 live_social_account 与 stream_key")

    home_page: Page = get_page(domain="onestream", page="Home", browser=browser, node_name=node_name, domain_instance=domain)
    dest_page: Page = get_page(domain="onestream", page="Destinations", browser=browser, node_name=node_name, domain_instance=domain)

    social_btn: Element = get_element(domain="onestream", page="Home", element="social_platforms_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    social_btn.wait(wait_type="wait_element_visible", timeout=120)
    social_btn.mouse(action="click", simulate="none", timeout=60)
    time.sleep(1.7)

    add_platform: Element = get_element(domain="onestream", page="Destinations", element="add_social_platform", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    add_platform.wait(wait_type="wait_element_visible", timeout=60)
    add_platform.mouse(action="click", simulate="none")
    time.sleep(1.7)

    custom_rtmp: Element = get_element(domain="onestream", page="Destinations", element="custom_rtmp_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    custom_rtmp.wait(wait_type="wait_element_visible", timeout=60)
    custom_rtmp.mouse(action="click", simulate="none")
    time.sleep(1.2)

    choose_container: Element = get_element(domain="onestream", page="Destinations", element="choose_platform_container", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    choose_container.wait(wait_type="wait_element_visible", timeout=30)
    choose_combobox: Element = get_element(domain="onestream", page="Destinations", element="choose_platform_combobox", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    choose_combobox.wait(wait_type="wait_element_visible", timeout=30)
    choose_combobox.mouse(action="click", simulate="none")
    time.sleep(1.7)

    fb_btn: Element = get_element(domain="onestream", page="Destinations", element="choose_platform_facebook_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    fb_btn.wait(wait_type="wait_element_visible", timeout=30)
    fb_btn.mouse(action="click", simulate="none")
    time.sleep(1.7)

    arrow_btn: Element = get_element(domain="onestream", page="Destinations", element="server_url_right_arrow_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    arrow_btn.wait(wait_type="wait_element_visible", timeout=30)
    arrow_btn.mouse(action="click", simulate="none")
    time.sleep(1.7)

    server_input: Element = get_element(domain="onestream", page="Destinations", element="server_facebook_url_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    server_input.wait(wait_type="wait_element_visible", timeout=30)
    server_input.mouse(action="click", simulate="none")
    time.sleep(1.7)

    social_input: Element = get_element(domain="onestream", page="Destinations", element="social_account_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    social_input.wait(wait_type="wait_element_visible", timeout=30)
    social_input.input(text=live_social_account, clear=True)
    time.sleep(1)

    stream_key_el: Element = get_element(domain="onestream", page="Destinations", element="stream_key_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    stream_key_el.wait(wait_type="wait_element_visible", timeout=30)
    stream_key_el.input(text=stream_key, clear=True)
    time.sleep(1)

    update_btn: Element = get_element(domain="onestream", page="Destinations", element="update_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=dest_page)
    update_btn.wait(wait_type="wait_element_visible", timeout=30)
    update_btn.mouse(action="click", simulate="none")
    time.sleep(7)
    domain.close_tab()


def create_video_stream_step(
    browser: Browser,
    node_name: str,
    domain: Domain = None,
    onestream_account: str = None,
    onestream_password: str = None,
    live_social_account: str = None,
    video_name: str = None,
):
    """
    Onestream 创建视频流：登录后点击创建流 -> 单视频 -> Onestream 存储 -> 搜索并选择视频 -> 选择直播社交账号 -> 开播 -> 确认 -> 关闭弹窗。
    """
    domain = get_domain(domain="onestream", browser=browser, node_name=node_name, start_url=ONESTREAM_HOME_URL) if domain is None else domain
    login_onestream_step(browser=browser, node_name=node_name, domain=domain, onestream_account=onestream_account, onestream_password=onestream_password)
    if not video_name:
        raise Exception("请提供 video_name")
    if not live_social_account:
        raise Exception("请提供 live_social_account")

    home_page: Page = get_page(domain="onestream", page="Home", browser=browser, node_name=node_name, domain_instance=domain)

    create_btn: Element = get_element(domain="onestream", page="Home", element="create_stream_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    create_btn.wait(wait_type="wait_element_visible", timeout=30)
    create_btn.mouse(action="click", simulate="none")
    time.sleep(1)

    single_container: Element = get_element(domain="onestream", page="Home", element="single_video_button_container", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    single_container.wait(wait_type="wait_element_visible", timeout=30)
    single_btn: Element = get_element(domain="onestream", page="Home", element="single_video_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    single_btn.find_element(timeout=30)
    single_btn.mouse(action="click", simulate="none")
    time.sleep(1)

    storage_btn: Element = get_element(domain="onestream", page="Home", element="onestream_storage_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    storage_btn.wait(wait_type="wait_element_visible", timeout=30)
    storage_btn.mouse(action="click", simulate="none")
    time.sleep(1)

    video_search: Element = get_element(domain="onestream", page="Home", element="video_search_input", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    video_search.wait(wait_type="wait_element_visible", timeout=30)
    video_search.input(text=video_name, clear=True)
    time.sleep(7)

    video_select_container: Element = get_element(domain="onestream", page="Home", element="video_select_container", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    video_select_container.wait(wait_type="wait_element_visible", timeout=30)
    video_select_btn: Element = get_element(domain="onestream", page="Home", element="video_select_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    video_select_btn.find_element(timeout=30)
    video_select_btn.mouse(action="click", simulate="none")
    time.sleep(5)

    live_account_btn: Element = get_element(domain="onestream", page="Home", element="live_social_account_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    live_account_btn.wait(wait_type="wait_element_visible", timeout=60)
    live_account_btn.mouse(action="click", simulate="none")
    time.sleep(1)

    go_live_btn: Element = get_element(domain="onestream", page="Home", element="go_live_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    go_live_btn.wait(wait_type="wait_element_visible", timeout=30)
    go_live_btn.mouse(action="click", simulate="none")
    time.sleep(2)

    confirm_btn: Element = get_element(domain="onestream", page="Home", element="confirm_live_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    confirm_btn.wait(wait_type="wait_element_visible", timeout=30)
    confirm_btn.mouse(action="click", simulate="none")
    time.sleep(7)

    close_popup: Element = get_element(domain="onestream", page="Home", element="close_popup_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)
    close_popup.wait(wait_type="wait_element_visible", timeout=60)
    close_popup.mouse(action="click", simulate="none")
    time.sleep(7)
    domain.close_tab()


def main():
    browser = Browser(node_api_base_url="https://browser.autowave.dev/api", auth_token="node_token_qwer2wsx")
    node_name = "26314"

    domain: Domain = get_domain(domain="facebook", browser=browser, node_name=node_name)
    result = live_stream_step(browser=browser, node_name=node_name, domain=domain)
    print(result)

    
if __name__ == "__main__":
    main()