import ctypes
import winreg as reg
from tkinter import *
from PIL import Image, ImageDraw, ImageFont
from pycomcigan import TimeTable
import os
from time import localtime
import datetime
import sys
day=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY',"MONDAY","MONDAY"]
ti=localtime()
t=Tk()
t.geometry("800x800")
t.title("배경화면 자동 변경 프로그램")
La1=Label(t, text="아래에 설정값을 입력하면\n기준이 바뀝니다.\n기본값은 부원중학교\n1학년 1반입니다.",font="맑은고딕 50")
La1.pack()
school=Label(t,text="중학교(풀네임) 입력",font="맑은고딕 20")
SclEn=Entry(font="맑은고딕 30")
school.pack()
SclEn.pack()
grade=Label(t,text="학년 입력(숫자만)",font="맑은고딕 20")
grdEn=Entry(font="맑은고딕 30")
grade.pack()
grdEn.pack()
classnum=Label(t,text="반 입력(숫자만)",font="맑은고딕 20")
clsEn=Entry(font="맑은고딕 30")
classnum.pack()
clsEn.pack()
def savething():
    global scl,grd,cls
    scl=SclEn.get()
    grd=grdEn.get()
    cls=clsEn.get()
    file=open("saved.txt","w",encoding="ANSI")
    file.write(f"{scl}\n{grd}\n{cls}")
    file.close()
    update()
savebu=Button(text="저장",font="맑은고딕 30",command=savething)
savebu.pack()
La2=Label(t,text="주의 : 이 창을 끄면\n프로그램이 종료됩니다.\n(10분 자동 새로고침 꺼짐)",background="red",font="맑은고딕 30")
La2.pack()
dow=day[ti.tm_wday]
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
try:
    os.system("del temp.jpg")
except: pass
def deletetemp():
    os.system("del temp.jpg")
    update()
def update():
    try:
        t.after_cancel(afterid)
    except: pass
    file=open("saved.txt","r",encoding="ANSI")
    listofthing=file.readlines()
    file.close()
    scl=listofthing[0].strip("\n")
    grd=listofthing[1].strip("\n")
    cls=listofthing[2].strip("\n")
    timetable = TimeTable(scl, week_num=0)
    tt = str(timetable.timetable[int(grd)][int(cls)][getattr(timetable, dow)])
    tt = tt.strip("[")
    tt = tt.strip("]")
    tt = " " + tt
    tt = tt.replace(",","\n")
    img = Image.open("cloud.jpg")
    d = ImageDraw.Draw(img)
    fnt1 = ImageFont.truetype("Cafe24Ohsquare-v2.0.otf", 70)
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y/%m/%d")
    d.text((1520,400), tt, font=fnt1, fill=(0,0,0))
    d.text((1520,1050), f"기준 : {scl} {grd}학년 {cls}반\n         {date_str}\n           {time_str}", font=fnt1, fill=(0,0,0))
    img.save('temp.jpg')
    reg_path = r"Control Panel\Desktop"
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_path, 0, reg.KEY_WRITE)
    reg.SetValueEx(key, "WallpaperStyle", 0, reg.REG_SZ, "0")
    reg.SetValueEx(key, "TileWallpaper", 0, reg.REG_SZ, "0")
    key.Close()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{current_dir}\\temp.jpg" , 3)
    afterid = t.after(1000, deletetemp) #1초=1000, 10분=600초, 600초=600000
update()
t.mainloop()