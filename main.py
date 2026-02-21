from AutoPy import Browser
from AutoPy.auto import get_domain, get_page, get_element
from AutoPy.domain import Domain
from AutoPy.page import Page
from AutoPy.element import Element


def main():
    browser = Browser(node_api_base_url="https://browser.autowave.dev/api", auth_token="node_token_qwer2wsx")
    node_name = "26314"

    domain: Domain = get_domain(domain="facebook", browser=browser, node_name=node_name)
    home_page: Page = get_page(domain="facebook", page="home", browser=browser, node_name=node_name, domain_instance=domain)
    if not home_page.is_current():
        home_page.go()

    live_video_button: Element = get_element(domain="facebook", page="home", element="live_video_button", browser=browser, node_name=node_name, domain_instance=domain, page_instance=home_page)

    result = live_video_button.mouse(action="click", simulate="simulated")
    print(result)

    
if __name__ == "__main__":
    main()