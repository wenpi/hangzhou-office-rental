#!/usr/bin/env python3
"""
线索监控脚本 - 搜索小红书/抖音/微博关键词，整理潜在客户线索
使用方式: python3 lead_monitor.py
结果保存到 leads/leads_YYYYMMDD.csv
"""

import json
import csv
import os
from datetime import datetime

# ===== 监控关键词配置 =====
KEYWORDS = [
    # 临平区
    "临平 办公室 求租", "临平 工位 找", "临平 办公场地",
    "临平区 创业 办公", "临平 联合办公", "临平 写字楼 租",
    # 拱墅区
    "拱墅 办公室 求租", "拱墅 工位 找", "拱墅区 办公场地",
    "拱墅 创业 办公", "崇贤 办公室", "星云城 办公",
    # 通用
    "杭州北 办公室 求租", "余杭 办公室 找", "杭州 联合办公 求推荐",
]

# ===== 搜索平台入口（手动搜索链接）=====
SEARCH_URLS = {
    "小红书": "https://www.xiaohongshu.com/search_result?keyword={keyword}",
    "抖音": "https://www.douyin.com/search/{keyword}",
    "微博": "https://s.weibo.com/weibo?q={keyword}&typeall=1&suball=1&timescope=custom:2025-01-01:2025-12-31",
    "百度贴吧": "https://tieba.baidu.com/f/search/res?qw={keyword}",
}

# ===== 回复话术模板 =====
REPLY_TEMPLATES = {
    "通用": """您好！看到您在找办公场地，我们在临平区和拱墅区有多个优质园区可以推荐：
🏢 丁兰数创智慧谷（临平区）- 适合科技/电商类企业
🌟 星云城（拱墅区）- 商业综合体，配套成熟
🏙️ 崇贤社区（拱墅区）- 性价比高，仓储+办公一体
独立办公室/工位均有，可注册地址，拎包入驻。
有需要可以联系我：18868807854（微信同号）""",

    "临平": """您好！看到您在找临平区的办公场地，我们正好在临平区有优质资源：
🏢 丁兰数创智慧谷 - 数字经济产业园，科技感十足
✅ 独立办公室/工位均有
✅ 可注册地址，拎包入驻
✅ 园区直租，无中介费
欢迎来看看，联系我：18868807854（微信同号）""",

    "拱墅": """您好！看到您在找拱墅区的办公场地，我们在拱墅有两个园区：
🌟 星云城 - 商业综合体，交通便利
🏙️ 崇贤社区 - 性价比高，仓储+办公可选
✅ 多种面积可选，灵活租期
✅ 可注册地址，园区直租
欢迎来看看，联系我：18868807854（微信同号）""",

    "初创/工作室": """您好！看到您在找办公场地，我们特别适合初创团队：
💰 价格实惠，短租3个月起
🚀 拎包入驻，当天可用
📋 可提供工商注册地址
📍 临平区/拱墅区均有房源
欢迎来实地看看，联系我：18868807854（微信同号）""",
}


def generate_search_links():
    """生成今日搜索链接清单"""
    today = datetime.now().strftime("%Y-%m-%d")
    output = [f"# 线索搜索清单 - {today}\n"]
    output.append("## 操作步骤")
    output.append("1. 逐个点击下方链接")
    output.append("2. 找到有效线索后，填入下方CSV模板")
    output.append("3. 根据线索类型选择对应话术回复\n")

    for platform, url_template in SEARCH_URLS.items():
        output.append(f"\n## {platform}")
        for kw in KEYWORDS[:5]:  # 每平台展示前5个关键词
            url = url_template.format(keyword=kw.replace(" ", "+"))
            output.append(f"- [{kw}]({url})")

    return "\n".join(output)


def save_leads_template():
    """创建线索记录CSV模板"""
    os.makedirs("leads", exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filepath = f"leads/leads_{today}.csv"

    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "日期", "平台", "帖子链接", "用户名", "需求描述",
                "面积需求", "预算", "区域偏好", "联系方式",
                "使用话术", "跟进状态", "备注"
            ])
            # 示例行
            writer.writerow([
                today, "小红书", "https://...", "@用户名",
                "找临平区10人左右的独立办公室",
                "50-80㎡", "5000-8000/月", "临平区",
                "私信中", "临平话术", "待跟进", ""
            ])
        print(f"✅ 线索表已创建: {filepath}")
    else:
        print(f"📋 线索表已存在: {filepath}")

    return filepath


def print_reply_templates():
    """打印所有话术模板"""
    print("\n" + "="*50)
    print("📝 回复话术库")
    print("="*50)
    for name, template in REPLY_TEMPLATES.items():
        print(f"\n【{name}话术】")
        print(template)
        print("-"*40)


if __name__ == "__main__":
    print("🔍 线索监控工具启动")
    print(f"📅 今日日期: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"🎯 监控关键词: {len(KEYWORDS)} 个\n")

    # 生成搜索链接
    links_md = generate_search_links()
    os.makedirs("leads", exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    links_file = f"leads/search_links_{today}.md"
    with open(links_file, "w", encoding="utf-8") as f:
        f.write(links_md)
    print(f"✅ 搜索链接已生成: {links_file}")

    # 创建线索记录表
    leads_file = save_leads_template()

    # 打印话术
    print_reply_templates()

    print("\n" + "="*50)
    print("📌 今日操作指引")
    print("="*50)
    print(f"1. 打开搜索链接文件: {links_file}")
    print("2. 逐个平台搜索关键词，找到求租帖子")
    print("3. 将有效线索填入: {leads_file}")
    print("4. 根据线索类型选择话术，手动回复帖子")
    print("5. 更新跟进状态")
    print("\n💡 提示: 每天花30-60分钟操作，预计可找到5-15条有效线索")
