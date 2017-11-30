# -*- coding: utf-8 -*-

import datetime
import os
import sys

def file2list(filepath):
    ret = []
    with open(filepath, 'r') as f:
        ret = [line.rstrip('\n') for line in f.readlines()]
    return ret

def list2file(filepath, ls):
    with open(filepath, 'w') as f:
        f.writelines(['%s\n' % line for line in ls] )

def is_monday(weekday_val):
    return weekday_val==0

def is_tuesday(weekday_val):
    return weekday_val==1

def is_wednesday(weekday_val):
    return weekday_val==2

def is_thursday(weekday_val):
    return weekday_val==3

def is_friday(weekday_val):
    return weekday_val==4

def is_saturday(weekday_val):
    return weekday_val==5

def is_sunday(weekday_val):
    return weekday_val==6

def is_weekday(weekday_val):
    return 0<=weekday_val<=4

def is_weekend(weekday_val):
    return not(is_weekday(weekday_val))

def get_error_location(depth=0):
    import inspect
    frame = inspect.currentframe().f_back
    lineno = frame.f_lineno
    return lineon

def dp(msg):
    if args.debug:
        print msg

def abort(msg):
    print 'Error: {0}'.format(msg)
    os.system('pause')
    exit(1)

def assert_y(y, lines):
    if y>=len(lines):
        abort('Out of range the line number "{0}", Max is "{1}".' \
              .format(y, len(lines)))

def datestr2dt(datestr):
    """ @param datestr A string formatted with `YYYY/MM/DD`. """
    y = int(datestr[0:4])
    m = int(datestr[5:7])
    d = int(datestr[8:10])
    dt = datetime.datetime(y, m, d)
    return dt

def dt2dowstr(dt):
    return ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][dt.weekday()]

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input', default=None, required=True,
        help='A input filename.')

    parser.add_argument('--debug', default=False, action='store_true',
        help='Debug mode. (Show information to debug.)')
    parser.add_argument('--raw-error', default=False, action='store_true',
        help='Debug mode. (Show raw error message.)')

    parser.add_argument('-y', default=None, type=int,
        help='The start line number of a input line. 0-ORIGIN.')
    parser.add_argument('--y2', default=None, type=int,
        help='The end line number of a input line. 0-ORIGIN.')
    parser.add_argument('-d', '--day', default=None, type=int,
        help='The day count to walk.')

    parser.add_argument('--to-today', default=False, action='store_true',
        help='Change the current task day to today. MUST: -y')
    parser.add_argument('--repeat', default=False, action='store_true',
        help='Walk day in the current task with rep:n param. MUST: -y.')
    parser.add_argument('--walk', default=False, action='store_true',
        help='Walk day in the current task. MUST: -y and -d.')
    parser.add_argument('--sort', default=False, action='store_true',
        help='Do sort.')

    args = parser.parse_args()
    return args

class Task:
    EMPTY_TIME = ' '*5

    # [Marks]
    #   inbo(Mark is a space)
    # 1 td
    # 2 tt, ts
    # 3 tom
    # 4 ye
    INBO = ' '
    TD   = '1'
    TT   = '2'
    TS   = TT
    TOM  = '3'
    YE   = '4'

    def __init__(self, line):
        #      01234567890123456789012345678
        fmt = 'M YYYY/MM/DD DOW HH:MM HH:MM '
        if len(line)<len(fmt):
            abort('Invalid format, length shortage "{0}".'.format(line))

        if line[1]!=' '  or \
           line[12]!=' ' or \
           line[16]!=' ' or \
           line[22]!=' ' or \
           line[28]!=' ':
            abort('Invalid format, wrong space delim pos "{0}".'.format(line))

        self._line = line
        self._sortmark    = line[0:1]
        self._date        = line[2:12]
        self._dow         = line[13:16]
        self._starttime   = line[17:22]
        self._endtime     = line[23:28]
        self._description = line[29:]

        self.complete()

        # extract all options from description
        self._options = {}
        for elm in self._description.split(' '):
            if elm.find(':')==-1:
                continue
            key, value = elm.split(':', 1)
            self._options[key] = value

    def complete(self):
        self._complete_dow()
        self._determin_sortmark()

    def _complete_dow(self):
        """ 曜日を日付から算出する. """
        if len(self._date.strip()):
            dt = datestr2dt(self._date)
            self._dow = dt2dowstr(dt)

    def _determin_sortmark(self):
        """ ソートマークを日付と開始/終了時刻から算出する. """
        if len(self._date.strip())==0:
            self._sortmark = self.INBO
            return

        dt = datestr2dt(self._date)
        today = datetime.datetime.today()
        # today() をそのまま使うと時分秒レベルの差が生じて
        # >0 や <0 で判定できないため,
        # 時分秒を省いた datetime オブジェクトを作る必要がある.
        today_without_time = datetime.datetime(today.year, today.month, today.day)

        delta = dt-today_without_time
        diff = int(delta.total_seconds())
        if diff<0:
            self._sortmark = self.YE
            return
        if diff>0:
            self._sortmark = self.TOM
            return

        s, e = len(self._starttime.strip()), len(self._endtime.strip())
        if s==0 and e==0:
            self._sortmark = self.TT
            return
        if s==0 and e:
            # 終了時間のみは容認しない.
            # 未記入に戻す.
            self._sortmark = self.TT
            self._endtime = self.EMPTY_TIME
            return
        if s and e==0:
            self._sortmark = self.TS
            return
        self._sortmark = self.TD

    def hold_me(self):
        try:
            holdday = int(self._options['hold'])
        except (KeyError, ValueError):
            return

        today = datetime.datetime.today()
        self._date = '{0}/{1:02d}/{2:02d}'.format(today.year, today.month, today.day)
        self._dow  = dt2dowstr(today)

        self.walk(holdday)

    def skip_me(self):
        # 日付が無い = Inbox タスクの場合は
        # 日付時刻スキップのしようがないので処理スキップ.
        if not(self._date.strip()):
            return

        y = int(self._date[0:4])
        m = int(self._date[5:7])
        d = int(self._date[8:10])
        dt = datetime.datetime(y, m, d)
        dt_original = datetime.datetime(y, m, d)

        delta1 = datetime.timedelta(days=1)
        walk_count = 0
        ops = self._options

        while True:
            wd = dt.weekday()
            do_skip = False

            if ops.get('skipmon') and is_monday(wd) or \
               ops.get('skiptue') and is_tuesday(wd) or \
               ops.get('skipwed') and is_wednesday(wd) or \
               ops.get('skipthu') and is_thursday(wd) or \
               ops.get('skipfri') and is_friday(wd) or \
               ops.get('skipsat') and is_saturday(wd) or \
               ops.get('skipsun') and is_sunday(wd) or \
               ops.get('skipweekday') and is_weekday(wd) or \
               ops.get('skipweekend') and is_weekend(wd):
                do_skip = True

            if not(do_skip):
                break

            walk_count += 1
            dt = dt + delta1
            if walk_count>7:
                # 一周した = 永遠にスキップされ続ける,
                # なので無効にする. とりあえずスキップ無しにしとく.
                dt = dt_original
                break

        self._date = '{0}/{1:02d}/{2:02d}'.format(dt.year, dt.month, dt.day)
        self._dow  = dt2dowstr(dt)

    def repeat_me(self):
        try:
            repday = int(self._options['rep'])
        except (KeyError, ValueError):
            return

        self.walk(repday)

    def to_today(self):
        today = datetime.datetime.today()
        self._date = '{0}/{1:02d}/{2:02d}'.format(today.year, today.month, today.day)
        self._dow  = dt2dowstr(today)

    def walk(self, day):
        # 0123456789
        # YYYY/MM/DD
        y = int(self._date[0:4])
        m = int(self._date[5:7])
        d = int(self._date[8:10])

        dt = datetime.datetime(y, m, d)
        delta = datetime.timedelta(days=abs(day))

        if day>=0:
            newdt = dt + delta
        else:
            newdt = dt - delta

        self._date = '{0}/{1:02d}/{2:02d}'.format(newdt.year, newdt.month, newdt.day)
        self._dow  = dt2dowstr(newdt)

    def if_invalid_then_to_today(self):
        """ ye や tom の無効タスクはどうせ today に変える.
        だったら自動的に変えてやろうって話.

            yesterday todo     -> tt
            yesterday starting -> ts
            yesterday done
            today     todo
            today     starting
            today     done
            tomorrow  todo
            tomorrow  starting -> ts
            tomorrow  done     -> ts(いきなりtdだと困惑するのでtsで目立たせる)

        ye, today, tom の判定には sortmark を用いる. """

        s, e = len(self._starttime.strip()), len(self._endtime.strip())
        if self._sortmark==self.YE:
            if s==0 and e==0: # todo
                self.to_today()
                return
            if s and e==0: # starting
                self.to_today()
                return
            return
        if self._sortmark == self.TOM:
            if s and e==0: # starting
                self.to_today()
                return
            if s and e: # done
                self.to_today()
                # 方針変更.
                # Before) tomorrow done は目立たせるため today start
                #         self._endtime = self.EMPTY_TIME
                # After ) 未来のタスクを潰したいケースもあるので today done
                return
            return
        return

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5}'.format(
            self._sortmark, self._date, self._dow,
            self._starttime, self._endtime,
            self._description
        )

    def print_options(self):
        for k, v in self._options.items():
            print '{0}: [{1}]'.format(k, v)

def apply_holding(lines):
    for i, line in enumerate(lines):
        if line.find('hold:')==-1:
            continue
        task = Task(line)
        task.hold_me()
        lines[i] = str(task)

def apply_skipping(lines):
    for i, line in enumerate(lines):
        if line.find('skip')==-1:
            continue
        task = Task(line)
        task.skip_me()
        lines[i] = str(task)

def apply_completion(lines):
    """ 記述が不足している or 不正なタスクを可能な限り補完する. """
    for i, line in enumerate(lines):
        task = Task(line)

        task.if_invalid_then_to_today()

        # 補完後の内容でソートマークを反映したいので
        # 最後に complete する.
        task.complete()
        lines[i] = str(task)

args = parse_arguments()

MYDIR = os.path.abspath(os.path.dirname(__file__))
infile = args.input
lines = file2list(infile)

logfile = os.path.join(MYDIR, 'tritask.log')
if not(os.path.exists(logfile)):
    # new file if does not exists.
    list2file(logfile, [])
loglines = file2list(logfile)

try:
    if args.debug and args.y!=None:
        task = Task(lines[args.y])
        print task
        task.print_options()

    if args.walk:
        y = args.y
        y2 = args.y2
        if y2==None:
            y2 = y
        assert_y(y, lines)
        assert_y(y2, lines)
        day = args.day

        for cnt in range(y2-y+1):
            targetidx = cnt + y
            line = lines[targetidx]
            task = Task(line)
            task.walk(day)
            lines[targetidx] = str(task)

        outfile = infile
        list2file(outfile, lines)
        exit(0)

    if args.repeat:
        y = args.y
        assert_y(y, lines)

        line = lines[y]
        task = Task(line)
        task.repeat_me()

        lines[y] = str(task)

        outfile = infile
        list2file(outfile, lines)
        exit(0)

    if args.to_today:
        y = args.y
        y2 = args.y2
        if y2==None:
            y2 = y
        assert_y(y, lines)
        assert_y(y2, lines)
        day = args.day

        for cnt in range(y2-y+1):
            targetidx = cnt + y
            line = lines[targetidx]
            task = Task(line)
            task.to_today()
            lines[targetidx] = str(task)

        outfile = infile
        list2file(outfile, lines)
        exit(0)

    if args.sort:
        outfile = infile

        # before sorting
        # --------------
        apply_holding(lines)
        apply_skipping(lines)
        apply_completion(lines)

        # sorting
        # -------
        lines.sort()

        # after sorthing
        # --------------
        pass

        list2file(outfile, lines)
        exit(0)
except Exception as e:
    if args.raw_error:
        raise
    errmsg = 'Type:{0} Detail:{1}'.format(str(type(e)), str(e))
    creationdate = datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S')
    logmsg = '{0} {1}'.format(creationdate, errmsg)
    loglines.insert(0, logmsg)
    list2file(logfile, loglines)

    # open logfile with system association.
    os.system('start "" "{0}"'.format(logfile))
    exit(1)
