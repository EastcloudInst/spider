import json

json_file = 'unicode_code_points.json'
encode_data = {}
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for dat in data:
        for da in data:
            for d in da:
                for item in d.items():
                    key = item[0]
                    value = item[1]
                num = int(key)
                if num >= 57344 and num <= 63743:
                    encode_data[key] = value

# 按照key进行排序
sorted_data = dict(sorted(encode_data.items(), key=lambda item: int(item[0])))

# 将排序后的数据保存到JSON文件中
with open('sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=4)

print("数据已按照key的数值大小排序并保存到'sorted_data.json'文件中。")

print(sorted_data)
print(len(sorted_data))