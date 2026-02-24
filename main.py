import time
from AutoPy import Browser, Domain
from AutoPy.error import LogicError
from AutoPy.page import Page, PopupPage
from AutoPy.element import Element

def live_stream_step(browser: Browser, node_name: str, domain: Domain = None):
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

    if domain is None:
        domain = FacebookDomain(browser=browser, node_name=node_name)

    # 检查页 - 是否自动跳转到检查页
    check_page: Page = CheckPage(browser=browser, node_name=node_name, domain=domain)
    if check_page.is_current_url():
        raise LogicError("账户状态错误, 请先解决账户状态问题!")
    
    # 登录按钮 - 是否自动跳转到
    login_page: Page = FacebookLoginPage(browser=browser, node_name=node_name, domain=domain)
    if login_page.is_current_url():
        raise LogicError("登录按钮存在, 请先登录!")

    # 首页
    home_page: Page = FacebookHomePage(browser=browser, node_name=node_name, domain=domain)
    if not home_page.is_current_url():
        home_page.go()

    # 直播设置和资格检查页
    live_setup_and_eligibility_check_page: Page = LiveSetupAndEligibilityCheckPage(browser=browser, node_name=node_name, domain=domain)
    if not live_setup_and_eligibility_check_page.go():
        raise LogicError("直播设置和资格检查页打开失败")

    # 直播页
    live_page: Page = LivePage(browser=browser, node_name=node_name, domain=domain)
    if not live_page.go():
        raise LogicError("直播页打开失败")

    # 点击 streaming software button
    streaming_software_button: Element = StreamingSoftwareButton(browser=browser, node_name=node_name, domain=domain, page=live_page)
    if not streaming_software_button.mouse(action="click", simulate="simulated"):
        raise LogicError("streaming software button 点击失败")

    time.sleep(1.1)

    # 获取 stream_key_input 的 value
    stream_key_input: Element = StreamKeyInput(browser=browser, node_name=node_name, domain=domain, page=live_page)
    stream_key_input_value = stream_key_input.get_attribute("value")
    if stream_key_input_value is None or stream_key_input_value == "":
        raise LogicError("stream_key_input 的 value 为空")

    time.sleep(0.3)

    return stream_key_input_value


def go_live_step(browser: Browser, node_name: str, post_title: str = None, post_description: str = None, domain: Domain = None):
    """
    直播按钮步骤：在已具备直播设置的前提下点击开播。
    若未在直播页则先执行与 live_stream_step 相同的导航（检查/登录/首页/直播设置/直播页），
    然后根据是否有「启用按钮」分支：
    - 无启用按钮：等待最终直播按钮可用 → 点击当前直播按钮 → 在添加标题弹窗中点击开播。
    - 有启用按钮：点击感受/活动按钮 → 可爱按钮 → 检查创建贴文显示 → 可选填贴文标题/描述 → 点击贴文保存 → 再执行开播流程。
    """
    from facebook import FacebookDomain
    from AutoPy.element import PreInstruction
    from facebook.Live import (
        LivePage,
        GoLiveButtonFinally,
        GoLiveButtonWithoutCurrent,
        GoLiveButtonOfAddTitleDialog,
        EnabledButton,
        FeelingActivityButton,
        LovelyButton,
        PostTitleInputField,
        PostDescriptionInputField,
        PostSaveButton,
        EndLiveButton,
    )

    if domain is None:
        domain = FacebookDomain(browser=browser, node_name=node_name)

    live_page: Page = LivePage(browser=browser, node_name=node_name, domain=domain)
    if not live_page.has_page_elements():
        if not live_page.go():
            raise LogicError("直播页打开失败")

    enabled_btn: Element = EnabledButton(browser=browser, node_name=node_name, domain=domain, page=live_page)
    has_enabled = enabled_btn.wait(wait_type="wait_element_visible", timeout=10, ignore_error=True)

    if has_enabled:
        # 有启用按钮：感受/活动 → 可爱 → 创建贴文 → 贴文标题/描述 → 贴文保存 → 再开播
        feeling_btn: Element = FeelingActivityButton(browser=browser, node_name=node_name, domain=domain, page=live_page)
        if not feeling_btn.mouse(action="click", simulate="simulated", pre=PreInstruction.FIND_ELEMENT):
            raise LogicError("感受/活动按钮不可用, 请检查感受/活动按钮状态")
        time.sleep(2.7)

        lovely_btn: Element = LovelyButton(browser=browser, node_name=node_name, domain=domain, page=live_page)
        if not lovely_btn.mouse(action="click", simulate="simulated", pre=PreInstruction.WAIT):
            raise LogicError("可爱按钮不可用, 请检查可爱按钮状态")
        time.sleep(1.7)

        if post_title:
            title_input: Element = PostTitleInputField(browser=browser, node_name=node_name, domain=domain, page=live_page)
            if not title_input.keyboard(action="type", text=post_title, pre=PreInstruction.WAIT):
                raise LogicError("贴文标题输入框不可用, 请检查贴文标题输入框状态")
            time.sleep(1)

        if post_description:
            desc_input: Element = PostDescriptionInputField(browser=browser, node_name=node_name, domain=domain, page=live_page)
            if not desc_input.keyboard(action="type", text=post_description, pre=PreInstruction.WAIT):
                raise LogicError("贴文描述输入框不可用, 请检查贴文描述输入框状态")
            time.sleep(1)

        save_btn: Element = PostSaveButton(browser=browser, node_name=node_name, domain=domain, page=live_page)
        if not save_btn.mouse(action="click", simulate="simulated", pre=PreInstruction.WAIT):
            raise LogicError("贴文保存按钮不可用, 请检查贴文保存按钮状态")
        time.sleep(3)

    # 等待最终直播按钮可点击（aria-disabled != "true"）
    go_live_finally: Element = GoLiveButtonFinally(browser=browser, node_name=node_name, domain=domain, page=live_page)
    for _ in range(60):
        if go_live_finally.get_attribute("aria-disabled", pre=PreInstruction.FIND_ELEMENT) != "true":
            break
        time.sleep(3.1)
    else:
        raise LogicError("最终直播按钮不可用, 请检查最终直播按钮状态")

    go_without = GoLiveButtonWithoutCurrent(browser=browser, node_name=node_name, domain=domain, page=live_page)
    if not go_without.mouse(action="click", simulate="simulated", pre=PreInstruction.FIND_ELEMENT):
        raise LogicError("facebook当前直播按钮不可用, 请检查Live Producer.当前直播按钮")
    time.sleep(3.2 if has_enabled else 1.7)

    if not has_enabled:
        go_in_dialog = GoLiveButtonOfAddTitleDialog(browser=browser, node_name=node_name, domain=domain, page=live_page)
        if not go_in_dialog.mouse(action="click", simulate="simulated"):
            raise LogicError("facebook添加标题对话框中的直播按钮不可用")
        time.sleep(3.3)

    end_live_button: Element = EndLiveButton(browser=browser, node_name=node_name, domain=domain, page=live_page)
    if not end_live_button.wait(wait_type="wait_element_visible"):
        raise LogicError("facebook结束直播按钮不可用, 请检查facebook结束直播按钮状态")
    time.sleep(2.6)

    domain.close_tab()


def login_onestream_step(browser: Browser, node_name: str, onestream_account: str = None, onestream_password: str = None, domain: Domain = None) -> bool:
    """
    Onestream 登录步骤：若无 tab 则创建并打开首页；若当前在登录页则输入账号密码并登录。
    """
    from onestream import OnestreamDomain
    from onestream.Login import LoginPage, LoginEmailInput, LoginPasswordInput, LoginButton

    if not onestream_account or not onestream_password:
        raise LogicError("当前在 Onestream 登录页，请提供 onestream_account 与 onestream_password")

    if domain is None:
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


def update_social_account_stream_key_step(browser: Browser, node_name: str, live_social_account: str = None, stream_key: str = None, domain: Domain = None) -> bool:
    """
    Onestream 更新社交账号直播密钥：先登录，进入社交平台页，搜索账号后点击更新 RTMP，输入 stream_key 并点击更新。
    """
    from onestream import OnestreamDomain
    from onestream.Destinations import (
        DestinationsPage,
        AccountSearchInput,
        RtmpUpdateButton,
        StreamKeyInput as OnestreamStreamKeyInput,
        UpdateButton,
    )

    if not live_social_account or not stream_key:
        raise LogicError("请提供 live_social_account 与 stream_key")

    if domain is None:
        domain = OnestreamDomain(browser=browser, node_name=node_name)
    
    dest_page: Page = DestinationsPage(browser=browser, node_name=node_name, domain=domain)
    if not dest_page.go():
        raise LogicError("Onestream 社交平台页打开失败")

    account_search: Element = AccountSearchInput(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not account_search.input(text=live_social_account, clear=True):
        raise LogicError("Onestream 社交平台账号搜索失败")

    rtmp_btn: Element = RtmpUpdateButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not rtmp_btn.mouse(action="click"):
        raise LogicError("Onestream 更新 RTMP 按钮点击失败")

    stream_key_el: Element = OnestreamStreamKeyInput(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not stream_key_el.input(text=stream_key, clear=True):
        raise LogicError("Onestream 直播密钥输入失败")

    update_btn: Element = UpdateButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not update_btn.mouse(action="click"):
        raise LogicError("Onestream 更新按钮点击失败")
    time.sleep(7)

    domain.close_tab()
    return True


def delete_social_account_step(browser: Browser, node_name: str, live_social_account: str = None, domain: Domain = None) -> bool:
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

    if domain is None:
        domain = OnestreamDomain(browser=browser, node_name=node_name)
    
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

    disconnect_confirm_button: Element = DisconnectConfirmButton(browser=browser, node_name=node_name, domain=domain, page=disconnect_popup_page)
    if not disconnect_confirm_button.mouse(action="click"):
        raise LogicError("Onestream 断开社交平台账号确认按钮点击失败")
    time.sleep(3)

    domain.close_tab()
    return True


def clear_all_social_accounts_step(browser: Browser, node_name: str, domain: Domain = None) -> bool:
    """
    Onestream 清除所有社交平台连接：先登录，进入社交平台页，若有账号则全选并全部断开后确认。
    """
    from onestream import OnestreamDomain
    from onestream.Destinations import (
        DestinationsPage,
        DisconnectAllSocialAccountPopupPage,
        SocialAccountAllSelectedButton,
        DisconnectConfirmButton,
    )

    if domain is None:
        domain = OnestreamDomain(browser=browser, node_name=node_name)

    # 进入社交平台页
    dest_page: Page = DestinationsPage(browser=browser, node_name=node_name, domain=domain)
    if not dest_page.go():
        raise LogicError("Onestream 社交平台页打开失败")

    # 全选所有社交平台账号
    all_sel: Element = SocialAccountAllSelectedButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not all_sel.mouse(action="click"):
        raise LogicError("Onestream 全选所有社交平台账号按钮点击失败")
    time.sleep(1)

    # 进入断开所有社交平台账号弹窗页
    disconnect_all_popup_page: PopupPage = DisconnectAllSocialAccountPopupPage(browser=browser, node_name=node_name, domain=domain)
    if not disconnect_all_popup_page.go():
        raise LogicError("Onestream 断开所有社交平台账号弹窗页打开失败")
    time.sleep(1)

    # 确认断开所有社交平台账号
    confirm_btn: Element = DisconnectConfirmButton(browser=browser, node_name=node_name, domain=domain, page=disconnect_all_popup_page)
    if not confirm_btn.mouse(action="click"):
        raise LogicError("Onestream 断开所有社交平台账号确认按钮点击失败")
    time.sleep(7)

    domain.close_tab()
    return True


def create_social_account_stream_key_step(browser: Browser, node_name: str, live_social_account: str = None, stream_key: str = None, domain: Domain = None) -> bool:
    """
    Onestream 创建社交账号并设置直播密钥：登录后进入社交平台，添加自定义 RTMP，选 Facebook，填服务器 URL/账号/密钥后更新。
    """
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

    if not live_social_account or not stream_key:
        raise LogicError("请提供 live_social_account 与 stream_key")

    if domain is None:
        domain = OnestreamDomain(browser=browser, node_name=node_name)

    dest_page: Page = DestinationsPage(browser=browser, node_name=node_name, domain=domain)
    if not dest_page.go():
        raise LogicError("Onestream 社交平台页打开失败")
    time.sleep(1.7)

    add_platform: Element = AddSocialPlatform(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not add_platform.mouse(action="click"):
        raise LogicError("Onestream 添加社交平台按钮点击失败")
    time.sleep(1.7)

    custom_rtmp: Element = CustomRtmpButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not custom_rtmp.mouse(action="click"):
        raise LogicError("Onestream 自定义 RTMP 按钮点击失败")
    time.sleep(1.2)

    choose_combobox: Element = ChoosePlatformCombobox(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not choose_combobox.mouse(action="click"):
        raise LogicError("Onestream 选择平台下拉框按钮点击失败")
    time.sleep(1.7)

    fb_btn: Element = ChoosePlatformFacebookButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not fb_btn.mouse(action="click"):
        raise LogicError("Onestream 选择 Facebook 按钮点击失败")
    time.sleep(1.7)

    arrow_btn: Element = ServerUrlRightArrowButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not arrow_btn.mouse(action="click"):
        raise LogicError("Onestream 服务器 URL 右箭头按钮点击失败")
    time.sleep(1.7)

    server_input: Element = ServerFacebookUrlInput(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not server_input.mouse(action="click"):
        raise LogicError("Onestream 服务器 URL 输入框点击失败")
    time.sleep(1.7)

    social_input: Element = SocialAccountInput(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not social_input.input(text=live_social_account, clear=True):
        raise LogicError("Onestream 社交平台账号输入失败")
    time.sleep(1)

    stream_key_el: Element = OnestreamStreamKeyInput(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not stream_key_el.input(text=stream_key, clear=True):
        raise LogicError("Onestream 直播密钥输入失败")
    time.sleep(1)

    update_btn: Element = UpdateButton(browser=browser, node_name=node_name, domain=domain, page=dest_page)
    if not update_btn.mouse(action="click"):
        raise LogicError("Onestream 更新按钮点击失败")
    time.sleep(7)

    domain.close_tab()
    return True


def create_video_stream_step(browser: Browser, node_name: str, live_social_account: str = None, video_name: str = None, domain: Domain = None) -> bool:
    """
    Onestream 创建视频流：登录后点击创建流 -> 单视频 -> Onestream 存储 -> 搜索并选择视频 -> 选择直播社交账号 -> 开播 -> 确认 -> 关闭弹窗。
    """
    from onestream import OnestreamDomain
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

    if not video_name or not live_social_account:
        raise LogicError("请提供 video_name 与 live_social_account")

    if domain is None:
        domain = OnestreamDomain(browser=browser, node_name=node_name)

    home_page: Page = HomePage(browser=browser, node_name=node_name, domain=domain)
    if not home_page.is_current_url():
        home_page.go()

    create_btn: Element = CreateStreamButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not create_btn.mouse(action="click"):
        raise LogicError("Onestream 创建流按钮点击失败")
    time.sleep(1)

    single_btn: Element = SingleVideoButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not single_btn.mouse(action="click"):
        raise LogicError("Onestream 单视频按钮点击失败")
    time.sleep(1)

    storage_btn: Element = OnestreamStorageButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not storage_btn.mouse(action="click"):
        raise LogicError("Onestream 存储按钮点击失败")
    time.sleep(1)

    video_search: Element = VideoSearchInput(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not video_search.input(text=video_name, clear=True):
        raise LogicError("Onestream 视频搜索输入失败")
    time.sleep(7)

    video_select_btn: Element = VideoSelectButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not video_select_btn.mouse(action="click"):
        raise LogicError("Onestream 视频选择按钮点击失败")
    time.sleep(5)

    live_account_btn: Element = LiveSocialAccountButton(browser=browser, node_name=node_name, domain=domain, page=home_page, live_social_account=live_social_account)
    if not live_account_btn.mouse(action="click"):
        raise LogicError("Onestream 直播社交账号按钮点击失败")
    time.sleep(1)

    go_live_btn: Element = OnestreamGoLiveButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not go_live_btn.mouse(action="click"):
        raise LogicError("Onestream 开播按钮点击失败")
    time.sleep(2)

    confirm_btn: Element = ConfirmLiveButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not confirm_btn.mouse(action="click"):
        raise LogicError("Onestream 确认开播按钮点击失败")
    time.sleep(7)

    close_popup: Element = ClosePopupButton(browser=browser, node_name=node_name, domain=domain, page=home_page)
    if not close_popup.mouse(action="click"):
        raise LogicError("Onestream 关闭弹窗按钮点击失败")
    time.sleep(7)

    domain.close_tab()
    return True


def main():
    browser = Browser(node_api_base_url="https://browser.autowave.dev/api", auth_token="node_token_qwer2wsx")
    node_name = "26314"

    from facebook import FacebookDomain
    domain = FacebookDomain(browser=browser, node_name=node_name)
    live_stream_step(browser=browser, node_name=node_name, domain=domain)
    result = go_live_step(browser=browser, node_name=node_name, post_title="go live", post_description="go live", domain=domain)

    print(result)


if __name__ == "__main__":
    main()