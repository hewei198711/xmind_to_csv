# coding:utf-8

"""
    testideas_xmind_to_csv.py

    将测试用例xmind转换为禅道csv导入的格式

    :author: hewei
    :date created: 2022-04-20
    :python version: 3.8

    安装依赖：
        pip install xmindparser
    Usage:
        将xmind文件导出为csv文件:
        [cmd 命令]
        python testcase_xmind_to_csv.py xmind文件路径
"""

import sys
import os
import csv
from xmindparser import xmind_to_dict


def parser_tree_to_list(tree, onetitle, titlelist=[]):
    "把xmind tree遍历成初始数据,并放到list中"
    
    if isinstance(tree, dict):
        if len(tree) >= 2:
            parser_tree_to_list(tree['topics'], str(onetitle), titlelist)
        if len(tree) == 1:
            parser_tree_to_list(tree['title'],str(onetitle), titlelist)

    elif isinstance(tree, list):
            for sontree in tree:
                parser_tree_to_list(sontree, str(onetitle)  + "_" + sontree['title'], titlelist)

    elif isinstance(tree,str):
            titlelist.append((str(onetitle) ))
            
    return titlelist

    
def xmind_to_tree(path):
    "把xmind文件解析成python dict,并返回xmind tree, onetitle"
    
    xmind = xmind_to_dict(path)
    tree = xmind[0]['topic']
    onetitle = tree['title']
    
    return tree, onetitle


def titlelist_delete_onetitle(titlelist):
    "删除titlelist中每个title中的第一个字段"
    
    caselist = []
    for title in titlelist:
        index = title.find("_")
        title = title[index + 1:]
        caselist.append(title)
            
    return caselist


def find_step_and_expectation(caselist):
    "caselist 把测试步骤和期望拆解出来"
    
    # 把每条数据拆分成 标题 测试步骤 预期
    caselist02 = []
    for title in caselist:
        case = title.split("_")
        casetitle = "_".join(case[:-2])
        caselist02.append([casetitle, case[-2], case[-1]])
    
    # 把相同标题的数据中的 测试步骤 预期 合并, ['title', '步骤一\n步骤二', '预期一\n预期二']
    caselist03 = [] 
    if caselist03:
        title = caselist03[-1][0] 
    else:
        title = ""      
    for case in caselist02:
        if caselist03:
            if case[0] == title:
                caselist03[-1][1] += f"\n{case[1]}"
                caselist03[-1][2] += f"\n{case[2]}"
            else:
                caselist03.append(case)
                title = caselist03[-1][0]
        else:
            caselist03.append(case)
            title = caselist03[-1][0]
    
    return caselist03

        
def testcaselist(caselist):
    """
    ['title', '步骤一\n步骤二', '预期一\n预期二'] 
    调整成用例结构 
    ["所属模块", "相关需求", "优先级", "关键词", "前置条件","用例标题", "测试步骤", "预期结果"]
    
    """
    testcaselist = []
    for i in caselist:
        test = i[0].split("_")
        if i[0].find("_成功路径_") != -1:
            mudule = f'{i[0][:i[0].find("_成功路径_")]}'
            title = f'{i[0][:i[0].find("_成功路径_")+5]}: {test[-4]}'
        elif i[0].find("_失败路径_") != -1:
            mudule = f'{i[0][:i[0].find("_失败路径_")]}'
            title = f'{i[0][:i[0].find("_失败路径_")+5]}: {test[-4]}'
        else:
            raise Exception(f"{i[0]}: 没有找到对应的字段:成功路径&失败路径")
            
        testcaselist.append([mudule, "", test[-3], test[-2], test[-1], title, i[1], i[2]])
    
    return testcaselist
    
    
def to_csv(path, caselist):
    "导出csv文件,匹配禅道格式"
    
    csv_case_list = [[
        "所属模块", "相关需求", "优先级", "关键词", "前置条件",
        "用例标题", "步骤", "预期", "用例类型", "适用阶段"
    ]]
    for i in caselist:
        csv_case_list.append([
            i[0], 
            i[1], 
            i[2], 
            i[3],
            i[4], 
            i[5],
            i[6], 
            i[7], 
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
        caselist = titlelist_delete_onetitle(titlelist)
        caselist = find_step_and_expectation(caselist)
        caselist = testcaselist(caselist)
        to_csv(csv_path, caselist)
    else:
        raise Exception('测试用例xmind文件不存在:' + xmind_file)


