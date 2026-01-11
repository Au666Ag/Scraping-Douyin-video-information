# Scraping-Douyin-video-information
Seleium自动化爬取抖音视频信息(名称、简介、点赞量、评论数、收藏数、转发数) 

Selenium automation for scraping Douyin video information (title, description, like count, comment count, favorite count, share count).


​
首先说明这个代码不用类也能写，或许更简单

### 前言：

这个需要现在相应浏览器的驱动，并且需要配置好环境变量，在这里提醒一下，一定要下载与浏览器版本相匹配的版本，不然启动会比较慢，随便搜一下就有教程。

### 一、实现抖音自动下滑

#### 1.构造通用函数

实现抖音下滑是通过抖音侧面的下滑按钮实现，但是在使用**seleium**打开抖音的时候，往往会出现卡顿，导致按钮延迟出现，如果程序在第一时间检测不到按钮会报错，所以需要设置等待时间，避免因为网路原因报错。我们先设置一个通用函数，就是下面代码：

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
这个函数是class类中的一个函数，所以第一个形参是**self**，第二个参数是**css**，这个参数是为了使用CSS选择器，用于传入css路径，第三个参数用来判断是否等待，这个后面在说

函数主体用*try和except*用来捕获错误，说实话这个代码太短了，用不上这个，可以删了，我写的时候不想看见一大串的错误，就写上了

接着是一个**if**语句，这个就和上面第三个参数有关了，但仔细看这个if和else执行的语句好像也差不多，为啥要用***wait=False***来判断？虽然if和else执行的语句差不多，但一个最多等待10秒，一个不等待，两者都是用来定位取消按钮的位置，进而点击按钮

但问题在于，直接登录抖音网址需要登录，还有一个“我明白了”需要点击取消，这两个页面的取消按钮，如果网络不好，没有第一时间显示出来，代码没有检测到按钮就会报错，这时候我们就需要给网络的等待的时间，代码很明显，就是等待10秒，意思是最多等待10秒，如果按钮还没有出现，就报错

而*else*执行的代码不需要等待，因为在不登陆刷视频的时候，偶尔也会弹出登录页面或者其他页面，这些页面的弹出是随着视频一起出来的，直接就出来了，所以不用等待，所以用**wait=False**来判断用不用等待

至于用来定位的语句：

`element_to_be_clickable((By.CSS_SELECTOR, css))和find_element(By.CSS_SELECTOR, css)`

使用的是seleium的内置函数，用法也超级简单，一学就会。

#### 2.使用通用函数
构造函数当然是为了用的，并且不用写辣么多重复的结构，就比如下面结构相似的四串代码：

确定按钮

`def sure_button(self,wait=False):
    return self.click("#douyin-web-recommend-guide-mask > div > button > span",wait)`
    
检测登录按钮

`def login_button(self,wait=False):
    return self.click("div > div.uotczcdY > div.YoNA2Hyj.qKr0RhiL > svg",wait)`

检测下滑按钮：

`def slide_button(self,wait=False):
    return self.click("div.xgplayer-playswitch-next > span > svg",wait)`

检测“继续观看按钮”

`def look_button(self,wait=False):
    return self.click("div.HDhMLx9a > div > div.oya2IBgA > div.beA0QPV4",wait)`
    
这四个都是不登陆在刷视频的时候会出现的弹窗，其中第一个和第二个都是打开抖音就会弹出，并且在随后的视频中随机出现，第三个是下滑按钮，控制视频下滑，没啥说，最后一个是随机弹出，但好像不影响获取信息，这个如果不影响就可以删除

再来说说这四个代码的构造，都传入两个参数，因为都在class类中，所以第一个参数是self，第一个形参是wait，并赋值False，然后return给click函数中的wait，这样就默认使用不等待的代码，直接点击取消按钮，至于click函数第一个参数，就是使用F12工具进行复制，很简单的

### 二、说一下这个类
这个类很简单，首先定义了一个douyin类，接着定义：

    def __init__(self,url):
        self.browser = webdriver.Chrome(service=service)
        self.browser.get(url)  # 打开一个网页
        self.login_button(wait=True)# 关闭刚开始的登录页面
        self.sure_button(wait=True)

这个函数传入了一个参数
___url___，
这个参数会在最后进行赋值，并且它就是一个网址，接着看看函数主体，***self.browser = webdriver.Chrome(service=service)***
这句是用来唤醒浏览器的，就是你的屏幕上会弹出浏览器弹窗，其中括号中的
___service=service___，是用来确定使用那个驱动的，一般来说，下一个匹配的驱动，配置好环境变量，就不用再规定驱动地址，但我下载好几个，我想指定其中一个，就这样指定***self.browser.get(url)***
这句代码就是用来搜索网页的，当然我们这个网页是抖音的官网

`self.login_button(wait=True)和self.sure_button(wait=True)`

这俩句代码是用来关闭登录页面和另一个页面，刚打开抖音的网页，会弹出登录页面和一个指导页面(网络不好会延迟)，这两个页面是必出现的，所以将这两句放在打开抖音网页之后，当出现取消按钮的时候，就点击，这里设置参数是True,就是可以等待10秒。

**wait=True**把原来默认的的**wait=False**覆盖，就实现了对不同情况的检测那有人就会说了，既然网络会有延迟，那都用等待10秒的，还能剩下好几行代码，这样也可以，但每次都用等待10的，那每个视频都会进行等待，而且我们设置的检测有三道，每次都检测，就是10+10+10=30秒，这样就大大降低了效率

### 三、提取主播名、视频简介、点赞量...

我们又在类中定义了一个函数：

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
                
这些代码就是用来获得信息的，看着好长，但其举行类似，也很简单，这四个类似的代码都使用seleium的内置函数用来查找信息的位置，类似于下面这种句子：

`introduce = self.browser.find_elements(By.CLASS_NAME,'title')`

括号中可以选择不同的方式进行定位，根据实际情况进行选择，比如上面这个，使用的是*By.CLASS_NAME*，这个是使用属性的值，但他的值有两个，如下图所示，只选择一个就行，我就选择了*title*

但要注意我们使用的是find_elements，说明捕获的值不止一个，而introduce是一个数组，也就是可以遍历，遍历然后通过`.get_attribute("textContent")`方法获得文本，如下代码所示：

        for item  in introduce:
            if item.get_attribute("textContent") not in extract['introduce']:
                extract['introduce'].append(item.get_attribute("textContent"))
            else:
                pass
                
其他的信息都只有一层标签可以先定位然后使用.text方法就能获得，但是这个视频简介分布在不同的标签嵌套中，使用`.get_attribute("textContent")`这个方法，只用找到包含所有简介的“最上层标签”，然后用*textContent*，就能获得所有文字，当然这个方法也可以用来提取属性的值

提取到文字之后就需要存入字典中，这就用到代码开头创建的字典，因为抖音的网页设置，每次我们都是捕获三个值，并且有两个是重复的，所以需要设置去重操作，判断是否在字典值的列表中，没有就添加，有就跳过，就是上面if语句执行的代码

这里再说一下，使用不同的选择器，就需要对应的“路径”

例如上面代码：

`By.XPATH,"//span[@class='arnSiSbK ypGAC_xH ONzzdL2F']/span/span/span/span"`

`By.CLASS_NAME,'title'`

或者使用By.Id等等...

四、主程序
主程序就是将所有的定义函数有逻辑的串联起来，代码如下：

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
    
这就是最后一部分代码，没有在class类中，所以不用写形参self，函数的主体开始有一个*time.sleep(3)*，因为刚打开网页抖音有点不稳定，让第一个呈现的视频播放3秒，也方便前期检查Bug，接着是一个死循环，用`num = random.randint(1, 5)`生成一个随机整数，因为在打开网页抖音的时候已经取消了登录页面和指导页面，所以现在正在播放第一个视频，直接用*dou.extract_()*提取相关信息就行，提取完后进行翻页，检测有没有弹出干扰页面：`dou.login_button()dou.look_button()`，接着进行随机停顿，模仿人的操作，然后输出

结果类似下面这种形式：

{'name': ['@风信子'], 'introduce': ['秋天的她 冬天还在吗.#转场展开'], 'like': ['35.7万'], 'comment': ['1.1万'], 'collect': ['1.2万'], 'repost': ['1.6万']}

{'name': ['@风信子', '@恒钧漫剪'], 'introduce': ['秋天的她 冬天还在吗.#转场展开', '二郎真君地位没落 但威严还是有人尊敬的 #神仙剪刀手 #好剧推荐 #好剧推荐 #动漫推荐展开'], 'like': ['35.7万', ''], 'comment': ['1.1万', ''], 'collect': ['1.2万', ''], 'repost': ['1.6万', '']}

{'name': ['@风信子', '@恒钧漫剪', '@流心影者'], 'introduce': ['秋天的她 冬天还在吗.#转场展开', '二郎真君地位没落 但威严还是有人尊敬的 #神仙剪刀手 #好剧推荐 #好剧推荐 #动漫推荐展开', '“杀神”和他那群“狼崽子”#动作电影 #成龙 #了不起的精讲团 #影视万字精讲 #影娱漫谈编辑部展开'], 'like': ['35.7万', '', '1.5万'], 'comment': ['1.1万', '', '73'], 'collect': ['1.2万', '', '1590'], 'repost': ['1.6万', '', '447']}

{'name': ['@风信子', '@恒钧漫剪', '@流心影者', '@燕燕娱星'], 'introduce': ['秋天的她 冬天还在吗.#转场展开', '二郎真君地位没落 但威严还是有人尊敬的 #神仙剪刀手 #好剧推荐 #好剧推荐 #动漫推荐展开', '“杀神”和他那群“狼崽子”#动作电影 #成龙 #了不起的精讲团 #影视万字精讲 #影娱漫谈编辑部展开', 'wx全网四大肉身成圣的博主，每一个都是人类的最终形态#蘑菇哥 #良子 #珍妮佛梓 #萝卜头 #离谱展开'], 'like': ['35.7万', '', '1.5万', '14.9万'], 'comment': ['1.1万', '', '73', '4274'], 'collect': ['1.2万', '', '1590', '2.7万'], 'repost': ['1.6万', '', '447', '1.1万']}


如果遇到直播的会直接跳过

​
