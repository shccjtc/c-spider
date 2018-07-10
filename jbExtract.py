# _*_ coding:utf-8 _*_

from os import path
import time
import os
import sys
import jieba
import jieba.analyse as analyse

rt=path.dirname(__file__)
d = rt +'\spider'
stopwords_path='./stopwords.txt'

# dd=d+'\A.txt'
# open(dd,'w').write('abc')


# print('rootfile'+sd)


def jiebaclearText(text):
    '''删除停止符'''
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read( )
    finally:
        f_stop.close( )
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)


def extract_filename(d):   
    '''提取爬出的txt数据'''
    L=[]   
    for root, dirs, files in os.walk(d): 
        # print(root)
        # print(dirs)
        # print(files) 
        for file in files:  
            if os.path.splitext(file)[1] == '.txt':  
                L.append(os.path.join(root, file))  
    return L

def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False


L=extract_filename(d)
direct='var dir=['
for p in L:
    direct+='{'
    text = open(p,encoding='UTF-8').read()
    seg_list=jieba.cut(text)
    wl_space_split=' '.join(seg_list)
    wl_space_split='var segment="'+jiebaclearText(wl_space_split)+'"'

    s='var keywords=['
    for key in analyse.extract_tags(text,20, withWeight=False):
        s+='"'+key+'",'
    s=s[:-1]+']'
    
    fw=p.replace('spider','output')
    fwlist=fw.split('\\')
    fw=''

    for part in fwlist:
        if os.path.splitext(part)[1] != '.txt':
            fw+=part
            print(part)
            if is_valid_date(part):
                direct+='"date":"'+part+'"'
            # print(fw)
            isExists=os.path.exists(fw)
            if not isExists:
                os.makedirs(fw)
            
            fw+='\\'
        else:
            direct+=',"title":"'+os.path.splitext(part)[0]+'"'
            fw+=part
            # print(fw)
    parent_path=path.dirname(fw)
    parent_path+='/direct.txt'
    fw1=os.path.splitext(fw)[0]+'_keywords.txt'
    fw2=os.path.splitext(fw)[0]+'_segment.txt'

    open(fw1,'w',encoding='utf-8').write(s)
    open(fw2,'w',encoding='utf-8').write(wl_space_split)
    direct+='},'
direct=direct[:-1]+']'
print(direct)
fdir=rt+'/index.txt'
open(fdir,'w',encoding='utf-8').write(direct)



# for key in analyse.textrank(text,20,False):
    # print(key)