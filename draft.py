from collections import Counter, defaultdict
import pandas as pd

### Matched based on pdf document and discretion
COMPANY_IND_MAP = {'银行业':'货币金融服务', '通讯设备、计算机及其他电子设备制造业':'计算机、通信和其他电子设备制造业', '仓储业':'装卸搬运和仓储业', '城市公共交通业':'道路运输业', 
                   '社会福利业':'社会工作', '广播、电视、电影和音像业':'广播、电视、电影和录音制作业', '环境管理业':'生态保护和环境治理业', '石油加工、炼焦及核燃料加工业':'石油、煤炭及其他燃料加工业', 
                   '研究与试验发展':'科学研究和技术服务业', '教育业':'教育', '纺织服装、鞋、帽制造业':'纺织服装、服饰业', '其他金融服务':'其他金融业', '橡胶制品业':'橡胶和塑料制品业', 
                   '塑料制品业':'橡胶和塑料制品业', '钢压延加工':'黑色金属冶炼和压延加工业', '装卸搬运和其他运输服务业':'装卸搬运和仓储业', '社会保障业':'社会保障', '仪器仪表及文化、办公用机械制造业':'仪器仪表制造业', 
                   '化学原料及化学制品制造业':'化学原料和化学制品制造业', '群众团体、社会团体和宗教组织':'群众团体、社会团体和其他成员组织', '新闻出版业':'新闻和出版业', '棉、化纤纺织及印染精加工':'纺织业', 
                   '汽车制造':'汽车制造业', '房屋和土木工程业':'建筑业', '印刷业和记录媒体的复制':'印刷和记录媒介复制业', '水泥、石灰和石膏的制造':'非金属矿物制品业', '废弃资源和废旧材料回收加工业':'废弃资源综合利用业', 
                   '电信和其他信息传输服务业':'信息传输、软件和信息技术服务业', '石灰石、石膏开采':'非金属矿采选业', '农、林、牧、渔服务业':'农、林、牧、渔业', '电力、热力的生产和供应业':'电力、热力生产和供应业', 
                   '建筑装饰业':'建筑装饰、装修和其他建筑业', '计算机服务业':'软件和信息技术服务业', '工艺品及其他制造业':'文教、工美、体育和娱乐用品制造业', '工程准备':'建筑装饰、装修和其他建筑业', '炼钢':'黑色金属冶炼和压延加工业', 
                   '自行车制造':'铁路、船舶、航空航天和其他运输设备制造业', '科技交流和推广服务业':'科技推广和应用服务业', '砖瓦、石材及其他建筑材料制造':'非金属矿物制品业', '铁合金冶炼':'黑色金属冶炼和压延加工业', 
                   '地质勘查业':'采矿业', '铁路运输设备制造':'铁路、船舶、航空航天和其他运输设备制造业', '铝冶炼':'有色金属冶炼和压延加工业', '火力发电':'电力、热力生产和供应业', '炼铁':'黑色金属冶炼和压延加工业', 
                   '水泥及石膏制品制造':'家具制造业', '造纸及纸质品业':'造纸和纸制品业', '木材加工及木、竹、藤、棕、草制品业':'木材加工和木、竹、藤、棕、草制品业', '电气机械及器材制造业':'电气机械和器材制造业', 
                   '卫生、社会保障和社会福利业':'公共管理、社会保障和社会组织', '软件业':'信息传输、软件和信息技术服务业', '文教体育用品制造业':'文教、工美、体育和娱乐用品制造业', '船舶及浮动装置制造':'铁路、船舶、航空航天和其他运输设备制造业', 
                   '饮料制造业':'酒、饮料和精制茶制造业', '铁矿采选':'黑色金属矿采选业', '公共管理和社会组织':'公共管理、社会保障和社会组织', '家用制冷电器具制造':'电气机械和器材制造业', '铜冶炼':'有色金属冶炼和压延加工业', 
                   '皮革、毛皮、羽毛（绒）及其制造业':'皮革、毛皮、羽毛及其制品和制鞋业', '核力发电':'电力、热力生产和供应业', '证券业':'资本市场服务', '科学研究、技术服务和地质勘查业':'科学研究和技术服务业', 
                   '电力、燃气及水的生产和供应业':'电力、热力、燃气及水生产和供应业', '黑色金属冶炼及压延加工业':'黑色金属冶炼和压延加工业', '水力发电':'电力、热力生产和供应业', '家用空气调节器制造':'电气机械和器材制造业', 
                   '摩托车制造':'铁路、船舶、航空航天和其他运输设备制造业', '人民政协和民主党派':'人民政协、民主党派', '交通运输设备制造业':'铁路、船舶、航空航天和其他运输设备制造业', '信息传输、计算机服务和软件业':'信息传输、软件和信息技术服务业', 
                   '铝矿采选':'有色金属矿采选业', '粘土及其他土砂石开采':'非金属矿采选业', '铜矿采选':'有色金属矿采选业', '其他黑色金属矿采选':'黑色金属矿采选业', '有色金属冶炼及压延加工业':'有色金属冶炼和压延加工业', 
                   '居民服务和其他服务业':'居民服务、修理和其他服务业'}
INDUSTRY_MAP = defaultdict(lambda: '?')
INDUSTRY_MAP.update(COMPANY_IND_MAP)
CATEGORY_MAP = defaultdict(lambda: '?')
CATEGORY_MAP.update({'农业':'A', '林业':'A', '畜牧业':'A', '渔业':'A', '农、林、牧、渔专业及辅助性活动':'A', '农、林、牧、渔业':'A',
                     '采矿业':'B', '煤炭开采和洗选业':'B', '石油和天然气开采业':'B', '黑色金属矿采选业':'B', '有色金属矿采选业':'B', '非金属矿采选业':'B', '开采专业及辅助性活动':'B', '其他采矿业':'B', 
                     '制造业':'C', '农副食品加工业':'C', '食品制造业':'C', '酒、饮料和精制茶制造业':'C', '烟草制品业':'C', '纺织业':'C', '纺织服装、服饰业':'C', '皮革、毛皮、羽毛及其制品和制鞋业':'C', 
                     '木材加工和木、竹、藤、棕、草制品业':'C', '家具制造业':'C', '造纸和纸制品业':'C', '印刷和记录媒介复制业':'C', '文教、工美、体育和娱乐用品制造业':'C', '石油、煤炭及其他燃料加工业':'C', 
                     '化学原料和化学制品制造业':'C', '医药制造业':'C', '化学纤维制造业':'C', '橡胶和塑料制品业':'C', '非金属矿物制品业':'C', '黑色金属冶炼和压延加工业':'C', '有色金属冶炼和压延加工业':'C', 
                     '金属制品业':'C', '通用设备制造业':'C', '专用设备制造业':'C', '汽车制造业':'C', '铁路、船舶、航空航天和其他运输设备制造业':'C', '电气机械和器材制造业':'C', '计算机、通信和其他电子设备制造业':'C', 
                     '仪器仪表制造业':'C', '其他制造业':'C', '废弃资源综合利用业':'C', '金属制品、机械和设备修理业':'C', 
                     '电力、热力、燃气及水生产和供应业':'D', '电力、热力生产和供应业':'D', '燃气生产和供应业':'D', '水的生产和供应业':'D', 
                     '建筑业':'E', '房屋建筑业':'E', '土木工程建筑业':'E', '建筑安装业':'E', '建筑装饰、装修和其他建筑业':'E', 
                     '批发和零售业':'F', '批发业':'F', '零售业':'F', 
                     '交通运输、仓储和邮政业':'G', '铁路运输业':'G', '道路运输业':'G', '水上运输业':'G', '航空运输业':'G', '管道运输业':'G', '多式联运和运输代理业':'G', '装卸搬运和仓储业':'G', '邮政业':'G', 
                     '住宿和餐饮业':'H', '住宿业':'H', '餐饮业':'H', 
                     '信息传输、软件和信息技术服务业':'I', '电信、广播电视和卫星传输服务':'I', '互联网和相关服务':'I', '软件和信息技术服务业':'I', 
                     '金融业':'J', '货币金融服务':'J', '资本市场服务':'J', '保险业':'J', '其他金融业':'J', 
                     '房地产业':'K', 
                     '租赁和商务服务业':'L', '租赁业':'L', '商务服务业':'L', 
                     '科学研究和技术服务业':'M', '研究和试验发展':'M', '专业技术服务业':'M', '科技推广和应用服务业':'M', 
                     '水利、环境和公共设施管理业':'N', '水利管理业':'N', '生态保护和环境治理业':'N', '公共设施管理业':'N', '土地管理业':'N', 
                     '居民服务、修理和其他服务业':'O', '居民服务业':'O', '机动车、电子产品和日用产品修理业':'O', '其他服务业':'O', 
                     '教育':'P', 
                     '卫生和社会工作':'Q', '卫生':'Q', '社会工作':'Q', 
                     '文化、体育和娱乐业':'R', '新闻和出版业':'R', '广播、电视、电影和录音制作业':'R', '文化艺术业':'R', '体育':'R', '娱乐业':'R', 
                     '公共管理、社会保障和社会组织':'S', '中国共产党机关':'S', '国家机构':'S', '人民政协、民主党派':'S', '社会保障':'S', '群众团体、社会团体和其他成员组织':'S', '基层群众自治组织':'S', 
                     '国际组织':'T',
                     '其它':'Z'})
SECTOR_MAP = {'A':'primary',
              'B':'secondary', 'C':'secondary', 'D':'secondary', 'E':'secondary', 
              'F':'tertiary', 'G':'tertiary', 'H':'tertiary', 'I':'tertiary', 'J':'tertiary', 'L':'tertiary', 'M':'tertiary', 'N':'tertiary', 'O':'tertiary', 'P':'tertiary', 'Q':'tertiary', 'R':'tertiary', 
              'K':'realestate', 
              'S':'government', 'T':'government', 
              'Z':'other_sector',
              '?':'other_sector'}


df = pd.read_csv("./land_city_new.csv")
df.fillna(0, inplace=True)
labels = list(df['company_industry'])
sub_industry = [l if l in CATEGORY_MAP else INDUSTRY_MAP[l] for l in labels]
industry = [CATEGORY_MAP[s] for s in sub_industry]
df.insert(8, 'industry', industry)
sector = [SECTOR_MAP[i] for i in industry]
df.insert(9, 'sector', sector)
df.to_csv('./land_city_new.csv', index=False)
count = Counter(sector)
print(count)
sectors1 = map(lambda x: SECTOR_MAP[CATEGORY_MAP[x]], labels)
count1 = Counter(sectors1)
print(count1)
# primary = 0
# secondary = 0
# tertiary = 0
# realestate = 0
# government = 0
# unknown = 0
# for label in labels:
#     if label not in CATEGORY_MAP:
#         if label not in COMPANY_IND_MAP:
#             count += 1
#             print(label, count)
#         else:
#             temp = COMPANY_IND_MAP[label]
#             if temp not in CATEGORY_MAP:
#                 print('Cannnot find category for', temp)
            # else:
            #     print(CATEGORY_MAP[temp])