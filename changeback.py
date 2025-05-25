#부원중학교 2025학년도 10102 강태웅이 만들었습니다.

import re
import ctypes
import winreg as reg
from tkinter import *
from PIL import Image, ImageDraw, ImageFont
from pycomcigan import TimeTable
import os
from time import localtime
import datetime
import sys  #모듈(추가기능) 불러오기
day=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY',"MONDAY","MONDAY"] #요일 설정
ti=localtime()
t=Tk() 
t.geometry("800x800")
t.title("배경화면 자동 변경 프로그램")#여러가지 기능 초기화/설정
La1=Label(t, text="아래에 설정값을 입력한 뒤\n저장 버튼을 누르면\n설정값이 저장됩니다.\n(기본값:부원중 1-1)",font="맑은고딕 50")
La1.pack()
school=Label(t,text="컴시간 알리미에 등록된\n중학교 이름 입력",font="맑은고딕 20")
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
clsEn.pack() #GUI 세팅1
def savething():
    global scl,grd,cls
    scl=SclEn.get()
    grd=grdEn.get()
    cls=clsEn.get()
    file=open("saved.txt","w",encoding="ANSI")
    file.write(f"{scl}\n{grd}\n{cls}")
    file.close()
    update() #파일 저장 코드
savebu=Button(text="저장",font="맑은고딕 30",command=savething)
savebu.pack()
La2=Label(t,text="주의\n1.이 창을 끄면 시간표 새로고침이 종료됩니다.\n2.컴시간 알리미에 등록된 학교만 사용할 수 있습니다.",background="red",font="맑은고딕 25")
La2.pack() #GUI 세팅2
dow=day[ti.tm_wday]
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
try:
    os.system("del temp.jpg")
except: pass #오류 방지 코드(파일 경로 설정)
def deletetemp():
    os.system("del temp.jpg")
    update()
def update():
    try: #코드 예약 취소
        t.after_cancel(afterid)
    except: pass
    file=open("saved.txt","r",encoding="ANSI")
    listofthing=file.readlines()
    file.close()#설정값 읽기
    scl=listofthing[0].strip("\n")
    grd=listofthing[1].strip("\n")
    cls=listofthing[2].strip("\n")
    timetable = TimeTable(scl, week_num=0)
    tt = timetable.timetable[int(grd)][int(cls)][getattr(timetable, dow)]
    updatedtt=[] #정보 읽기 및 준비
    for i in range(0,len(tt)):
        editedtt=str(tt[i]).split("(")
        editedstrtt=str(editedtt[0].strip("\'"))
        updatedtt.append(editedstrtt)
    updatedtt=str(updatedtt)
    updatedtt = updatedtt.strip("[")
    updatedtt = updatedtt.strip("]")
    check = re.compile(r"'")
    while check.search(updatedtt):
        updatedtt = updatedtt.replace("'",'')
    updatedtt = " " + updatedtt
    updatedtt = updatedtt.replace(",","\n") #보기 편하게 변경
    img = Image.open("cloud.jpg")
    d = ImageDraw.Draw(img)
    fnt1 = ImageFont.truetype("Cafe24Ohsquare-v2.0.otf", 115)
    fnt2 = ImageFont.truetype("Cafe24Ohsquare-v2.0.otf", 90)
    now = datetime.datetime.now()
    date_str = now.strftime("%Y/%m/%d") #시간표 준비
    d.text((550,300), updatedtt, font=fnt1, fill=(0,0,0))
    d.text((1300,300), f"설정값 :\n{scl} {grd}학년 {cls}반\n\n오늘 날짜 :\n{date_str}\n\nMade by 2025학년도 강태웅", font=fnt2, fill=(0,0,0))
    img.save('temp.jpg') #이미지로 저장
    reg_path = r"Control Panel\Desktop"
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_path, 0, reg.KEY_WRITE)
    reg.SetValueEx(key, "WallpaperStyle", 0, reg.REG_SZ, "0")
    reg.SetValueEx(key, "TileWallpaper", 0, reg.REG_SZ, "0")
    key.Close()
    reg_path2=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    key=reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path2, 0, ) 
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{current_dir}\\temp.jpg" , 3) #바탕화면으로 설정
    afterid = t.after(600000, deletetemp) #1초=1000, 10분=600초, 600초=600000
update() #기능 실행 코드 정의/실행
t.mainloop() #코드 계속 반복

#부원중학교 2025학년도 10102 강태웅이 만들었습니다.