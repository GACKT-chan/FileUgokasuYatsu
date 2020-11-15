#!/usr/local/bin/python3
# coding: utf-8

import shutil
import os
import re
from mutagen.easyid3 import EasyID3

before = "iTunes\iTunes Media\Music"
after = "mp3" #移動後のフォルダ
ext = ".mp3" #移動させたい拡張子
extension = ext.replace('.','')
tagID = "album" #フィルター
sl = "/"
tag = ""
counter = 0

for dir_name in os.listdir(before):
    #隠しフォルダを例外処理
    if dir_name == ".iTunes Preferences.plist":
        continue

    for dirin_name in os.listdir(before+sl+dir_name):
        for file_name in os.listdir(before+sl+dir_name+sl+dirin_name): 
            m = re.search(r'.*'+ext,file_name)
            if m != None:
                print(file_name)
                counter = counter + 1
                #ID3タグを取得
                tags = EasyID3(before+sl+dir_name+sl+dirin_name+sl+file_name)
                try:
                    #特定のタグを選択
                    tag = tags[tagID]
                except:
                    #アルバム名が存在しない場合
                    tag = "ER"
                #括弧を省く
                tagName = str(tag).replace('[\'','').replace('\']','')
                #フォルダ名に使えない文字を"_"に置き換え
                tagName = tagName.replace('/','_').replace('"','_').replace(':','_').replace('?','_').replace('<','_').replace('>','_').replace('|','_').replace('[_','').replace('_]','')
                #アルバム名のフォルダが無ければ作成
                if not os.path.isdir(after+sl+tagName):
                    os.makedirs(after+sl+tagName)
                #アルバム名のフォルダにファイルを移動
                try:
                    shutil.move(before+sl+dir_name+sl+dirin_name+sl+file_name, after+sl+tagName)
                except:
                    shutil.move(before+sl+dir_name+sl+dirin_name+sl+file_name, after+sl+"exists")

if counter == 0:
    print('There was no',extension,'files.')
elif counter == 1:
    print('1 file moved.')
else:
    print(counter,'files moved.')