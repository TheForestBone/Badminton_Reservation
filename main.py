import time
import requests 
import schedule
from aip import AipOcr # pip install baidu-aip
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  # 这部分是下拉框
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler


dict = {
    'account': '202211964',  # 学号
    'pwd': 'wangrui0226*',  # 密码
    'date' : '2024-12-05',
    'time' : '18:00-20:00',
    'event' : '综合体育馆乒乓球',
    'field' : '3',
    'booking hour' : 17,  # 预约小时
    'booking min' : 36, # 预约分钟,例如12:00整开始预约
}

baidu_dict = {
        'image path' : 'C:/Users/dyc63/Desktop/', # 验证码保存位置
        'APP_ID' : '46730544',  # 百度图像识别的APP_ID,这个默认是我的,但请不要一直用,我会吃不起饭的
        'API_KEY' : 'kBybLiI9aFhu1CG0iOCKQalT',
        'SECRET_KEY' : 'C19FARkGVuxSufCGe1QhQcGYEuuITtIG',
}

driver = webdriver.Edge()
driver.get(r'https://pass.sdu.edu.cn/cas/login?service=https%3A%2F%2Fservice.sdu.edu.cn%2Ftp_up%2F')
# 山大官网

# 将浏览器窗口最大化
driver.maximize_window()

# 找到用户名输入框并输入用户名
username_input = driver.find_element('id', 'un')
username_input.send_keys(dict['account'])  # 改为自己的账号

# 找到密码输入框并输入密码
password_input = driver.find_element('id', 'pd')
password_input.send_keys(dict['pwd'])  # 改为自己的密码

# 找到登录按钮并点击
login_button = driver.find_element('id', 'index_login_btn')
login_button.click()

time.sleep(2)
# 找到服务大厅链接并点击
# 等待元素在页面上出现
wait = WebDriverWait(driver, 2)  # 根据需要调整超时时间
service_hall_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '服务大厅')))

# 找到服务大厅链接并点击
service_hall_link.click()

# 等待元素在页面上出现
search_input = wait.until(EC.presence_of_element_located((By.ID, 'text_SearchService')))

# 找到搜索框元素
search_input = driver.find_element('id', 'text_SearchService')

# 输入搜索词（体育场馆预约）
search_input.send_keys('体育场馆预约')

# 模拟按下回车键，触发搜索
search_input.send_keys(Keys.RETURN)

print('正在点击体育场馆预约按钮🔘......')
def task():
    element1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, 
            '/html/body/div[1]/div[2]/div[13]/div/div[1]/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[2]/img')))
    element1.click()

    print('正在切换到iframe......')

    element2 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'formIframe')))

    # 切换到此iframe中
    driver.switch_to.frame(element2)

    print('正在点击这个iframe🔘......')

    # 等待元素可见
    element3 = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="body_0"]/div[1]/div[2]/div[2]/div/button')))

    # 使用JavaScript模拟点击
    element3.click()

    # 实例化select

    s1 = wait.until(EC.presence_of_element_located((By.ID, 'JHYYSJ')))  # 计划预约时间
    driver.execute_script('arguments[0].style.display = "block";', s1)
    Select(s1).select_by_visible_text(dict['date'])

    s2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'XZSYSD')))  # 选择预约时段
    driver.execute_script('arguments[0].style.display = "block";', s2)
    time.sleep(0.1)
    Select(s2).select_by_value(dict['date'] + dict['time'])

    s3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'CGLX')))  # 场馆类型
    driver.execute_script('arguments[0].style.display = "block";', s3)
    time.sleep(0.1)
    Select(s3).select_by_value(dict['date'] + dict['time'] + dict['event'])

    s4 = wait.until(EC.presence_of_element_located((By.ID, 'CGBH')))  # 场馆编号
    driver.execute_script('arguments[0].style.display = "block";', s4)
    Select(s4).select_by_visible_text(dict['field'])

    s5 = wait.until(EC.presence_of_element_located((By.ID, 'RYLX')))
    driver.execute_script('arguments[0].style.display = "block";', s5)
    s1.send_keys('学生')

    # 退出iframe并返回到主页面
    driver.switch_to.default_content()

    # 提交申请
    button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "commit"))
    )

    button.click()
    print('此处进行到提交申请')

    # 如下是验证码部分
    element = wait.until(EC.presence_of_element_located((By.ID, 'applyCodeImage')))

    left = int(element.location['x'] + 600)  # 获取图片左上角坐标x
    top = int(element.location['y'] + 250)
    right = int(left + 150)
    bottom = int(top + 100)  # 获取图片右下角y

    print('此处进行到获取验证码')
    # 通过Image处理图像

    current_dir = baidu_dict['image path']
    path1 = current_dir + 'test.png'  # 生成随机文件名
    path2 = current_dir + 'test2.png'
    path3 = current_dir + 'converted.png'

    driver.save_screenshot(path1)  # 截取当前窗口并保存图片
    im = Image.open(path1)  # 打开图片
    im2 = im.crop((left, top, right, bottom))  # 截图验证码
    im2.save(path2)  # 保存验证码图片
    print('图片保存完毕')
    print(left, top, right, bottom)

    # 使用百度API识别验证码
    def get_code():
        #  这部分是用的我的百度API，不知道什么时候会限流，到时候可能会开发一个APP让使用者填写自己的API

        client = AipOcr(baidu_dict['APP_ID'], baidu_dict['API_KEY'], baidu_dict['SECRET_KEY'])  # 百度API文档中提供的方法识别文字

        # 由于我处理的验证码图片没有太多的线条，所以直接采用灰度是验证码数字更加清晰，具体的处理方式可根据验证码的实际情况而定
        im1 = Image.open(path2)
        # 转换为灰度图像
        im11 = im1.convert('L')
        im11.save(path3)

        # 读取图片，应为百度API中提供的方法参数只能是字节流
        with open(path3, 'rb') as f:
            image = f.read()
        # 使用API中提供的方法识别验证码并返回验证码
        code = client.basicGeneral(image)

        print(code['words_result'][0]['words'])
        return code['words_result'][0]['words']

    number = get_code()

    s1 = wait.until(EC.presence_of_element_located((By.ID, 'applyCode')))
    s1.send_keys(number)

    s1 = wait.until(EC.presence_of_element_located((By.ID, 'fp_apply_code_apply')))
    # s1.click()
    # 这部分不要直接提交了,不然重复预约会被退学.

scheduler = BlockingScheduler()

# 使用 'cron' 触发器，在每天的 16:45 执行任务
scheduler.add_job(task, 'cron', hour=dict['booking hour'], minute=dict['booking min'])
scheduler.start()
