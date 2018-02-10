※ このリポジトリはメンテンスされていません。また、間違いではないもののESC/POSにとって無駄なコマンドが含まれます。 https://booth.pm/ja/items/489108 や 続編 https://booth.pm/ja/items/666872 …読もう！

# python-escpos for Japanese

* python-escpos という素晴らしいライブラリ
  * Python3に対応していない
  * 日本語出力に対応していない
  * 直そう
* Python3向けにしました
  * `print`などに加え、`str`と`byte`の区別により変更が必要なところも変えた
  * `Network`を用いた場合のみ
  * 他は未確認
* 日本語対応しました
  * TM-T90でしか動作確認していません
  * 非推奨コマンドを使っているかも
  * プリンターが対応しているけど、出せない文字もある
    * Shift-JISに無い文字は無視することにしたため
	* `㍉`とか
  * 倍幅文字の出力は頑張った
    * 褒めて欲しい


## 変更点

### `set`を分割
* `setAlign`
* `setFont`
* `setType`
* `setWidth`
* `setDensity`

### 日本語出力用メソッドの追加
* `jpInit`
  * Shift-JISコードが効くようにする
* `jpText`
  * 漢字モードをON/OFFして日本語を出力
  * 英数字だけでも普通に使える(と思う。プリンターの仕様に依存)
  * 倍幅文字など、拡大印刷も設定できる


## サンプル
* `sample/receipt`ディレクトリに、58mm幅レシート出力用サンプルあり
* `zenhan`モジュールのインストールが必要


## 参考文献
* http://www.delfi.com/SupportDL/Epson/Manuals/TM-T88IV/Programming%20manual%20APG_1005_receipt.pdf
* (`CONFIDENTIAL`って書いているんですが...)
