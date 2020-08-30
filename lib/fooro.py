#!/usr/bin/python3

from . import common
from . import table

naki_pai1 = [ # チー用
    '1m', '2m', '3m', '4m', '5m', '6m', '7m',
    '1p', '2p', '3p', '4p', '5p', '6p', '7p',
    '1s', '2s', '3s', '4s', '5s', '6s', '7s',
]

naki_pai2 = [ # ポン/カン用
    '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
    '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
    '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
    '東', '南', '西', '北', '白', '發', '中',
]


def chi(x):
    '''
    BIT	HEX	内容
    1-2	0x0003	食われた人(上家からしかチーできないので常に3)
    3	0x0004	順子フラグ 1
    4-5	0x0018	最小の数牌のID mod 4
    6-7	0x0060	真ん中の数の数牌のID mod 4
    8-9	0x0180	最大の数牌のID mod 4
    10	0x0200	空き
    11-16	0xfc00	t。1m-7m,1s-7s,1p-7pの21枚の中で floor(t/3)番目のものを最小の数牌とする。
    '''

    t = int(x[0:6], 2)

    min_hai = naki_pai1[int(t / 3)] # 構成面子の最小牌
    if min_hai[0] == '5': # 5は赤の分だけずれるので修正
        base_id = table.pai.index(min_hai) - 1
    else:
        base_id = table.pai.index(min_hai)

    hai1_id = base_id + 0 + int(x[11:13], 2) # 構成面子の小さい数の牌ID
    hai2_id = base_id + 4 + int(x[9:11], 2)  # 構成面子の真ん中の牌ID
    hai3_id = base_id + 8 + int(x[7:9], 2)   # 構成面子の大きい数の牌ID

    naki_hai = str(int(min_hai[0]) + t % 3) + min_hai[1] # 鳴いた牌
    if naki_hai[0] == '5': # 鳴いた牌が5で面子構成に赤が含まれていたら0に置き換え
        if hai1_id in (16, 52, 88) or hai2_id in (16, 52, 88) or hai3_id in (16, 52, 88):
            naki_hai = '0' + naki_hai[1]

    mentu = [table.pai[hai1_id], table.pai[hai2_id], table.pai[hai3_id]]
    #print('DEBUG:', i, x, t, min_hai, naki_hai, mentu, hai1_id, hai2_id, hai3_id)
    mentu.remove(naki_hai)
    mentu.insert(0, '[' + naki_hai + ']')

    return('チー(' + ' '.join(mentu) + ')')


def pon(x):
    '''
    BIT	HEX	内容
    1-2	0x0003	食われた人 下家1,対面2,上家3
    3	0x0004	空き
    4	0x0008	刻子フラグ 刻子なら1
    5	0x0010	加槓フラグ 加槓なら1
    6-7	0x0060	未使用牌ID mod4
    8-9	0x0180	空き
    10-16	0xfe00	t。1m-中の34枚の中で floor(t/3)番目のものを鳴いた牌とする。
            未使用牌を除いて昇順に並べた時、t % 3番めの牌が鳴かれた牌
    '''

    # Todo: 赤をポンしたとき
    a = table.pai.index(naki_pai2[int(int(x[0:7], 2) / 3)])
    if x[14:] == '01': # 下家
        k = ' '.join((table.pai[a], table.pai[a], '[' + table.pai[a] + ']'))
    if x[14:] == '10': # 対面
        k = ' '.join((table.pai[a], '[' + table.pai[a] + ']', table.pai[a]))
    if x[14:] == '11': # 上家
        k = ' '.join(('[' + table.pai[a] + ']', table.pai[a], table.pai[a]))

    return('ポン(' + k +')')


def kakan(x):
    '''
    ポンと同じ
    '''

    # Todo: 赤
    a = table.pai.index(naki_pai2[int(int(x[0:7], 2) / 3)])
    if x[14:] == '01': # 下家
        k = ' '.join((table.pai[a], table.pai[a], table.pai[a], '[' + table.pai[a] + ']'))
    if x[14:] == '10': # 対面
        k = ' '.join((table.pai[a], '[' + table.pai[a] + ']', table.pai[a], table.pai[a]))
    if x[14:] == '11': # 上家
        k = ' '.join(('[' + table.pai[a] + ']', table.pai[a], table.pai[a], table.pai[a]))

    return('加槓(' + k + ')')


def kan(x):
    a = table.pai.index(naki_pai2[int(int(x[0:7], 2) / 3)])
    if x[14:] == '00': # 暗槓
        if naki_pai2[int(int(x[0:7], 2) / 3)][0] == '5': # 赤が含まれる場合
            k = ' '.join((table.pai[a], table.pai[a-1], table.pai[a], table.pai[a]))
        else:
            k = ' '.join((table.pai[a], table.pai[a], table.pai[a], table.pai[a]))
        ret = '暗槓(' + k +')'
    if x[14:] == '01': # 下家
        k = ' '.join((table.pai[a], table.pai[a], table.pai[a], '[' + table.pai[a] + ']'))
        ret = '大明槓(' + k + ')'
    if x[14:] == '10': # 対面
        k = ' '.join((table.pai[a], '[' + table.pai[a] + ']', table.pai[a], table.pai[a]))
        ret = '大明槓(' + k + ')'
    if x[14:] == '11': # 上家
        k = ' '.join(('[' + table.pai[a] + ']', table.pai[a], table.pai[a], table.pai[a]))
        ret = '大明槓(' + k + ')'

    return(ret)