xml2data
========

xml2data is a Python library for converting xml into native data, according to css-selector like template.

Requirements
------------

Python 2.x


Install
-------

    python setup.py install

Example
-------

the following converts [a webpage](http://hp.vector.co.jp/authors/VA038583/
) containing some app information:

```python
import xml2data
template = """{
  'apps': [div#main-container div.section:first-child div.goods-container div.goods @ {
      'name': div.top span.name,
      'url': div.top span.name a $[href],
      'description': div.goods div.bottom
  }],
  'author': div#main-container div.section div.text p a:first-child $text,
  'twitter': div#main-container div.section div.text p a:nth-child(2) $[href]
}"""
data = xml2data.urlload('http://hp.vector.co.jp/authors/VA038583/', template)
```

results:

```python
data == {
  'apps': [{
      'name': 'copipex',
      'url': './down/copipex023.zip',
      'description': '<コピー⇒貼付け> が <マウスで範囲選択⇒クリック> で可能に'
    }, {
      'name': 'gummi',
      'url': './gummi.html', 
      'description': 'ウィンドウの任意の部分を別窓に表示。操作も可能'
    }, {
      'name': 'PAWSE',
      'url': './down/pawse032.zip',
      'description': 'Pauseキーで、アプリケーションの一時停止、実行速度の制限が可能に'
    }, {
      'name': 'onAir',
      'url': './onair.html',
      'description': '現在放送中のテレビ番組のタイトルを一覧表示'
    }],
  'author': 'slay', 
  'twitter': 'http://twitter.com/slaypni'
}
```
