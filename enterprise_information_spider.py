# coding utf-8
"""
作者：Hester
日期：2023/6/29
"""
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.keys import Keys
import logging
import time

def get_company_patents(company_name):
    # 初始化 Edge 选项
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无界面模式，可以加快爬取速度
    edge_options.add_argument("--disable-web-security")  # 禁用浏览器的混合内容警告
    edge_options.add_argument("--allow-running-insecure-content") # 禁用浏览器的混合内容警告
    edge_options.add_argument(r"C:\Users\Hitting\Desktop\policy\MicrosoftWebDriver.exe") # 浏览器路径（需要修改成自己电脑上的路径）

    # 创建 Edge 浏览器对象
    LOGGER.setLevel(logging.ERROR) # 隐藏网站警告信息
    driver = webdriver.Edge(options=edge_options)

    try:
        print("访问天眼查登录页面")
        driver.get("https://www.tianyancha.com/login")
        print("访问成功\n")

        print("输入用户名和密码")
        username = '13922761129'
        password = 'lll123456'

        # 等待登录模块加载完成
        login_module = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'module1')))

        # 切换到密码登录选项卡
        password_login_tab = login_module.find_element(By.XPATH, './/div[@active-tab="1"]')
        password_login_tab.click()

        # 输入手机号和密码
        phone_input = driver.find_element(By.XPATH, '//input[@name="phone"]')
        phone_input.send_keys(username)

        password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
        password_input.send_keys(password)

        # 提交登录表单
        login_button = driver.find_element(By.XPATH, '//div[@tyc-event-ch="Login.PasswordLogin.Login"]')
        login_button.click()

        # 等待登录成功
        WebDriverWait(driver, 10).until(EC.url_contains('https://www.tianyancha.com/usercenter'))

        print("等待登录成功并获取 Cookie")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-container"))
        )
        cookies = driver.get_cookies()

        print("设置 Cookie")
        for cookie in cookies:
            driver.add_cookie(cookie)

        print("访问指定公司的专利页面")
        search_url = f"https://www.tianyancha.com/search?key={company_name}&checkFrom=searchBox"
        driver.get(search_url)

        print("等待专利列表加载完成")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".in-block .search-item-outer"))
        )

        print("提取全部专利数据")
        patent_elements = driver.find_elements(By.CSS_SELECTOR, ".in-block .search-item-outer")
        patent_data = []

        for element in patent_elements:
            patent_title = element.find_element(By.CSS_SELECTOR, ".in-block a").text
            patent_data.append(patent_title)

        return patent_data

    finally:
        driver.quit()


if __name__=='__main__':
    company_name = input("请输入公司名称：")
    patents = get_company_patents(company_name)
    for patent in patents:
        print(patent)

