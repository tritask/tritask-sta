# 2018/12/10 v1.6.1+
- Add キー割り当てから Start Task, End Task, Sort を呼び出せるようにする

## キー割り当てから各操作を一発で呼び出す
今回、tritask.mac 内の操作をキー割り当てから一発で呼び出す機能を追加した。

設定手順:

- (1) tritask_cmd_start.mac や tritask_cmd_end.mac をマクロ登録する
- (2) 1 に対してキー割り当てを割り当てる
  - 例: PageUp に tritask_cmd_start を、PageDown に tritask_cmd_end を

利用方法:

- キー割り当てにて割り当てたショートカットキーを押す

制約事項:

- tritask_cmd_XXXX.mac は tritask.mac と同じフォルダに置く必要がある

# 2018/11/17 v1.6.1
- Modify ソート処理の性能改善(1万行など行数多い時の処理終了時間をおおよそ数十 % 削減)

# 2018/11/15 v1.6.0
- Add "Smart Walk"
- Modify from "Walk +1 day" to "Walk +1 day(Smart-walk)"

# 2018/11/12 v1.5.0
- Remove タイムバインド機能( `timebind:HHMM-HHMM`)

## タイムバインドの削除について
タイムバインドはリマインダーを実現するための機能であったが、処理としては「指定タスクの位置を上の行に持ってくる」だけであり、リマインダーとしての効力は薄い。ソートのタイミングで気付くことはできるが、ソートしなければ気付けない。これではリマインダーとは言えない。

リマインダー機能を一から作り込むのは大変であり、また Tritask の本質ではないことと、既に別のツールが存在しておりそれらに頼れば良いことから、今回タイムバインドの削除を決意した。

# 2018/11/01 v1.4.0
- Add 実行時間の見積もりを指定する属性( `m:15` で見積=15分の意)
- Add "Report Today" (今日のタスク数と見積もり時間を表示)
- Add バージョン情報表示機能( `python helper.py -v -i dummy` を実行)

# 2018/10/11 v1.3.0
- Add "Simple Completion" (現在行のみを補正(曜日修正など)する)

# 2018/09/30 v1.2.1
- Modify スキップの文法を `skip:月火水木金土日休平` 式に変更する
- Modify 上記文法がハイライトされるようにする about trita.hilight

# 2018/05/11 v1.2.0
- Add タスク集計機能( `python --report -i data.trita` を実行)

# 2018/04/26 v1.1.0
- Add "Walk +1 day"
- Add "Open Reference"
- Add "Close Task"
- Modify メニュー項目を読みやすいよう並べ替える
- Add CHANGELOG.md
