import xml.etree.ElementTree as ET
from ebooklib import epub
from six import b
import ebooklib

class myEpubHtml(epub.EpubHtml):
    # _template_name = 'chapter'

    def __init__(self, uid=None, file_name='', media_type='', content=None, title='',
                 lang=None, direction=None, media_overlay=None, media_duration=None):
        super(myEpubHtml, self).__init__(uid, file_name, media_type, content)

        self.title = title
        self.lang = lang
        self.direction = direction

        self.media_overlay = media_overlay
        self.media_duration = media_duration

        self.links = []
        self.properties = []
        self.pages = []
    
    def get_content(self, default=None):
        return self.content

    def get_body_content(self):
        return self.content

from fontTools.ttLib import woff2
from fontTools.ttLib import TTFont
import time

def woff2ttf(input_path):
    # 定义 WOFF2 文件和输出的 TTF 文件路径
    input_woff2_file = input_path
    output_ttf_file = 'read.ttf'

    # 使用 fonttools 进行解压缩
    woff2.decompress(input_woff2_file, output_ttf_file)

    print(f'WOFF2 文件已转换为 TTF 文件: {output_ttf_file}')

def show_ttf(ttf_path):
    # 打开并读取 TTF 文件
    font = TTFont(ttf_path)

    # 打印基本的字体信息
    print("Font family name:", font['name'].getName(1, 3, 1).toStr())
    print("Font subfamily name:", font['name'].getName(2, 3, 1).toStr())

    # 访问字符映射表 (CMap)
    cmap = font['cmap'].getcmap(0, 0).cmap

    # 打印所有的字符映射
    print("\nCharacter Map (CMap):")
    i = 0
    for codepoint, name in cmap.items():
        tmp = f'uni{codepoint:04x}'
        # and f'{codepoint:04x}' == 'e721'
        if not tmp == name and f'{codepoint:04x}' == 'e721':
            print(f"U+{codepoint:04X}: {name}")
            i = i + 1
        if i == 50:
            # time.sleep(1)
            i = 0
            
    # 示例：查找特定字符的 Unicode 编码
    glyph_name = 'c'
    for codepoint, name in cmap.items():
        if name == glyph_name:
            print(f"\nThe character '{glyph_name}' is mapped to Unicode codepoint U+{codepoint:04X}")

    # 关闭字体文件
    font.close()

if __name__=='__main__':
   debug_path = 'spider/novel_spider/'
   show_ttf('read.ttf')


