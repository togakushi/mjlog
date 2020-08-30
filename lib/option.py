#!/usr/bin/python3

import argparse

epilog_msg = '''
【和銃データ】
和了率: 和了回数/総局数
自摸和: 自摸和回数/和了回数
栄和: 栄和回数/和了回数
和了時： 和了したときの手牌状況
放銃率: 放銃回数/総局数
放銃時: 放銃したときの手牌状況
放銃相手: 放銃した相手の手牌状況
被自摸率: ツモられ

【立直データ】
立直率: リーチ宣言回数/総局数
立直後： リーチしたあとの和銃状況
立直収支: リーチ宣言した局収支の平均(供託含む)

【副露データ】
副露率: 副露した局/総局数
副露後： 副露したあとの和銃状況
副露収支: 副露した局収支の平均(供託含む)
'''
 
def parser():
    p = argparse.ArgumentParser(
        formatter_class = argparse.RawTextHelpFormatter,
        description = '天鳳 牌譜ログ 解析スクリプト',
        epilog = '-' * 70 + epilog_msg,
        add_help = True,
    )
    p.add_argument('-l', '--log', nargs='*', required=True)
    p.add_argument('--limit', type=int, default=0, help='解析ログを指定数に絞る')
    p.add_argument('-p', '--player', default=None, nargs='*')
    p.add_argument('-i', '--init', action='store_true', help='配牌情報を表示する')
    p.add_argument('-s', '--sute', action='store_true', help='捨牌情報を表示する')
    p.add_argument('-r', '--result', action='store_true', help='局収支情報を表示する')
    p.add_argument('-o', '--owari', action='store_true', help='最終情報を表示する')
    p.add_argument('-v', '--verbos', action='store_true', help='ちょっとした情報を表示する')
    p.add_argument('-x', '--vicissitudes', choices=['houju', 'h', 'reach', 'r', 'fooro', 'f', 'basic', 'b'], help='成績遷移')
    p.add_argument('-c', '--count', type=int, default=15, help='成績遷移を指定数だけに絞る')
    p.add_argument('-q', '--quiet', action='store_false', help='統計情報を表示しない')
    p.add_argument('-d', '--debug', action='store_true', help='デバッグ情報を表示する')

    return(p.parse_args())
