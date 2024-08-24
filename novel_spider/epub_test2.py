from ebooklib import epub

# 创建 EPUB 书籍
book = epub.EpubBook()
book.set_identifier('id123456')
book.set_title('My Multi-Chapter Book')
book.set_language('en')

# 创建多个章节
chapter1 = epub.EpubHtml(title='Chapter 1', file_name='chapter1.xhtml', lang='en')
chapter1.content = '<h1>Chapter 1</h1><p>This is the first chapter.</p>'
book.add_item(chapter1)

chapter2 = epub.EpubHtml(title='Chapter 2', file_name='chapter2.xhtml', lang='en')
chapter2.content = '<h1>Chapter 2</h1><p>This is the second chapter.</p>'
book.add_item(chapter2)

chapter3 = epub.EpubHtml(title='Chapter 3', file_name='chapter3.xhtml', lang='en')
chapter3.content = '<h1>Chapter 3</h1><p>This is the third chapter.</p>'
book.add_item(chapter3)

# 添加章节到目录（TOC）和 spine（显示顺序）
book.toc = (
    epub.Link('chapter1.xhtml', 'Chapter 1', 'chap_1'),
    epub.Link('chapter2.xhtml', 'Chapter 2', 'chap_2'),
    epub.Link('chapter3.xhtml', 'Chapter 3', 'chap_3')
)

book.spine = ['nav']
book.spine.append(chapter1)
book.spine.append(chapter2)
book.spine.append(chapter3)

# 添加默认的导航文件（必需）
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# 输出 EPUB 文件
epub.write_epub('MyBook.epub', book, {})