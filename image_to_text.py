from cnocr import CnOcr
import os
def image_to_text(download_dir,article_name,pages):
    file_path = download_dir+"/p2t/" + article_name
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(file_path+".txt","w", encoding='utf-8') as f:
      ocr = CnOcr()         
      n=0

      for n in range(pages):
        i=0
        j=0
        
        image_name=f'./pdfimages/{article_name}/images_'+str(n+1)+'.png'
        res = ocr.ocr(image_name)
        #print(res[0].keys())
        string_list = [ ]
        for i in range(len(res)):
          for j in res[i]["text"]:
            string_list.append(j)
        ocr_result_string = "".join(string_list)
        f.write(ocr_result_string)    #这句话自带文件关闭功能，不需要再写f.close()
        print(f"{article_name}文字转换结束。")
