from selenium.webdriver import Chrome, ActionChains
import time, requests, re, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # WebDriverWait注意大小写
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = Chrome(desired_capabilities=caps, executable_path=r"D:\JetBrains\driver\chromedriver.exe")
    url = "https://qzone.qq.com/"
    driver.get(url)
    print('请登录...')
    while driver.current_url == url:
        time.sleep(0.1)
    print('登陆成功！')
    print('打开相册中...')
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "相册")))
    driver.find_element_by_link_text("相册").click()
    # for i in range(3):
    #     time.sleep(1)  # 滚动到底部以加载所有数据
    #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)  # 不能注释掉
    iframe = driver.find_element_by_tag_name('iframe')
    xp = '//ul[@class="js-album-list-ul"]//a[@class="c-tx2 js-album-desc-a"]'
    for i in range(30):
        try:
            driver.execute_script("window.scrollTo(0,400+200*%d)" % int(i / 6))  # 始高400列高200，每行6个
            driver.switch_to.frame(iframe)
            time.sleep(2)
            photos = driver.find_elements_by_xpath(xp)
            p = photos[i]
            print('打开第%d个相册' % (i + 1), '\t', p.text)
            p.click()
            driver.execute_script("window.scrollTo(0,0)")
            time.sleep(2)
            driver.back()
        except:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0,0)")  # 回到顶部
            driver.switch_to.default_content()
            driver.find_element_by_link_text("相册").click()

            time.sleep(5)
            driver.execute_script("window.scrollTo(0,400+200*%d)" % int(i / 6))  # 始高400列高200，每行6个
            driver.switch_to.frame(iframe)
            time.sleep(2)
            photos = driver.find_elements_by_xpath(xp)
            p = photos[i]
            print('打开第%d个相册' % (i + 1), '\t', p.text)
            p.click()
            driver.execute_script("window.scrollTo(0,0)")
            time.sleep(2)
            driver.back()

    # AllPhotos = driver.find_elements_by_xpath('//ul[@class="js-album-list-ul"]//a[@class="c-tx2 js-album-desc-a"]')
    # print('共有%d个相册。' % len(AllPhotos))

    # # driver.close()
