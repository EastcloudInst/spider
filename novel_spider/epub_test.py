from ebooklib import epub
from utils import creat_toc_ncx, myEpubHtml

# 创建 EPUB 书籍
book = epub.EpubBook()
book.set_identifier('id123456')
book.set_title('My Book Title')
book.set_language('en')

# 创建一个章节
chapter1 = epub.EpubHtml(title='Chapter 1', file_name='chapter1.xhtml', lang='en')
chapter1.content = '''
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8"/>
    <style>@font-face{font-family:read; font-display:block; src: url('fonts/read.woff2') format('woff2');} #TextContent p:last-of-type{font-family: "read" !important;}</style>
</head>
<body>
    <h1>序章</h1>
    <div id="TextContent">
        <p>毫无男女间的紧张感嘛。</p>
        <p>要惹你生气或难过，是不是根本不可能啊？</p>
        <p>那子，是不是不够格当女主角啊……？</p>
        <p>「啊～～关于那个的话，你放心吧。」</p>
        <p>你那不行吧，加藤？</p>
        <p>不踏出脚步，是无法往前进的喔。</p>
        <p>「因为你从现在起，每天放学以后都要和我一起过了。」</p>
        <p>「这是告白？」</p>
        <p>「果你那，然后表现得动摇一点怎么？」</p>
        <p>加藤的表情，又逐渐变得像昨天那淡白。</p>
        <p>「我在此郑重宣布，加藤！」</p>
        <p>「唔……嗯？」</p>
        <p>因此，感觉到苗头不对的我，打算硬将话题带下去……</p>
        <p>「我要将你——栽培成令人心动得小鹿乱撞的一女主角！」</p>
        <p>「…………」</p>
        <p>「……说点话吧。」</p>
        <p>「……我要说什么才好？」</p>
        <p>我打算硬将话题带下去，结果她是和昨天一，脸上变得越来越没有个。</p>
        <p>「总……总之，这个给你！你看看这个！」</p>
        <p>「情书？」</p>
        <p>「我就说了，果你那的话，是不是可以来个更有戏剧的反应啊？」</p>
        <p>「……企画书？」</p>
        <p>「你都可以不在乎别人反应继续话说下去耶。」</p>
        <p>「……欸，这什么啊？」</p>
        <p>标题：</p>
        <p>未定（小惠惠的甜蜜暑假？）</p>
        <p>类型：</p>
        <p>未定（恋爱AVG、恋爱SLG、桌面小程式）</p>
        <p>品概念：</p>
        <p>特写彻底放在本的一女主角加藤惠身上，</p>
        <p>令她将魅力发挥到极限就是唯一的最高目标。</p>
        <p>「就说是企画书啦，少女游戏的企画书。」</p>
        <p>「…………」</p>
        <p>「话虽此，我没有钱也没有人脉让这个变成商业，所以应该算同人品吧。」</p>
        <p>「…………」</p>
        <p>「而且，它就是来将『加藤惠』这个角色，打造成魅力女星的手段。」</p>
        <p>「……我觉得你这些话听起来超瞎的，是我自己品味过时的关系吗？」</p>
        <p>「不要紧，我也有稍微搞砸的感觉。」</p>
        <p>「才稍微而已啊……」</p>
        <p>「有，在下一页有更详细一点的设定……」</p>
        <p>角色设定：</p>
        <p>加藤惠（化名）</p>
        <p>一女主角。在樱花飞舞的坡上遇见的少女。</p>
        <p>丰之崎学园二年级。</p>
        <p>身高：由本人填写。</p>
        <p>体重：由本人填写。</p>
        <p>围：由本人填写。</p>
        <p>腰围：由本人填写。</p>
        <p>围：由本人填写。</p>
        <p>兴趣：由本人填写。</p>
        <p>专长：由本人填写。</p>
        <p>自我期望：虽然有点不好意思，我会拚命努力的。请大家为我加油喔♪</p>
        <p>「……欸。」</p>
        <p>「……怎么了吗？」</p>
        <p>「上面提到的体重和三围之类，是要我写吗？由我自己写？」</p>
        <p>「哎呀，那部分的资料我实在不会有嘛。」</p>
        <p>「这行为不是叫扰？」</p>
        <p>「说那什么话，你接下来就要成为少女游戏的女主角啰。这可不是介意个人情报的时候了喔。」</p>
        <p>「……虽然我吐槽的点多得不胜枚举，先告诉我为什么有感言的部分写好了？而且语尾加了♪。」</p>
        <p>「我能代你表达心情而已。」</p>
        <p>「……安艺，你有握我今天会原谅你，对不对？」</p>
        <p>「像加藤这么善解人意的女生，我最喜欢了。」</p>
        <p>「也许我有点误判你的厚脸皮程度了。」</p>
        <p>「看吧，你果然不生气也不害羞，简直完！」</p>
        <p>即使问一句「可不可以跟我上个床？」，似乎也可以当玩笑话带过。</p>
        <p>唉，虽然症结就是出在她那个。</p>
        <p>像这个时候，女生要不就大发脾气、要不就放声哭出来，才能立竿见影地勾起男方的罪恶感或保护嘛……从少女游戏的观点而言。</p>
        <p>「欸，加藤……所以你要不要和我一起这个当成目标？」</p>
        <p>「所以是，什么当目标？」</p>
        <p>「少女游戏的女主角。」</p>
        <p>「…………」</p>
        <p>「可爱、角色鲜明、而且充满魅力，让任何人玩过游戏都会当成『自己的新娘』，你要不要像那，当个最有人气的女主角？」</p>
        <p>「抱歉，我是不太懂你的意思。」</p>
        <p>「嗯，我能明白你犹豫不前的心情。毕竟我自己也有点没头没脑地就豁出去了。」</p>
        <p>「既然你明白的话，我希望你可以踩刹车耶。」</p>
        <p>「即使此，即使此我是……！」</p>
        <p>「安……安艺？」</p>
        <p>「我是……将你塑造成女主角。我要制一款由『加藤惠』这个女孩子领衔主演的游戏！」</p>
        <p>面对我满怀热忱的呐喊，加藤露出稍微不那么淡白的目光，将话听了进去。</p>
        <p>「……为什么？」</p>
        <p>附带一提，我们在上学途中。</p>
        <p>「你昨天说过吧。你说我的角色不够鲜明，而且不上不下。」</p>
        <p>但是不要紧。上课钟快响了，所以周围一个同学也没有。</p>
        <p>……嗯，好像也不是不要紧啦。</p>
        <p>「可是安艺，为什么你这么坚持要找我？」</p>
        <p>「那是因为……」</p>
        <p>我从遇见你的时候就被吸引了。</p>
        <p>再次碰面的时候，梦曾经因而破灭。</p>
        <p>然而，我无法就此放弃。</p>
        <p>无论闭上几次眼睛，在我眼底……</p>
        <p>都会浮现那时候穿着白色洋装的你。</p>
        <p>然后那身影，和眼前穿着制服的你相叠。</p>
        <p>……和站在那家伙旁边笑着的你，身影相叠。</p>
        <p>我无法再欺骗自己的感情。</p>
        <p>就算你眼中并没有我。</p>
        <p>所以，我要证明。</p>
        <p>证明我们在那棵樱花树下相遇，是对的。</p>
        <p>证明对我来说、对你来说，那都是命中注定。</p>
        <p>证明我有希望，和你这的女生成为情侣。</p>
        <p>证明你有一天，会这的我当成男人。</p>
        <p>「像这，下一页写了男主角的独白，你觉得何？」</p>
        <p>「安艺，你真的有心邀我加入吗？」</p>
        <p>「嗯～～果然提到女主角以前的男人不太妙对吧？对于有处女情结的脑残并不讨好……」</p>
        <p>「我都说听不懂你的意思了嘛。」</p>
        <p>今天的涉，就这么以失败告终。</p>
        <p>因为过几秒以后，远远听见上课钟响起的我们便匆促结束涉，脸色发青地冲向学校了。</p>
        <p>不过，即使此我仍不悲观。</p>
        <p>从一始我就不觉得花两三天就能够说服她。</p>
        <p>接下来我会每天死缠烂打地涉，就算花上几个星期、几个月，也绝对要让加藤回心转意。</p>
        <p>我绝对不会放弃的，加藤……</p>
        <p>※ ※ ※</p>
        <p>接着，又隔一天的早上。</p>
        <p>「啊，安艺。我昨天过了，果是要放学后一起活动的话，反正我目前既没有参加社团、也没有打工，又不打算那么拚命功，那就奉陪啰。」</p>
        <p>「加藤，你……好讲话也该有个限度吧。」</p>
        <p>爹，屎式继垢亢喳吕评矩。</p>
    </div>
</body>
</html>
'''
# 添加 XHTML 文件
html_item = myEpubHtml(title='Chapter1', uid="html_chapter", file_name="chapter1.xhtml", media_type="application/xhtml+xml", content=chapter1.content.encode('utf-8'))
book.add_item(html_item)

chapter2 = epub.EpubHtml(title='Chapter 2', file_name='chapter2.xhtml', lang='en')
chapter2.content = '<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Chapter 2</h1><p>This is the first chapter.</p></body></html>'
book.add_item(chapter2)

# 添加章节到导航项和 spine（章节顺序）
book.toc = (html_item, chapter2)
book.spine = ['nav', html_item, chapter2]

# content = ({'text': 'chapter 1', 'content': 'chapter1.xhtml'}, {'text': 'chapter 2', 'content': 'chapter2.xhtml'})
# creat_toc_ncx('id123456',content)
# # 添加手动生成的 toc.ncx 文件
# toc_ncx_item = epub.EpubItem(uid='ncx', file_name='toc.ncx', media_type='application/x-dtbncx+xml', content=open('toc.ncx', 'rb').read())
# book.add_item(toc_ncx_item)

# 自动生成 toc.ncx
# book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# 添加字体文件到EPUB
book.add_item(epub.EpubItem(uid="font_woff2", file_name="fonts/read.woff2", media_type="application/font-woff2", content=open("read.woff2", "rb").read()))


# 设置 CSS 样式
style = 'body { font-family: Arial, sans-serif; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="styles/nav.css", media_type="text/css", content=style)
book.add_item(nav_css)

# 输出 EPUB 文件
epub.write_epub('MyBook.epub', book, {})
