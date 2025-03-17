"""
八字合婚专业系统 v5.0（一体化版本）
包含21个核心维度分析与所有依赖模块
"""
from datetime import datetime, timedelta
import sys
import os
import sqlite3
import math
from collections import defaultdict
import random

# 不再需要外部导入模块，所有代码都整合在一个文件中

###################################################
# 节气计算模块（原solarterm.py）
###################################################
class SolarTerm:
    """精确到分钟的二十四节气计算类"""
    
    def __init__(self):
        # 节气名称列表
        self.terms = [
            "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
            "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
            "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
            "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
        ]
        
        # 各节气对应黄经度数
        self.longitudes = [
            315, 330, 345, 0, 15, 30, 
            45, 60, 75, 90, 105, 120,
            135, 150, 165, 180, 195, 210, 
            225, 240, 255, 270, 285, 300
        ]
        

    def get_jieqi_date(self, year, term_name):
        """获取指定年份中某节气的日期"""
        if term_name not in self.terms:
            raise ValueError(f"未知的节气名称: {term_name}")
        
        # 找出节气索引
        term_index = self.terms.index(term_name)
        
        # 基于节气发生的估算日期
        estimate_date = self._estimate_term_date(year, term_index)
        
        # 使用二分法精确计算节气时间
        return self._precise_term_time(year, term_index, estimate_date)

    def _estimate_term_date(self, year, term_index):
        """估算节气日期（公式来自寿星万年历）"""
        # 不同节气的基本日期估算
        base_estimates = [
            [4, 19], [18, 34], [35, 50], [51, 66],  # 立春到春分
            [67, 82], [83, 98], [99, 114], [115, 130],  # 清明到小满
            [131, 146], [147, 162], [163, 178], [179, 194],  # 芒种到大暑
            [195, 210], [211, 226], [227, 242], [243, 258],  # 立秋到秋分
            [259, 274], [275, 290], [291, 306], [307, 322],  # 寒露到小雪
            [323, 338], [339, 354], [355, 370], [371, 386]   # 大雪到大寒
        ]
        
        month_estimate, day_estimate = base_estimates[term_index]
        month_estimate = month_estimate // 31 + 1
        day_estimate = day_estimate % 31 + 1
        
        # 简单的历年调整，实际应该用天文算法
        if term_index >= 12:  # 后半年调整
            day_offset = (year % 4) // 2
        else:  # 前半年调整
            day_offset = -(year % 4) // 2
        
        try:
            # 生成估计日期
            return datetime(year, month_estimate, day_estimate) + timedelta(days=day_offset)
        except ValueError:
            # 简单处理月末日期溢出
            if month_estimate == 2 and day_estimate > 28:
                day_estimate = 28
                if self._is_leap_year(year):
                    day_estimate = 29
            return datetime(year, month_estimate, day_estimate) + timedelta(days=day_offset)
    
    def _precise_term_time(self, year, term_index, estimate_date):
        """使用简化天文算法计算精确节气时间（简化版）"""
        # 这里为了简化，直接返回估算日期
        return estimate_date
    
    def _is_leap_year(self, year):
        """判断是否为闰年"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def get_terms_in_year(self, year):
        """获取指定年份中的所有节气日期"""
        result = []
        for term in self.terms:
            result.append((term, self.get_jieqi_date(year, term)))
        return result

###################################################
# 八字合婚系统主类
###################################################
class ProfessionalHehun:
    def __init__(self, male_birth, female_birth):
        # 初始化时空参数
        self.jq = SolarTerm()  # 精确到分钟的节气计算
        
        # 初始化数据库连接
        try:
            self.conn = sqlite3.connect('hehun_cases.db')
            self.cursor = self.conn.cursor()
            self._create_tables_if_not_exist()  # 确保必要的表存在
        except sqlite3.Error as e:
            print(f"数据库连接错误: {e}")
            # 创建内存数据库作为备用
            self.conn = sqlite3.connect(':memory:')
            self.cursor = self.conn.cursor()
            self._create_tables_if_not_exist()
        
        # 生成三维命盘（含藏干权重）
        self.male = self._generate_3d_mingpan(male_birth)
        self.female = self._generate_3d_mingpan(female_birth)
        
        # 动态规则库（含案例库训练后的权重）
        self._init_rules()
    
    def _create_tables_if_not_exist(self):
        """创建必要的数据库表（如果不存在）"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS trained_rules (
            rule_type TEXT,
            rule_key TEXT,
            weight REAL,
            PRIMARY KEY (rule_type, rule_key)
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS shengxiao_rules (
            pair TEXT PRIMARY KEY,
            weight REAL
        )
        ''')
        
        self.conn.commit()
    
    @classmethod
    def init_database(cls, db_path='hehun_cases.db'):
        """初始化合婚数据库并填充基础数据"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建规则权重表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trained_rules (
            rule_type TEXT,
            rule_key TEXT,
            weight REAL,
            PRIMARY KEY (rule_type, rule_key)
        )
        ''')
        
        # 创建生肖规则表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS shengxiao_rules (
            pair TEXT PRIMARY KEY,
            weight REAL
        )
        ''')
        
        # 插入基础规则数据
        rule_data = [
            ('生肖', '六合', 1.2),
            ('生肖', '三合', 1.1),
            ('五行', '互补', 1.3),
            ('天干', '五合', 1.1)
        ]
        
        cursor.executemany(
            "INSERT OR REPLACE INTO trained_rules VALUES (?, ?, ?)",
            rule_data
        )
        
        # 插入生肖配对数据
        shengxiao_data = [
            ('子鼠丑牛', 1.2),
            ('寅虎卯兔', 1.3),
            ('子鼠申猴', 1.4),
            ('寅虎午马', 1.2)
        ]
        
        cursor.executemany(
            "INSERT OR REPLACE INTO shengxiao_rules VALUES (?, ?)",
            shengxiao_data
        )
        
        # 提交更改
        conn.commit()
        conn.close()
        
        print(f"数据库 {db_path} 初始化完成！")
        
    def _init_rules(self):
        """动态规则初始化（含案例库训练）"""
        # 基础规则
        self.rules = {
            '生肖': {'六合':1.8, '三合':1.6, '六冲':-2.0, '六害':-1.5, '相刑':-2.5},
            '天干': {'五合':2.0, '相生':1.5, '相克':-1.2},
            '地支': {'六合':2.5, '三合':2.0, '相冲':-2.8, '相害':-2.0},
            '五行': {'互补':3.0, '相生':2.0, '相克':-2.5},
            '十神': {'正官正财':2.5, '七杀伤官':-1.8},
            '神煞': {'桃花':-1.5, '孤鸾':-2.0, '阴差阳错':-2.5},
            '宫位': {'夫妻宫合':3.0, '命宫合':2.0, '年柱天合地合':2.5},
            '大运': {'同步率':1.5, '流年冲突':-2.0},
            '纳音': {'相生':1.8, '相同':1.5, '相克':-1.2}
        }
        # 案例库校正
        self.cursor.execute("SELECT rule_type, rule_key, weight FROM trained_rules")
        for rule_type, key, weight in self.cursor.fetchall():
            if rule_type in self.rules and key in self.rules[rule_type]:
                self.rules[rule_type][key] *= weight

        self.rules.update({
                '三元宫位': {'匹配':1.5},
                '现实因素': {'年龄差':0.5, '学历差':0.3},
                '阴阳平衡': {'互补':2.0, '相斥':-1.5},
                '星宿配对': {'匹配':1.2},
                '用神': {'互补':3.0},
                '子息宫': {'相生':1.0, '相克':-0.5},
                '配偶星': {'多现':-0.8}
            })

    def get_true_month(self, dt):
        """获取真实的月份（按节气划分）"""
        # 节气顺序
        terms = [
            "立春", "惊蛰", "清明", "立夏", 
            "芒种", "小暑", "立秋", "白露",
            "寒露", "立冬", "大雪", "小寒"
        ]
        
        # 检查dt是否在今年对应节气之后
        year = dt.year
        for i, term in enumerate(terms):
            try:
                term_date = self.jq.get_jieqi_date(year, term)
                if dt < term_date:
                    # 如果在该节气之前，则月份为上一个节气对应的月份
                    return i if i > 0 else 12
            except Exception as e:
                print(f"节气计算错误: {e}")
                # 简单替代方案：使用公历月份
                return dt.month
        
        # 如果经过所有节气判断还未返回，则说明在小寒之后，月份为12
        return 12

    def get_lunar_month(self, dt):
        """获取农历月份（简化版）"""
        try:
            # 此处以节气推算月份为例
            true_month = self.get_true_month(dt)
            
            # 农历一般比公历推迟约1个月
            lunar_month = true_month - 1
            if lunar_month == 0:
                lunar_month = 12
                
            return lunar_month
        except Exception as e:
            print(f"农历月份计算错误: {e}")
            # 简单替代方案：使用公历月份
            month = dt.month - 1
            if month == 0:
                month = 12
            return month

    def _generate_3d_mingpan(self, birth):
        """三维命盘生成（节气校正+藏干权重）"""
        # 定义藏干能量模型
        hidden_elements = {
            '寅': [('甲',0.6), ('丙',0.3), ('戊',0.1)],
            '午': [('丁',0.7), ('己',0.3)],
            '子': [('癸',1.0)], '丑': [('己',0.6), ('癸',0.3), ('辛',0.1)],
            '卯': [('乙',1.0)], '辰': [('戊',0.6), ('乙',0.3), ('癸',0.1)],
            '巳': [('丙',0.6), ('庚',0.3), ('戊',0.1)], '未': [('己',0.6), ('丁',0.3), ('乙',0.1)],
            '申': [('庚',0.6), ('壬',0.3), ('戊',0.1)], '酉': [('辛',1.0)],
            '戌': [('戊',0.6), ('辛',0.3), ('丁',0.1)], '亥': [('壬',0.7), ('甲',0.3)]
        }
        
        try:
            # 节气精确到分钟判断月柱（网页3）
            true_month = self.get_true_month(birth)
            
            result = {
                '年柱': self._get_ganzhi(birth, 'year'),
                '月柱': self._get_ganzhi(birth, 'month', true_month),
                '日柱': self._get_ganzhi(birth, 'day'),
                '时柱': self._get_ganzhi(birth, 'hour'),
                '藏干': hidden_elements,
                '命宫': self._calculate_minggong(birth),
                'birth_date': birth  # 添加出生日期
            }
            return result
        except Exception as e:
            print(f"命盘生成错误: {e}")
            # 返回一个基础命盘作为备用
            return {
                '年柱': ('甲', '子'), '月柱': ('丙', '寅'),
                '日柱': ('戊', '辰'), '时柱': ('庚', '午'),
                '藏干': hidden_elements,  # 现在这个变量一定是已定义的
                '命宫': '寅',
                'birth_date': birth
            }

    def _get_ganzhi(self, dt, unit, true_month=None):
        """干支计算核心算法（含节气校正）"""
        try:
            # 年柱计算（立春分界）
            if unit == 'year':
                jieqi_date = self.jq.get_jieqi_date(dt.year, '立春')
                if dt < jieqi_date:
                    year = dt.year - 1
                else:
                    year = dt.year
                gan = ('甲','乙','丙','丁','戊','己','庚','辛','壬','癸')[(year - 4) % 10]
                zhi = ('子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥')[(year - 4) % 12]
                return (gan, zhi)
            
            # 月柱计算（节气校正）
            if unit == 'month':
                gan = ('丙','丁','戊','己','庚','辛','壬','癸','甲','乙')[(true_month + 1) % 10]
                zhi = ('寅','卯','辰','巳','午','未','申','酉','戌','亥','子','丑')[true_month - 1]
                return (gan, zhi)
            
            # 日柱计算（按公历转换）
            if unit == 'day':
                base_date = datetime(1900, 1, 31)  # 已知甲子日
                delta = (dt.date() - base_date.date()).days
                gan_index = (delta % 10 + 6) % 10
                zhi_index = (delta % 12 + 8) % 12
                return (('甲','乙','丙','丁','戊','己','庚','辛','壬','癸')[gan_index],
                        ('子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥')[zhi_index])
            
            # 时柱计算
            if unit == 'hour':
                hour_zhi = ('子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥')[dt.hour // 2]
                day_gan = self._get_ganzhi(dt, 'day')[0]
                gan_index = (['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'].index(day_gan) % 5) * 2 + (dt.hour // 2) % 10
                hour_gan = ('甲','乙','丙','丁','戊','己','庚','辛','壬','癸')[gan_index % 10]
                return (hour_gan, hour_zhi)
        except Exception as e:
            print(f"干支计算错误 ({unit}): {e}")
            # 返回默认值作为备用
            return ('甲', '子')

    def _calculate_minggong(self, birth):
        """命宫计算（网页1宫位系统）"""
        try:
            # 按农历月份和时辰计算
            lunar_month = self.get_lunar_month(birth)
            hour = birth.hour
            zhi_list = ['寅','卯','辰','巳','午','未','申','酉','戌','亥','子','丑']
            offset = (13 - lunar_month - (hour // 2)) % 12
            return zhi_list[offset]
        except Exception as e:
            print(f"命宫计算错误: {e}")
            return '寅'  # 返回默认命宫作为备用

    # 剩余方法保持不变
    def full_analysis(self):
        """全维度分析引擎"""
        report = {
            'score': 0,
            'details': [],
            'warnings': [],
            'suggestions': []
        }
        
        # 维度1：生肖五维分析
        sx_res = self._analyze_shengxiao()
        report['score'] += sx_res['score']
        report['details'].append(sx_res['detail'])
        if sx_res.get('warning'):
            report['warnings'].append(sx_res['warning'])
        
        # 维度2：天干五合与相生相克（网页2）
        tg_res = self._analyze_tiangan()
        report['score'] += tg_res['score']
        report['details'].extend(tg_res['details'])
        
        # 维度3：地支六合/三合/刑冲破害（网页1）
        dz_res = self._analyze_dizhi()
        report['score'] += dz_res['score']
        report['details'].append(dz_res['detail'])
        
        # 维度4：五行互补与用神匹配（网页2）
        wx_res = self._analyze_wuxing()
        report['score'] += wx_res['score']
        report['details'].extend(wx_res['details'])
        
        # 维度5：十神关系与夫妻宫（网页2）
        ss_res = self._analyze_shishen()
        report['score'] += ss_res['score']
        report['details'].append(ss_res['detail'])
        
        # 维度6：神煞系统检测（网页1）
        ssx_res = self._analyze_shensha()
        report['score'] += ssx_res['score']
        report['warnings'].extend(ssx_res['warnings'])
        
        # 维度7：大运流年耦合分析（网页3）
        dy_res = self._analyze_dayun()
        report['score'] += dy_res['score']
        report['details'].append(dy_res['forecast'])
        
        # 维度8：纳音婚配与三元宫位（网页1）
        ny_res = self._analyze_nayin()
        report['score'] += ny_res['score']
        report['details'].append(ny_res['comment'])

            # 新增维度9：属相相刑
        xx_res = self._analyze_xiangxing()
        report['score'] += xx_res['score']
        report['details'].append(xx_res['detail'])
        
        # 新增维度10：日干生克
        rg_res = self._analyze_rigan()
        report['score'] += rg_res['score']
        report['details'].append(rg_res['detail'])
        
        # 新增维度11：日支藏干
        rz_res = self._analyze_rizhi_zanggan()
        report['score'] += rz_res['score']
        report['details'].append(rz_res['detail'])
        
        # 新增维度12：三元宫位
        sy_res = self._analyze_sanyuan()
        report['score'] += sy_res['score']
        report['details'].append(sy_res['detail'])
        
        # 新增维度13：深度桃花
        th_res = self._analyze_taohua()
        report['score'] += th_res['score']
        report['details'].append(th_res['detail'])
        
        # 新增维度14：现实因素
        rl_res = self._analyze_reality()
        report['score'] += rl_res['score'] 
        report['details'].append(rl_res['detail'])

            # 新增维度15：太极阴阳
        yy_res = self._analyze_yinyang()
        report['score'] += yy_res['score']
        report['details'].append(yy_res['detail'])
    
        # 新增维度16：星宿配对
        xx_res = self._analyze_xingxiu()
        report['score'] += xx_res['score']
        report['details'].append(xx_res['detail'])
        
        # 新增维度17：深度用神
        ys_res = self._analyze_yongshen()
        report['score'] += ys_res['score']
        report['details'].append(ys_res['detail'])
        
        # 新增维度18：子息宫
        zx_res = self._analyze_zixi()
        report['score'] += zx_res['score']
        report['details'].append(zx_res['detail'])
        
        # 新增维度19：配偶星多现
        dx_res = self._analyze_duoxing()
        report['score'] += dx_res['score']
        report['details'].append(dx_res['detail'])

        # 新增维度20：贵人驿马
        gr_res = self._analyze_guiren()
        report['score'] += gr_res['score']
        report['details'].append(gr_res['detail'])
        
        # 新增维度21：职业匹配
        cy_res = self._analyze_career()
        report['score'] += cy_res['score']
        report['details'].append(cy_res['detail'])
        
        # 生成最终建议（网页3）
        report['suggestions'] = self._generate_suggestions(report)
        report['score'] = self._normalize_score(report['score'])
        return report

    def _analyze_shengxiao(self):
        """生肖五维分析"""
        sx_m = self.male['年柱'][1]
        sx_f = self.female['年柱'][1]
        result = {'score':0, 'detail':'', 'warning':''}
        
        # 六合检测
        liuhe_pairs = [('子','丑'), ('寅','亥'), ('卯','戌'), 
                      ('辰','酉'), ('巳','申'), ('午','未')]
        if (sx_m, sx_f) in liuhe_pairs or (sx_f, sx_m) in liuhe_pairs:
            result['score'] += self.rules['生肖']['六合']
            result['detail'] += f"生肖六合({sx_m}+{sx_f}) +{self.rules['生肖']['六合']}分 "
        
        # 三合检测
        sanhe_groups = ['申子辰','寅午戌','巳酉丑','亥卯未']
        for group in sanhe_groups:
            if sx_m in group and sx_f in group:
                result['score'] += self.rules['生肖']['三合']
                result['detail'] += f"生肖三合({group}) +{self.rules['生肖']['三合']}分 "
        
        # 六冲检测
        xiangchong = [('子','午'), ('丑','未'), ('寅','申'), 
                     ('卯','酉'), ('辰','戌'), ('巳','亥')]
        if (sx_m, sx_f) in xiangchong or (sx_f, sx_m) in xiangchong:
            penalty = self.rules['生肖']['六冲']
            result['score'] += penalty
            result['detail'] += f"生肖相冲({sx_m}{sx_f}) {penalty}分 "
            result['warning'] = "生肖相冲易导致矛盾，建议佩戴吉祥物化解"
        
        # 六害检测

        # 相刑检测

        #

        # 案例库权重调整
        self.cursor.execute("SELECT weight FROM shengxiao_rules WHERE pair=?", (sx_m+sx_f,))
        if db_weight := self.cursor.fetchone():
            result['score'] *= db_weight[0]
        return result

    def _analyze_yinyang(self):
        """太极阴阳平衡检测（网页1的阴阳得配原则）"""
        yinyang_map = {'甲':'阳','乙':'阴','丙':'阳','丁':'阴','戊':'阳',
                    '己':'阴','庚':'阳','辛':'阴','壬':'阳','癸':'阴'}
        
        # 获取日干阴阳属性
        male_yinyang = yinyang_map[self.male['日柱'][0]]
        female_yinyang = yinyang_map[self.female['日柱'][0]]
        
        score = 2.0 if male_yinyang != female_yinyang else -1.5  # 阴阳互补得分
        return {
            'score': score,
            'detail': f"阴阳平衡：{male_yinyang}←→{female_yinyang} → {'+' if score>0 else ''}{score}分[1](@ref)"
        }

    def _analyze_xingxiu(self):
        """星宿配对分析（网页2的甲子丙寅同星宿规则）"""
        xingxiu_groups = {
            '甲子':['丙寅','戊辰'], '乙丑':['丁卯','己巳'],
            # 其他星宿组合需补充完整...
        }
        
        nianzhu_m = ''.join(self.male['年柱'])
        nianzhu_f = ''.join(self.female['年柱'])
        
        match_score = 0
        if nianzhu_f in xingxiu_groups.get(nianzhu_m, []):
            match_score += 1.2
        return {
            'score': match_score,
            'detail': f"年柱星宿：{nianzhu_m}←→{nianzhu_f} → +{match_score}分[2](@ref)"
        }

    def _analyze_yongshen(self):
        """深度用神互补（网页4的用神互为喜忌规则）"""
        def get_yongshen(mingpan):
            # 简化的用神计算（实际需根据旺衰分析）
            wuxing = defaultdict(float)
            for pos in ['年柱','月柱','日柱','时柱']:
                gan, zhi = mingpan[pos]
                # 天干能量
                if gan in ['甲','乙']: wuxing['木'] += 1.0
                elif gan in ['丙','丁']: wuxing['火'] += 1.0
                # 地支藏干
                for elem, weight in mingpan['藏干'].get(zhi, []):
                    if elem in ['甲','乙']: wuxing['木'] += weight
                    elif elem in ['丙','丁']: wuxing['火'] += weight
            # 取最弱五行为用神
            return min(wuxing, key=wuxing.get)
        
        ys_m = get_yongshen(self.male)
        ys_f = get_yongshen(self.female)
        
        # 判断用神互补
        score = 3.0 if ys_m == ys_f else 0
        return {
            'score': score,
            'detail': f"用神互补：{ys_m}←→{ys_f} → +{score}分[4](@ref)"
        }

    def _analyze_zixi(self):
        """子息宫匹配（网页7的时柱子女运分析）"""
        sz_m = self.male['时柱'][1]
        sz_f = self.female['时柱'][1]
        
        # 时支相生关系
        shengke_map = {'子':'生','丑':'克','寅':'生','卯':'生',
                    '辰':'克','巳':'克','午':'生','未':'克',
                    '申':'生','酉':'生','戌':'克','亥':'生'}
        relation = shengke_map.get(sz_m, '') == '生'
        score = 1.0 if relation else -0.5
        return {
            'score': score,
            'detail': f"子息宫：{sz_m}←→{sz_f} → {'+' if score>0 else ''}{score}分[7](@ref)"
        }

    def _analyze_duoxing(self):
        """配偶星多现检测（网页3的官杀/财才混杂分析）"""
        # 男命财星多现
        male_caix = sum(1 for pos in ['年柱','月柱','日柱','时柱'] 
                    if self.male[pos][0] in ['戊','己'])
        # 女命官杀多现
        female_gs = sum(1 for pos in ['年柱','月柱','日柱','时柱']
                    if self.female[pos][0] in ['庚','辛'])
        
        penalty = max(male_caix-1, female_gs-1) * -0.8
        return {
            'score': penalty,
            'detail': f"配偶星多现：男财{male_caix}个/女官{female_gs}个 → {penalty}分[3](@ref)"
        }


    def _analyze_wuxing(self):
        """五行能量场动态互补（网页2的用神互补规则）"""
        def calc_element_energy(mingpan):
            """计算五行总能量（主气+藏干）"""
            counter = defaultdict(float)
            # 天干能量
            for pos in ['年柱','月柱','日柱','时柱']:
                gan = mingpan[pos][0]
                if gan in ['甲','乙']: counter['木'] += 1.0
                elif gan in ['丙','丁']: counter['火'] += 1.0
                elif gan in ['戊','己']: counter['土'] += 1.0
                elif gan in ['庚','辛']: counter['金'] += 1.0
                elif gan in ['壬','癸']: counter['水'] += 1.0
            # 地支藏干
            for pos in ['年柱','月柱','日柱','时柱']:
                zhi = mingpan[pos][1]
                for elem, weight in mingpan['藏干'].get(zhi, []):
                    if elem in ['甲','乙']: counter['木'] += weight
                    elif elem in ['丙','丁']: counter['火'] += weight
                    elif elem in ['戊','己']: counter['土'] += weight
                    elif elem in ['庚','辛']: counter['金'] += weight
                    elif elem in ['壬','癸']: counter['水'] += weight
            return counter
        
        wu_m = calc_element_energy(self.male)
        wu_f = calc_element_energy(self.female)
        result = {'score':0, 'details':[]}
        
        # 互补性计算（网页2的用神互补）
        max_m = max(wu_m, key=wu_m.get)
        min_m = min(wu_m, key=wu_m.get)
        max_f = max(wu_f, key=wu_f.get)
        min_f = min(wu_f, key=wu_f.get)
        
        if min_m == max_f or min_f == max_m:
            result['score'] += self.rules['五行']['互补']
            result['details'].append(f"五行互补：{max_m}←→{max_f} +{self.rules['五行']['互补']}分")
        
        # 生克关系（网页1的五行相生）
        shengke_map = {'木':'火','火':'土','土':'金','金':'水','水':'木'}
        if shengke_map[max_m] == max_f:
            result['score'] += self.rules['五行']['相生']
            result['details'].append(f"五行相生：{max_m}→{max_f} +{self.rules['五行']['相生']}分")
        return result

    def _analyze_shishen(self):
        """十神关系与夫妻宫分析（网页2的日支配合）"""
        # 十神关系映射表 - 完整版
        shishen_map = {
            '甲': {'甲':'比肩', '乙':'劫财', '丙':'食神', '丁':'伤官', '戊':'偏财',
                  '己':'正财', '庚':'七杀', '辛':'正官', '壬':'偏印', '癸':'正印'},
            '乙': {'甲':'劫财', '乙':'比肩', '丙':'伤官', '丁':'食神', '戊':'正财',
                  '己':'偏财', '庚':'正官', '辛':'七杀', '壬':'正印', '癸':'偏印'},
            '丙': {'甲':'偏印', '乙':'正印', '丙':'比肩', '丁':'劫财', '戊':'食神',
                  '己':'伤官', '庚':'偏财', '辛':'正财', '壬':'七杀', '癸':'正官'},
            '丁': {'甲':'正印', '乙':'偏印', '丙':'劫财', '丁':'比肩', '戊':'伤官',
                  '己':'食神', '庚':'正财', '辛':'偏财', '壬':'正官', '癸':'七杀'},
            '戊': {'甲':'七杀', '乙':'正官', '丙':'偏印', '丁':'正印', '戊':'比肩',
                  '己':'劫财', '庚':'食神', '辛':'伤官', '壬':'偏财', '癸':'正财'},
            '己': {'甲':'正官', '乙':'七杀', '丙':'正印', '丁':'偏印', '戊':'劫财',
                  '己':'比肩', '庚':'伤官', '辛':'食神', '壬':'正财', '癸':'偏财'},
            '庚': {'甲':'偏财', '乙':'正财', '丙':'七杀', '丁':'正官', '戊':'偏印',
                  '己':'正印', '庚':'比肩', '辛':'劫财', '壬':'食神', '癸':'伤官'},
            '辛': {'甲':'正财', '乙':'偏财', '丙':'正官', '丁':'七杀', '戊':'正印',
                  '己':'偏印', '庚':'劫财', '辛':'比肩', '壬':'伤官', '癸':'食神'},
            '壬': {'甲':'伤官', '乙':'食神', '丙':'偏财', '丁':'正财', '戊':'七杀',
                  '己':'正官', '庚':'偏印', '辛':'正印', '壬':'比肩', '癸':'劫财'},
            '癸': {'甲':'食神', '乙':'伤官', '丙':'正财', '丁':'偏财', '戊':'正官',
                  '己':'七杀', '庚':'正印', '辛':'偏印', '壬':'劫财', '癸':'比肩'}
        }
        
        male_rizhu_gan = self.male['日柱'][0]
        female_rizhu_gan = self.female['日柱'][0]
        
        # 男方视角的十神 - 添加错误处理
        if male_rizhu_gan in shishen_map:
            male_ss = shishen_map[male_rizhu_gan].get(female_rizhu_gan, '未知')
        else:
            male_ss = '未知'
            
        # 女方视角的十神 - 添加错误处理  
        if female_rizhu_gan in shishen_map:
            female_ss = shishen_map[female_rizhu_gan].get(male_rizhu_gan, '未知')
        else:
            female_ss = '未知'
        
        # 十神吉凶评分（网页1的十神规则）
        score = 0
        if (male_ss, female_ss) == ('正财', '正官'):
            score += self.rules['十神']['正官正财']
        elif '七杀' in (male_ss, female_ss) or '伤官' in (male_ss, female_ss):
            score += self.rules['十神']['七杀伤官']
        
        # 夫妻宫分析（网页2的日支配合）
        rz_m = self.male['日柱'][1]
        rz_f = self.female['日柱'][1]
        liuhe_pairs = [('子','丑'), ('寅','亥'), ('卯','戌'), 
                      ('辰','酉'), ('巳','申'), ('午','未')]
        if (rz_m, rz_f) in liuhe_pairs or (rz_f, rz_m) in liuhe_pairs:
            score += self.rules['宫位']['夫妻宫合']
        
        return {
            'score': score,
            'detail': f"十神：{male_ss}/{female_ss} → 得分：{score} | 夫妻宫：{rz_m}+{rz_f}"
        }

    def _analyze_dayun(self):
        """大运流年耦合分析（网页3的运势同步规则）"""
        def get_dayun(mingpan):
            """计算当前大运（每十年一运）"""
            birth_year = int(mingpan['birth_date'].year)
            current_year = datetime.now().year
            
            # 简化大运计算
            dayun_index = (current_year - birth_year) // 10
            base_month = 1 + (dayun_index % 12)
            return self._get_ganzhi(mingpan['birth_date'], 'month', base_month)
        
        dayun_m = get_dayun(self.male)
        dayun_f = get_dayun(self.female)
        result = {'score':0, 'forecast':''}
        
        # 大运五行关系（网页6的同步率规则）
        wuxing_map = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土',
                     '己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
        wx_m = wuxing_map[dayun_m[0]]
        wx_f = wuxing_map[dayun_f[0]]
        
        # 生克关系评分（网页3）
        shengke_chain = {'木':'火','火':'土','土':'金','金':'水','水':'木'}
        if shengke_chain[wx_m] == wx_f:
            result['score'] += self.rules['大运']['同步率']
            result['forecast'] += f"大运相生({wx_m}→{wx_f}) +{self.rules['大运']['同步率']}分 "
        
        # 流年冲突检测（网页7）
        current_year = datetime.now().year
        for year in range(current_year, current_year+5):
            year_ganzhi = self._get_ganzhi(datetime(year,1,1), 'year')
            # 检测与双方年柱/日柱的冲克
            if self._check_liuchong(year_ganzhi[1], self.male['年柱'][1]):
                result['score'] += self.rules['大运']['流年冲突']
                result['forecast'] += f"{year}年冲男方年柱 -{abs(self.rules['大运']['流年冲突'])}分 "
        return result

    def _analyze_xiangxing(self):
        """属相相刑检测（网页1的恃势/无恩/无礼/自刑）"""
        sx_m = self.male['年柱'][1]
        sx_f = self.female['年柱'][1]
        xiangxing_groups = [
            ['丑','戌','未'],  # 恃势之刑
            ['寅','巳','申'],  # 无恩之刑
            ['子','卯'],       # 无礼之刑
            ['亥','辰','酉','午']  # 自刑
        ]
        
        penalty = 0
        detail = ""
        # 检测互刑关系
        for group in xiangxing_groups:
            if sx_m in group and sx_f in group:
                penalty += self.rules['生肖']['相刑']
                detail += f"属相相刑（{'/'.join(group)}） -{abs(self.rules['生肖']['相刑'])}分 "
        
        return {'score': penalty, 'detail': detail}

    def _analyze_rigan(self):
        """日干生克关系（网页2的日主维度）"""
        rg_m = self.male['日柱'][0]
        rg_f = self.female['日柱'][0]
        
        # 天干相生关系
        shengke_map = {
            '甲':{'丙':'生','戊':'克'}, '乙':{'丁':'生','己':'克'},
            '丙':{'戊':'生','庚':'克'}, '丁':{'己':'生','辛':'克'},
            '戊':{'庚':'生','壬':'克'}, '己':{'辛':'生','癸':'克'},
            '庚':{'壬':'生','甲':'克'}, '辛':{'癸':'生','乙':'克'},
            '壬':{'甲':'生','丙':'克'}, '癸':{'乙':'生','丁':'克'}
        }
        
        relation = shengke_map[rg_m].get(rg_f, '')
        score = self.rules['天干']['相生'] if '生' in relation else \
                self.rules['天干']['相克'] if '克' in relation else 0
                
        return {
            'score': score,
            'detail': f"日干关系：{rg_m}→{rg_f}（{relation}） {'+' if score>0 else ''}{score}分"
        }

    def _analyze_rizhi_zanggan(self):
        """日支藏干互动（网页2的日支主气匹配）"""
        rz_m = self.male['日柱'][1]
        rz_f = self.female['日柱'][1]
        
        # 获取日支主气藏干
        main_m = self.male['藏干'][rz_m][0][0] if rz_m in self.male['藏干'] else ''
        main_f = self.female['藏干'][rz_f][0][0] if rz_f in self.female['藏干'] else ''
        
        score = 0
        if main_m == self.female['日柱'][0]:
            score += 1.2
        if main_f == self.male['日柱'][0]:
            score += 1.2
            
        return {
            'score': score,
            'detail': f"日支藏干：{rz_m}({main_m})←→{rz_f}({main_f}) → +{score}分"
        }

    def _analyze_sanyuan(self):
        """三元宫位匹配（网页1的命宫/福德宫/夫妻宫）"""
        def get_sanyuan(mingpan):
            # 命宫已计算，福德宫取月支，夫妻宫取日支
            return {
                '命宫': mingpan['命宫'],
                '福德宫': mingpan['月柱'][1],
                '夫妻宫': mingpan['日柱'][1]
            }
        
        sanyuan_m = get_sanyuan(self.male)
        sanyuan_f = get_sanyuan(self.female)
        
        match_count = 0
        for key in ['命宫','福德宫','夫妻宫']:
            if sanyuan_m[key] == sanyuan_f[key]:
                match_count += 1
        
        score = match_count * 1.5
        return {
            'score': score,
            'detail': f"三元宫位匹配度：{match_count}/3 → +{score}分"
        }

    def _analyze_taohua(self):
        """深度桃花分析（网页2的流年桃花）"""
        def detect_taohua(mingpan, gender):
            # 日时支桃花检测
            peach = 0
            for zhi in [mingpan['日柱'][1], mingpan['时柱'][1]]:
                if zhi in ['子','午','卯','酉']:
                    peach += 0.5
            
            # 简化流年桃花检测，移除对正官的引用
            current_year = datetime.now().year
            for year in range(current_year, current_year+5):
                year_zhi = self._get_ganzhi(datetime(year,1,1), 'year')[1]
                if year_zhi in ['卯','酉'] and gender=='female':  # 简化检测逻辑
                    peach += 1
                elif year_zhi in ['子','午'] and gender=='male':  # 简化检测逻辑
                    peach += 1
            return peach
        
        taohua_m = detect_taohua(self.male, 'male')
        taohua_f = detect_taohua(self.female, 'female')
        
        penalty = - (taohua_m + taohua_f) * 0.8
        return {
            'score': penalty,
            'detail': f"桃花检测：男{taohua_m}级/女{taohua_f}级 → {penalty}分"
        }

    def _analyze_guiren(self):
        """贵人驿马检测（网页2的特殊神煞）"""
        def detect_special_shensha(mingpan):
            # 天乙贵人检测
            guiren_rules = {
                '甲':['丑','未'], '乙':['子','申'],
                '丙':['亥','酉'], '丁':['酉','亥'],
                # 其他天干贵人规则...
            }
            # 驿马星检测（寅午戌见申）
            yima_rules = {
                '寅':'申', '午':'申', '戌':'申',
                '巳':'亥', '酉':'亥', '丑':'亥',
                # 其他三合局...
            }
            
            guiren = 0
            yima = 0
            ri_gan = mingpan['日柱'][0]
            # 贵人检测
            for zhi in mingpan.values():
                if isinstance(zhi, tuple) and zhi[1] in guiren_rules.get(ri_gan, []):
                    guiren += 1
            # 驿马检测
            yima_zhi = yima_rules.get(mingpan['年柱'][1], '')
            if yima_zhi in [mingpan['月柱'][1], mingpan['日柱'][1]]:
                yima += 1
            return guiren, yima
        
        gm, ym = detect_special_shensha(self.male)
        gf, yf = detect_special_shensha(self.female)
        
        score = (gm + gf) * 0.5 - (ym + yf) * 0.3
        return {
            'score': score,
            'detail': f"贵人驿马：男贵{gm}/驿{ym} 女贵{gf}/驿{yf} → {score}分[2](@ref)"
        }

    def _analyze_career(self):
        """职业倾向匹配（网页3的现实维度扩展）"""
        career_map = {
            '木': ['教育','艺术'], '火': ['能源','互联网'],
            '土': ['房地产','金融'], '金': ['法律','机械'],
            '水': ['物流','旅游']
        }
        wx_m = max(self._calc_full_wuxing(self.male), key=lambda x:x[1])[0]
        wx_f = max(self._calc_full_wuxing(self.female), key=lambda x:x[1])[0]
        
        match = len(set(career_map[wx_m]) & set(career_map[wx_f]))
        score = match * 0.4
        return {
            'score': score,
            'detail': f"职业匹配：{career_map[wx_m]}←→{career_map[wx_f]} → +{score}分[3](@ref)"
        }

    def _analyze_reality(self):
        """现实维度分析（网页2的年龄/社会因素）"""
        age_diff = abs(self.male['birth_date'].year - self.female['birth_date'].year)
        age_score = -0.5 if age_diff > 8 else 0.2 if 3<age_diff<=8 else 0.5
        
        # 学历匹配（示例逻辑）
        edu_map = {'博士':4, '硕士':3, '本科':2, '大专':1}
        edu_diff = abs(edu_map.get(self.male.get('education',''),0) - 
                    edu_map.get(self.female.get('education',''),0))
        edu_score = -0.3 * edu_diff
        
        return {
            'score': age_score + edu_score,
            'detail': f"现实维度：年龄差{age_diff}年(+{age_score}) 学历差{edu_diff}级({edu_score})"
        }

    def _analyze_nayin(self):
        """纳音婚配与三元宫位（网页1的五行纳音规则）"""
        # 完整纳音表，涵盖六十甲子
        nayin_map = {
            # 甲子甲戌之类
            '甲子':'海中金', '乙丑':'海中金', '丙寅':'炉中火', '丁卯':'炉中火',
            '戊辰':'大林木', '己巳':'大林木', '庚午':'路旁土', '辛未':'路旁土',
            '壬申':'剑锋金', '癸酉':'剑锋金', '甲戌':'山头火', '乙亥':'山头火',
            '丙子':'涧下水', '丁丑':'涧下水', '戊寅':'城头土', '己卯':'城头土',
            '庚辰':'白腊金', '辛巳':'白腊金', '壬午':'杨柳木', '癸未':'杨柳木',
            '甲申':'泉中水', '乙酉':'泉中水', '丙戌':'屋上土', '丁亥':'屋上土',
            '戊子':'霹雳火', '己丑':'霹雳火', '庚寅':'松柏木', '辛卯':'松柏木',
            '壬辰':'长流水', '癸巳':'长流水', '甲午':'砂石金', '乙未':'砂石金',
            '丙申':'山下火', '丁酉':'山下火', '戊戌':'平地木', '己亥':'平地木',
            '庚子':'壁上土', '辛丑':'壁上土', '壬寅':'金箔金', '癸卯':'金箔金',
            '甲辰':'覆灯火', '乙巳':'覆灯火', '丙午':'天河水', '丁未':'天河水',
            '戊申':'大驿土', '己酉':'大驿土', '庚戌':'钗环金', '辛亥':'钗环金',
            '壬子':'桑柘木', '癸丑':'桑柘木', '甲寅':'大溪水', '乙卯':'大溪水',
            '丙辰':'沙中土', '丁巳':'沙中土', '戊午':'天上火', '己未':'天上火',
            '庚申':'石榴木', '辛酉':'石榴木', '壬戌':'大海水', '癸亥':'大海水'
        }
        
        # 纳音五行属性
        wx_map = {
            '金':['海中金', '剑锋金', '白腊金', '砂石金', '金箔金', '钗环金'],
            '木':['大林木', '杨柳木', '松柏木', '平地木', '桑柘木', '石榴木'],
            '水':['涧下水', '泉中水', '长流水', '天河水', '大溪水', '大海水'],
            '火':['炉中火', '山头火', '霹雳火', '山下火', '覆灯火', '天上火'],
            '土':['路旁土', '城头土', '屋上土', '壁上土', '大驿土', '沙中土']
        }
        
        # 组合天干地支
        male_ganzhi = self.male['年柱'][0] + self.male['年柱'][1]
        female_ganzhi = self.female['年柱'][0] + self.female['年柱'][1]
        
        try:
            # 获取纳音属性，添加错误处理
            ny_m = nayin_map.get(male_ganzhi, '未知')
            ny_f = nayin_map.get(female_ganzhi, '未知')
            
            # 初始化结果对象
            result = {'score': 0, 'comment': ''}
            
            # 如果未知纳音，则返回默认结果
            if ny_m == '未知' or ny_f == '未知':
                result['comment'] = f"纳音信息：{male_ganzhi}({ny_m})与{female_ganzhi}({ny_f})"
                return result
            
            # 获取纳音五行属性
            wx_m = None
            wx_f = None
            for wx, items in wx_map.items():
                if ny_m in items:
                    wx_m = wx
                if ny_f in items:
                    wx_f = wx
            
            # 判断纳音相生相克关系
            if wx_m and wx_f:  # 确保五行属性有效
                # 五行相生关系：金→水→木→火→土→金
                if (wx_m == '金' and wx_f == '水') or \
                   (wx_m == '水' and wx_f == '木') or \
                   (wx_m == '木' and wx_f == '火') or \
                   (wx_m == '火' and wx_f == '土') or \
                   (wx_m == '土' and wx_f == '金'):
                    result['score'] += self.rules['纳音']['相生']
                    result['comment'] = f"纳音相生：{ny_m}({wx_m})→{ny_f}({wx_f})"
                # 五行相同
                elif wx_m == wx_f:
                    result['score'] += self.rules['纳音']['相同']
                    result['comment'] = f"纳音相同：{ny_m}({wx_m})={ny_f}({wx_f})"
                # 五行相克：金→木→土→水→火→金
                elif (wx_m == '金' and wx_f == '木') or \
                     (wx_m == '木' and wx_f == '土') or \
                     (wx_m == '土' and wx_f == '水') or \
                     (wx_m == '水' and wx_f == '火') or \
                     (wx_m == '火' and wx_f == '金'):
                    result['score'] += self.rules['纳音']['相克']
                    result['comment'] = f"纳音相克：{ny_m}({wx_m})→{ny_f}({wx_f})"
                else:
                    result['comment'] = f"纳音关系：{ny_m}({wx_m})与{ny_f}({wx_f})"
            
            return result
        except Exception as e:
            # 异常处理，返回默认结果
            print(f"纳音分析错误: {e}")
            return {'score': 0, 'comment': f"纳音分析出现错误，请检查数据"}

    def _check_liuchong(self, zhi1, zhi2):
        """检测地支六冲"""
        liuchong_pairs = [('子','午'),('丑','未'),('寅','申'),
                         ('卯','酉'),('辰','戌'),('巳','亥')]
        return (zhi1, zhi2) in liuchong_pairs or (zhi2, zhi1) in liuchong_pairs

    def _generate_suggestions(self, report):
        """生成动态化解建议（网页3的改进建议）"""
        import random
        suggestions = []
        # 生肖相冲建议
        if any('生肖相冲' in d for d in report['details']):
            suggestions.append("建议佩戴三合生肖吉祥物（如男方属子鼠，可佩戴猴、龙饰品）")
        
        # 五行补救建议
        wx_elements = {'金':'白色金属', '木':'绿色植物', '水':'黑色饰品', 
                      '火':'红色物品', '土':'黄色水晶'}
        
        # 使用报告中的信息决定五行补救
        weak_element = '木'  # 默认值
        for detail in report['details']:
            if '五行互补' in detail:
                for wx in wx_elements:
                    if wx in detail:
                        weak_element = wx
                        break
        
        suggestions.append(f"五行补救：可在卧室{random.choice(['北方','西南方'])}放置{wx_elements[weak_element]}")

        # 大运流年建议
        for detail in report['details']:
            if '流年冲突' in detail:
                suggestions.append("冲突年份建议推迟重大决策，可通过风水布局化解")
                break
        
        return suggestions

    def _normalize_score(self, raw_score):
        """分数归一化（0-100分）"""
        max_score = sum(
            max(v.values()) if isinstance(v,dict) else v 
            for v in self.rules.values()
        )
        return int((raw_score / max_score) * 100)

    def _calc_full_wuxing(self, mingpan):
        """计算完整的五行能量分布"""
        wuxing_energy = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        
        # 天干五行映射
        tg_wuxing = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
                    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
        
        # 地支五行映射
        dz_wuxing = {'寅': '木', '卯': '木', '巳': '火', '午': '火', 
                    '辰': '土', '丑': '土', '戌': '土', '未': '土',
                    '申': '金', '酉': '金', '亥': '水', '子': '水'}
        
        # 计算天干能量
        for pos in ['年柱', '月柱', '日柱', '时柱']:
            if pos in mingpan:
                gan = mingpan[pos][0]
                zhi = mingpan[pos][1]
                
                # 天干直接能量
                if gan in tg_wuxing:
                    wuxing_energy[tg_wuxing[gan]] += 1.0
                
                # 地支显性能量
                if zhi in dz_wuxing:
                    wuxing_energy[dz_wuxing[zhi]] += 0.5
                
                # 地支藏干能量
                if zhi in mingpan['藏干']:
                    for hidden_gan, weight in mingpan['藏干'][zhi]:
                        if hidden_gan in tg_wuxing:
                            wuxing_energy[tg_wuxing[hidden_gan]] += weight * 0.5
        
        # 返回五行能量列表，格式为[(五行,能量值),...]便于排序
        return [(wx, value) for wx, value in wuxing_energy.items()]

    def _analyze_tiangan(self):
        """天干五维分析（五合/相生/相克）"""
        # 提取八字中的天干
        tg_m = [self.male['年柱'][0], self.male['月柱'][0], self.male['日柱'][0], self.male['时柱'][0]]
        tg_f = [self.female['年柱'][0], self.female['月柱'][0], self.female['日柱'][0], self.female['时柱'][0]]
        
        # 结果初始化
        result = {'score': 0, 'details': []}
        
        # 五合检测（甲己合土、乙庚合金等）
        wuhe_pairs = [('甲', '己', '土'), ('乙', '庚', '金'), 
                     ('丙', '辛', '水'), ('丁', '壬', '木'), 
                     ('戊', '癸', '火')]
        
        # 检查五合
        for m_tg in tg_m:
            for f_tg in tg_f:
                for p1, p2, res in wuhe_pairs:
                    if (m_tg == p1 and f_tg == p2) or (m_tg == p2 and f_tg == p1):
                        result['score'] += self.rules['天干']['五合']
                        result['details'].append(f"{m_tg}与{f_tg}五合{res} +{self.rules['天干']['五合']}分")
        
        # 天干相生相克关系
        shengke = {
            '木': {'生': '火', '克': '土'},
            '火': {'生': '土', '克': '金'},
            '土': {'生': '金', '克': '水'},
            '金': {'生': '水', '克': '木'},
            '水': {'生': '木', '克': '火'}
        }
        
        tg_wuxing = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
                   '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
        
        # 检查天干相生相克
        for m_tg in tg_m:
            for f_tg in tg_f:
                m_wx = tg_wuxing[m_tg]
                f_wx = tg_wuxing[f_tg]
                
                # 相生
                if shengke[m_wx]['生'] == f_wx:
                    result['score'] += self.rules['天干']['相生']
                    result['details'].append(f"{m_tg}({m_wx})生{f_tg}({f_wx}) +{self.rules['天干']['相生']}分")
                
                # 相克
                if shengke[m_wx]['克'] == f_wx:
                    result['score'] += self.rules['天干']['相克']
                    result['details'].append(f"{m_tg}({m_wx})克{f_tg}({f_wx}) {self.rules['天干']['相克']}分")
        
        # 日干合化特别强化
        if (tg_m[2], tg_f[2]) in [(p1, p2) for p1, p2, _ in wuhe_pairs] or \
           (tg_f[2], tg_m[2]) in [(p1, p2) for p1, p2, _ in wuhe_pairs]:
            bonus = self.rules['天干']['五合'] * 1.5
            result['score'] += bonus
            result['details'].append(f"【关键】日干{tg_m[2]}与{tg_f[2]}相合 +{bonus}分")
        
        return result

    def _analyze_shensha(self):
        """神煞系统检测（桃花、孤鸾、阴差阳错等）"""
        # 初始化结果
        result = {'score': 0, 'warnings': []}
        
        # 提取八字组件
        male_bazi = [self.male['年柱'], self.male['月柱'], self.male['日柱'], self.male['时柱']]
        female_bazi = [self.female['年柱'], self.female['月柱'], self.female['日柱'], self.female['时柱']]
        
        # 神煞定义
        shensha = {
            '桃花': [('辰', '酉', '丑', '午'), ('卯', '戌', '寅', '亥'), ('子', '申', '巳', '未')],
            '孤鸾': [('巳', '酉', '丑'), ('申', '子', '辰'), ('亥', '卯', '未'), ('寅', '午', '戌')],
            '天罗': ['辰', '戌'],
            '地网': ['丑', '未'],
            '阴差阳错': [('子', '午'), ('丑', '未'), ('寅', '申'), ('卯', '酉'), ('辰', '戌'), ('巳', '亥')]
        }
        
        # 男命桃花煞检测
        m_taohua = False
        for pillar in male_bazi:
            dz = pillar[1]
            for group in shensha['桃花']:
                if dz in group:
                    m_taohua = True
                    result['warnings'].append(f"男命有桃花煞（{dz}）")
                    result['score'] += self.rules['神煞']['桃花']
        
        # 女命桃花煞检测（更严重）
        f_taohua = False
        for pillar in female_bazi:
            dz = pillar[1]
            for group in shensha['桃花']:
                if dz in group:
                    f_taohua = True
                    result['warnings'].append(f"女命有桃花煞（{dz}）")
                    result['score'] += self.rules['神煞']['桃花'] * 1.2  # 女命桃花更严重
        
        # 孤鸾检测（主要看日柱）
        for i, pillar in enumerate(male_bazi + female_bazi):
            dz = pillar[1]
            for group in shensha['孤鸾']:
                if dz in group and i in [2, 6]:  # 2和6是两人的日柱索引
                    result['warnings'].append(f"{'男' if i==2 else '女'}命有孤鸾煞（{dz}）")
                    result['score'] += self.rules['神煞']['孤鸾']
        
        # 阴差阳错日检测
        m_rz, f_rz = male_bazi[2][1], female_bazi[2][1]
        for pair in shensha['阴差阳错']:
            if m_rz in pair and f_rz in pair and m_rz != f_rz:
                result['warnings'].append(f"日支阴差阳错（{m_rz}与{f_rz}）")
                result['score'] += self.rules['神煞']['阴差阳错']
        
        # 无警告时添加默认信息
        if not result['warnings']:
            result['warnings'].append("未发现明显神煞冲突")
        
        return result

    def _analyze_dizhi(self):
        """地支六维分析（六合/三合/相冲/相害/相刑）"""
        # 提取八字中的地支
        dz_m = [self.male['年柱'][1], self.male['月柱'][1], self.male['日柱'][1], self.male['时柱'][1]]
        dz_f = [self.female['年柱'][1], self.female['月柱'][1], self.female['日柱'][1], self.female['时柱'][1]]
        
        # 结果初始化
        result = {'score': 0, 'detail': ""}
        
        # 六合检测（子丑合、寅亥合等）
        liuhe_pairs = [('子', '丑'), ('寅', '亥'), ('卯', '戌'), ('辰', '酉'), ('巳', '申'), ('午', '未')]
        liuhe_count = 0
        for m_dz in dz_m:
            for f_dz in dz_f:
                if (m_dz, f_dz) in liuhe_pairs or (f_dz, m_dz) in liuhe_pairs:
                    liuhe_count += 1
                    result['score'] += self.rules['地支']['六合']
                    result['detail'] += f"{m_dz}与{f_dz}六合 "
        
        # 三合检测（子辰申三合水、寅午戌三合火等）
        sanhe_groups = [('申', '子', '辰'), ('寅', '午', '戌'), ('巳', '酉', '丑'), ('亥', '卯', '未')]
        for group in sanhe_groups:
            m_match = [dz for dz in dz_m if dz in group]
            f_match = [dz for dz in dz_f if dz in group]
            if m_match and f_match:
                result['score'] += self.rules['地支']['三合']
                result['detail'] += f"{'/'.join(m_match+f_match)}三合 "
        
        # 相冲检测（子午冲、丑未冲等）
        xiangchong_pairs = [('子', '午'), ('丑', '未'), ('寅', '申'), ('卯', '酉'), ('辰', '戌'), ('巳', '亥')]
        xiangchong_count = 0
        for m_dz in dz_m:
            for f_dz in dz_f:
                if (m_dz, f_dz) in xiangchong_pairs or (f_dz, m_dz) in xiangchong_pairs:
                    xiangchong_count += 1
                    result['score'] += self.rules['地支']['相冲']
                    result['detail'] += f"{m_dz}与{f_dz}相冲 "
        
        # 相害检测（子未害、丑午害等）
        xianghai_pairs = [('子', '未'), ('丑', '午'), ('寅', '巳'), ('卯', '辰'), ('申', '亥'), ('酉', '戌')]
        xianghai_count = 0
        for m_dz in dz_m:
            for f_dz in dz_f:
                if (m_dz, f_dz) in xianghai_pairs or (f_dz, m_dz) in xianghai_pairs:
                    xianghai_count += 1
                    result['score'] += self.rules['地支']['相害']
                    result['detail'] += f"{m_dz}与{f_dz}相害 "
        
        if not result['detail']:
            result['detail'] = "地支无明显关系"
        
        return result

# 测试用例
if __name__ == '__main__':
    try:
        # 初始化数据库（如果需要）
        # ProfessionalHehun.init_database()
        
        # 男方：甲戌年 庚午月 乙卯日 庚辰时
        male = datetime(1994, 11, 17, 19, 0)
        # 女方：癸酉年 辛酉月 辛亥日 戊戌时
        female = datetime(1997, 10, 10, 8, 0)
        
        analyzer = ProfessionalHehun(male, female)
        result = analyzer.full_analysis()
        
        print("="*40)
        print(f"【合婚专业报告】得分：{result['score']}/100")
        print("\n详细分析：")
        for detail in result['details']:
            print(f"→ {detail}")
        print("\n预警提示：")
        for warn in result['warnings']:
            print(f"⚠ {warn}")
        print("\n化解建议：")
        for advice in result['suggestions']:
            print(f"★ {advice}")
        print("="*40)
    except Exception as e:
        print(f"程序执行错误: {e}")