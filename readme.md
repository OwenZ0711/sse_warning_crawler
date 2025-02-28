此程序可以把上交所监管文案的第一页所有pdf扒下来然后进行监管分类

1. 文件介绍
  synth.py是主程序，进行网络爬虫,文件下载并且输出结果，下载过的文件只会保留一份，文件用机构名称+日期命名
  pdf_to_image.py 把pdf中的文件提取成图像，同一个文件只会留一个版本的图像文件夹
  image_to_text.py 把图像里面的文字扒出来并生成text file，同一个pdf的图像只会生成一个text file，新的会覆盖
  type_identifier.py 识别出第二句话开始到“上述行为违反了”前的最后一句话的内容，如果包含提示词直接选中，不包含的话问预训练模型进行识别

2. 运行方法
需要python >= 3.8

**```pip install -r requirements.txt```**

**```python synth.py```**

3. 关于chromedriver
  chrome driver下载地址为 https://googlechromelabs.github.io/chrome-for-testing/
  然后这个需要和当前chrome版本一致（右上角，设置，关于chrome），目前我用的133版本，如果版本不一致需要更新不然报错
