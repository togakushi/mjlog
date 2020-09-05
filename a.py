#!/usr/bin/python3

from lib import main
from lib import common
from lib import option
from lib import analysis

if __name__ == '__main__':
    args = option.parser()

    # 解析するログのリストを生成
    mjloglist = []
    if args.logdir:
        for x in args.logdir:
            mjloglist += main.logserach(x)
    else:
        mjloglist = args.log

    if args.limit and args.limit < len(mjloglist):
        mjloglist = mjloglist[len(mjloglist) - args.limit:]

    if args.debug:
        print('DEBUG: mjloglist ->', mjloglist)


    (analysis.game, analysis.result, analysis.agari_dist, analysis.counter) = analysis.initialize()

    header_flag = True
    output = []

    for mjlog in mjloglist:
        t = main.logopen(args, mjlog)
        if t:
            gamedata = common.GetGameData(t)
            gamedata['対局者'] = common.GetPlayerName(t)

            if not str(gamedata['卓']) in args.taku.split(','):
                continue

            if gamedata['sanma']:
                # 三麻解析ループ
                main.loop3(args, gamedata, t)
            else:
                # 四麻解析ループ
                main.loop4(args, gamedata, t)

                if common.TargetExists(args, t) and args.vicissitudes:
                    # 放銃率遷移
                    if args.vicissitudes[0] == 'h':
                        output +=  analysis.houju(args, header_flag)
                    # 立直率遷移
                    if args.vicissitudes[0] == 'r':
                        output +=  analysis.reach(args, header_flag)
                    # 副露率遷移
                    if args.vicissitudes[0] == 'f':
                        output +=  analysis.fooro(args, header_flag)
                    # 基本情報
                    if args.vicissitudes[0] == 'b':
                        output +=  analysis.basic(args, header_flag)

                    header_flag = False

    # 解析結果出力
    if not args.vicissitudes and args.quiet:
        analysis.display(args)
    else:
        if not args.count or len(output) - args.count < 0:
            start = 1
        else:
            start = len(output) - args.count
        if output:
            print(output[0]) # header出力
            for x in range(start, len(output)):
                print(output[x])
        else:
            print('No Data')
