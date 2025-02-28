import paddle
from paddlenlp.transformers import ErnieTokenizer, ErnieForSequenceClassification
def type_identifier(download_dir, article_name):
    # 提取文件内内容并返回成字符串
    def extract_text_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # start = content.find('<DOCUMENT>') + len('<DOCUMENT>')
                # end = content.find('</DOCUMENT>')
                # if start == -1 or end == -1 or start >= end:
                #     print("Error: <DOCUMENT> or </DOCUMENT> tags not found or malformed.")
                #     return None
                # return content[start:end].strip()
                return content.strip()
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None


    def find_start_end(text):
        i = 0
        j = len(text)-1
        if text.find("上述行为违反了") != -1: #想确定的这个的前面一句话为结尾
          j = text.find("上述行为违反了")
        while i < j and not (text[i]=="。" and text[j]=="。"):
            if text[i] != "。":
                i += 1
            if text[j] != "。":
                j -= 1
        if j < i:
            print("找不到句号")
            return -1
        else:
          return [i,j]

    # F查找警告方式
    def check_warning_type(text, warning):
        if warning in text:
            return 1, f"是，文本提及"
        else:
            prompt = f"文本是否非常明确地指出'{warning}'相关的警告？"
            start_end = find_start_end(text)
            inputs = tokenizer(prompt + "\n\n文本：" + text[start_end[0] + 1:start_end[1] + 1], return_tensors="pd", truncation=True)
            print("starting process")
            with paddle.no_grad():
                outputs = model(**inputs)
                prediction = paddle.nn.functional.softmax(outputs, axis=-1)[0][1].item()
            return prediction > 0.6, f"{'是' if prediction > 0.6 else '否'}，概率: {prediction:.2f}"


    # 提取文件
    file_path = f'{download_dir}p2t/{article_name}.txt'  # Replace with your actual file path
    extracted_text = extract_text_from_file(file_path)

    # if extracted_text:
    #     print("Extracted Text from File:")
    #     print(extracted_text)
    # else:
    #     print("Failed to extract text from file.")
        
    # 初始化Ernie模型
    model_name = "ernie-1.0-base-zh"
    try:
        tokenizer = ErnieTokenizer.from_pretrained(model_name)
        model = ErnieForSequenceClassification.from_pretrained(model_name, num_labels = 2)
    except Exception as e:
        print(f"Error loading model: {e}")
        exit()


    # 识别的警告类型
    warning_types = ["拉抬打压价格", "异常交易", "首次公开","发行证券", "IPO", "虚假申报","询价", "网下询价", "公平交易","首次公开发行证券"]

    # 处理文件形式
    results = {}
    for warning in warning_types:
        is_present, explanation = check_warning_type(extracted_text, warning)
        results[warning] = explanation
    return results



        