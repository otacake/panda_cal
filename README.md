<h1>これは何？</h1>

PandAのまだやっていない課題をGoogleカレンダーに登録してくれるものです。</p>
こう書くとかっこいいですが実際はPandAをひたすらスクレイピングしてひたすらカレンダーに書き込むだけです。
しかもほぼ自分用なので正直どれくらい役立つか全くわかりません。
それでもよければ使ってやってください。喜びます。
</p>
<strong>2020/06/13追記</strong>
どうやらPandAにはAPIがあるっぽいので、スクレイピングではなくAPIから課題情報を取得できるようにしたいと考えています。

<h1>具体的な使い方</h1>
pythonの環境とは別に、GoogleカレンダーAPIを取得する必要があります。
GoogleカレンダーAPIの取得方法については<a href = "https://qiita.com/hajime_migi/items/d7d0a310995a99297e80">こちら</a>を参考にするのが良いでしょう。
また、適宜モジュールをimportする必要があると思います。モジュールがない場合はpipまたはcondaでインストールしてください。
インストールの具体的な方法は各自Qiitaや公式ドキュメントを参考にしてください

<h1>使用上の注意とか</h1>
使用は全て<strong>自己責任</strong>でお願いします。
<strong>このプログラムの使用により生じるいかなる不具合にも作成者は責任を負いかねます。</strong>
webスクレイピングはサーバーに大きな負担を与える可能性もあります。
time.sleep()関数などを使って処理を何度か止めるようにしましょう。
</p>
基本的には自由に使ってもらってかまいません。
いいのができたら<a href="https://twitter.com/shima_shima_ss">作成者</a>にぜひ見せてください。喜びます。
よろしくお願い致します。
