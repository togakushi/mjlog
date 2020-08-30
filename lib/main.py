#!/usr/bin/python3

import os
import gzip
import xml.etree.ElementTree as ET
from urllib.parse import unquote

from . import common
from . import table
from . import analysis
from . import fooro
from . import end


def logopen(args, mjlog):
    t = None
    if os.path.exists(mjlog):
        try: # 雑に読み込み
            f = gzip.open(mjlog, 'rb')
            t = ET.parse(f)
        except:
            f = open(mjlog, 'rb')
            t = ET.parse(f)
        finally:
            f.close()
            if args.verbos:
                print(mjlog)

    return(t)


def loop3(args, gamedata, t):
    return


def loop4(args, gamedata, t):
    player = gamedata['対局者']
    sutehai = {}
    flag = {}
    junme = {}

    for mj in t.getiterator():
        # 開局
        if mj.tag == 'GO':
            analysis.game['試合数'] += 1
            if common.IsTarget(args, player):
                analysis.game['参加試合数']  += 1
                analysis.game['卓'].append(gamedata['卓'])
            sekijun = ['東家', '南家', '西家', '北家']
            h = ''.join([str(x) for x in range(len(sekijun))])
            continue

        # 対局者情報
        if mj.tag == 'UN':
            continue

        # 配牌
        if mj.tag == 'INIT':
            analysis.game['局数'] += 1
            if common.IsTarget(args, player):
                analysis.game['参加局数']  += 1

            oya = mj.attrib['oya']
            ba = common.ba(mj.attrib['seed'].split(',')[0], mj.attrib['seed'].split(',')[1])
            dora = table.pai[int(mj.attrib['seed'].split(',')[5])]

            if common.IsTarget(args, player, int(oya)):
                flag['oya'] = True
            else:
                flag['oya'] = False

            if args.init | args.sute | args.result:
                print()
                print(ba, 'ドラ表示:', dora, '親:', player[int(mj.attrib['oya'])])

            msg = ('  配牌>\n')
            c = 0
            for seki in h[int(mj.attrib['oya']):] + h[:int(mj.attrib['oya'])]:
                shanten = common.CountShanten(mj.attrib['hai' + seki])
                msg += '    {}({}): {} / {}\n'.format(
                    sekijun[c],
                    player[int(seki)],
                    ' '.join(common.data_to_hai(mj.attrib['hai' + seki])),
                    shanten,
                )
                if common.IsTarget(args, player, int(seki)):
                    analysis.counter['向聴数'].append(shanten)
                c += 1

            if args.init:
                print(msg[:-1])

            # 変数初期化
            sutehai = { # 捨牌
                0: [], # Aさん
                1: [], # Bさん
                2: [], # Cさん
                3: [], # Dさん
            }
            flag['reach'] = {0: False, 1: False, 2: False, 3: False}
            flag['naki'] = {0: False, 1: False, 2: False, 3: False}
            junme = { 0: 0, 1: 0, 2: 0, 3: 0 }
            naki_count = 0 # 解析対象者の副露数
            last_p = int(oya)  # 河に牌を捨てた最後の人

        # 和了
        if mj.tag == 'AGARI':
            if args.sute:
                end.ho(sekijun, oya, player, sutehai)
            end.agari(args, player, sutehai, mj, flag, junme)

            if 'owari' in mj.attrib:
                end.owari(args, sekijun, player, mj)

            if args.debug:
                print('DEBUG:', [player[x] for x in range(len(sekijun))])
                print('DEBUG:', flag)
                print('DEBUG:', mj.tag, mj.attrib)

        # 流局
        if mj.tag == 'RYUUKYOKU':
            for x in range(len(sekijun)):
                if common.IsTarget(args, player, x) and flag['reach'][x]:
                    analysis.counter['立直流局'] += 1
                if common.IsTarget(args, player, x) and flag['naki'][x]:
                    analysis.counter['副露流局'] += 1

            if args.sute:
                end.ho(sekijun, oya, player, sutehai)
            end.ryuukyoku(args, player, sekijun, mj)

            if 'owari' in mj.attrib:
                end.owari(args, sekijun, player, mj)

            if args.debug:
                print('DEBUG:', [player[x] for x in range(len(sekijun))])
                print('DEBUG:', flag)
                print('DEBUG:', mj.tag, mj.attrib)

        if mj.tag == 'DORA':
            continue
        if mj.tag == 'TAIKYOKU':
            continue

        # ツモ
        if mj.tag[0] in ('T', 'U', 'V', 'W'):
            p = ('T', 'U', 'V', 'W').index(mj.tag[0])
            junme[p] += 1

        # 捨牌
        if mj.tag[0] in ('D', 'E', 'F', 'G'):
            p = ('D', 'E', 'F', 'G').index(mj.tag[0])
            sutehai[p].append(mj.tag[1:])
            last_p = p

        # 鳴き
        if mj.tag == 'N':
            p = int(mj.attrib['who'])
            junme[p] += 1

            for m in mj.attrib['m'].split(','):
                x = format(int(m), '#018b')[2:]
                if x[13] == '1': # チー
                    sutehai[last_p].append('-1')
                    if common.IsTarget(args, player, p): # 解析対象者の鳴きか？
                        naki_count += 1
                        if not flag['naki'][p]: # 偽なら初鳴き
                            analysis.counter['副露'] += 1
                    flag['naki'][p] = True
                else:
                    if x[12] == '1': # ポン
                        sutehai[last_p].append('-1')
                        if common.IsTarget(args, player, p): # 解析対象者の鳴きか？
                            naki_count += 1
                            if not flag['naki'][p]: # 偽なら初鳴き
                                analysis.counter['副露'] += 1
                        flag['naki'][p] = True
                    if x[11] == '1': # 加槓
                        sutehai[p].append('-1')
                        if common.IsTarget(args, player, p): # 解析対象者の鳴きか？
                            analysis.counter['加槓'] += 1
                if x[10:16] == '100000': # 北抜き
                    sutehai[int(mj.attrib['who'])].append('-2')
                else:
                    if x[11:14] == '000': # カン
                        if x[14:] == '00': # 暗槓
                            if common.IsTarget(args, player, p): # 解析対象者の鳴きか？
                                naki_count += 1
                                analysis.counter['暗槓'] += 1
                                # 暗槓は初鳴きの判定をしない
                                #if not flag['naki'][p]: # 偽なら初鳴き
                                #    analysis.counter['副露'] += 1
                        else: # 大明槓
                            sutehai[last_p].append('-1')
                            if common.IsTarget(args, player, p): # 解析対象者の鳴きか？
                                naki_count += 1
                                analysis.counter['大明槓'] += 1
                                if not flag['naki'][p]: # 偽なら初鳴き
                                    analysis.counter['副露'] += 1
                            flag['naki'][p] = True

            if common.IsTarget(args, player, p): # 解析対象者の鳴きか？
                if naki_count >= 4: # 4回鳴いたら裸
                    analysis.counter['裸'] += 1

        # リーチ
        if mj.tag == 'REACH':
            if mj.attrib['step'] == '1': # 立直宣言
                if common.IsTarget(args, player, int(mj.attrib['who'])):
                    analysis.counter['立直'] += 1
                    analysis.counter['立直巡目'].append(junme[int(mj.attrib['who'])])
                    if True in flag['reach'].values():
                        analysis.counter['追掛立直'] += 1
                    else:
                        analysis.counter['先制立直'] += 1
            if mj.attrib['step'] == '2': # 立直成立
                flag['reach'][int(mj.attrib['who'])] = True
