import sys, fitz
import datetime
from cnocr import CnOcr
import pandas as pd
import os
import paddle
from paddlenlp.transformers import ErnieTokenizer, ErnieForSequenceClassification
from type_identifier import type_identifier
from image_to_text import image_to_text
from pdf_to_image import pyMuPDF_fitz
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

SOURCE_LINK = "https://www.sse.com.cn"
YOUR_DRIVER_PATH = "your_driver_path"
FILE_NUM = None """你想要扒第一页前多少个"""
"""_summary_ 把pdflink下载到download_dir, 检查是否有重复的了，如果有了就把重复的删除
"""
def download_pdfs(pdf_link, pdf_name, driver, download_dir):
    new_file_path = None
    try:
        # 去pdf链接
        past_files = os.listdir(download_dir)
        print(past_files)
        driver.get(f"{pdf_link}")
        #等下载
        time.sleep(2)
        
        # 确认下载
        # Verify download
        downloaded_files = os.listdir(download_dir)
        print(downloaded_files)
        new_file = None
        for file in downloaded_files:
            if file not in past_files:
                new_file = file
        if new_file:
            # Get the first downloaded file
            original_file = os.path.join(download_dir, new_file)
            print("original_file:",original_file)
            
            # Wait for download to complete if it's a .crdownload file
            while original_file.endswith('.crdownload'):
                time.sleep(1)  # Wait for download to finish
                downloaded_files = os.listdir(download_dir)
                new_file = None
                for file in downloaded_files:
                    if file not in past_files:
                        new_file = file
                original_file = os.path.join(download_dir, new_file)
            
            # Define new file name
            new_file_path = os.path.join(download_dir, pdf_name+".pdf")
            
            # Check if new_file_name already exists in the directory
            if os.path.exists(new_file_path):
                print(f"'{pdf_name}' 已经存在了，只保留一个")
                os.remove(original_file)
            else:
                # Rename the file if the target name doesn't exist
                os.rename(original_file, new_file_path)
                print(f"把乱码文件名改为{new_file_path}")
        else:
            print("程序开始后还没下载任何pdf呢")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        return new_file_path

final_result = pd.DataFrame(columns=['名称','链接','是否达到要求','成分'])

all_pdf_links = []
# 下载路径，就下载到本程序的包里面，如果需要随时改
download_dir = os.path.abspath("./all_pdfs/")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = webdriver.ChromeOptions()

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # Download PDF instead of opening
}

chrome_options.add_experimental_option("prefs", prefs)

# Initialize WebDriver with options
driver = webdriver.Chrome(
    service=Service(executable_path = "YOUR_DRIVER_PATH"),#这里要改
    options=chrome_options
)


driver.get(SOURCE_LINK+"/regulation/members/measures/")
div_text = "/html/body/div[8]/div/div[2]/div/div/div[1]/div[2]/table/tbody[2]/tr"
tr_elements = driver.find_elements(By.XPATH, "/html/body/div[8]/div/div[2]/div/div/div[1]/div[2]/table/tbody[2]/tr")
for i in range(len(tr_elements)):
    specific_a_tag = driver.find_element(By.XPATH, f"{div_text}[{i+1}]/td[2]/div/a")
    pdf_name = driver.find_element(By.XPATH, f"{div_text}[{i+1}]/td[3]").text + driver.find_element(By.XPATH, f"{div_text}[{i+1}]/td[4]").text
    # Get the href attribute
    href = specific_a_tag.get_attribute("href")
    all_pdf_links.append((href,pdf_name))
print(all_pdf_links)
time.sleep(5)
tracker = 0
for pdf_link,pdf_name in all_pdf_links:
    # download pdf
    new_file_path = download_pdfs(pdf_link=pdf_link,
                  pdf_name=pdf_name,
                  driver = driver, download_dir = download_dir)
    print("downloaded", new_file_path)
    pageCount = pyMuPDF_fitz(download_dir=download_dir, article_name = pdf_name, imagePath = './pdfimages')
    image_to_text(download_dir="./", article_name=pdf_name, pages = pageCount)
    component = type_identifier(download_dir="./",article_name=pdf_name)
    selected = '否'
    component_str = ""
    print(f"{pdf_name}警告类型识别结果：")
    for warning, result in component.items():
        print(f"{warning}: {result}")
        component_str += f'{warning}: {result}\n'
        if result[0] == "是":
            print("符合审查结果")
            selected = '是'
    res = pd.DataFrame([{'名称':pdf_name,'链接':pdf_link,'是否达到要求':selected,'成分':component_str}])
    final_result = pd.concat([final_result, res], ignore_index=True)
    '''
    tracker += 1
    if tracker == FILE_NUM:
        break
    '''
    '''
    # 如果只需要头一个文件, 加个break就行
    break
    '''
final_result.to_excel("./汇总.xlsx")
