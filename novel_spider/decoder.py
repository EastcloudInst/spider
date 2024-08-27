import re
import os
import json

def get_docoder_dict():
    # 给定的文本
    text = '0(1 2("","3"),"的").0(1 2("","3"),"一").0(1 2("","3"),"是").0(1 2("","3"),"了").0(1 2("","3"),"我").0(1 2("","3"),"不").0(1 2("","3"),"人").0(1 2("","3"),"在").0(1 2("","3"),"他").0(1 2("","3"),"有").0(1 2("","3"),"这").0(1 2("","3"),"个").0(1 2("","3"),"上").0(1 2("","3"),"们").0(1 2("","3"),"来").0(1 2("","3"),"到").0(1 2("","3"),"时").0(1 2("","3"),"大").0(1 2("","3"),"地").0(1 2("","3"),"为").0(1 2("","3"),"子").0(1 2("","3"),"中").0(1 2("","3"),"你").0(1 2("","3"),"说").0(1 2("","3"),"生").0(1 2("","3"),"国").0(1 2("","3"),"年").0(1 2("","3"),"着").0(1 2("","3"),"就").0(1 2("","3"),"那").0(1 2("","3"),"和").0(1 2("","3"),"要").0(1 2("","3"),"她").0(1 2("","3"),"出").0(1 2("","3"),"也").0(1 2("","3"),"得").0(1 2("","3"),"里").0(1 2("","3"),"后").0(1 2("","3"),"自").0(1 2("","3"),"以").0(1 2("","3"),"会").0(1 2("","3"),"家").0(1 2("","3"),"可").0(1 2("","3"),"下").0(1 2("","3"),"而").0(1 2("","3"),"过").0(1 2("","3"),"天").0(1 2("","3"),"去").0(1 2("","3"),"能").0(1 2("","3"),"对").0(1 2("","3"),"小").0(1 2("","3"),"多").0(1 2("","3"),"然").0(1 2("","3"),"于").0(1 2("","3"),"心").0(1 2("","3"),"学").0(1 2("","3"),"么").0(1 2("","3"),"之").0(1 2("","3"),"都").0(1 2("","3"),"好").0(1 2("","3"),"看").0(1 2("","3"),"起").0(1 2("","3"),"发").0(1 2("","3"),"当").0(1 2("","3"),"没").0(1 2("","3"),"成").0(1 2("","3"),"只").0(1 2("","3"),"如").0(1 2("","3"),"事").0(1 2("","3"),"把").0(1 2("","3"),"还").0(1 2("","3"),"用").0(1 2("","3"),"第").0(1 2("","3"),"样").0(1 2("","3"),"道").0(1 2("","3"),"想").0(1 2("","3"),"作").0(1 2("","3"),"种").0(1 2("","3"),"开").0(1 2("","3"),"美").0(1 2("","3"),"乳").0(1 2("","3"),"阴").0(1 2("","3"),"液").0(1 2("","3"),"茎").0(1 2("","3"),"欲").0(1 2("","3"),"呻").0(1 2("","3"),"肉").0(1 2("","3"),"交").0(1 2("","3"),"性").0(1 2("","3"),"胸").0(1 2("","3"),"私").0(1 2("","3"),"穴").0(1 2("","3"),"淫").0(1 2("","3"),"臀").0(1 2("","3"),"舔").0(1 2("","3"),"射").0(1 2("","3"),"脱").0(1 2("","3"),"裸").0(1 2("","3"),"骚").0(1 2("","3"),"唇")'

    # 正则表达式匹配键值对
    matches = re.findall(r'0\(1 2\("(.+?)","3"\),"(.+?)"\)', text)

    # 将匹配结果转换为字典
    decoder_dict = {key: value for key, value in matches}

    # print(decoder_dict)

    return decoder_dict

def decoder(text):
    decoder_dict = get_docoder_dict()
    str_list = list(text)
    i = 0
    for t in text:
        if t in decoder_dict:
            t = decoder_dict[t]
            str_list[i] = t
        i = i + 1
    return ''.join(str_list)

def decode_css_content(content):
    decode_dict_path = 'decode_dict.json'
    with open(decode_dict_path, 'r', encoding='utf-8') as f:
        decode_dict = json.load(f)
    decode_content = ''
    for c in content:
        # UTF-8 字节序列
        utf8_bytes = c.encode('utf-8')

        # 将 UTF-8 字节解码为 Unicode 编码点
        unicode_char = utf8_bytes.decode('utf-8')
        unicode_code_point = ord(unicode_char)
        unicode_key = f"{unicode_code_point:x}"
        if unicode_key in decode_dict:
            decode_content = decode_content + decode_dict[unicode_key]
        elif unicode_code_point >= 57344 and unicode_code_point <= 63743:
            decode_content = decode_content + '*'
    print(f"decoded result is: {decode_content}")
    return decode_content
        


def get_encode_content(content):
    new_data = []
    for c in content:
        # UTF-8 字节序列
        utf8_bytes = c.encode('utf-8')

        # 将 UTF-8 字节解码为 Unicode 编码点
        unicode_char = utf8_bytes.decode('utf-8')
        unicode_code_point = ord(unicode_char)

        # 输出 Unicode 编码点
        # print(f"Unicode 编码点: {unicode_code_point}, U+{unicode_code_point:X}")

        # 格式化为 "U+XXXX" 形式
        formatted_code_point = f"U+{unicode_code_point:X}"
        # 定义要写入的数据结构
        # 这里选择使用列表，每个元素都是一个包含 "unicode_code_point" 键的字典
        new_entry = {f"{unicode_code_point}": formatted_code_point}
        new_data.append(new_entry)

    # 定义 JSON 文件路径
    json_file = 'unicode_code_points.json'

    # 检查 JSON 文件是否存在
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                # 尝试加载现有的 JSON 数据
                data = json.load(f)
                # 确保数据是一个列表
                # if not isinstance(data, list):
                #     data = []
            except json.JSONDecodeError:
                # 如果文件为空或内容无效，初始化为空列表
                data = []
    else:
        # 如果文件不存在，初始化为空列表
        data = []

    # 将新的编码点条目追加到数据列表中
    data.append(new_data)

    # 将更新后的数据写回 JSON 文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"已将 {formatted_code_point} 追加到 {json_file} 文件中。")
