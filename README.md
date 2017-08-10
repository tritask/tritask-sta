# tritask-sta
[Tritask](https://github.com/tritask/tritask-spec) のオレオレ実装例です。

![tritasksta_image](https://user-images.githubusercontent.com/23325839/28743090-32fc207c-747c-11e7-81f3-6a9764bffb43.jpg)

<!-- toc -->
- [tritask-sta](#tritask-sta)
  - [コンセプト](#コンセプト)
  - [システム要件](#システム要件)
  - [インストール](#インストール)
  - [使い方、マニュアル](#使い方マニュアル)
  - [FAQ](#faq)
    - [Q: タスクの新規/コピー時にカーソル位置がずれたり余分な空白が入ったりします](#q-タスクの新規コピー時にカーソル位置がずれたり余分な空白が入ったりします)
  - [License](#license)
  - [Author](#author)

## コンセプト
TaskChute から見積もり機能とカテゴリ機能(セクションやモード)を引いて、plain text 要素を足した感じ。

- 秀丸エディタ上でサクサク動かせる
- でも秀丸エディタだけではキツイので Python にも頼った
- 日付操作は柔軟に行いたい(n日後に設定、とか簡単にしたい)
- タスクの細かい並び順はタスク内容の記述を工夫すればいい

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

## 使い方、マニュアル
tritask.mac マクロを実行するとメニューが表示されるので、実行したい操作を選択します。

詳しい操作はマニュアルを参照してください（@todo そのうち作る）。

## FAQ

### Q: タスクの新規/コピー時にカーソル位置がずれたり余分な空白が入ったりします
秀丸エディタの自動インデントをオフにしてください。

- ファイルタイプ別の設定 > 体裁 > インデント > 自動インデント のチェックを外す。

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
