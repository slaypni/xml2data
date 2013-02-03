# -*- coding: utf-8 -*-

import unittest
from xml2data import urlload, load, loads, Parser
from minimock import restore, Mock
from StringIO import StringIO


class Xml2DataTestCase(unittest.TestCase):

    def patch_urllib2(self):
        class ResStub():
            def __init__(self):
                self.text = StringIO(_PUNILABO_HTML)
                self.__iter__ = self.text.__iter__
                self.next = self.text.next

            def info(self):
                return {
                    'Content-Type': 'text/html'
                }

        import urllib2
        urllib2.urlopen = Mock('urllib2.urlopen')
        urllib2.urlopen.mock_returns = ResStub()

    def unpatch_urllib2(self):
        restore()

    url = 'http://hp.vector.co.jp/authors/VA038583/'
    format = """
        {'apps': [html body div#doc div#main-container div.section:first-child
                 div.goods-container div.goods @ {
            'name': div.top span.name $text,
            'version': div.top span.version $text,
            'url': div.top span.name h3 a $[href],
            'description': div.goods div.bottom $text
            }],
         'author': html body div#doc div#main-container div.section div.text p a:first-child $text,
         'twitter': html body div#doc div#main-container div.section div.text p a:nth-child(2) $[href]
        }
    """
    answer = {
        'apps': [{'name': 'copipex', 'version': 'ver 0.2.3', 
                  'url': './down/copipex023.zip',
                  'description': '<コピー⇒貼付け> が <マウスで範囲選択⇒クリック> で可能に'},
                 {'name': 'gummi', 'version': 'ver 0.1.0', 
                  'url': './gummi.html', 
                  'description': 'ウィンドウの任意の部分を別窓に表示。操作も可能'},
                 {'name': 'PAWSE', 'version': 'ver 0.3.2',
                  'url': './down/pawse032.zip',
                  'description': 'Pauseキーで、アプリケーションの一時停止、実行速度の制限が可能に'},
                 {'name': 'onAir', 'version': 'ver 1.2.0',
                  'url': './onair.html',
                  'description': '現在放送中のテレビ番組のタイトルを一覧表示'}],
        'author': 'slay',
        'twitter': 'http://twitter.com/slaypni'
    }

    def test_urlload(self):
        self.patch_urllib2()

        data = urlload(self.url, self.format)
        self.assertEqual(data, self.answer)

        self.unpatch_urllib2()

    def test_load(self):
        data = load(StringIO(_PUNILABO_HTML), self.format)
        self.assertEqual(data, self.answer)

    def test_loads(self):
        data = loads(_PUNILABO_HTML, self.format)
        self.assertEqual(data, self.answer)

        data = loads(_PUNILABO_HTML.decode('shift-jis'), self.format)
        self.assertEqual(data, self.answer)


class ParserTestCase(unittest.TestCase):

    def test_parse_str(self):
        self.assertEqual(Parser.parse("'abc'"), 'abc')
        self.assertEqual(Parser.parse('"123"'), '123')
        self.assertEqual(Parser.parse("''"), '')
        self.assertEqual(Parser.parse("'\\''"), '\'')
        self.assertEqual(Parser.parse("'\\\\'"), '\\\\')
        self.assertEqual(Parser.parse("'\\\\\\''"), '\\\\\'')
        
    def test_parse_num(self):
        self.assertEqual(Parser.parse('123'), 123)
        self.assertEqual(Parser.parse('-123'), -123)

    def test_parse_dict(self):
        self.assertEqual(Parser.parse('{}'), {})
        self.assertEqual(Parser.parse("{' ': 123,}"), {' ': 123})
        self.assertEqual(Parser.parse("""
            {
                'abc': -123,
                ''   : 'xyz'
            }
            """), {'abc': -123, '': 'xyz'})

    @unittest.expectedFailure
    def test_parse_list(self):
        self.assertEqual(Parser.parse('[]'), [])
        self.assertEqual(Parser.parse("['abc',]"), ['abc'])
        self.assertEqual(Parser.parse("['abc', 123]"), ['abc', 123])

    def test_parse_selector(self):
        html = """
            <html>
                <body>
                    <div id='caption'>
                        abc
                    </div>
                    <div id='catalog'>
                        <div class='app'>
                            <a href='http://www.mozilla.jp/firefox/'>FireFox</a>
                            <ul class='os'>
                                <li>Windows</li>
                                <li>Mac</li>
                                <li>Linux</li>
                            </ul>
                        </div>
                        <div class='app'>
                            <a href='http://www.apple.com/safari/'>Safari</a>
                            <ul class='os'>
                                <li>Mac</li>
                            </ul>
                        </div>
                    </div>
                </body>
            </html>"""
        self.assertEqual(Parser.parse('div#caption $text', html), 'abc')
        self.assertEqual(Parser.parse('div#caption', html), 'abc')  # abbreviation
        self.assertEqual(Parser.parse('[div#catalog div.app @ a $text]', html),
                         ['FireFox', 'Safari'])
        self.assertEqual(Parser.parse('[div#catalog div.app @ [ul.os li @ $text]]', html), 
                         [['Windows', 'Mac', 'Linux'], ['Mac']])
        self.assertEqual(Parser.parse('[div#catalog div.app @ a $[href]]', html),
                         ['http://www.mozilla.jp/firefox/',
                          'http://www.apple.com/safari/'])
        self.assertEqual(Parser.parse("""
            {
                'caption': div#caption,
                'apps' : [div#catalog div.app @ {
                    'name': a $text,
                    'link': a $[href]
                }]
            }
            """, html),
            {
                'caption': 'abc',
                'apps': [
                    {
                        'name': 'FireFox',
                        'link': 'http://www.mozilla.jp/firefox/'
                    },
                    {
                        'name': 'Safari',
                        'link': 'http://www.apple.com/safari/'
                    }
                ]
            })


_PUNILABO_HTML = u"""<!DOCTYPE html><html><head><title>ぷにラボ - PUNI Laboratory -</title><meta name="viewport" content="width=440"><meta charset="shift-jis"><link rel="stylesheet" type="text/css" href="main.css"></head><style TYPE="text/css"></style><body><div id='doc'><div id='top-container'><div id='top-left-container'><div id='title-container'><div id='title-top'><h1>ぷにラボ</h1></div><div id='title-middle'></div><div id='title-bottom'><h1>PUNI Laboratory</h1></div></div><div id='history-container'><div class='section'><div class='title'>更新履歴</div></div><textarea id='history' readonly>2006/05/05 Webサイト公開</textarea></div></div><div id='top-right-container'><div id='ad-container'><div class='ad-padding top'></div><div style='height: 130px;'></div><div style='height: 54px;'></div><div class='ad-padding bottom'></div></div></div></div><div id='main-container'><div class='section'><div class='title'>ソフトウェア</div><div class='goods-container'><div class='goods'><div class='top'><span class='name'><h3><a href='./down/copipex023.zip'>copipex</a></h3></span><span class='version'>ver 0.2.3</span><span class='platform'>[Windows NT]</span><span><a href='./copipex_history.txt'>history.txt</a></span><span><a href='./copipex_readme.txt'>readme.txt</a></span></div><div class='bottom'>&lt;コピー⇒貼付け&gt; が &lt;マウスで範囲選択⇒クリック&gt; で可能に</div></div><div class='goods'><div class='top'><span class='name'><h3><a href='./gummi.html'>gummi</a></h3></span><span class='version'>ver 0.1.0</span><span class='platform'>[Windows Vista, 7]</span></div><div class='bottom'>ウィンドウの任意の部分を別窓に表示。操作も可能</div></div><div class='goods'><div class='top'><span class='name'><h3><a href='./down/pawse032.zip'>PAWSE</a></h3></span><span class='version'>ver 0.3.2</span><span class='platform'>[Windows NT]</span><span><a href='./pawse_history.txt'>history.txt</a></span><span><a href='./pawse_readme.txt'>readme.txt</a></span></div><div class='bottom'>Pauseキーで、アプリケーションの一時停止、実行速度の制限が可能に</div></div><div class='goods'><div class='top'><span class='name'><h3><a href='./onair.html'>onAir</a></h3></span><span class='version'>ver 1.2.0</span><span class='platform'>[Windows]</span><span style='color:#F20;'>頒布休止中</span></div><div class='bottom'>現在放送中のテレビ番組のタイトルを一覧表示</div></div></div></div><div class='section'><div class='title'>Webサービス</div><div class='goods-container'><div class='goods'><div class='top'><span class='name'><h3><a href='http://chatploo.appspot.com/'>Chatploo</a></h3></span></div><div class='bottom'>シンプルな使い捨てグループチャット</div></div></div></div><div class='section'><div class='title'>ブックマークレット</div><div class='goods-container'><div class='goods'><div class='top'><span class='name'><h3><a href='http://slaypni.appspot.com/anchor_thumbnails_catalog.html'>Anchor Thumbnails Catalog</a></h3></span></div><div class='bottom'>リンク先サイトのサムネイルを一覧表示</div></div><div class='goods'><div class='top'><span class='name'><h3><a href='http://slaypni.appspot.com/anchor_thumbnail_glass.html'>Anchor Thumbnail Glass</a></h3></span></div><div class='bottom'>リンク先サイトのサムネイルをポップアップ表示</div></div></div></div><div class='section'><div class='title'>お知らせ</div><div class='text'><a href="http://www.forest.impress.co.jp/" target="_blank">窓の杜</a>様にて、copipexを<a href="http://www.forest.impress.co.jp/article/2008/07/10/okiniiri.html" target="_blank">紹介</a>していただきましたー。(08/07/10)<br><a href="http://www.forest.impress.co.jp/" target="_blank">窓の杜</a>様にて、PAWSEを<a href="http://www.forest.impress.co.jp/article/2008/06/11/okiniiri.html" target="_blank">紹介</a>していただきましたー。(08/06/11)<br></div></div><div class='section'><div class='title'>このサイトについて</div><div class='text'>自作のソフトウェアの公開・頒布をしてます</div><div class='text'><p>Administrator: <a href='http://www.hatena.ne.jp/slaypni/' style='color:#000;text-decoration: none;'>slay</a> [<a href='http://twitter.com/slaypni'>twitter</a>]</p><p>mail: <span class='mh'>(enable javascript to show address)</span>pc_run.zzn.com</p></div></div></div></div></body><script type='text/javascript' src='//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js'></script><script type="text/javascript">$(function(){$('.mh').text('punilabo@')});</script><script type="text/javascript">var _gaq=_gaq || [];_gaq.push(['_setAccount', 'UA-27471978-1']);_gaq.push(['_trackPageview']);(function(){var ga=document.createElement('script');ga.type='text/javascript';ga.async=true;ga.src=('https:'==document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';var s=document.getElementsByTagName('script')[0];s.parentNode.insertBefore(ga, s);})();</script><script type="text/javascript"><!--var ID="100606759";var AD=4;var FRAME=0;// --></script><script src="./ax.xrea.l.js" type="text/javascript"></script><noscript><a href="http://w1.ax.xrea.com/c.f?id=100606759" target="_blank"><img src="http://w1.ax.xrea.com/l.f?id=100606759&url=X" alt="AX" border="0"></a></noscript></html>""".encode('shift-jis')
