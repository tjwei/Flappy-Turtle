'''
============
中文程式翻譯
============

 flappybird.py (English) ==> ryFlappybird.py (almost Chinese)

 呂仁園， Renyuan Lyu 2014/05/26

 使用 中文龜模組 turtle_tc.py

 https://github.com/renyuanL/pythonTurtleInChinese/blob/master/turtle_tc.py
 
 renyuan.lyu@gmail.com
 http://google.com/+RenyuanLyu
 
'''
#
# Original program from
#
# Author: tjw (https://github.com/tjwei/Flappy-Turtle)
# Welcome to PyCon APAC 2014/Taiwan!
# More info on https://tw.pycon.org/2014apac/
#


from turtle_tc import *

#
# Python 3 關鍵字全數保留 (約30個 簡單英文字)，不翻。
#

#
# 簡短 暫時性變數 (如 n, i, t, x, y, z) ， 不翻。
#

#
#
#

from subprocess import Popen
import sys
import glob

#
# 借助外部程式 mplayer.exe 來放音。
#
# 要提供給 它 指令， 透過 Popen 來呼叫。
#
def 放音(音名, 音量=10):

    檔名 = 音名 + ".mp3"
    指令 = ["mplayer", "-softvol", "-really-quiet", "-volume", str(音量), 檔名]

    try:
        print(指令)
        #Popen(指令)
    except:
        pass

開幕()

重設幕大小(216, 500)
設立(288, 512)
追蹤器(False, 0)
藏龜()

[加形狀(f) for f in glob.glob("*.gif")]

字型名=    "Comic Sans MS"
速度x=     100
地線=     -200 + 56 + 12
水管距=    230
背景寬=    286

def 文字龜(x, y, 色):

    龜= 龜類()

    龜.藏龜()
    龜.提筆()
    龜.前往(x, y)
    龜.速度(0)
    龜.顏色(色)

    return 龜

def 圖畫龜(檔名):

    龜= 龜類(檔名 + ".gif")
    龜.速度(0)
    龜.提筆()

    return 龜

分數龜=        文字龜( 0,  130, 黃)
最佳分數龜=    文字龜(90,  180, 紅)
廣告龜=        文字龜( 0, -270, 藍)

水管群=       [(圖畫龜("tube1"), 圖畫龜("tube2")) for i in 範圍(3)]
地群=         [圖畫龜("ground") for i in 範圍(3)]
鳥=            圖畫龜("bird1")

背景圖("bg1.gif")

廣告詞= '''更多好玩的在
PyCon 亞太
2014/台灣
'''

標題(廣告詞)

class 遊戲類:

    狀態= "結束"
    分數= 最佳分數 = 0

遊戲= 遊戲類()

def 開始遊戲(遊戲):

    遊戲.最佳分數 = max(遊戲.分數, 遊戲.最佳分數)
    遊戲.水管群y = [10000] * 3
    遊戲.撞擊t, 遊戲.撞擊y = 0, 0
    遊戲.狀態 = "活著"
    遊戲.水管底 = 0
    遊戲.分數 = 0
    遊戲.開始時間= 時間()
    廣告龜.清除()
    更新遊戲(遊戲)

def 計算y(t, 遊戲):

    return 遊戲.撞擊y - 100 * (t - 遊戲.撞擊t) * (t - 遊戲.撞擊t - 1)


def 更新遊戲(遊戲):

    if 遊戲.狀態 == "死亡":

        放音("clickclick")

        廣告龜.寫(
              廣告詞,
              align="center",
              font=(字型名, 24, "bold")
              )
        睡(2)
        遊戲.狀態 = "結束"
        return

    t= 時間() - 遊戲.開始時間

    鳥y= 計算y(t, 遊戲)

    if 鳥y <= 地線:

        鳥y= 地線
        遊戲.狀態= "死亡"

    x= int(t * 速度x)

    水管底= -(x % 水管距) - 40

    if 遊戲.水管底 < 水管底:

        if 遊戲.水管群y[2] < 1000:

            遊戲.分數 += 1
            放音("bip")

        遊戲.水管群y = 遊戲.水管群y[1:] + [隨機整數(-100, 50)]

    遊戲.水管底= 水管底

    for i in 範圍(3):

        水管群[i][0].前往(
            水管底 + 水管距 * (i - 1), 250 + 遊戲.水管群y[i])
        水管群[i][1].前往(
            水管底 + 水管距 * (i - 1), -150 + 遊戲.水管群y[i])

    if 遊戲.水管群y[2] < 1000:

        水管左= 水管底 + 水管距 - 28
        水管右= 水管底 + 水管距 + 28
        水管上= 遊戲.水管群y[2] + 250 - 160
        水管下= 遊戲.水管群y[2] - 150 + 160

        中心= Vec2D(0, 鳥y - 2)
        左端= Vec2D(水管左, 水管上) - 中心
        右端= Vec2D(水管右, 水管上) - 中心

        if (水管左 < 18 and 水管右 > -18) and 鳥y - 12 <= 水管下:
            遊戲.狀態 = "死亡"

        if (水管左 <= 8 and 水管右 >= -8) and 鳥y + 12 >= 水管上:
            遊戲.狀態 = "死亡"

        if abs(左端) < 14 or abs(右端) < 14:
            遊戲.狀態 = "死亡"

    背景底= -(x % 背景寬)

    for i in 範圍(3):

        地群[i].前往(背景底 + 背景寬 * (i - 1), -200)

    鳥.形狀("bird%d.gif" % abs(int(t * 4) % 4 - 1))

    鳥.前往(0, 鳥y)

    分數龜.清除()

    分數龜.寫(
          "%s" % (遊戲.分數),
          align="center",
          font=(字型名, 80, "bold")
          )

    if 遊戲.最佳分數:

        最佳分數龜.清除()

        最佳分數龜.寫(
                '''最佳分數:
                %d''' % (遊戲.最佳分數),
                align= "center",
                font= (字型名, 14, "bold")
                )

    更新畫面()

    在計時器若干毫秒之後(lambda: 更新遊戲(遊戲), 10)


def 飛(遊戲=遊戲):

    if 遊戲.狀態 == "結束":

        開始遊戲(遊戲)
        return

    t = 時間() - 遊戲.開始時間

    鳥y= 計算y(t, 遊戲)

    if 鳥y > 地線:

        遊戲.撞擊t, 遊戲.撞擊y= t, 鳥y
        #放音("tack", 10)

在按鍵時(飛, 空白鍵)

聽鍵盤()

進入主迴圈()

sys.exit(1)

