#!/usr/bin/python3

import copy

from . import common
from . import table
from . import analysis
from . import fooro

def ho(args, sekijun, oya, player, sutehai):
    print('  河>')
    c = 0
    latest = ''

    h = ''.join([str(x) for x in range(len(sekijun))])

    for seki in h[int(oya):] + h[:int(oya)]:
        sute = []
        for x in sutehai[int(seki)]:
            if int(x) == -1: # 鳴かれ
                latest = sute.pop()
                sute.append('(' + latest + ')')
                continue
            elif int(x) == -2: # 北抜き
                sute.append('(北)')
                continue
            else:
                sute.append(table.pai[int(x)])
            latest = table.pai[int(x)]

        print('    {}({}): {}'.format(sekijun[c], player[int(seki)], ' '.join(sute)))
        c += 1


def agari(args, player, sutehai, mj, flag, junme, saisyukei):
    '''
    和了したときの状態を表示
    '''

    msg = '  和了>\n'

    if args.debug:
        print('DEBUG:', mj.attrib)

    player_no = common.GetPosition(args, player)
    sc = [int(x) for x in mj.attrib['sc'].split(',')]

    if not player_no == None:
        if flag['reach'][player_no]:
            analysis.counter['立直収支'].append(sc[player_no * 2 + 1] * 100)
        if flag['naki'][player_no]:
            analysis.counter['副露収支'].append(sc[player_no * 2 + 1] * 100)

    if mj.attrib['who'] == mj.attrib['fromWho']:
        msg += '    和了: {} (ツモ)\n'.format(player[int(mj.attrib['who'])])

        analysis.add_agari(player[int(mj.attrib['who'])], 1)
        hitumo  = [0, 1, 2, 3]
        hitumo.remove(int(mj.attrib['who']))
        for x in hitumo:
            analysis.add_agari(player[x], 7)
            if player_no == x: # 解析対象
                if flag['oya']:
                    analysis.counter['被自摸_親'].append(sc[player_no * 2 + 1] * 100)
                else:
                    analysis.counter['被自摸_子'].append(sc[player_no * 2 + 1] * 100)

        # 和銃分布
        if common.IsTarget(args, player, int(mj.attrib['who'])):
            p = int(mj.attrib['who'])
            analysis.counter['和了巡目'].append(junme[p])
            analysis.counter['和了点'].append(int(mj.attrib['ten'].split(',')[1]))

            if flag['reach'][p]:
                analysis.agari_dist['和了時']['立直'] += 1
                analysis.counter['立直和了'] += 1
                analysis.counter['立直収入'].append(sc[player_no * 2 + 1] * 100)
            if flag['naki'][p]:
                analysis.agari_dist['和了時']['副露'] += 1
                analysis.counter['副露和了'] += 1
                analysis.counter['副露収入'].append(sc[player_no * 2 + 1] * 100)
            if not flag['reach'][p] and not flag['naki'][p]:
                analysis.agari_dist['和了時']['ダマ'] += 1
    else:
        msg += '    和了: {} 放銃: {}\n'.format(player[int(mj.attrib['who'])], player[int(mj.attrib['fromWho'])])

        analysis.add_agari(player[int(mj.attrib['who'])], 2)
        analysis.add_agari(player[int(mj.attrib['fromWho'])], 3)
        yokoidou = [0, 1, 2, 3]
        yokoidou.remove(int(mj.attrib['who']))
        yokoidou.remove(int(mj.attrib['fromWho']))
        for x in yokoidou:
            analysis.add_agari(player[x], 0)

        # 和銃分布
        if common.IsTarget(args, player, int(mj.attrib['who'])):
            p = int(mj.attrib['who'])
            analysis.counter['和了巡目'].append(junme[p])
            analysis.counter['和了点'].append(int(mj.attrib['ten'].split(',')[1]))

            if flag['reach'][p]:
                analysis.agari_dist['和了時']['立直'] += 1
                analysis.counter['立直和了'] += 1
                analysis.counter['立直収入'].append(sc[player_no * 2 + 1] * 100)
            if flag['naki'][p]:
                analysis.agari_dist['和了時']['副露'] += 1
                analysis.counter['副露和了'] += 1
                analysis.counter['副露収入'].append(sc[player_no * 2 + 1] * 100)
            if not flag['reach'][p] and not flag['naki'][p]:
                analysis.agari_dist['和了時']['ダマ'] += 1

        if common.IsTarget(args, player, int(mj.attrib['fromWho'])):
            p = int(mj.attrib['fromWho'])
            a = int(mj.attrib['who'])

            analysis.counter['放銃巡目'].append(junme[p])
            analysis.counter['放銃点'].append(int(mj.attrib['ten'].split(',')[1]))
            analysis.counter['放銃時向聴数'].append(common.CountShanten(','.join(saisyukei)))

            if flag['reach'][p]:
                analysis.agari_dist['放銃時']['立直'] += 1
                analysis.counter['立直放銃'] += 1
                analysis.counter['立直支出'].append(sc[player_no * 2 + 1] * 100)
            if flag['naki'][p]:
                analysis.agari_dist['放銃時']['副露'] += 1
                analysis.counter['副露放銃'] += 1
                analysis.counter['副露支出'].append(sc[player_no * 2 + 1] * 100)
            if not flag['reach'][p] and not flag['naki'][p]:
                analysis.agari_dist['放銃時']['面前'] += 1
            if flag['reach'][a]:
                analysis.agari_dist['放銃相手']['立直'] += 1
            if flag['naki'][a]:
                analysis.agari_dist['放銃相手']['副露'] += 1
            if not flag['reach'][a] and not flag['naki'][a]:
                analysis.agari_dist['放銃相手']['ダマ'] += 1

    # ドラ
    omo_d = []
    ura_d = []
    if 'doraHai' in mj.attrib:
        for x in mj.attrib['doraHai'].split(','):
            omo_d.append(common.dora(int(x)))
    if 'doraHaiUra' in mj.attrib:
        for x in mj.attrib['doraHaiUra'].split(','):
            ura_d.append(common.dora(int(x)))
    if ura_d == []:
        msg += '    ドラ: {}\n'.format(' '.join(omo_d))
    else:
        msg += '    ドラ: {} 裏ドラ: {}\n'.format(' '.join(omo_d), ' '.join(ura_d))

    mentu = ''
    if 'm' in mj.attrib:
        for m in mj.attrib['m'].split(','):
            x = format(int(m), '#018b')[2:]
            #print('DEBUG:', i, x)

            if x[13] == '1': # チー
                mentu = mentu + fooro.chi(x) + ' '
            else:
                if x[12] == '1': # ポン
                    mentu = mentu + fooro.pon(x) + ' '
                if x[11] == '1': # 加槓
                    mentu = mentu + fooro.kakan(x) + ' '
            if x[10:16] == '100000': # 北抜き
                pass
            else:
                if x[11:14] == '000': # カン
                    mentu = mentu + fooro.kan(x) + ' '

    saisyukei = common.data_to_hai(mj.attrib['hai'])
    saisyukei.remove(table.pai[int(mj.attrib['machi'])])

    msg += '    最終形: {} {} 和了牌: {}\n'.format(' '.join(saisyukei), mentu, table.pai[int(mj.attrib['machi'])])

    if 'yaku' in mj.attrib:
        y = ''
        han = 0
        for x in range(0,len(mj.attrib['yaku'].split(',')),2):
            y = y + '{0}({1}) '.format(
                table.yaku[int(mj.attrib['yaku'].split(',')[x])],
                mj.attrib['yaku'].split(',')[x + 1]
            )
            han = han + int(mj.attrib['yaku'].split(',')[x+1])
        if mj.attrib['ten'].split(',')[2] == '0':
            msg += '    得点: {}符 {}翻 {}点\n'.format(
                mj.attrib['ten'].split(',')[0], han, mj.attrib['ten'].split(',')[1]
            )
        else:
            msg += '    得点: {} {}点\n'.format(
                table.ten_class[int(mj.attrib['ten'].split(',')[2])], mj.attrib['ten'].split(',')[1]
            )
        msg += '    役: {}\n'.format(y)
    if 'yakuman' in mj.attrib:
        y = ''
        for x in mj.attrib['yakuman'].split(','):
            y = y + '{0} '.format(table.yaku[int(x)])
            msg += '    得点: {} {}点\n'.format(
                table.ten_class[int(mj.attrib['ten'].split(',')[2])],
                mj.attrib['ten'].split(',')[1]
            )
        msg += '    役: {}\n'.format(y)

    if args.result and common.IsTarget(args, player):
        print(msg.strip())


def ryuukyoku(args, player, sekijun, mj):
    '''
    流局したときの状態を表示
    '''

    msg = '  流局>\n'

    if 'type' in mj.attrib:
        if mj.attrib['type'] == 'nm':
            if not 'hai0' in mj.attrib:
                a = 0
            if not 'hai1' in mj.attrib:
                a = 1
            if not 'hai2' in mj.attrib:
                a = 2
            if not 'hai3' in mj.attrib:
                a = 3
            analysis.add_agari(player[a], 8)
            msg += '    {} {}\n'.format(table.ryuukyoku_type[mj.attrib['type']], player[a])
        else:
            for x in range(len(sekijun)):
                analysis.add_agari(player[x], 6)
            if mj.attrib['type'] == 'reach4':
                msg += '    {}\n'.format(table.ryuukyoku_type[mj.attrib['type']])
                if mj.attrib['type'] == 'reach4':
                    msg += '      {}: {}\n'.format(player[0], common.data_to_hai(mj.attrib['hai0']))
                    msg += '      {}: {}\n'.format(player[1], common.data_to_hai(mj.attrib['hai1']))
                    msg += '      {}: {}\n'.format(player[2], common.data_to_hai(mj.attrib['hai2']))
                    msg += '      {}: {}\n'.format(player[3], common.data_to_hai(mj.attrib['hai3']))
            if mj.attrib['type'] == 'yao9':
                msg += '    {}\n'.format(table.ryuukyoku_type[mj.attrib['type']])
    else:
        tenpai = []
        noten = [0, 1, 2, 3]

        if 'hai0' in mj.attrib:
            tenpai.append(0)
            noten.remove(0)
        if 'hai1' in mj.attrib:
            tenpai.append(1)
            noten.remove(1)
        if 'hai2' in mj.attrib:
            tenpai.append(2)
            noten.remove(2)
        if 'hai3' in mj.attrib:
            tenpai.append(3)
            noten.remove(3)
        for x in tenpai:
            analysis.add_agari(player[x], 4)
        for x in noten:
            analysis.add_agari(player[x], 5)

        msg += '    聴牌: {}\n'.format(' '.join([player[x] for x in tenpai]))

    if args.result and common.IsTarget(args, player):
        print(msg.strip())


def owari(args, sekijun, player, mj):
    result = { # 局収支
        0: [], # Aさん
        1: [], # Bさん
        2: [], # Cさん
        3: [], # Dさん
    }

    msg = '  終局>\n'

    for x in sekijun:
        p = sekijun.index(x)
        soten = int(mj.attrib['owari'].split(',')[p * 2]) * 100
        point = float(mj.attrib['owari'].split(',')[p * 2 + 1])
        result[p] = (soten, point)

    rank = 0
    for point in sorted([result[k][1] for k in result.keys()], reverse=True):
        rank += 1
        for p in result.keys():
            if point in result[p]:
                analysis.sum_ten(player[p], result[p][0])
                analysis.sum_point(player[p], result[p][1])
                analysis.recode_rank(player[p], rank)
                msg += '    {}位: {} {} ({})\n'.format(rank, player[p], result[p][0], result[p][1])

    if args.owari:
        print(msg.strip())


def paifu(player, haipai, tumohai, sutehai):
    for seki in range(len(player)):
        haishi = haipai[seki].copy()
        tmp_tumohai = tumohai[seki].copy()
        tmp_sutehai = sutehai[seki].copy()

        print(player[seki])
        print('  配牌', common.data_to_hai(','.join(haishi)))
        print('  ツモ', tmp_tumohai)
        print('  打牌', tmp_sutehai)
        for x in range(len(tmp_sutehai)):
            if tmp_tumohai:
                x1 = tmp_tumohai.pop(0)
                haishi.append(x1)

            if tmp_sutehai:
                x2 = tmp_sutehai.pop(0)
                if int(x2) < 0:
                    continue
                if x2 in haishi:
                    haishi.remove(x2)
            print('  : {}({}) -> {}({}) : {}'.format(
                table.pai[int(x1)], x1,
                table.pai[int(x2)], x2,
                common.data_to_hai(','.join(haishi))
            ))
        print('  最終', common.data_to_hai(','.join(haishi)), common.CountShanten(','.join(haishi)))


def GetSaisyuukei(args, player, haipai, tumohai, sutehai):
    player_no = common.GetPosition(args, player)
    if player_no == None:
        return(None)

    haishi = haipai[player_no].copy()
    tmp_tumohai = tumohai[player_no].copy()
    tmp_sutehai = sutehai[player_no].copy()

    for x in range(len(tmp_sutehai)):
        if tmp_tumohai:
            x1 = tmp_tumohai.pop(0)
            haishi.append(x1)

        if tmp_sutehai:
            x2 = tmp_sutehai.pop(0)
            if int(x2) < 0:
                continue
            if x2 in haishi:
                haishi.remove(x2)

    if args.debug:
        print('DEBUG[最終形]:', haipai)
        print('DEBUG[最終形]:', tumohai)
        print('DEBUG[最終形]:', sutehai)
        print('DEBUG[最終形]:', haishi)

    return(haishi)
