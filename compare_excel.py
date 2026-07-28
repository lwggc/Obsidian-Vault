# -*- coding: utf-8 -*-
"""Analyze the 408 Excel file and compare with my notes."""
import json, re, sys, os

# Load Excel dump
with open('excel_dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load my 408 summary as reference
with open('408总结.md', 'r', encoding='utf-8') as f:
    summary = f.read()

# Load my detailed notes
my_notes = {}
for fname in ['数据结构27重新起航.md', '操作系统27重新起航.md', '计组27重新起航.md', '计网27重新起航.md']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove image links for cleaner analysis
            content_no_img = re.sub(r'!\[\[.*?\]\]', '', content)
            content_no_img = re.sub(r'!\[.*?\]\(.*?\)', '', content_no_img)
            my_notes[fname] = content_no_img
    except:
        pass

# Categorize
categories = {}
for item in data:
    cat = item['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(item)

print("=" * 80)
print("408笔记对比分析")
print("=" * 80)

# For each subject, do keyword matching
def search_in_notes(keywords, notes_text):
    """Search for keywords in notes and return matching sentences."""
    results = []
    for kw in keywords:
        if not kw or len(kw) < 2:
            continue
        # Find matching lines
        lines = notes_text.split('\n')
        for i, line in enumerate(lines):
            if kw.lower() in line.lower():
                # Get context
                start = max(0, i-1)
                end = min(len(lines), i+2)
                context = '\n'.join(lines[start:end])
                if context not in results:
                    results.append(context.strip())
    return results[:5]

subject_config = {
    'ds': {
        'name': '数据结构',
        'file': '数据结构27重新起航.md',
        'keywords': ['时间复杂度', '空间复杂度', '顺序表', '链表', '栈', '队列',
                    '树', '二叉树', '图', '查找', '排序', 'B树', 'B+树', '哈希',
                    '散列', '堆', '红黑树', '平衡二叉树', 'AVL', '关键路径',
                    '拓扑', 'KMP', '串', '矩阵', '哈夫曼', '并查集']
    },
    '计组': {
        'name': '计算机组成原理',
        'file': '计组27重新起航.md',
        'keywords': ['IEEE754', '补码', '浮点数', 'Cache', 'DRAM', 'SRAM',
                    'ALU', '控制器', '微程序', 'DMA', '中断', '流水线',
                    '主存', '磁盘', 'RAID', 'CPU', '指令', '寻址', 'RISC', 'CISC']
    },
    'OS': {
        'name': '操作系统',
        'file': '操作系统27重新起航.md',
        'keywords': ['进程', '线程', '调度', '同步', '互斥', '死锁', '信号量',
                    '内存', '分页', '分段', '虚拟内存', '页面置换', '文件',
                    '磁盘', 'I/O', 'PV', '管程', '银行家', 'PCB', 'TLB']
    },
    'CN': {
        'name': '计算机网络',
        'file': '计网27重新起航.md',
        'keywords': ['TCP', 'UDP', 'IP', '路由', 'OSPF', 'RIP', 'BGP',
                    '以太网', '交换机', 'CSMA', 'HTTP', 'DNS', 'DHCP',
                    'ARP', 'ICMP', 'VLAN', 'NAT', 'CIDR', 'MAC', '拥塞',
                    '慢开始', '拥塞避免', '流量控制', '滑动窗口']
    },
    '计网': {
        'name': '计算机网络',
        'file': '计网27重新起航.md',
        'keywords': ['TCP', 'UDP', 'IP', '路由', 'OSPF', 'RIP', 'BGP']
    }
}

for cat, config in subject_config.items():
    if cat not in categories:
        continue
    cards = categories[cat]
    print(f"\n{'=' * 80}")
    print(f"Category: {config['name']} ({cat}) - {len(cards)} cards")
    print('=' * 80)

    notes_content = my_notes.get(config['file'], '')

    # Also search in summary
    combined_notes = notes_content + '\n' + summary

    # Sample some cards and look up in notes
    sample_count = min(50, len(cards))
    issues_found = 0

    for i, card in enumerate(cards):
        q = card['question'][:100]
        a = card['answer'][:200]

        # Extract key terms from question
        # Remove special markers like [F##...]
        clean_q = re.sub(r'\[F##.*?\]', '', q)
        # Extract meaningful keywords
        words = re.findall(r'[一-龥a-zA-Z]{2,}', clean_q)
        main_keywords = words[:5] if len(words) > 5 else words

        # Search in my notes
        matches = search_in_notes(main_keywords, combined_notes)

        if matches and i < sample_count:
            print(f"\n  --- Card {i+1} ---")
            print(f"  Q: {q[:80]}...")
            print(f"  A: {a[:100]}...")
            print(f"  My notes found: {len(matches)} matching section(s)")
            for m in matches[:2]:
                print(f"    > {m[:120]}")

print("\n\nDone with initial comparison.")
