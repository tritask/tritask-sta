# tritask-sta specification
<!-- toc -->
- [tritask-sta](#tritask-sta)
- [タスクの種類](#タスクの種類)
  - [有効なタスク](#有効なタスク)
  - [無効なタスク](#無効なタスク)
- [各フィールドの実装](#各フィールドの実装)
  - [マーク](#マーク)
  - [日付と曜日](#日付と曜日)
  - [属性](#属性)
    - [繰り返し(Repeat)](#繰り返しrepeat)
    - [スキップ(skip)](#スキップskip)
    - [ホールド(Hold)](#ホールドhold)
- [操作一覧](#操作一覧)
  - [TEMPLATE](#template)
  - [Add Task](#add-task)
  - [Add Inbox](#add-inbox)
  - [Copy Task](#copy-task)
  - [Start Task](#start-task)
  - [End Task](#end-task)
  - [Jump to Starting-Task](#jump-to-starting-task)
  - [Clear Date](#clear-date)
  - [Change to Today](#change-to-today)
  - [Sort](#sort)
  - [Walk day](#walk-day)
  - [Programming this macro](#programming-this-macro)

# タスクの種類

## 有効なタスク

```
                             INBOX
1 2017/07/11 Thu  9:52 10:33 YESTERDAY DONE
2 2017/07/12 Wed             TODAY TODO
3 2017/07/12 Wed  9:52       TODAY START
4 2017/07/12 Wed  9:52 10:33 TODAY DONE
5 2017/07/13 Thu             TOMORROW TODO
```

| 種類名 | 略称 | 説明 |
| ------ | ---- | ---- |
| INBOX| inbo | 実行日の決まっていないタスク（メモとしても使用可） |
| YESTERDAY DONE| ye | 昨日以前に終了したタスク |
| TODAY TODO | tt | 今日行うタスク |
| TODAY START | ts | 現在実行中のタスク |
| TODAY DONE | td | 今日終了したタスク |
| TOMORROW TODO | tom | 明日以降のタスク |

## 無効なタスク

YESTERDAY TODO, YESTERDAY START, TOMORROW DONE, TOMORROW START は存在しない。

```
1 2017/07/11 Thu             YESTERDAY TODO      <=== INVALID
1 2017/07/11 Thu  9:52       YESTERDAY START     <=== INVALID
2 2017/07/12 Wed             TODAY TODO
3 2017/07/12 Wed  9:52       TODAY START
4 2017/07/12 Wed  9:52 10:33 TODAY DONE
5 2017/07/13 Thu 10:00       TOMORROW START      <=== INVALID
5 2017/07/13 Thu 10:00 10:22 TOMORROW DONE       <=== INVALID
```

ただしツール側でバリデーションや修正処理を行う義務は無い。

# 各フィールドの実装

## マーク
タスク種別に対するマークは以下のとおりに定める。

| マーク値 | タスク種別 |
| -------- | ---- |
| ` `(スペース) | inbo(Inbox) |
| `1` | td(Today Done) |
| `2` | tt(Today Todo), ts(Today Starting) |
| `3` | tom(Tomorrow Todo) |
| `4` | ye(Yesterday Done) |

意図としては、まずインボックスやメモなど汎用的な inbo は最上位に表示させる。また today, tom, ye については、today が一番使うはずなので一番上、次いで明日以降の予定である tom、最後に過去である ye の順にしてある。

## 日付と曜日
以下のパターンのみ有効とする。

- 日付も曜日も空文字列(inbo)
- 有効な日付と、それに対応する曜日(today, tom or ye)
- 有効な日付と、曜日は空文字列(曜日については **ツールがソート時に日付から自動補完する** )

有効でないパターンが入力された時、ツールの挙動は Undefined である。

以下に実際のフォーマットでの例を挙げる。

```
                             inbo
2 2017/07/12 Wed             tt
2 2017/07/12                 tt(曜日部分はソート時に補完される)
2            Wed             不正なフォーマット(日付がない)
2 2017/07/12 WED             不正なフォーマット(曜日のCase-Sensitiveが合っていない)
2 2017/07/32 WED             不正なフォーマット(日付が有効でない)
```

## 属性

### 繰り返し(Repeat)
- `rep:N`
- N は 1 以上の整数

このタスクを終了すると、N日後の tom が複製される。

- 例
  - `rep:1` 毎日実行する繰り返し。
  - `rep:7` 一週間に一度実行する繰り返し。
  - `rep:30` （おおよそ）一月に一度実行する繰り返し。

### スキップ(skip)
- `skipmon:1`, `skiptue:1`, ... `skipsun:1`
- `skipweekday:1`
- `skipweekend:1`
- Value は何でもよいが、慣習的に 1 が望ましい

このタスクは、ソートされた時、日付が「指定された曜日」だった場合に、日付が +1 される。

- 例
  - `rep:1 skipweekend:1` 平日のみ毎日実行する繰り返し
  - `rep:1 skipwed:1 skipsun:1` 水曜日と日曜日以外で毎日実行する繰り返し

指定は曜日個別、平日、終末（土曜日と日曜日）の三パターンを指定可能。

全ての曜日が指定された場合、永遠にインクリメントされ続けるため、 **ツール側で停止しなければならない**。

### ホールド(Hold)
- `hold:N`
- N は整数

このタスクは、ソートされた時に、今日を `0` として、その差分の日付が常に設定される

- 例
  - `hold:0` このタスクは常に日付が今日になる
  - `hold:1` このタスクは常に日付が明日になる
  - `hold:-1` このタスクは常に日付が昨日になる

# 操作一覧

注釈
- 「指定タスク」とは現在選択している（キャレットがある）行のタスクを指す
- 「複数選択」とは複数選択している行全てのタスクを指す
- Before/After 内では、キャレットは `I` で表記する

## TEMPLATE
(一言説明)

Before

```
適用前の内容
```

After

```
適用前の内容
```

(詳細説明)

## Add Task
現在行に tt を追加する。

Before

```
  2017/08/04 Fri             タスク1
  2017/08/04 Fri             Iタスク2
  2017/08/04 Fri             タスク3
```

After

```
  2017/08/04 Fri             タスク1
  2017/08/04 Fri             I
  2017/08/04 Fri             タスク2
  2017/08/04 Fri             タスク3
```

## Add Inbox
現在行に inbo を追加する。

Before

```
  2017/08/04 Fri             タスク1
  2017/08/04 Fri             Iタスク2
  2017/08/04 Fri             タスク3
```

After

```
  2017/08/04 Fri             タスク1
                             I
  2017/08/04 Fri             タスク2
  2017/08/04 Fri             タスク3
```

## Copy Task
指定タスクを次行に複製する。その際、開始時刻と終了時刻はクリアする。

Before

```
  2017/08/04 Fri 09:30 09:54 Iタスク2
  2017/08/04 Fri             タスク3
```

After

```
  2017/08/04 Fri 09:30 09:54 タスク2
  2017/08/04 Fri             タスク2I
  2017/08/04 Fri             タスク3
```

## Start Task
指定タスクに開始時刻を書き込む。

Before

```
  2017/08/04 Fri             Iタスク1
```

After(14:30に開始した場合)

```
  2017/08/04 Fri 14:30I      タスク1
```

既に開始されている場合は開始時刻をクリアする（開始時刻記入のトグル）。

## End Task
指定タスクに終了時刻を書き込む。

Before

```
  2017/08/04 Fri 13:31       Iタスク rep:3
```

After(14:30に終了した場合)

```
  2017/08/04 Fri 13:31 14:30 タスク rep:3
4 2017/08/07 Mon             タスク rep:3I
```

もし repeat 属性がある場合、当該タスクを（日付を指定日後に変更してから）複製する。

開始時刻が書き込まれてない場合は無効タスク（開始してないのに終了している）となってしまうが、処理の中断や警告は行わない。

## Jump to Starting-Task
ts のある行にジャンプする。

Before

```
  2017/08/04 Fri             タスクI
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri 14:34       タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
```

After

```
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
  2017/08/04 FriI14:34       タスク
  2017/08/04 Fri             タスク
  2017/08/04 Fri             タスク
```

ts が複数存在する場合、最初に登場する ts にジャンプする。

本操作を続けて適用しても二つ目の ts、三つ目の ts というふうにジャンプはしない。

## Clear Date
指定タスクの日付を空文字列にする（inboにする）。

Before

```
  2017/08/04 Fri             タスクI
```

After

```
                             Iタスク
```

## Change to Today
指定タスクの日付を今日にする。複数選択可能。

Before（二つとも選択しているとする）

```
4 2017/08/02 Wed             タスク
4                            タスク
```

After（今日が 17/08/05 とする）

```
2 2017/08/05 Sat             タスク
2 2017/08/05 Sat             タスク
```

## Sort
現在開いている trita ファイルに対してソートを実行する。

ただしソートを実行する前に全行を走査し、以下の前処理を行う。

- 日付に対応するマークを付ける（既にマークが記入されている場合は上書きする）
- 日付に対応する曜日を埋める（既に曜日が記入されている場合は上書きする）
- 属性の解釈を行う
  - hold がある場合、日付を指定日にホールドする
  - skip がある場合、日付が指定スキップ日であれば、そうならなくなるまで日付を増やす

## Walk day
指定タスクの日付を指定日だけ増減させる。複数選択対応。

指定可能な増減値は整数値。

- 増減値の例
  - `-3` : 3日前
  - `0` : 今日
  - `1` : 1日後
  - `+1` : 1日後

## Programming this macro
マクロファイル tritask.mac を秀丸エディタで開く。