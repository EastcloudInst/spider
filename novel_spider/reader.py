import os
from typing import Union
def get_content(book: str, vol: Union[str, int], chapter: Union[str, int], prefix='catalogs'):
    if isinstance(vol, int):
        vol = f'第{vol}卷'
    if isinstance(chapter, int):
        chapter = f'第{chapter}话.html'
        
    # 指定文件路径
    file_path = os.path.join(prefix, book, vol, chapter)
    print(file_path)

    try:
        # 打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取整个文件内容
            content = file.read()
            # print(content)
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到，请检查路径是否正确。")
    except IOError:
        print(f"发生I/O错误，无法读取文件 {file_path}。")

    return content