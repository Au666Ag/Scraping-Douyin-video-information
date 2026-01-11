from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
# 指定 chromedriver 的路径
driver_path = r"D:\pycharm\conda\envs\xuexi\Scripts\chromedriver-win64\chromedriver.exe"

# 初始化 WebDriver
service = Service(executable_path=driver_path)

# 初始化
extract = {
    'name':[],
    'introduce':[],
    'like':[],
    'comment':[],
    'collect':[],
    'repost':[]
}

# 创建一个类
class douyin:
    def __init__(self,url):
        self.browser = webdriver.Chrome(service=service)
        self.browser.get(url)  # 打开一个网页
        self.login_button(wait=True)# 关闭刚开始的登录页面
        self.sure_button(wait=True)

    # 定义通用方法
    def click(self,css,wait=False):
        try:
            if wait:
                element = (WebDriverWait(self.browser, 10).until
                (
                EC.element_to_be_clickable((By.CSS_SELECTOR, css))
            ))
            else:
                element = self.browser.find_element(By.CSS_SELECTOR, css)

            if element.is_displayed():
                element.click()
                return True
        except Exception as e:
            if wait:
                print(f"错误是：{e}")
    # 确定按钮
    def sure_button(self,wait=False):
        return self.click("#douyin-web-recommend-guide-mask > div > button > span",wait)

    # 检测登录按钮
    def login_button(self,wait=False):
        return self.click("div > div.uotczcdY > div.YoNA2Hyj.qKr0RhiL > svg",wait)

    # 检测下滑按钮
    def slide_button(self,wait=False):
        return self.click("div.xgplayer-playswitch-next > span > svg",wait)

    # 检测“继续观看按钮”
    def look_button(self,wait=False):
        return self.click("div.HDhMLx9a > div > div.oya2IBgA > div.beA0QPV4",wait)
# 提取
    def extract_(self):
        # 主播名
        name = self.browser.find_elements(By.CLASS_NAME,'account-name-text')
        for item  in name:
            if item.get_attribute("textContent") not in extract['name']:
                extract['name'].append(item.get_attribute("textContent"))
            else:
                pass
        # 视频简介
        introduce = self.browser.find_elements(By.CLASS_NAME,'title')
        for item  in introduce:
            if item.get_attribute("textContent") not in extract['introduce']:
                extract['introduce'].append(item.get_attribute("textContent"))
            else:
                pass
        # 点赞量
        like = self.browser.find_elements(By.CLASS_NAME,'KV_gO8oI')
        for item  in like:
            if item.text not in extract['like']:
                extract['like'].append(item.text)
            else:
                pass
        # 评论
        comment = self.browser.find_elements(By.CLASS_NAME,'X_wB9MpJ')
        for item  in comment:
            if item.text not in extract['comment']:
                extract['comment'].append(item.text)
            else:
                pass
        # 收藏
        collect = self.browser.find_elements(By.CLASS_NAME,'OjAuUiYV')
        for item  in collect:
            if item.text not in extract['collect']:
                extract['collect'].append(item.text)
            else:
                pass
        # 转发
        repost = self.browser.find_elements(By.CLASS_NAME,'hzIYk71v')
        for item  in repost:
            if item.text not in extract['repost']:
                extract['repost'].append(item.text)
            else:
                pass
# 主程序
def main():
    time.sleep(3)
    while True:
        num = random.randint(1, 5)
        dou.extract_()
        dou.slide_button()
        dou.login_button()
        dou.look_button()
        time.sleep(num)
        print(extract)
if __name__ =="__main__":
    dou = douyin("https://www.douyin.com/?recommend=1")
    main()