#!/usr/bin/python3

import os
import unicodedata
from urllib.parse import unquote
from datetime import datetime as dt

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

from . import table

def data_to_hai(hai):
    '''
    カンマで区切った牌IDの文字列から牌に変換して配列で返す
    '''

    ret = []
    for i in sorted([int(x) for x in hai.split(',')]):
        ret.append(table.pai[i])

    return(ret)


def array_to_hai(hai):
    '''
    配列を牌に変換して返す
    '''

    #[table.pai[int(x)] for x in hai]]
    pass


def ba(b, s):
    msg = ''
    if 0 <= int(b) <= 3:
        msg = '東' + str(int(b) + 1) + '局'
    if 4 <= int(b) <= 7:
        msg = '南' + str(int(b) - 3) + '局'
    if 8 <= int(b) <= 11:
        msg = '西' + str(int(b) - 7) + '局'
    if 12 <= int(b) <= 15:
        msg = '北' + str(int(b) - 11) + '局'

    msg = msg + str(int(s)) + '本場'

    return(msg)


def dora(id):
    '''
    与えられたドラ表示牌の牌IDからドラとなる牌を返す
    '''

    if 32 <= id <= 35: # 9m	32	33	34	35
        id = -4
    if 68 <= id <= 71: # 9p	68	69	70	71
        id = 32
    if 104 <= id <= 107: # 9s	104	105	106	107
        id = 96
    if 120 <= id <= 123: # 北	120	121	122	123
        id = 104
    if 132 <= id <= 135: # 中	132	133	134	135
        id = 120

    d = table.pai[id + 4]
    if d[0] == '0': # 赤が選択された場合
        d = '5' + d[1]

    return(d)


def CountTobi(sc):
    '''
    点数からマイナス(飛び)を数える
    '''

    tobi = 0
    for x in sc:
        if x < 0:
            tobi += 1

    return(tobi)


def CountShanten(haishi):
    '''
    牌姿データからシャンテン数を数える
    '''

    man = ''
    pin = ''
    sou = ''
    honors = ''

    for x in haishi.split(','):
        if table.pai2[int(x)][1] == 'm':
            man += table.pai2[int(x)][0]
        if table.pai2[int(x)][1] == 'p':
            pin += table.pai2[int(x)][0]
        if table.pai2[int(x)][1] == 's':
            sou += table.pai2[int(x)][0]
        if table.pai2[int(x)][1] == 'z':
            honors += table.pai2[int(x)][0]

    shanten = Shanten()
    tiles = TilesConverter.string_to_34_array(
        man = man,
        pin = pin,
        sou = sou,
        honors = honors,
    )

    return(shanten.calculate_shanten(tiles))


def TargetExists(args, t):
    if not args.player:
        return(False)

    for mj in t.getiterator():
        if mj.tag == 'UN' and 'rate' in mj.attrib:
            for x in ('n0', 'n1', 'n2', 'n3'):
                if unquote(mj.attrib[x]) in args.player:
                    return(True)

    return(False)


def GetPlayerName(t):
    n0 = None; n1 = None; n2 = None; n3 = None
    for mj in t.getiterator():
        if mj.tag == 'UN' and 'rate' in mj.attrib:
            n0 = unquote(mj.attrib['n0'])
            n1 = unquote(mj.attrib['n1'])
            n2 = unquote(mj.attrib['n2'])
            n3 = unquote(mj.attrib['n3'])

    return(n0, n1, n2, n3)


def GetGameData(t):
    gamedata = {}
    for mj in t.getiterator():
        if mj.tag == 'GO':
            i = int(mj.attrib['type'])
            if 0x010 & i == 0:
                gamedata['sanma'] = False
            else:
                gamedata['sanma'] = True

            # 0:一般 1:上級 2:特上 3:鳳凰
            gamedata['卓'] = (i & 0x0020) >> 4 | (i & 0x0080) >> 7

    return(gamedata)


def IsTarget(args, player, p = None):
    '''
    解析対象者が含まれているが判定する
    '''
    ret = False
    if args.player:
        if p == None:
            for x in range(4):
                for pn in args.player:
                    if pn == player[x]:
                        ret = True
        else:
            for pn in args.player:
                if pn == player[p]:
                    ret = True

    return(ret)


def TargetCount(args, data):
    '''
    解析対象プレイヤーのカウンターを合算する
    '''

    count = 0
    if args.player:
        for x in args.player:
            if x in data:
                count += data[x]

    return(count)


def TargetMerge(args, data):
    '''
    解析対象プレイヤーのリストを結合する
    '''

    ret = []
    if args.player:
        for x in args.player:
            if x in data:
                ret = ret + data[x]

    return(ret)


def GetPosition(args, player):
    '''
    プレイヤーの席位置を取得する
    '''

    ret = None
    if args.player:
        for p in args.player:
            if p in player:
                ret = player.index(p)

    return(ret)


def left(string, digit,):
    '''
    2バイト文字をカウントして左寄せする
    '''

    for c in string:
        if unicodedata.east_asian_width(c) in ('F', 'W', 'A'):
            digit -= 2
        else:
            digit -= 1

    return(string + ' ' * digit)


def TimestampSort(filelist):
    timestamplist = {}
    for fp in filelist:
        timestamplist[fp] = dt.fromtimestamp(os.path.getctime(fp))

    r = sorted(timestamplist.items(), key=lambda x:x[1])

    return([r[x][0] for x in range(len(r))])