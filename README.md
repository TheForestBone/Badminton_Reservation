# Badminton_Reservation
A simple script to help you to book a place for Badminton in Shandong university.

这是一个可以帮你预约山东大学羽毛球场的小脚本程序。

## 注意事项：
- 本代码对于最后的图片验证码是采用的百度api图像识别，所以请注册一个自己的百度api账号，网址如下：
<p align="center"><a href="https://ai.baidu.com/">百度AI开放平台</a></p>

- 关于图像识别部分，采用的方法是截图屏幕图像，并上传到百度进行识别，所以我给定的尺寸可以不太标准，具体部分如下：
```
    left = int(element.location['x'] + 600)  # 获取图片左上角坐标x
    top = int(element.location['y'] + 250)
    right = int(left + 150)
    bottom = int(top + 100)  # 获取图片右下角y
```
这部分的数值建议大家根据自己的电脑分辨率自行调整，一旦设置好就不会再更改。

**希望大家多多运动，强身健体，为祖国健康工作五十年！**
