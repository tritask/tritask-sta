# -*- coding: utf-8 -*-

import datetime
import unittest

import helper as tritask

"""
                                  2020


      January                   February                   March
 Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
           1  2  3  4                         1       1  2  3  4  5  6  7
  5  6  7  8  9 10 11       2  3  4  5  6  7  8       8  9 10 11 12 13 14
 12 13 14 15 16 17 18       9 10 11 12 13 14 15      15 16 17 18 19 20 21
 19 20 21 22 23 24 25      16 17 18 19 20 21 22      22 23 24 25 26 27 28
 26 27 28 29 30 31         23 24 25 26 27 28 29      29 30 31            
                                                                         


       April                      May                       June
 Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
          <1> 2  3  4                      1  2          1  2  3  4  5  6
  5  6  7  8  9 10 11       3  4  5  6  7  8  9       7  8  9 10 11 12 13
 12 13 14 15 16 17 18      10 11 12 13 14 15 16      14 15 16 17 18 19 20
 19 20 21 22 23 24 25      17 18 19 20 21 22 23      21 22 23 24 25 26 27
 26 27 28 29 30            24 25 26 27 28 29 30      28 29 30            
                           31                                            


        July                     August                  September
 Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
           1  2  3  4                         1             1  2  3  4  5
  5  6  7  8  9 10 11       2  3  4  5  6  7  8       6  7  8  9 10 11 12
 12 13 14 15 16 17 18       9 10 11 12 13 14 15      13 14 15 16 17 18 19
 19 20 21 22 23 24 25      16 17 18 19 20 21 22      20 21 22 23 24 25 26
 26 27 28 29 30 31         23 24 25 26 27 28 29      27 28 29 30         
                           30 31                                         


      October                   November                  December
 Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
              1  2  3       1  2  3  4  5  6  7             1  2  3  4  5
  4  5  6  7  8  9 10       8  9 10 11 12 13 14       6  7  8  9 10 11 12
 11 12 13 14 15 16 17      15 16 17 18 19 20 21      13 14 15 16 17 18 19
 18 19 20 21 22 23 24      22 23 24 25 26 27 28      20 21 22 23 24 25 26
 25 26 27 28 29 30 31      29 30                     27 28 29 30 31      
                                                                         
"""

class datetime_FixedToday(datetime.datetime):
    @classmethod
    def today(cls):
        return cls(2020, 4, 1, 12, 34, 56)
datetime.datetime = datetime_FixedToday

TT = tritask.Task.TT
TS = tritask.Task.TS
TD = tritask.Task.TD
TOM = tritask.Task.TOM
YE = tritask.Task.YE
emptysortmark = ' '
emptytime = ' '*5

class TestHelper(unittest.TestCase):
    def setUp(self):
        self._clear_args()

        self._today_dt, _ = tritask.today_and_today_without_time()
        self._today_datestr = tritask.dt2datestr(self._today_dt)
        self._today_dowstr = tritask.dt2dowstr(self._today_dt)
        self._now_timestr =tritask.nowtimestr()

    def tearDown(self):
        pass

    def _clear_args(self):
        self._args = tritask.parse_arguments()

    def add_task(self, taskname):
        return '{} {} {} {} {} {}'.format(
            emptysortmark,
            self._today_datestr,
            self._today_dowstr,
            emptytime,
            emptytime,
            taskname
        )

    def add_task_with_dow(self, taskname, dowstr):
        return '{} {} {} {} {} {}'.format(
            emptysortmark,
            self._today_datestr,
            dowstr,
            emptytime,
            emptytime,
            taskname
        )

    def add_task_with_start_end(self, taskname, starttime=emptytime, endtime=emptytime):
        return '{} {} {} {} {} {}'.format(
            emptysortmark,
            self._today_datestr,
            self._today_dowstr,
            starttime,
            endtime,
            taskname
        )

    def test_walk(self):
        self._args.y = 0
        self._args.day = 1
        self._args.walk = True

        line = self.add_task('walk test')
        lines = []
        lines.append(line)

        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/02 Thu {} {} walk test'.format(
            TT,
            emptytime,
            emptytime,
        ))

    def test_smartwalk(self):
        self._args.y = 0
        self._args.smartwalk = True

        line = self.add_task('smart rep:4 walk')
        lines = []
        lines.append(line)

        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/05 Sun {} {} smart rep:4 walk'.format(
            TT,
            emptytime,
            emptytime,
        ))

    def test_repeat(self):
        self._args.y = 0
        self._args.repeat = True

        line = self.add_task('repeat rep:13')
        lines = []
        lines.append(line)

        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/14 Tue {} {} repeat rep:13'.format(
            TT,
            emptytime,
            emptytime,
        ))

    def test_change_to_today(self):
        lines = []
        line = self.add_task('after 10day task to today rep:10')
        lines.append(line)

        # 10日後のタスクをつくる
        self._clear_args()
        self._args.y = 0
        self._args.repeat = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self._clear_args()
        self._args.y = 0
        self._args.to_today = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        # expect sormark は TT ではない!!
        # Task.complete() のコメントを参照.
        # ここでは Task インスタンス生成時に complete が走るので,
        # 「10日後のタスク」のときのsortmarkになる, つまり TOM
        self.assertEqual(lines[0], '{} 2020/04/01 Wed {} {} after 10day task to today rep:10'.format(
            TOM,
            emptytime,
            emptytime,
        ))

    def test_simple_completion(self):
        self._args.y = 0
        self._args.use_simple_completion = True

        line = self.add_task_with_dow('task with invalid dow', 'AAA')
        lines = []
        lines.append(line)

        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/01 Wed {} {} task with invalid dow'.format(
            TT,
            emptytime,
            emptytime,
        ))

    def test_sort_order_name(self):
        lines = []
        lines.append(self.add_task('22'))
        lines.append(self.add_task('4444'))
        lines.append(self.add_task('1'))

        self._args.sort = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/01 Wed {} {} 1'.format(
            TT,
            emptytime,
            emptytime,
        ))

        self.assertEqual(lines[1], '{} 2020/04/01 Wed {} {} 22'.format(
            TT,
            emptytime,
            emptytime,
        ))

        self.assertEqual(lines[2], '{} 2020/04/01 Wed {} {} 4444'.format(
            TT,
            emptytime,
            emptytime,
        ))

    def test_sort_status_today(self):
        lines = []
        lines.append(self.add_task('today todo'))
        lines.append(self.add_task_with_start_end('today starting', '10:30'))
        lines.append(self.add_task_with_start_end('today done', '10:30', '10:33'))

        self._args.sort = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/01 Wed {} {} today done'.format(
            TD,
            '10:30',
            '10:33',
        ))

        self.assertEqual(lines[1], '{} 2020/04/01 Wed {} {} today todo'.format(
            TT,
            emptytime,
            emptytime,
        ))

        self.assertEqual(lines[2], '{} 2020/04/01 Wed {} {} today starting'.format(
            TS,
            '10:30',
            emptytime,
        ))

    def test_sort_status_ye_and_tom(self):
        lines = []
        lines.append(self.add_task('yesterday todo'))
        lines.append(self.add_task_with_start_end('yesterday starting', '10:30'))
        lines.append(self.add_task_with_start_end('yesterday done', '10:30', '10:33'))
        lines.append(self.add_task('tomorrow todo'))
        lines.append(self.add_task_with_start_end('tomorrow starting', '10:30'))
        lines.append(self.add_task_with_start_end('tomorrow done', '10:30', '10:33'))

        # 日付操作は tritask 経由で実施.
        # テストコード側であえて日付操作ロジックを用意すると重複なので,
        # なるべく tritask 側のシステムを利用してつくる.
        #
        # 二回以上 proceed する時は args のクリアが必要.
        #
        # 昨日
        self._clear_args()
        self._args.y = 0
        self._args.y2 = 2
        self._args.day = -1
        self._args.walk = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)
        # 明日
        self._clear_args()
        self._args.y = 3
        self._args.y2 = 5
        self._args.day = 1
        self._args.walk = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self._clear_args()
        self._args.sort = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        actual_lines = lines
        expect_lines = []
        expect_lines.append('{} 2020/04/01 Wed {} {} tomorrow done'.format(
            TD,
            '10:30',
            '10:33',
        )) #'明日のtodoは無効, 今日のdoneになる'
        expect_lines.append('{} 2020/04/01 Wed {} {} yesterday todo'.format(
            TT,
            emptytime,
            emptytime,
        )) #'昨日のtodoは無効, 今日のtodoになる'
        expect_lines.append( '{} 2020/04/01 Wed {} {} tomorrow starting'.format(
            TS,
            '10:30',
            emptytime,
        )) #'明日のstartingは無効, 今日のstaringになる'
        expect_lines.append('{} 2020/04/01 Wed {} {} yesterday starting'.format(
            TS,
            '10:30',
            emptytime,
        )) #'昨日のstartingは無効, 今日のstaringになる'
        expect_lines.append('{} 2020/04/02 Thu {} {} tomorrow todo'.format(
            TOM,
            emptytime,
            emptytime,
        )) #'明日のtodoは有効'
        expect_lines.append('{} 2020/03/31 Tue {} {} yesterday done'.format(
            YE,
            '10:30',
            '10:33',
        )) #'昨日のdoneは有効'
        self.assertEqual(expect_lines, actual_lines)

    def test_skip(self):
        lines = []
        lines.append(self.add_task('1 来週火曜日になる rep:1 skip:水木金土日月'))
        lines.append(self.add_task('2 直近の休日になる rep:1 skip:平'))
        lines.append(self.add_task('3 来週月曜日になる rep:1 skip:木水休金'))
        lines.append(self.add_task('4 無限スキップ防止でスキップしない skip:水木金土日月火'))

        self._args.sort = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self.assertEqual(lines[0], '{} 2020/04/01 Wed {} {} 4 無限スキップ防止でスキップしない skip:水木金土日月火'.format(
            TT,
            emptytime,
            emptytime,
        ))

        self.assertEqual(lines[1], '{} 2020/04/04 Sat {} {} 2 直近の休日になる rep:1 skip:平'.format(
            TOM,
            emptytime,
            emptytime,
        ))

        self.assertEqual(lines[2], '{} 2020/04/06 Mon {} {} 3 来週月曜日になる rep:1 skip:木水休金'.format(
            TOM,
            emptytime,
            emptytime,
        ))

        self.assertEqual(lines[3], '{} 2020/04/07 Tue {} {} 1 来週火曜日になる rep:1 skip:水木金土日月'.format(
            TOM,
            emptytime,
            emptytime,
        ))

    def test_posteriori_end(self):
        lines = []
        lines.append(self.add_task_with_start_end('done task1', '08:01', '08:03'))
        lines.append(self.add_task_with_start_end('done task2', '08:04', '08:13'))
        lines.append(self.add_task('posteriori end'))

        self._clear_args()
        self._args.sort = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        self._clear_args()
        self._args.y = 2
        self._args.end_now = True
        tritask.proceed_lines_and_is_save_required(self._args, lines)

        actual_lines = lines
        expect_lines = []
        expect_lines.append('{} 2020/04/01 Wed {} {} done task1'.format(
            TD,
            '08:01',
            '08:03',
        ))
        expect_lines.append('{} 2020/04/01 Wed {} {} done task2'.format(
            TD,
            '08:04',
            '08:13',
        ))
        expect_lines.append('{} 2020/04/01 Wed {} {} posteriori end'.format(
            TT,
            '08:13',
            tritask.nowtimestr(),
        )) # 最後に終えたタスクの終了時間が開始時間になり, 現在時間が終了時間になる

        self.assertEqual(expect_lines, actual_lines)

if __name__ == '__main__':
    unittest.main()
