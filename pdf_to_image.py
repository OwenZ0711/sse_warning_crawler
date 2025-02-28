import sys, fitz
import os
import datetime
 
def pyMuPDF_fitz(download_dir, article_name, imagePath):
    #startTime_pdf2img = datetime.datetime.now() #记个时
    pdfPath = download_dir+"/"+article_name+".pdf"
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 默认图片大小为：792X612
        # 每个尺寸的缩放系数为1.3，生成分辨率提高2.6的图像。
        zoom_x = 1.3       
        zoom_y = 1.3
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # 创建路径
        if not os.path.exists(imagePath):
            os.makedirs(imagePath) 
        if not os.path.exists(imagePath+"/"+article_name):
            os.makedirs(imagePath+"/" + article_name)
            
        pix.save(imagePath+'/'+article_name+"/"f'images_{str(pg+1)}.png')   # 将图片写入指定的文件夹内
        
    # endTime_pdf2img = datetime.datetime.now()
    # print('pdf2img时间=',(endTime_pdf2img - startTime_pdf2img).seconds)
    print(f"{article_name}图片转换结束")
    return pdfDoc.page_count
 
