from . import common
from . import table

game = {}
result ={}
agari_dist = {}
counter = {}
def initialize():
    game = {
        '試合数': 0,
        '局数': 0,
        '参加試合数': 0,
        '参加局数': 0,
        '卓': [],
    }

    result ={
        '横移動': {},
        '自摸和': {},
        '栄和': {},
        '放銃': {},
        '聴牌': {},
        '不聴': {},
        '途中流局': {},
        '被自摸': {},
        '流し満貫': {},
    }

    agari_dist = {
        '和了時': {'副露': 0, '立直': 0, 'ダマ': 0,},
        '放銃時': {'副露': 0, '立直': 0, '面前': 0,},
        '放銃相手': {'副露': 0, '立直': 0, 'ダマ': 0,},
    }

    counter = {
        # 立直データ
        '立直': 0, '立直和了': 0, '立直放銃': 0, '立直流局': 0,
        '立直巡目': [], '先制立直': 0, '追掛立直': 0,
        '立直収支': [], '立直収入': [], '立直支出': [],
        # 和了データ
        '和了巡目': [], '放銃巡目': [],
        # 副露データ
        '副露': 0, '副露和了': 0, '副露放銃': 0, '副露流局': 0,
        '副露収支': [], '副露収入': [], '副露支出': [],
        '裸': 0, '暗槓': 0, '加槓': 0, '大明槓': 0,
        # 収支データ
        '和了点': [], '放銃点': [], '被自摸_親': [], '被自摸_子': [],
        # その他
        '向聴数': [],
    }

    return(game, result, agari_dist, counter)


def add_agari(player, flag):
    if flag == 0: # 横移動
        if player in result['横移動']:
            result['横移動'][player] += 1
        else:
            result['横移動'][player] = 1
    if flag == 1: # 自摸和
        if player in result['自摸和']:
            result['自摸和'][player] += 1
        else:
            result['自摸和'][player] = 1
    if flag == 2: # 栄和
        if player in result['栄和']:
            result['栄和'][player] += 1
        else:
            result['栄和'][player] = 1
    if flag == 3: # 栄和
        if player in result['放銃']:
            result['放銃'][player] += 1
        else:
            result['放銃'][player] = 1
    if flag == 4: # 聴牌
        if player in result['聴牌']:
            result['聴牌'][player] += 1
        else:
            result['聴牌'][player] = 1
    if flag == 5: # 不聴
        if player in result['不聴']:
            result['不聴'][player] += 1
        else:
            result['不聴'][player] = 1
    if flag == 6: # 途中流局
        if player in result['途中流局']:
            result['途中流局'][player] += 1
        else:
            result['途中流局'][player] = 1
    if flag == 7: # 被自摸(ツモられ)
        if player in result['被自摸']:
            result['被自摸'][player] += 1
        else:
            result['被自摸'][player] = 1
    if flag == 8: # 流し満貫
        if player in result['流し満貫']:
            result['流し満貫'][player] += 1
        else:
            result['流し満貫'][player] = 1


total_ten = {}
def sum_ten(player, ten):
    if player in total_ten:
        total_ten[player].append(ten)
    else:
        total_ten[player] = [ten]


total_point = {}
def sum_point(player, point):
    if player in total_point:
        total_point[player].append(point)
    else:
        total_point[player] = [point]


total_rank = {}
def recode_rank(player, rank):
    if player in total_rank:
        total_rank[player].append(rank)
    else:
        total_rank[player] = [rank]


def display(args):
    line_width = 80
    print('=' * line_width)

    #print('解析対象ログ数> 試合数: {} / 局数: {}'.format(game['試合数'], game['局数']))
    if args.debug: print('DEBUG:', agari_dist)

    if args.player:
        print('解析対象者>', ', '.join([x for x in args.player]))
        print('解析ログ数> 試合数: {} / 局数: {}'.format(game['参加試合数'], game['参加局数']))
        print('対戦卓    > 一般卓: {} / 上級卓: {} / 特上卓: {} / 鳳凰卓: {}'.format(
            game['卓'].count(0),
            game['卓'].count(1),
            game['卓'].count(2),
            game['卓'].count(3),
        ))

        # 順位
        print('-' * line_width)
        # 解析対象者の順位データをマージ
        total_r = common.TargetMerge(args, total_rank)
        total_t = common.TargetMerge(args, total_ten)
        total_p = common.TargetMerge(args, total_point)
        print('【順位データ】')
        if game['参加局数']:
            print('1位: {} ({:.3%}) / 2位: {} ({:.3%}) / 3位: {} ({:.3%}) / 4位: {} ({:.3%})'.format(
                total_r.count(1), total_r.count(1) / len(total_r),
                total_r.count(2), total_r.count(2) / len(total_r),
                total_r.count(3), total_r.count(3) / len(total_r),
                total_r.count(4), total_r.count(4) / len(total_r),
            ))
            print('  平均順位: {:.03f} / 連対率: {:.3%} / 飛び: {} ({:.3%})'.format(
                sum(total_r) / len(total_r),
                (total_r.count(1) + total_r.count(2)) / len(total_r),
                common.CountTobi(total_t), common.CountTobi(total_t) / len(total_r)
            ))
            print('  累積ポイント: {} / 平均ポイント: {:.4}'.format(sum(total_p), sum(total_p) / len(total_p)))
        else:
            print('No Data')

        # 和銃 / ダブロンがあるので局数とカウントの合計は一致しない
        print('-' * line_width)
        print('【和銃データ】')
        # 解析対象者の和了回数を合算
        agari_tumo = common.TargetCount(args, result['自摸和'])
        agari_ron = common.TargetCount(args, result['栄和'])

        if game['参加局数']:
            print('和了率: {:.3%} ({}回) / 和了巡目: {:.4}'.format(
                (agari_tumo + agari_ron) / game['参加局数'], agari_tumo + agari_ron,
                sum(counter['和了巡目']) / len(counter['和了巡目']),
            ))
            print('  自摸和: {}回 ({:.3%}) / 栄和: {}回 ({:.3%})'.format(
                agari_tumo, agari_tumo / (agari_tumo + agari_ron),
                agari_ron, agari_ron / (agari_tumo + agari_ron),
            ))

            if sum(agari_dist['和了時'].values()):
                print('  和了時> 副露: {}回 ({:.3%}) / 立直: {}回 ({:.3%}) / ダマ: {}回 ({:.3%})'.format(
                    agari_dist['和了時']['副露'],
                    agari_dist['和了時']['副露'] / sum(agari_dist['和了時'].values()),
                    agari_dist['和了時']['立直'],
                    agari_dist['和了時']['立直'] / sum(agari_dist['和了時'].values()),
                    agari_dist['和了時']['ダマ'],
                    agari_dist['和了時']['ダマ'] / sum(agari_dist['和了時'].values()),
                ))
            else:
                print('  和了時> 副露: {}回 ({:.3%}) / 立直: {}回 ({:.3%}) / ダマ: {}回 ({:.3%})'.format(0, 0, 0, 0, 0, 0))
            print('  平均和了: {}点 / 最大和了: {}点'.format(
                int(sum(counter['和了点']) / len(counter['和了点'])),
                max(counter['和了点']),
            ))
            if common.TargetCount(args, result['放銃']):
                print('放銃率: {:.3%} ({}回) / 放銃巡目: {:.4}'.format(
                    common.TargetCount(args, result['放銃']) / game['参加局数'],
                    common.TargetCount(args, result['放銃']),
                    sum(counter['放銃巡目']) / len(counter['放銃巡目']),
                ))
            else:
                print('放銃率: {:.3%} ({}回) / 放銃巡目: {:.4}'.format(0, 0, float(0)))

            if sum(agari_dist['放銃時'].values()):
                print('  放銃時  > 副露: {}回 ({:.3%}) / 立直: {}回 ({:.3%}) / 面前: {}回 ({:.3%})'.format(
                    agari_dist['放銃時']['副露'],
                    agari_dist['放銃時']['副露'] / sum(agari_dist['放銃時'].values()),
                    agari_dist['放銃時']['立直'],
                    agari_dist['放銃時']['立直'] / sum(agari_dist['放銃時'].values()),
                    agari_dist['放銃時']['面前'],
                    agari_dist['放銃時']['面前'] / sum(agari_dist['放銃時'].values()),
                ))
            else:
                print('  放銃時> 副露: {}回 ({:.3%}) / 立直: {}回 ({:.3%}) / 面前: {}回 ({:.3%})'.format(0, 0, 0, 0, 0, 0))

            if sum(agari_dist['放銃相手'].values()):
                print('  放銃相手> 副露: {}回 ({:.3%}) / 立直: {}回 ({:.3%}) / ダマ: {}回 ({:.3%})'.format(
                    agari_dist['放銃相手']['副露'],
                    agari_dist['放銃相手']['副露'] / sum(agari_dist['放銃相手'].values()),
                    agari_dist['放銃相手']['立直'],
                    agari_dist['放銃相手']['立直'] / sum(agari_dist['放銃相手'].values()),
                    agari_dist['放銃相手']['ダマ'],
                    agari_dist['放銃相手']['ダマ'] / sum(agari_dist['放銃相手'].values()),
                ))
            else:
                print('  放銃相手> 副露: {}回 ({:.3%}) / 立直: {}回 ({:.3%}) / ダマ: {}回 ({:.3%})'.format(0, 0, 0, 0, 0, 0))

            if len(counter['放銃点']):
                print('  平均放銃: {}点 / 最大放銃: {}点'.format(
                    int(sum(counter['放銃点']) / len(counter['放銃点'])),
                    max(counter['放銃点']),
                ))
            else:
                print('  平均放銃: {}点 / 最大放銃: {}点'.format(0, 0))

            print('被自摸率: {:.3%} ({}回)'.format(
                common.TargetCount(args, result['被自摸']) / game['参加局数'],
                common.TargetCount(args, result['被自摸']),
            ))
            if len(counter['被自摸_親']):
                print('  親: {}回 ({:.3%}) / 平均支出: {}点 / 最大支出: {}点'.format(
                    len(counter['被自摸_親']),
                    abs(len(counter['被自摸_親']) / common.TargetCount(args, result['被自摸'])),
                    abs(int(sum(counter['被自摸_親']) / len(counter['被自摸_親']))),
                    abs(min(counter['被自摸_親'])),
                ))
            else:
                print('  親: {}回 ({:.3%}) / 平均支出: {}点 / 最大支出: {}点'.format(0, 0, 0, 0))
            if len(counter['被自摸_子']):
                print('  子: {}回 ({:.3%}) / 平均支出: {}点 / 最大支出: {}点'.format(
                    len(counter['被自摸_子']),
                    abs(len(counter['被自摸_子']) / common.TargetCount(args, result['被自摸'])),
                    abs(int(sum(counter['被自摸_子']) / len(counter['被自摸_子']))),
                    abs(min(counter['被自摸_子'])),
                ))
            else:
                print('  子: {}回 ({:.3%}) / 平均支出: {}点 / 最大支出: {}点'.format(0, 0, 0, 0))
        else:
            print('No Data')
        #if args.player in result['横移動']:
        #    print('横移動:', result['横移動'][args.player])

        # 立直
        print('-' * line_width)
        print('【立直データ】')
        if game['参加局数']:
            print('立直率: {:.3%} ({}回) / 立直巡目: {:.4}'.format(
                counter['立直'] / game['参加局数'], counter['立直'],
                sum(counter['立直巡目']) / len(counter['立直巡目']),
            ))
            print('  先制: {}回 ({:.3%}) / 追っかけ: {}回 ({:.3%})'.format(
                counter['先制立直'],
                counter['先制立直'] / counter['立直'] if counter['立直'] else 0,
                counter['追掛立直'],
                counter['追掛立直'] / counter['立直'] if counter['立直'] else 0,
            ))
            print('  立直後> 和了: {}回 ({:.3%}) / 放銃: {}回 ({:.3%}) / 流局: {}回 ({:.3%})'.format( 
                counter['立直和了'],
                counter['立直和了'] / counter['立直'] if counter['立直'] else 0,
                counter['立直放銃'],
                counter['立直放銃'] / counter['立直'] if counter['立直'] else 0,
                counter['立直流局'],
                counter['立直流局'] / counter['立直'] if counter['立直'] else 0,
            ))
            print('  立直収支: {}点 / 立直収入: {}点 / 立直支出: {}点'.format(
                int(sum(counter['立直収支']) / counter['立直'] if counter['立直'] else 0),
                int(sum(counter['立直収入']) / counter['立直和了'] if counter['立直和了'] else 0),
                int(abs(sum(counter['立直支出']) / counter['立直放銃'])) if counter['立直放銃'] else 0,
            ))
        else:
            print('No Data')

        # 副露
        print('-' * line_width)
        print('【副露データ】')
        if game['参加局数']:
            print('副露率: {:.3%} ({}回)'.format(counter['副露'] / game['参加局数'], counter['副露']))
            print('  副露後> 和了: {}回 ({:.3%}) / 放銃: {}回 ({:.3%}) / 流局: {}回 ({:.3%})'.format( 
                counter['副露和了'],
                counter['副露和了'] / counter['副露'] if counter['副露'] else 0,
                counter['副露放銃'],
                counter['副露放銃'] / counter['副露'] if counter['副露'] else 0,
                counter['副露流局'],
                counter['副露流局'] / counter['副露'] if counter['副露'] else 0,
            ))
            print('  副露収支: {}点 / 副露収入: {}点 / 副露支出: {}点'.format(
                int(sum(counter['副露収支']) / counter['副露'] if counter['副露'] else 0),
                int(sum(counter['副露収入']) / counter['副露和了'] if counter['副露和了'] else 0),
                int(abs(sum(counter['副露支出']) / counter['副露放銃']) if counter['副露放銃'] else 0),
            ))
            print('  裸: {}回 ({:.3%})'.format(counter['裸'], counter['裸']/counter['副露']))
            print('  槓> 暗槓: {}回 / 加槓 {}回 / 大明槓: {}回'.format(
                counter['暗槓'], counter['加槓'], counter['大明槓'],
            ))
        else:
            print('No Data')

        # 流局
        print('-' * line_width)
        print('【流局データ】')
        if game['参加局数']:
            ryukyoku_count = 0
            for x in ('聴牌', '不聴', '途中流局', '流し満貫'):
                ryukyoku_count += common.TargetCount(args, result[x])
            print('流局率: {:.3%} ({}回)'.format(ryukyoku_count / game['参加局数'], ryukyoku_count))
            print('  聴牌: {}回 ({:.3%}) / 不聴: {}回 ({:.3%})'.format(
                common.TargetCount(args, result['聴牌']),
                common.TargetCount(args, result['聴牌']) / ryukyoku_count if ryukyoku_count else 0,
                common.TargetCount(args, result['不聴']),
                common.TargetCount(args, result['不聴']) / ryukyoku_count if ryukyoku_count else 0,
            ))
            for x in ('途中流局', '流し満貫'):
                if common.TargetCount(args, result[x]):
                    print('  {}: {}回 ({:.3%})'.format(
                        x,
                        common.TargetCount(args, result[x]),
                        common.TargetCount(args, result[x]) / ryukyoku_count,
                    ))
        else:
            print('No Data')

        # 運要素
        print('-' * line_width)
        print('【その他データ】')
        if game['参加局数']:
            print('配牌時向聴数: {:.4}'.format(sum(counter['向聴数']) / len(counter['向聴数'])))
            for i in range(7):
                print('  {}: {}回 ({:.3%})'.format(
                    table.shanten[i], counter['向聴数'].count(i),
                    counter['向聴数'].count(i) / len(counter['向聴数'])
                ))
                #print('  一向聴: {}回 ({:.3%}) / 六向聴: {}回 ({:.3%})'.format(
                #    counter['向聴数'].count(1),
                #    counter['向聴数'].count(1) / len(counter['向聴数']),
                #    counter['向聴数'].count(6),
                #    counter['向聴数'].count(6) / len(counter['向聴数']),
                #))
        else:
            print('No Data')
    else:
        # 解析対象プレイヤーが未指定の場合は全員分の成績を出す
        for x in total_ten.keys():
            print('  {}: {:5}試合 / 累計ポイント: {:7} / 平均ポイント: {:7.2f} / 平均点: {:.2f}'.format(
                common.left(x, 20),
                len(total_ten[x]),
                sum(total_point[x]),
                sum(total_point[x]) / len(total_point[x]),
                sum(total_ten[x]) / len(total_ten[x]),
            ))


def houju(args, header_flag):
    msg = []
    if header_flag:
        tmp  = '試合数 /   放銃率 回数 / 放銃巡目 '
        tmp += '/ 放銃時> 副露          立直          面前 '
        tmp += '/ 放銃相手> 副露        立直          ダマ '
        tmp += '/ 平均放銃点'
        msg.append(tmp)
    if game['参加局数']:
        tmp  = '{:6} / {:>8.3%}  {:>3} /    {:>5.02f} / '.format(
            game['参加試合数'],
            common.TargetCount(args, result['放銃']) / game['参加局数'],
            common.TargetCount(args, result['放銃']),
            sum(counter['放銃巡目']) / len(counter['放銃巡目']))
        tmp += '{:>8.3%} {:>3}  {:>8.3%} {:>3}  {:>8.3%} {:>3} / '.format(
            agari_dist['放銃時']['副露'] / sum(agari_dist['放銃時'].values()), agari_dist['放銃時']['副露'],
            agari_dist['放銃時']['立直'] / sum(agari_dist['放銃時'].values()), agari_dist['放銃時']['立直'],
            agari_dist['放銃時']['面前'] / sum(agari_dist['放銃時'].values()), agari_dist['放銃時']['面前'])
        tmp += '{:>8.3%} {:>3}  {:>8.3%} {:>3}  {:>8.3%} {:>3} / '.format(
            agari_dist['放銃相手']['副露'] / sum(agari_dist['放銃相手'].values()), agari_dist['放銃相手']['副露'],
            agari_dist['放銃相手']['立直'] / sum(agari_dist['放銃相手'].values()), agari_dist['放銃相手']['立直'],
            agari_dist['放銃相手']['ダマ'] / sum(agari_dist['放銃相手'].values()), agari_dist['放銃相手']['ダマ'])
        tmp += '{:6}'.format(int(sum(counter['放銃点']) / len(counter['放銃点'])))
        msg.append(tmp)

    return(msg)


def reach(args, header_flag):
    msg = []
    if header_flag:
        tmp  = '試合数 /   立直率 回数 / 立直巡目  先制率  回数 / '
        tmp += '立直後>  和了         放銃         流局 / '
        tmp += '立直収支 立直収入 立直支出'
        msg.append(tmp)
    if game['参加局数']:
        tmp  = '{:6} / {:>8.3%}  {:>3} /   {:>5.02f} {:>8.3%}   {:>3} / '.format(
            game['参加試合数'],
            counter['立直'] / game['参加局数'], counter['立直'],
            sum(counter['立直巡目']) / len(counter['立直巡目']),
            counter['先制立直'] / counter['立直'], counter['先制立直'])
        tmp += '{:>8.3%} {:>3}  {:>8.3%} {:>3} {:>8.3%} {:>3} /'.format( 
            counter['立直和了'] / counter['立直'], counter['立直和了'],
            counter['立直放銃'] / counter['立直'], counter['立直放銃'],
            counter['立直流局'] / counter['立直'], counter['立直流局'])
        tmp += '{:>8} {:>8} {:>8}'.format(
            int(sum(counter['立直収支']) / counter['立直']),
            int(sum(counter['立直収入']) / counter['立直和了']),
            int(abs(sum(counter['立直支出']) / counter['立直放銃'])) if counter['立直放銃'] else 0)
        msg.append(tmp)

    return(msg)


def fooro(args, header_flag):
    msg = []
    if header_flag:
        tmp  = '試合数 /   副露率 回数 / 副露後> 和了         放銃         流局 / '
        tmp += '副露収支 副露収入 副露支出'
        msg.append(tmp)
    if game['参加局数']:
        tmp  = '{:6} / {:>8.3%}  {:>3} /'.format(
            game['参加試合数'],
            counter['副露'] / game['参加局数'], counter['副露'])
        tmp += '{:>8.3%} {:>3} {:>8.3%} {:>3} {:>8.3%} {:>3} /'.format( 
            counter['副露和了'] / counter['副露'], counter['副露和了'],
            counter['副露放銃'] / counter['副露'], counter['副露放銃'],
            counter['副露流局'] / counter['副露'], counter['副露流局'])
        tmp += '{:>8} {:>8} {:>8}'.format(
            int(sum(counter['副露収支']) / counter['副露']),
            int(sum(counter['副露収入']) / counter['副露和了']),
            int(abs(sum(counter['副露支出']) / counter['副露放銃'])))
        msg.append(tmp)

    return(msg)


def basic(args, header_flag):
    msg = []
    if header_flag:
        tmp  = '試合数 局数 / 和了率   放銃率   立直率   副露率   / '
        tmp += '平均(和了/放銃/立直収支/副露収支) / '
        tmp += '順位        平均  連対率   飛び率   / '
        tmp += 'ポイント(累積/平均)'
        msg.append(tmp)
    if game['参加局数']:
        # 順位
        total_r = common.TargetMerge(args, total_rank)
        total_t = common.TargetMerge(args, total_ten)
        total_p = common.TargetMerge(args, total_point)

        agari_tumo = common.TargetCount(args, result['自摸和'])
        agari_ron = common.TargetCount(args, result['栄和'])

        tmp  = '{:6} {:4} / {:>8.3%} {:>8.3%} {:>8.3%} {:>8.3%} / '.format(
            game['参加試合数'], game['参加局数'],
            (agari_tumo + agari_ron) / game['参加局数'],
            common.TargetCount(args, result['放銃']) / game['参加局数'],
            counter['立直'] / game['参加局数'],
            counter['副露'] / game['参加局数'])
        tmp += '  {:>7} {:>7} {:>7} {:>7} / '.format(
            int(sum(counter['和了点']) / len(counter['和了点']) if len(counter['和了点']) else 0),
            int(sum(counter['放銃点']) / len(counter['放銃点']) if len(counter['放銃点']) else 0),
            int(sum(counter['立直収支']) / counter['立直'] if counter['立直'] else 0),
            int(sum(counter['副露収支']) / counter['副露'] if counter['副露'] else 0))
        tmp += '{:>02}-{:>02}-{:>02}-{:>02} {:>.03f} {:>8.3%} {:>8.3%} / '.format(
            total_r.count(1), total_r.count(2), total_r.count(3), total_r.count(4),
            sum(total_r) / len(total_r),
            (total_r.count(1) + total_r.count(2)) / len(total_r),
            common.CountTobi(total_t) / len(total_r))
        tmp += '{:>8} {:>8.03f}'.format(sum(total_p), sum(total_p) / len(total_p))
        msg.append(tmp)

    return(msg)

