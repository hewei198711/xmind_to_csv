# coding:utf-8

"""
    testideas_xmind_to_csv.py

    将测试思路xmind转换为禅道csv导入的格式

    :author: hewei
    :date created: 2022-04-20
    :python version: 3.8

    安装依赖：
        pip install xmindparser
    Usage:
        将xmind文件导出为csv文件:
        [cmd 命令]
        python testideas_xmind_to_csv.py xmind文件路径
    
    xmind格式要求:
        所有字段中不允许有下划线 _
"""

import sys
import os
import csv
from xmindparser import xmind_to_dict


def parser_tree_to_list(tree, onetitle, titlelist=[]):
    "把xmind tree遍历成初始数据,并放到list中"
    
    if isinstance(tree, dict):
        if len(tree) >= 2:
            parser_tree_to_list(tree['topics'], str(onetitle).strip(), titlelist)
        if len(tree) == 1:
            parser_tree_to_list(tree['title'],str(onetitle).strip(), titlelist)

    elif isinstance(tree, list):
            for sontree in tree:
                parser_tree_to_list(sontree, str(onetitle).strip()  + "_" + sontree['title'].strip(), titlelist)

    elif isinstance(tree,str):
            titlelist.append((str(onetitle).strip()))
            
    return titlelist

    
def xmind_to_tree(path):
    "把xmind文件解析成python dict,并返回xmind tree, onetitle"
    
    xmind = xmind_to_dict(path)
    tree = xmind[0]['topic']
    onetitle = tree['title']
    
    return tree, onetitle


def titlelist_to_caselist(titlelist):
    "titlelist列表由[title1, title2****]转成[('title1', 'p1', '测试步骤'),('title2', 'p3', '测试步骤')]"
    
    caselist = []
    for title in titlelist:
        if title.lower().find("p") != -1 and title[title.lower().find("p")+1] in ["1", "2", "3"]:
            caselist.append((
                title, # 用例标题
                title[title.lower().find("p"):title.lower().find("p") +2], # 用例级别
                title[title.lower().find("p")+3:], # 测试步骤
                ))
        else:
            caselist.append((title, "p2", title))
            
    return caselist
    

def to_csv(path, caselist):
    "导出csv文件,匹配禅道格式"
    
    csv_case_list = [[
        "所属模块", "相关需求", "优先级", "关键词", "前置条件",
        "用例标题", "步骤", "预期", "用例类型", "适用阶段"
    ]]
    for i in caselist:
        csv_case_list.append([
            "请填写所属模块", 
            "", 
            i[1], 
            "v3.2.0",
            "", 
            i[0],
            i[2], 
            "检查正确", 
            "功能测试", 
            "功能测试阶段"])
    
    # 将用例写入csv文件
    with open(path, 'w', newline='', encoding='gbk') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_case_list)
        print('用例xmind已成功导出为csv文件,请根据禅道模块处理所属模块')
    

if __name__ == "__main__":
    xmind_file = sys.argv[1]
    csv_path = f"{xmind_file[:-6]}.csv"
    if xmind_file[-6:] == '.xmind' and os.path.exists(xmind_file):  # 判断文件存在，格式是Xmind
        
        tree, onetitle = xmind_to_tree(xmind_file)
        titlelist = parser_tree_to_list(tree, onetitle)
        caselist = titlelist_to_caselist(titlelist)
        to_csv(csv_path, caselist)
    else:
        print('测试思路xmind文件不存在:' + xmind_file)
        exit(0)
