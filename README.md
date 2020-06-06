# tritask-sta
tritask-sta は [タスク管理メソッド Tritask](https://github.com/tritask/tritask-web) を実装したタスク管理ツールです。

![tritask_sta_demo](https://user-images.githubusercontent.com/23325839/36819300-517d1a7a-1d2c-11e8-92bb-7cbcf4fd2cbd.gif)

<!-- toc -->
- [tritask-sta](#tritask-sta)
    - [特徴](#特徴)
    - [システム要件](#システム要件)
    - [インストール](#インストール)
    - [使い方](#使い方)
    - [強調定義ファイル trita.hilight について](#強調定義ファイル-tritahilight-について)
    - [FAQ > インストール](#faq--インストール)
        - [Q: Python のインストールに失敗します](#q-python-のインストールに失敗します)
        - [Q: trita ファイルを秀丸エディタに関連付けることができません](#q-trita-ファイルを秀丸エディタに関連付けることができません)
    - [FAQ > Tritask 操作](#faq--tritask-操作)
        - [Q: タスクの新規/コピー時にカーソル位置がずれたり余分な空白が入ったりします](#q-タスクの新規コピー時にカーソル位置がずれたり余分な空白が入ったりします)
        - [Q: なぜかタスク操作が成功しません(黒い画面が出るだけで何も起こりません)](#q-なぜかタスク操作が成功しません黒い画面が出るだけで何も起こりません)
        - [Q: リファレンス機能でリファレンスが開かれません](#q-リファレンス機能でリファレンスが開かれません)
    - [FAQ > Tritask 上級者向け](#faq--tritask-上級者向け)
        - [Q: `--report` というオプションがありますが、これは何ですか？](#q---report-というオプションがありますがこれは何ですか)
        - [Q: Start Task などの操作をショートカットキー一発で呼び出すことはできますか？](#q-start-task-などの操作をショートカットキー一発で呼び出すことはできますか)
        - [Q: アクセラレーター(Start Task の `(S)` など)が気に入らないので変えたいのですが可能ですか？](#q-アクセラレーターstart-task-の-s-などが気に入らないので変えたいのですが可能ですか)
    - [License](#license)
    - [Author](#author)

## 特徴
- 秀丸エディタ上でバリバリ操作できる
- ルーチンタスクが利用可能
  - 例1: 毎日繰り返す → rep:1
  - 例2: 3日毎に繰り返すが休日は省く → rep:3 skip:休
- タスクの開始、終了、日付操作など主要操作はショートカットキー一発で行える

## システム要件
- Windows 7+
- Python 3.6
- 秀丸エディタ
  - 動作確認を行っているのは V8.69
  - 古いバージョンだとマクロが動作しないかもしれません

## インストール
- (1)環境の準備
  - 上記システム要件を全て満たす
  - ※Python インストール方法など詳細は割愛
- (2)入手
  - [ダウンロードページ](https://tritask.github.io/tritask-sta-bin/) から zip をダウンロード
  - git に慣れている方は `git clone` などでも可能
- (3)秀丸エディタの設定
  - [tritask.mac](tritask.mac) をマクロ登録する
- (4)データファイルの準備
  - .trita ファイルを新規する（空ファイルなり [サンプル](sample.trita) 使うなり）
- (5)秀丸エディタの設定
  - tritask.mac を「キー割り当て」や「ツールバー」から素早く呼び出せるようにする
  - trita ファイル用の強調表示設定を適用する
    - その他 > ファイルタイプ別の設定 > 設定の一覧
    - 適当な設定をコピーして trita 用設定をつくる
    - 秀丸エディタで trita ファイルを開き、trita 用設定を選んだ後、[trita.hilight](trita.hilight) を強調表示設定として読み込む

## 使い方
tritask.mac マクロを実行するとメニューが表示されるので、実行したい操作を選択します。

詳細については以下ドキュメントを参照してください。

- [Tritask ウェブサイト](https://github.com/tritask/tritask-web)
- [tritask-sta の詳しい仕様や使い方について](specification.md)
  - 各操作リファレンスもあります(たとえば Add task とは何か、など)
- [tritask-sta 更新履歴](CHANGELOG.md)

## 強調定義ファイル trita.hilight について
秀丸エディタ上で trita ファイルを見易く＆扱いやすくするために、専用の強調定義ファイルを用意しています。

出来ること:

- 各種文法のハイライト表示
  - 属性(繰り返しの `rep:1` など)
  - 未完了タスク
  - 開始中タスク
  - 土曜日を青色で、日曜日を赤色で表示
- 見出し(` --`を含む行)のサポート
  - 強調表示
  - 秀丸エディタの「次(前)の見出しに移動」も使えます

## FAQ > インストール

### Q: Python のインストールに失敗します
管理者権限でインストールしてください。

### Q: trita ファイルを秀丸エディタに関連付けることができません
管理者権限で実行してください。

秀丸エディタから関連付けることも可能です。

- 1: 秀丸エディタ > 「その他」メニュー > 動作環境
- 2: 関連付け
- 3: 「関連付け可能な拡張子の登録」ボタン
- 3: 「追加」ボタンから `trita` を登録

## FAQ > Tritask 操作

### Q: タスクの新規/コピー時にカーソル位置がずれたり余分な空白が入ったりします
秀丸エディタの **自動インデントをオフ** にしてください。

- ファイルタイプ別の設定 > 体裁 > インデント > 自動インデント のチェックを外す

### Q: なぜかタスク操作が成功しません(黒い画面が出るだけで何も起こりません)
**秀丸エディタ上での表示が折り返されていないか** を確認してください。

折り返されている場合、tritask.mac が正常に動作しないため、このような動作になります。折り返されないように、行の文字数、ウィンドウ幅、折り返し設定などを変更してください（.trita ファイルタイプの折り返し設定は「折り返さない（最大幅で折り返し）」にすることをおすすめします）。

以下は正しくない例です（15文字で折り返す設定の場合）。

```
2 2017/09/16 Sat             タ
スク1
2 2017/09/16 Sat             タ
スク2
2 2017/09/16 Sat             タ
スク3
```

折り返された結果、「スク1」「スク2」のように不正な行が発生してしまっています。こうなると tritask.mac は正常に動作しません。

以下は正しい例です（折り返しがありません）。

```
2 2017/09/16 Sat             タスク1
2 2017/09/16 Sat             タスク2
2 2017/09/16 Sat             タスク3
```

### Q: リファレンス機能でリファレンスが開かれません
上記と同様の原因です。**秀丸エディタ上での表示が折り返されていないか** を確認してください。

特に過去タスクのリファレンスを開く場合、**そのタスクより上にあるタスク行のどこかで折り返し（による余分な行）が発生していないか** を確認してみてください。

（詳しい話をしておくと）リファレンス機能は、helper.py に対して「N行目のタスクが持つリファレンスを開いてください」という風に命令を与えているのですが、折り返しにより余分な行があると、行数指定 N の位置がずれてしまい、このエラーが生じます。

## FAQ > Tritask 上級者向け

### Q: `--report` というオプションがありますが、これは何ですか？
tritask-sta の中でも特に作者寄り（作者自身が使うことしか考えてない）な集計機能です。trita ファイルの終了済タスクを集計した結果をファイルに保存します。

trita ファイルと同じディレクトリに以下が生成されます:

- `report_daily.md`
- `report_monthy.md`
- `report_hourly.md`

ファイルの中身例を以下に示します(monthlyを例に):

```markdown
# Monthly
All 11 keys.

- 2018/05 : 166 Tasks, Total:36.6[H], Avg:13.2[M]
- 2018/04 : 737 Tasks, Total:152.9[H], Avg:12.4[M]
- 2018/03 : 719 Tasks, Total:181.5[H], Avg:15.1[M]
- 2018/02 : 678 Tasks, Total:161.9[H], Avg:14.3[M]
- 2018/01 : 609 Tasks, Total:133.2[H], Avg:13.1[M]
- 2017/12 : 752 Tasks, Total:157.3[H], Avg:12.5[M]
- 2017/11 : 728 Tasks, Total:167.2[H], Avg:13.8[M]
- 2017/10 : 500 Tasks, Total:106.1[H], Avg:12.7[M]
- 2017/09 : 728 Tasks, Total:172.4[H], Avg:14.2[M]
- 2017/08 : 441 Tasks, Total:107.2[H], Avg:14.6[M]
- 2017/07 : 227 Tasks, Total:58.5[H], Avg:15.5[M]
```

こんな具合に日毎、月毎、時間帯毎の集計を保存します。

### Q: Start Task などの操作をショートカットキー一発で呼び出すことはできますか？
一部操作のみ v1.6.1+ にて対応しました。

設定手順:

- (1) tritask_cmd_start.mac や tritask_cmd_end.mac をマクロ登録する
- (2) 1 に対してキー割り当てを割り当てる
  - 例: PageUp に tritask_cmd_start を、PageDown に tritask_cmd_end を

利用方法:

- キー割り当てにて割り当てたショートカットキーを押す

制約事項:

- tritask_cmd_XXXX.mac は tritask.mac と同じフォルダに置く必要がある

### Q: アクセラレーター(Start Task の `(S)` など)が気に入らないので変えたいのですが可能ですか？
tritask.mac を編集すれば可能です。

以下のあたりを見てください。

```
...
// [[[ menu item start
#idx=#I_ADD; $items[#idx]         = "(&A)Add Task";
#idx=#I_ADDINBO; $items[#idx]     = "(&X)Add Inbox";
#idx=#I_COPY; $items[#idx]        = "(&C)Copy Task";
#idx=#I_START; $items[#idx]       = "(&S)Start Task";
#idx=#I_END; $items[#idx]         = "(&E)End Task";
#idx=#I_CLOSE; $items[#idx]       = "(&Q)Close Task";
#idx=#I_EDIT_TASK; $items[#idx]   = "(&/)Edit Task";
#idx=#I_SEP1; $items[#idx]        = "\x01";
#idx=#I_WALK; $items[#idx]        = "(&D)Walk day <Multi>";
#idx=#I_WALK_1; $items[#idx]      = "(&1)Walk +1 day(Smart-walk) <Multi>";
#idx=#I_TO_TODAY; $items[#idx]    = "(&T)Change to Today <Multi>";
#idx=#I_CLR_DATE; $items[#idx]    = "(&I)Clear Date";
#idx=#I_SEP2; $items[#idx]        = "\x01";
#idx=#I_SORT; $items[#idx]        = "(& )Sort";
#idx=#I_JUMP_STA; $items[#idx]    = "(&J)Jump to Starting-Task";
#idx=#I_REF; $items[#idx]         = "(&R)Open Reference";
#idx=#I_SIMPLE_COMP; $items[#idx] = "(&W)Simple Completion";
#idx=#I_SEP3; $items[#idx]        = "\x01";
#idx=#I_REPORT_TODAY; $items[#idx]= "(&.)Report Today or Selected-Range";
#idx=#I_SEP4; $items[#idx]        = "\x01";
#idx=#I_EDIT_SCRI; $items[#idx]   = "(&P)Programming helper script";
#idx=#I_EDIT_ME; $items[#idx]     = "(&P)Programming this macro";
#idx=#idx+1; #maxidx = #idx;
// menu item end ]]]
...
```

たとえば Start Task の発動を S キーから H キーに変えたい場合、以下のように修正します。

```
#idx=#I_START; $items[#idx]       = "(&S)Start Task";

        ↓

#idx=#I_START; $items[#idx]       = "(&H)Start Task";
```

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
