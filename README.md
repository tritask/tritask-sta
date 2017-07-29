# tritask-sta
[Tritask](https://github.com/tritask/tritask-spec) のオレオレ実装例です。

![tritasksta_image](https://user-images.githubusercontent.com/23325839/28743090-32fc207c-747c-11e7-81f3-6a9764bffb43.jpg)

<!-- toc -->
- [tritask-sta](#tritask-sta)
  - [コンセプト](#コンセプト)
  - [システム要件](#システム要件)
  - [インストール](#インストール)
  - [使い方](#使い方)
  - [マニュアル](#マニュアル)
  - [License](#license)
  - [Author](#author)

## コンセプト
- 秀丸エディタ上でサクサク動かしたい
- でも秀丸エディタだけではキツイので Python にも頼った
- 見積もり機能は要らない
- でも日付操作は柔軟に行いたい
- あと見易いよう強調表示したい
- タスクの細かい並び順は文字を工夫して制御すればいい(例: 先頭が`a`だと`b`より上に表示される)

## システム要件
- Windows7+
- Python 2.7
- 秀丸エディタ

## インストール
- `git clone https://github.com/tritask/tritask-sta` などで一式をダウンロード
- 秀丸エディタに [tritask.mac](tritask.mac) をマクロ登録する
- （推奨）キー割り当てやツールバーへの配置などを設定して素早く呼び出せるようにしておく
- .trita ファイルを新規する（空ファイルでも良いが [サンプル](sample.trita) もアリ）
- （推奨）trita ファイル用の強調表示設定をつくる
  - その他 > ファイルタイプ別の設定 > 設定の一覧
  - 適当な設定をコピーして trita 用設定をつくる
  - 秀丸エディタで trita ファイルを開き、trita 用設定を選んだ後、[trita.hilight](trita.hilight) を強調表示設定として読み込む

## 使い方
tritask.mac マクロを実行するとメニューが表示されるので、実行したい操作を選択します。

## マニュアル
@todo そのうち作る。

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
