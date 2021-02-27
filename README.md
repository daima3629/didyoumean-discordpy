# didyoumean-discordpy
![PyPI](https://img.shields.io/pypi/v/didyoumean-discordpy) [![GitHub license](https://img.shields.io/github/license/daima3629/didyoumean-discordpy)](https://github.com/daima3629/didyoumean-discordpy/blob/master/LICENSE)

## description
[discord.py](https://github.com/Rapptz/discord.py)のcommandsフレームワークの拡張ライブラリです。  
画像のように、間違ったコマンドを打ったとき、似たコマンドが見つかった場合にそのコマンドを表示させることができます。  
![](https://i.imgur.com/HMdXF1I.png)  

デフォルトでは3件まで似たコマンドを表示させることができます。

## how to use
1. インストール
    - `python3 -m pip install didyoumean-discordpy`
    - (Windowsの場合)`py -3 -m pip install didyoumean-discordpy`
2. 拡張機能として追加  
    例:  
    ```python
    bot.load_extension("didyoumean-discordpy")
    ```
これだけで利用することができます。

## modding
このライブラリでは、
- 似たコマンドの最大表示数
- 似たコマンドを表示させるときのメッセージ
を変更することができます。

### set max suggest
[`DidYouMean.max_suggest`](https://github.com/daima3629/didyoumean-discordpy/blob/master/didyoumean-discordpy/main.py#L27-L45)に最大表示数となる値を代入してください。  
例:  
```python
bot.get_cog("DidYouMean").max_suggest = 2
```

### change message generator
まず、[`MessageGenerator`](https://github.com/daima3629/didyoumean-discordpy/blob/master/didyoumean-discordpy/message_generator.py#L6-L40)を継承したクラスを作成してください。  
`send`メソッドをオーバーライドすることで自分好みのメッセージを出すことができます。
その後、[`DidYouMean.set_message_generator`](https://github.com/daima3629/didyoumean-discordpy/blob/master/didyoumean-discordpy/main.py#L27-L45)を使用して自作したメッセージジェネレータを登録します。  
例:  
```python
from didyoumean-discordpy.message_generator import MessageGenerator

class MyMessageGenerator(MessageGenerator):
    async def send(self, ctx):
        # do something...


bot.get_cog("DidYouMean").set_message_generator(MyMessageGenerator)
```

## developers
- daima3629