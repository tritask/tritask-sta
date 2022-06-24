# -*- coding: utf-8 -*-

import ctypes
import datetime
import os
import sys

NAME    = 'Tritask'
VERSION = '1.11.0'
INFO    = '{} {}'.format(NAME, VERSION)

MB_OK = 0
def message_box(message, title, mbtype):
    return ctypes.windll.user32.MessageBoxW(0, str(message), str(title), mbtype)

def ok(message, title):
    message_box(message, title, MB_OK)

def open_version_dialog():
    message = INFO
    title = 'Version'
    ok(message, title)

def file2list(filepath):
    ret = []
    with open(filepath, encoding='utf8', mode='r') as f:
        ret = [line.rstrip('\n') for line in f.readlines()]
    return ret

def list2file(filepath, ls):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.writelines(['{:}\n'.format(line) for line in ls] )

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
        print(msg)

def abort(msg):
    print('Error: {0}'.format(msg))
    exit(1)

def assert_y(y, lines):
    if y>=len(lines):
        abort('Out of range the line number "{0}", Max is "{1}".' \
              .format(y, len(lines)))

# datetime() 生成はコストがかかる処理なので
# 一度生成した分を保持しておいて使い回す.
dt_store = {}
def datestr2dt(datestr):
    """ @param datestr A string formatted with `YYYY/MM/DD`. """
    y = int(datestr[0:4])
    m = int(datestr[5:7])
    d = int(datestr[8:10])

    # 文字列連結はコストが高いので数値計算だけでキーをつくる.
    # 2011 10 12 -> 20111002
    key = y*10000 + m*100 + d

    if key in dt_store:
        dt = dt_store[key]
    else:
        dt = datetime.datetime(y, m, d)
        dt_store[key] = dt

    return dt

def dt2datestr(dt):
    """ @param dt A datetime.datetime object.
    @return A string `YYYY/MM/DD formatted. """
    return '{0}/{1:02d}/{2:02d}'.format(dt.year, dt.month, dt.day)

def dt2dowstr(dt):
    return ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][dt.weekday()]

def today_and_today_without_time():
    # without time について:
    #     today() をそのまま使うと時分秒レベルの差が生じて
    #     >0 や <0 で判定できないため,
    #     時分秒を省いた datetime オブジェクトを別途作って利用する.

    p1 = datetime.datetime.today()
    p2 = datetime.datetime(p1.year, p1.month, p1.day)
    return (p1, p2)

def nowtimestr():
    dt, _ = today_and_today_without_time()
    return dt.strftime('%H:%M')

def reference_opener(refinfo):
    dirname = args.refconf_dir
    ext = args.refconf_ext

    do_not_use_new_creation = not(refinfo.use_new_creation)

    # reference もデータなので trita ファイルと同じディレクトリにする.
    # Q: 保存先を指定できるようにはしない?
    # A: しない. コマンドライン引数をあまり複雑にしたくない.
    tritafile_fullpath = os.path.abspath(args.input)
    basedir = os.path.dirname(tritafile_fullpath)
    dp('[Ref::BaseDir "{}"'.format(basedir))

    outputdir_fullpath = os.path.join(basedir, dirname)
    dp('[Ref::FullDir "{}"'.format(basedir))
    if not(os.path.isdir(outputdir_fullpath)):
        if do_not_use_new_creation:
            return
        os.mkdir(outputdir_fullpath)

    refname = refinfo.name
    reffile_name = '{}.{}'.format(refname, ext)
    reffile_fullpath = os.path.join(outputdir_fullpath, reffile_name)
    if not(os.path.exists(reffile_fullpath)):
        if do_not_use_new_creation:
            return
        # reference ファイル単体で開いても関連がわかりやすよう
        # 元タスク情報を書き込んでおく.
        contents = []
        contents.append(refinfo.taskline)
        contents.append('') # 空行. 個人的好み.
        list2file(reffile_fullpath, contents)

    os.system('start "" "{0}"'.format(reffile_fullpath))

def open_commandline_with_system_association(commandline):
    os.system('start "" "{:}"'.format(commandline))

class ReferenceInfo:
    def __init__(self, name, task):
        self._name = name
        self._task = task

        self._use_new_creation = True

    def do_not_use_new_creation(self):
        self._use_new_creation = False

    @property
    def name(self):
        return self._name

    @property
    def use_new_creation(self):
        return self._use_new_creation

    @property
    def taskline(self):
        return str(self._task)

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

    def __init__(self, line, predefined_todays=None):
        """ @param predefined_todays A tuple (today, today_without_time). """

        # For Performance
        # ---------------

        # 事前につくった today datetime object を使うことで
        # Task インスタンス毎に新規生成するコストを抑える.
        self._today_dt = None
        self._today_dt_without_time = None
        if predefined_todays!=None:
            self._today_dt = predefined_todays[0]
            self._today_dt_without_time = predefined_todays[1]

        # Parse Basic elements
        # --------------------

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

        # Completion after parsing
        # ------------------------

        self.complete()

        # Parse task-attributes
        # ---------------------

        # extract all options from description
        self._options = {}
        for elm in self._description.split(' '):
            if elm.find(':')==-1:
                continue
            key, value = elm.split(':', 1)
            self._options[key] = value

    # is_xxxx() は既に sort されていることを前提とする.
    # もっというと, 先に sort した後で使うことを想定している.
    # (開発者都合だが sort mark 使った方が判定が楽だから....)

    def is_today(self):
        m = self._sortmark
        if m==self.TT or m==self.TS or m==self.TD:
            return True
        return False

    def is_today_done(self):
        m = self._sortmark
        if m==self.TD:
            return True
        return False

    def is_today_todo(self):
        m = self._sortmark
        if m==self.TT:
            return True
        return False

    def is_hold(self):
        try:
            int(self._options['hold'])
        except (KeyError, ValueError):
            return False
        return True

    def is_contained_in_description(self, keyword):
        description = self._description
        if len(description.strip()) == 0:
            return False
        if description.find(keyword) == -1:
            return False
        return True

    def get_estimate_info(self):
        """ @return A taple: (result_as_boolean, 0 or estimate_minute) """
        result = False
        estimate_minute = 0

        is_found_option = True
        try:
            int(self._options['m'])
        except (KeyError, ValueError):
            is_found_option = False

        if is_found_option:
            result = True
            estimate_minute = int(self._options['m'])

        return (result, estimate_minute)

    # Q: complete() は walk や to_today など sortmark が変わるタイミングでは呼ばない？
    #    -> 呼ばない.
    #       sortmark は sort すれば反映されるから.
    # Q: なぜ呼ばない?
    #    -> 面倒だから.
    #       この処理には complete 入れている, こっちに入れてない……
    #       こういったことが起こるが面倒くさい.
    #       だったら最初から「入れません」「sormarkはsortすれば反映されます」が潔い.
    #    -> 2022/06/16、clone の処理で clonee の sortmark が(walk()してるのに)更新されてないの、ちょっと迷った
    #       が、実装としては副作用なくて綺麗なのでそのままでいい。
    def complete(self):
        self._determin_dow()
        self._determin_sortmark()

    def _determin_dow(self):
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

        if self._today_dt!=None:
            today = self._today_dt
            today_without_time = self._today_dt_without_time
        else:
            today, today_without_time = today_and_today_without_time()

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
        self._date = dt2datestr(today)
        self._dow  = dt2dowstr(today)

        self.walk(holdday)

    def skip_me(self):
        # 日付が無い = Inbox タスクの場合は
        # 日付時刻スキップのしようがないので処理スキップ.
        if not(self._date.strip()):
            return

        # 終了したタスク(終了時刻が存在するタスク)は
        # 「skip 対象の曜日ではあるが、当該実行日以前に先回りで処理した」
        # 可能性があるため, skip しない
        #
        # 例: 
        # - 「2019/12/17 Tue             task-A skip:月 rep:1」
        # - task-A を 2019/12/16 Mon 時点で消化した場合
        # - skip しない場合、
        #   「2019/12/16 Mon 19:10 19:23 task-A skip:月 rep:1」
        #   このようなログにも skip が働いてしまい
        #   「2019/12/16 Tue 19:10 19:23 task-A skip:月 rep:1」
        #   このような「嘘のデータ」になってしまう
        #   (実際に消化したのは Mon なのに Tue だとみなされている)
        if len(self._endtime.strip())!=0:
            return

        y = int(self._date[0:4])
        m = int(self._date[5:7])
        d = int(self._date[8:10])
        dt = datetime.datetime(y, m, d)
        dt_original = datetime.datetime(y, m, d)

        delta1 = datetime.timedelta(days=1)
        walk_count = 0
        ops = self._options

        # skip:月 -> 月曜日はスキップ
        # skip:月木 -> 月曜日と木曜日スキップ
        # skip:平土 -> 平日と土曜日はスキップ
        # skip:休水 -> 休日と水曜日はスキップ
        skipees_by_str = ops.get('skip')
        if skipees_by_str == None:
            return
        use_mon_skip = skipees_by_str.find('月')!=-1
        use_tue_skip = skipees_by_str.find('火')!=-1
        use_wed_skip = skipees_by_str.find('水')!=-1
        use_thu_skip = skipees_by_str.find('木')!=-1
        use_fri_skip = skipees_by_str.find('金')!=-1
        use_sat_skip = skipees_by_str.find('土')!=-1
        use_sun_skip = skipees_by_str.find('日')!=-1
        use_weekday_skip = skipees_by_str.find('平')!=-1
        use_weekend_skip = skipees_by_str.find('休')!=-1

        while True:
            wd = dt.weekday()
            do_skip = False

            if use_mon_skip and is_monday(wd) or \
               use_tue_skip and is_tuesday(wd) or \
               use_wed_skip and is_wednesday(wd) or \
               use_thu_skip and is_thursday(wd) or \
               use_fri_skip and is_friday(wd) or \
               use_sat_skip and is_saturday(wd) or \
               use_sun_skip and is_sunday(wd) or \
               use_weekday_skip and is_weekday(wd) or \
               use_weekend_skip and is_weekend(wd):
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

        self._date = dt2datestr(dt)
        self._dow  = dt2dowstr(dt)

    def repeat_me(self):
        try:
            repday = int(self._options['rep'])
        except (KeyError, ValueError):
            return

        self.walk(repday)

    def to_today(self):
        today = datetime.datetime.today()
        self._date = dt2datestr(today)
        self._dow  = dt2dowstr(today)

    def start_and_end_manually(self, starttime, endtime):
        self._starttime = starttime
        self._endtime = endtime

    def to_todaytodo(self):
        self.to_today()
        self.start_and_end_manually(self.EMPTY_TIME, self.EMPTY_TIME)
        self.complete()

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

        self._date = dt2datestr(newdt)
        self._dow  = dt2dowstr(newdt)

    def smartwalk(self):
        """ smartwalk とは rep:N に対して N 日後を設定する Walk.
        rep:N なタスクは N 日後に繰り越すことが多いが,
        Walk だといちいち N を指定しなければならず手間.
        Smart Walk:
        - rep:N がある場合は N 日後に繰り越す.
        - rep:N がない場合は翌日に繰り越す. """

        # repeat_me() と実装が似ているが,
        # rep:N が無いケースも考慮必要なため DRY の対象ではない.

        DEFAULT_REPDAY_WHEN_NO_REP_ATTR = 1
        repday = DEFAULT_REPDAY_WHEN_NO_REP_ATTR
        try:
            repday = int(self._options['rep'])
        except (KeyError, ValueError):
            pass

        self.walk(repday)

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

    def reset_clonee_count(self):
        clonee_count = self.get_clonee_count()

        self._options['clone'] = 0

        # options の tostring を行う機構がないので強引だが文字列的に済ませる
        before = 'clone:{}'.format(clonee_count)
        after = 'clone:0'
        self._description = self._description.replace(before, after)

    def remove_clonee_option(self):
        clonee_count = self.get_clonee_count()

        del self._options['clone']

        before = 'clone:{}'.format(clonee_count)
        after = ''
        self._description = self._description.replace(before, after)

    def get_clonee_count(self):
        INVALID_MEANS_NO_COUNT_VIRTUALLY = 0
        try:
            clonee_count = int(self._options['clone'])
        except (KeyError, ValueError):
            clonee_count = INVALID_MEANS_NO_COUNT_VIRTUALLY

        return clonee_count

    def get_my_reference_name(self):
        try:
            refname = self._options['ref']
        except KeyError:
            raise RuntimeError('Reference attribute does not exists on this task.')

        if len(refname) == 0:
            raise RuntimeError('Reference value must not be a empty. (`ref:` is invalid)')

        refinfo = ReferenceInfo(refname, self)

        # 終了済タスクの場合は reference ファイルを作らない.
        # 「古い reference ファイルは削除しておこう」等で消してるだけかもしれないから.
        if len(self._endtime.strip()) != 0:
            refinfo.do_not_use_new_creation()

        return refinfo

    def get_my_commandline(self):
        try:
            commandline = self._options['o']
        except KeyError:
            raise RuntimeError('Open Commandline attribute does not exists on this task.')

        if len(commandline) == 0:
            raise RuntimeError('Open Commandline value must not be a empty. (`o:` is invalid)')

        return commandline

    @property
    def endtime(self):
        return self._endtime

    @property
    def description(self):
        return self._description

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5}'.format(
            self._sortmark, self._date, self._dow,
            self._starttime, self._endtime,
            self._description
        )

    def print_options(self):
        for k, v in self._options.items():
            print('{0}: [{1}]'.format(k, v))

def apply_holding(lines):
    for i, line in enumerate(lines):
        if line.find('hold:')==-1:
            continue
        task = Task(line)
        task.hold_me()
        lines[i] = str(task)

def apply_skipping(lines):
    for i, line in enumerate(lines):
        if line.find('skip:')==-1:
            continue
        task = Task(line)
        task.skip_me()
        lines[i] = str(task)

def apply_completion(lines):
    """ 記述が不足している or 不正なタスクを可能な限り補完する. """
    predefined_todays = today_and_today_without_time()

    for i, line in enumerate(lines):
        # today datetime object は生成に時間がかかるので
        # 事前に生成していたものを参照させて生成時間をカット.
        task = Task(line, predefined_todays)

        task.if_invalid_then_to_today()

        # 補完後の内容でソートマークを反映したいので
        # 最後に complete する.
        task.complete()
        lines[i] = str(task)

def apply_cloning(lines):
    additonal_lines = []

    for i, line in enumerate(lines):

        if line.find('clone:') == -1:
            continue

        task = Task(line)
        clonee_count = task.get_clonee_count()
        if clonee_count == 0:
            continue

        task.reset_clonee_count()
        task.walk(1)
        task.complete() # sortmark が更新されなくて today todo のままになるので明示的に更新
        clonee_line = str(task)
        lines[i] = clonee_line

        for i in range(clonee_count):
            cloned_task = Task(line)
            cloned_task.remove_clonee_option()
            cloned_task.to_todaytodo()
            cloned_line = str(cloned_task)
            additonal_lines.append(cloned_line)

    lines.extend(additonal_lines)

def apply_old_clonee_clearning(lines):
    '''
    1: 実行日が今日で、`clone:0`を持ってるタスクT1があったら、
    2: T1のタスク名から`replace('clone:0', '')`してタスク名TNをget
    3: 実行日が今日で、タスク名がTNであるタスクをサーチ
    4: 3を全部消す

    先に2を一気に行って対象タスク名のリストを得る。
    その後、「対象タスク名を含むタスクを消す処理」を通す。
    まだ汎用性は無さそうなのでここでハードコード。
    '''

    target_tasknames_of_clonee = []
    for i, line in enumerate(lines):
        if line.find('clone:0') == -1:
            continue
        task = Task(line)
        if not task.is_today():
            continue
        taskname = task.description
        # clonee task の名前は、`clone:0` が削除されたものに等しい
        clonee_taskname = taskname.replace('clone:0','')
        target_tasknames_of_clonee.append(clonee_taskname)

    # lines から指定行を削除するのはムズいので、
    # 削除対象行を全部取得した後、それらを remove() で一つずつ消す。
    # (普通に実装すると index がずれていって狂うので、remove() など探索的な削除メソッドに頼る)
    removee_lines = []
    for i, line in enumerate(lines):
        task = Task(line)
        if not task.is_today():
            continue
        taskname = task.description
        for clonee_taskname in target_tasknames_of_clonee:
            if taskname==clonee_taskname:
                removee_lines.append(line)
                break
    for removee_line in removee_lines:
        lines.remove(removee_line)

def apply_simple_completion(lines):
    # Simple Completion: Task.complete() を行うだけ.
    # Task の ctor で complete() が走るので
    # いったん to inst して to str するだけで completion できる.
    for i, line in enumerate(lines):
        task = Task(line)
        lines[i] = str(task)

def apply_today_report(lines):
    today_task_count = 0
    today_done_task_count = 0
    today_todo_task_count = 0
    today_estimate_total_minute = 0

    for i, line in enumerate(lines):
        task = Task(line)
        if not(task.is_today()):
            continue

        # ホールドされたタスクは区切りタスクだと思うので
        # 集計対象には含めない.
        if task.is_hold():
            continue

        today_task_count += 1
        if task.is_today_done():
            today_done_task_count += 1
        if task.is_today_todo():
            today_todo_task_count += 1

        if not(task.is_today_done()):
            # 未完了(Doneしてない)分のみ見積もりも計算
            # -> あとどれくらいで終わるかが知りたい.
            is_estimate_given, estimate_minute = task.get_estimate_info()
            if is_estimate_given:
                today_estimate_total_minute += estimate_minute

    # あると便利な情報をついでにつくっておく
    # --------------------------------------

    today_estimate_total_hour = round(today_estimate_total_minute/60.0, 2)

    _today_dt = datetime.datetime.today()
    _today_estimate_total_delta_min = datetime.timedelta(minutes=today_estimate_total_minute)
    _today_endtime_dt = _today_dt + _today_estimate_total_delta_min
    today_endtime = _today_endtime_dt.strftime('%H:%M')


    # ダイアログでレポート表示
    # ------------------------

    result_by_str = """Done {}/{} tasks. (Rest:{})
Your goal time {}. (Rest:{:02}H)""".format(
        today_done_task_count,
        today_task_count,
        today_todo_task_count,
        today_endtime,
        today_estimate_total_hour,
    )

    title = '{} Today report'.format(NAME)
    ok(result_by_str, title)

def apply_selected_range_report(lines):
    ''' 指定範囲をとにかく集計する.
    Today やら Done やらは一切考えない.
    絞りたいなら lines をつくる呼び出し元で対処する. '''

    task_count = 0
    estimate_total_minute = 0

    for i, line in enumerate(lines):
        task = Task(line)

        # ホールドされたタスクは区切りタスクだと思うので
        # 集計対象には含めない.
        if task.is_hold():
            continue

        task_count += 1

        is_estimate_given, estimate_minute = task.get_estimate_info()
        if is_estimate_given:
            estimate_total_minute += estimate_minute

    estimate_total_hour = round(estimate_total_minute/60.0, 2)

    result_by_str = """All {} tasks, {:02}[H].""".format(
        task_count,
        estimate_total_hour,
    )

    title = '{} Selected-Range report'.format(NAME)
    ok(result_by_str, title)

def apply_to_multiple_line(lines, args, methodname):
    """ @param methodname 使いたい Task クラスのメソッド名
    最初は getattr でリフレクションしようとしたが, 
    ハック要素強すぎて読みづらいので, 条件分岐で泥臭くすることに. """
    y = args.y
    y2 = args.y2
    if y2==None:
        y2 = y
    assert_y(y, lines)
    assert_y(y2, lines)

    for cnt in range(y2-y+1):
        targetidx = cnt + y
        line = lines[targetidx]
        task = Task(line)

        if methodname == 'smartwalk':
            task.smartwalk()
        elif methodname == 'walk':
            day = args.day
            task.walk(day)
        elif methodname == 'to_today':
            task.to_today()
        else:
            raise NotImplementedError('apply_to_multiple_line invalid methodname "{}"'.format(methodname))

        lines[targetidx] = str(task)

def apply_to_keyword_today_line(lines, args, methodname):
    walking_tag = args.walking_tag
    for curidx,line in enumerate(lines):
        if line.find(walking_tag) == -1:
            continue

        task = Task(line)
        if not(task.is_today_todo()):
            continue
        # line,find だけだと「description 以外の部分で一致した」ケースがある.
        # 高い精度のために, description 内での find も判定する.
        if not(task.is_contained_in_description(walking_tag)):
            continue

        if methodname == 'smartwalk':
            task.smartwalk()
        elif methodname == 'walk':
            day = args.day
            task.walk(day)
        elif methodname == 'to_today':
            task.to_today()
        else:
            raise NotImplementedError('apply_to_keyword_today_line invalid methodname "{}"'.format(methodname))

        lines[curidx] = str(task)

def apply_to_multiple_line_or_keyword_today_line(lines, args, methodname):
    walking_tag = args.walking_tag
    if walking_tag != None:
        apply_to_keyword_today_line(lines, args, methodname)
        return

    apply_to_multiple_line(lines, args, methodname)

def apply_posteriori_end_to_the_task(lines, line_number_of_target_task):
    """指定タスクを報告的終了(Posteriori end)する.

    報告的終了とは「さっきまでをXXXXやってました」を記録すること.
    - 開始時間は, 直近最も遅く終えたタスクの終了時間(latest done task)
    - 終了時間は, 現在日時

    今までの「start(これからXXXXをやります)」「end(終わりました)」ではなく,
    startを省略して一気に「end(さっきまでXXXXをやってました)」を記録する.

    startしそびれたタスクを後から記録するのに便利な方式である.

    @param lines 破壊的 """

    today_task = None
    for i, line in enumerate(lines):
        task = Task(line)
        if not(task.is_today_done()):
            continue
        today_task = task
    # とりあえずソートされていることを前提とする.
    # その場合, 最も後の行にある today done が latest done task になる.
    latest_done_task_in_today = today_task
    if latest_done_task_in_today==None:
        return

    starttime = latest_done_task_in_today.endtime
    endtime = nowtimestr()

    line = lines[line_number_of_target_task]
    task = Task(line)
    task.start_and_end_manually(starttime, endtime)

    lines[line_number_of_target_task] = str(task)

class reporting:

    def main():
        reporting.report()

    def _report_per_a_classifier(a_classifier, caption, report_outname):
        """ @param a_classifier classifier.daily とか classifier.monthly とか
        @param caption 'Daily' など観点名
        @param report_outname レポート内容保存先ファイル名 """

        # trita ファイルと同じディレクトリに保存する
        report_outpdir = os.path.abspath(os.path.dirname(args.input))
        report_outpath = os.path.join(report_outpdir, report_outname)

        formatter = reporting.MarkdownFormatter(filename=report_outpath)

        element_count = len(a_classifier.keys())
        formatter.header(caption, element_count)

        counter = reporting.Counter(a_classifier)
        data_dict = counter.data_dict

        # 降順でパースする
        sorted_keys = sorted(data_dict.keys())
        sorted_keys.reverse()

        for k in sorted_keys:
            classified_key = k
            counted_data = data_dict[k]
            formatter.body(counted_data, classified_key)

        formatter.footer()

        formatter.save()

    def report():
        countee_tasks = []
        for idx,line in enumerate(lines):
            countee_task = reporting.CounteeTask(line)
            if countee_task.is_invalid():
                continue
            countee_tasks.append(countee_task)
        dp('All {} tasks.'.format(len(countee_tasks)))

        classifier = reporting.Classifier(countee_tasks)

        # report 機能はコマンドライン引数をシンプルにしたい＆
        # どうせオレオレ用なので保存ファイル名は決め打ちでいいっす.
        reporting._report_per_a_classifier(classifier.daily, 'Daily', 'report_daily.md')
        reporting._report_per_a_classifier(classifier.monthly, 'Monthly', 'report_monthly.md')
        reporting._report_per_a_classifier(classifier.hourband, 'Hourly', 'report_hourly.md')

    # あまり上手く練れてないけど、タスクハッシュつくってカウント数でランキングしてみる機能
    def report_taskcountranking():
        print('All {} tasks.'.format(len(lines)))

        tasks = []
        for idx,line in enumerate(lines):
            task = Task(line)

            # 本当は区切りタスクや今日のタスクなどは省くべきだろうが
            # とりあえず全部扱ってみる

            tasks.append(task)

        ranking_dict = {}
        for task in tasks:
            taskname = task.description
            not_found = not taskname in ranking_dict
            if not_found:
                ranking_dict[taskname] = {}
                ranking_dict[taskname]['count'] = 0
            ranking_dict[taskname]['count'] += 1

        # 慣れないのでメモ
        # - 辞書のソートは items() ベースじゃないとできない
        # - items() は「(key, value) の tuple」から成るリスト
        #
        # item を print してみるとこうなってる
        #   ('今日のタスク(実行中)', {'count': 1})
        #   ('--- 明日以降のタスク hold:1', {'count': 1})
        #   ('明日のタスク', {'count': 3})
        ranking_asc_sorted_items = sorted(
            ranking_dict.items(),
            key=lambda item:item[1]['count']
        )
        ranking_desc_sorted_items = reversed(ranking_asc_sorted_items)

        for item in ranking_desc_sorted_items:
            taskname, count = item[0], item[1]['count']
            print('- {}: {}'.format(count, taskname))

        #print('All {} no-dup tasked.'.format(len(ranking_asc_sorted_list)))

    class Formatter:
        def __init__(self, *args, **kwargs):
            pass

        def body(self, counted_data, classifiled_key):
            self._aw_total_min  = counted_data.actual_worktime_total
            self._aw_total_hour = round(self._aw_total_min/60, 1)
            self._aw_avg_min    = round(counted_data.actual_worktime_average, 1)
            self._task_count    = counted_data.task_count

            self._body(classifiled_key)

        def header(self, caption, element_count):
            raise NotImplementedError

        def footer(self):
            raise NotImplementedError

        def _body(self, classifiled_key):
            raise NotImplementedError

        def save(self):
            raise NotImplementedError

    class DebugPrintFormatter(Formatter):
        def __init__(self, *args):
            super().__init__(*args)

            self._lines = []

        def header(self, caption, element_count):
            self._lines.append('[{}]'.format(caption))
            self._lines.append('All {} keys.'.format(element_count))

        def footer(self):
            pass

        def _body(self, classifiled_key):
            line = '{} : {} tasks with Total:{}[M]({}[H]) Avg:{}[M]'.format(
                classifiled_key,
                self._task_count,
                self._aw_total_min,
                self._aw_total_hour,
                self._aw_avg_min
            )
            self._lines.append(line)

        def save(self):
            for line in self._lines:
                dp(line)

    class MarkdownFormatter(Formatter):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            try:
                filepath = kwargs['filename']
            except KeyError:
                raise RuntimeError('MarkdownFormatter requires the filepath to save!')

            self._filepath = filepath
            self._lines = []

        def header(self, caption, element_count):
            self._lines.append('# {}'.format(caption))
            self._lines.append('All {} keys.'.format(element_count))
            self._lines.append('')

        def footer(self):
            pass

        def _body(self, classifiled_key):
            line = '- {} : {} Tasks, Total:{}[H], Avg:{}[M]'.format(
                classifiled_key,
                self._task_count,
                self._aw_total_hour,
                self._aw_avg_min
            )
            self._lines.append(line)

        def save(self):
            list2file(self._filepath, self._lines)

    class CountedData():
        def __init__(self):
            self._task_count = 0

            self._actual_worktimes = []

        def plus_task_count(self, count):
            self._task_count += count

        def add_actual_worktime(self, countee_task):
            starttimestr = countee_task._starttime
            endtimestr = countee_task._endtime

            # 作業実績時間は end - start.
            # これを datetime を使って計算する.
            # datetime では year/month/day が必要なのでダミーを使う.

            # 13:25 13:55
            # ^^ ^^ ^^ ^^
            # sh sm eh em

            fixeddate = (2011, 11, 11)
            try:
                starth, startm = int(starttimestr[0:2]), int(starttimestr[3:5])
                endh, endm = int(endtimestr[0:2]), int(endtimestr[3:5])
                dt_start = datetime.datetime(*fixeddate, starth, startm)
                dt_end = datetime.datetime(*fixeddate, endh, endm)
            except ValueError:
                # エラーは出ないと思ってるけど, とりあえず出してみるか.
                dp('actual worktime calcerror at ' + countee_task)
                raise

            delta = dt_end - dt_start
            actual_second = delta.total_seconds()

            # tritask は分単位なので最低でも分で扱う.
            # が, 時単位はでかすぎる(基本的にタスクは粒度が小さいはず)ので
            # 時単位には丸めない.
            actual_minute = int(actual_second/60)

            # 1分未満のタスクはとりあえず 1 分として計算してみる.
            # 細かい定期タスクが多い場合, 0ばかりになっちゃうから.
            if actual_minute==0:
                actual_minute = 1

            self._actual_worktimes.append(actual_minute)

        @property
        def task_count(self):
            return self._task_count

        @property
        def actual_worktime_total(self):
            total = 0
            for t in self._actual_worktimes:
                total += t
            return total

        @property
        def actual_worktime_average(self):
            total = self.actual_worktime_total
            average = total / len(self._actual_worktimes)
            return average

    class Counter():
        #classified_dict = {
        #   "2018/04/07" : [CounteeTask, CounteeTask, ...]
        #   ...
        #}
        #
        #counted_data_with_classified = {
        #   "2018/04/07" : CountedData
        #   ...
        #}
        def __init__(self, classified_dict):
            self._counted_data_with_classified = {}

            for k in classified_dict:
                countee_tasks = classified_dict[k]

                counted_data = reporting.CountedData()
                task_count = len(countee_tasks)

                # タスク数
                counted_data.plus_task_count(task_count)

                # 作業実績時間系
                for countee_task in countee_tasks:
                    counted_data.add_actual_worktime(countee_task)

                self._counted_data_with_classified[k] = counted_data

        @property
        def data_dict(self):
            return self._counted_data_with_classified

    # 日毎, 月毎などの集約を行うクラス.
    # 内部的には各タスクが返した「私はこのキーで分類してください」情報を
    # そのままキーとして辞書に突っ込んでるだけ.
    # (つまり全タスクを分類キー単位で仕分けたい)
    class Classifier():
        def __init__(self, countee_tasks):
            self._d_daily = {}
            self._d_monthly = {}
            self._d_hourband = {}

            for countee_task in countee_tasks:
                key_daily = countee_task.key_daily
                key_monthly = countee_task.key_monthly
                key_hourband = countee_task.key_hourband

                self._smart_append(self._d_daily, key_daily, countee_task)
                self._smart_append(self._d_monthly, key_monthly, countee_task)
                self._smart_append(self._d_hourband, key_hourband, countee_task)

        def _smart_append(self, container, key, value):
            if not key in container:
                container[key] = []
            container[key].append(value)

        @property
        def daily(self):
            return self._d_daily

        @property
        def monthly(self):
            return self._d_monthly

        @property
        def hourband(self):
            return self._d_hourband

    class CounteeTask(Task):
        def __init__(self, *args):
            super().__init__(*args)

            self._is_invalid = False

            # 以下のタスクは集計対象外.
            # - 終了していないタスク
            # - 区切り
            # - インボックス(日付が未定)
            is_not_ended = len(self._endtime.strip())==0
            has_separator = self._description.find(' --') != -1
            is_inbox = len(self._date.strip())==0
            if is_not_ended or has_separator or is_inbox:
                self._is_invalid = True
                return

        def is_invalid(self):
            return self._is_invalid

        # 1 2018/04/27 Fri 13:00 14:01 Task1
        #  ||
        #  VV
        # Daily    : YYYY/MM/DD 2018/04/27
        # Monthly  : YYYY/MM    2018/04
        # Hour     : HH         13

        @property
        def key_daily(self):
            return self._date

        @property
        def key_monthly(self):
            return '/'.join(self._date.split('/')[:2])

        @property
        def key_hourband(self):
            h_str = self._starttime.split(':')[0]
            h_int = int(h_str)
            return '{:02}'.format(h_int)

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # options
    # -------

    parser.add_argument('-i', '--input', default=None,
        help='A input filename.')

    parser.add_argument('-y', default=None, type=int,
        help='The start line number of a input line. 0-ORIGIN.')
    parser.add_argument('--y2', default=None, type=int,
        help='The end line number of a input line. 0-ORIGIN.')

    parser.add_argument('--walking-tag', default=None, type=str,
        help='The keyword in today tasks to walk.')
    parser.add_argument('-d', '--day', default=None, type=int,
        help='The day count to walk.')

    parser.add_argument('--to-today', default=False, action='store_true',
        help='Change the current task day to today. MUST: -y')
    parser.add_argument('--repeat', default=False, action='store_true',
        help='Walk day in the current task with rep:n param. MUST: -y.')
    parser.add_argument('--walk', default=False, action='store_true',
        help='Walk day in the current task. MUST: -y and -d.')
    parser.add_argument('--smartwalk', default=False, action='store_true',
        help='Walk +N or +1 day in the current task. MUST: -y')
    parser.add_argument('--sort', default=False, action='store_true',
        help='Do sort.')

    parser.add_argument('--use-simple-completion', default=False, action='store_true',
        help='Do simple completion of each line, but do not sort and to-today completion.')

    parser.add_argument('--ref', default=False, action='store_true',
        help='Open the reference writing space. MUST: -y')
    parser.add_argument('--refconf-dir', default='ref',
        help='--ref options: The location which the reference file saved.')
    parser.add_argument('--refconf-ext', default='md',
        help='--ref options: The extension which the reference file has.')

    parser.add_argument('--open', default=False, action='store_true',
        help='[ONLY WINDOWS] Open the commandline of `o:(COMMAND-LINE)` attribute with system association. MUST: -y.')

    parser.add_argument('--end-now', default=False, action='store_true',
        help='End the task as `from (endtime of the latest done task) to (now)`. MUST: -y')

    # reporting
    # ---------

    parser.add_argument('--today-dialog-report', default=False, action='store_true',
        help='[ONLY WINDOWS] Display today report with dialog.')
    parser.add_argument('--selected-range-dialog-report', default=False, action='store_true',
        help='[ONLY WINDOWS] Display report of selected range with dialog.')

    parser.add_argument('--report', default=False, action='store_true',
        help='Debug mode for reporting.')

    parser.add_argument('--task-count-ranking', default=False, action='store_true',
        help='Display the ranking of given tasks based on occuring-count.')

    # deugging
    # --------

    parser.add_argument('-v', '--version', default=False, action='store_true',
        help='[ONLY WINDOWS] Display "{}" to version dialog.'.format(INFO))

    parser.add_argument('--debug', default=False, action='store_true',
        help='Debug mode. (Show information to debug.)')
    parser.add_argument('--raw-error', default=False, action='store_true',
        help='Debug mode. (Show raw error message.)')

    args = parser.parse_args()
    return args

def get_default_configs():
    """ valueについて
    - None or 文字列で定義する
    - 二値を表現したい場合は, FalseをNoneで, Trueを任意の文字列で.
    """

    # 未実装メモ
    # - debug-display-config-with-dialog-after-sorting
    #   sort後にdialogすると, なぜか秀丸エディタ側でtritaファイルが空になる.
    #   西尾開くと空になってない(つまりtritaファイルの中身が実際に空になったわけではない)が,
    #   非常に心臓に悪い. 原因もわからないのでいったんナシ.
    #   config のデバッグがしたくなったら別手段を検討しよう.

    configs = {
        'keywords-to-exclude-from-task-count' : '',
        'debug-display-config-with-dialog-after-sorting' : None,
    }

    return configs
configs_in_global = get_default_configs()

def load_configs_from_lines(configs, lines):
    """ @param configs ここに反映する. 破壊的. """

    # config行は泥臭く判定する.
    # 以下あたりを使ってうまく.
    #
    #                              config keywords-to-exclude-from-task-count   |●,diary 
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^~~~~~~                                       ^
    # 1                            2                                            3

    TASKLINE_LENGTH_BEFORE_DESCRIPTION = 29
    CONFIG_MARK = 'config'
    CONFIG_DELIMITOR = '|'
    minimum_length = TASKLINE_LENGTH_BEFORE_DESCRIPTION + len(CONFIG_MARK)

    for i, line in enumerate(lines):
        if len(line) <= minimum_length:
            continue
        # config は inbox task として書くことを想定
        if line[:TASKLINE_LENGTH_BEFORE_DESCRIPTION].strip() != '':
            continue
        if line.find(CONFIG_MARK) == -1:
            continue
        # config 表記の先頭はスペースで開けることを想定
        # この制約により config をオフりたい場合は zconfig
        #                                          ^
        #                                 このように何か付けるだけで済む
        if line.find(' ' + CONFIG_MARK) == -1:
            continue
        if line.find(CONFIG_DELIMITOR) == -1:
            continue

        MAXSPLIT = 1
        _, kv = line.split(CONFIG_MARK, MAXSPLIT)
        key, value = kv.split(CONFIG_DELIMITOR, MAXSPLIT)

        # key は whitespace で見た目整えることを想定
        # 正しい key を得るために whitespace を省く
        key = key.strip()

        try:
            configs[key] = value
        except KeyError:
            raise KeyError('No config key "{}"'.format(key))

def proceed_lines_and_is_save_required(args, lines):
    """ @param lines 破壊的 """

    load_configs_from_lines(configs_in_global, lines)

    if args.debug and args.y!=None:
        task = Task(lines[args.y])
        print(task)
        task.print_options()

    if args.report:
        reporting.main()
        return False

    if args.task_count_ranking:
        reporting.report_taskcountranking()
        return False

    if args.today_dialog_report:
        apply_today_report(lines)
        return False

    if args.selected_range_dialog_report:
        y = args.y
        y2 = args.y2
        if y==None or y2==None:
            ok('Do select lines what you get the report.', NAME)
            return False
        assert_y(y, lines)
        assert_y(y2, lines)
        apply_selected_range_report(lines[y:y2+1])
        return False

    if args.ref:
        y = args.y
        assert_y(y, lines)

        line = lines[y]
        task = Task(line)
        refinfo = task.get_my_reference_name()
        reference_opener(refinfo)
        return False

    if args.open:
        y = args.y
        assert_y(y, lines)

        line = lines[y]
        task = Task(line)
        commandline = task.get_my_commandline()
        open_commandline_with_system_association(commandline)
        return False

    if args.end_now:
        y = args.y
        assert_y(y, lines)

        apply_posteriori_end_to_the_task(lines, y)

        return True

    if args.walk:
        apply_to_multiple_line_or_keyword_today_line(lines, args, 'walk')
        return True

    if args.smartwalk:
        apply_to_multiple_line_or_keyword_today_line(lines, args, 'smartwalk')
        return True

    if args.repeat:
        y = args.y
        assert_y(y, lines)

        line = lines[y]
        task = Task(line)
        task.repeat_me()

        lines[y] = str(task)

        return True

    if args.to_today:
        apply_to_multiple_line_or_keyword_today_line(lines, args, 'to_today')
        return True

    if args.use_simple_completion:
        apply_simple_completion(lines)
        return True

    if args.sort:
        apply_holding(lines)
        apply_skipping(lines)
        apply_completion(lines)

        apply_cloning(lines)
        apply_old_clonee_clearning(lines)

        lines.sort()

        return True

    raise RuntimeError('No valid option.')

def ________Main________from_here____():
    pass

if __name__ == '__main__':
    args = parse_arguments()

    if args.version:
        open_version_dialog()
        exit(0)

    MYDIR = os.path.abspath(os.path.dirname(__file__))
    infile = args.input
    lines = file2list(infile)

    logfile = os.path.join(MYDIR, 'tritask.log')
    if not(os.path.exists(logfile)):
        # new file if does not exists.
        list2file(logfile, [])
    loglines = file2list(logfile)

    try:
        is_save_required = proceed_lines_and_is_save_required(args, lines)
        if is_save_required:
            outfile = infile
            list2file(outfile, lines)
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
