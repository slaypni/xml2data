# -*- coding: utf-8 -*-

import unittest
from xml2data import urlopen, Parser


class Xml2DataTestCase(unittest.TestCase):

    def test_urlopen(self):
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
                      'url':'./onair.html',
                      'description': '現在放送中のテレビ番組のタイトルを一覧表示'}],
            'author': 'slay',
            'twitter': 'http://twitter.com/slaypni'
        }

        data = urlopen(url=url, format=format)
        self.assertEqual(data, answer)


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
        self.assertEqual(Parser.parse('div#caption', html), 'abc') # abbreviation
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
                         
        
