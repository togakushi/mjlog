#!/usr/bin/python3

import argparse

epilog_msg = '''
【和銃データ】
\t和了率: 和了回数/総局数
\t自摸和: 自摸和回数/和了回数
\t栄和: 栄和回数/和了回数
\t和了時： 和了したときの手牌状況
\t放銃率: 放銃回数/総局数
\t放銃時: 放銃したときの手牌状況
\t放銃相手: 放銃した相手の手牌状況
\t被自摸率: ツモられ

【立直データ】
\t立直率: リーチ宣言回数/総局数
\t立直後： リーチしたあとの和銃状況
\t立直収支: リーチ宣言した局収支の平均(供託含む)

【副露データ】
\t副露率: 副露した局/総局数
\t副露後： 副露したあとの和銃状況
\t副露収支: 副露した局収支の平均(供託含む)
'''
 
help_vicissitudes = '''
成績遷移を表示する
\thouju, h: 放銃率遷移
\treach, r: 立直率遷移
\tfooro, f: 副露率遷移
\tbasic, b: 基本情報遷移
'''.strip()

def parser():
    p = argparse.ArgumentParser(
        formatter_class = argparse.RawTextHelpFormatter,
        description = '天鳳 牌譜ログ 解析スクリプト',
        epilog = '-' * 70 + epilog_msg + '-' * 70,
        add_help = True,
    )

    p.add_argument(
        '-q', '--quiet', action = 'store_false',
        help = '統計情報を表示しない',
    )
    p.add_argument(
        '-d', '--debug', action = 'store_true',
        help = 'デバッグ情報を表示する',
    )

    g1 = p.add_argument_group('解析指定オプション')
    g1.add_argument(
        '-l', '--log', required=True, nargs = '*',
        metavar = 'mjlog',
        help = '解析するログを指定(必須)',
    )
    g1.add_argument(
        '--limit', type = int, default = 0,
        metavar = '制限数',
        help = '\n解析ログを指定数に絞る\n(default: 0)',
    )
    g1.add_argument(
        '-p', '--player', default = None, nargs = '*',
        metavar = 'プレイヤー名',
        help = '解析対象プレイヤー名を指定',
    )
    g1.add_argument(
        '-t', '--taku', default = '0,1,2,3',
        metavar = '0,1,2,3',
        help = '解析対象の卓をカンマ区切りで指定する\n0:一般 1:上級 2:特上 3:鳳凰\n(default: 0,1,2,3)',
    )

    g2 = p.add_argument_group('対局情報表示オプション')
    g2.add_argument(
        '-i', '--init', action = 'store_true',
        help = '各局の配牌情報を表示する',
    )
    g2.add_argument(
        '-s', '--sute', action = 'store_true',
        help = '各局の捨牌情報を表示する',
    )
    g2.add_argument(
        '-r', '--result', action = 'store_true',
        help = '各局の局収支情報を表示する',
    )
    g2.add_argument(
        '-o', '--owari', action = 'store_true',
        help = '各試合の最終情報を表示する',
    )
    g2.add_argument(
        '-v', '--verbos', action = 'store_true',
        help = 'ちょっとした情報を表示する(お試し中)',
    )

    g3 = p.add_argument_group('成績遷移表示オプション')
    g3.add_argument(
        '-x', '--vicissitudes',
        choices = ['houju', 'h', 'reach', 'r', 'fooro', 'f', 'basic', 'b'],
        help = help_vicissitudes,
    )
    g3.add_argument(
        '-c', '--count', type = int, default = 15,
        metavar = '件数',
        help = '\n成績遷移の表示件数を指定数だけに絞る\n(default: 15)',
    )

    return(p.parse_args())
