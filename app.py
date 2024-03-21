import requests
import re
import os
from flask import Flask, render_template, request, jsonify, g

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

pan=['+-+-+', '*****', '*o+o*', '*+o+*', '*o+o*', '*****', '*@*@*', '*****', '*o+o*', '*+o+*', '*o+o*', '*****', '+-+-+']
bi=[[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,11,-2,11,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2],[-2,-2,-2,-2,-2]]
zhen=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
yuan=[[0,0,0,0,0],[0,0,0,0,0],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[0,0,0,0,0],[0,0,0,0,0]]
qi={'0':-2,'sl':8,'jz':7,'sz-1':6,'sz-2':6,'luz-1':5,'luz-2':5,'tz-1':4,'tz-2':4,'yz-1':3,'yz-2':3,'lz-1':2,'lz-2':2,'lz-3':2,'pz-1':1,'pz-2':1,'pz-3':1,'gb-1':0,'gb-2':0,'gb-3':0,'dl-1':9,'dl-2':9,'dl-3':9,'zd-1':10,'zd-2':10,'jq':-1}
mp=[]
tot=0
for i in range(50):mp=mp+[[]]
for i in range(13):
    for j in range(5):
        if yuan[i][j]==0:
            mp[tot].append(i)
            mp[tot].append(j)
            tot+=1
fx=[0,1,0,-1]
fy=[1,0,-1,0]
bai0=False
bai1=False
names=['工','排','连','营','团','旅','师','军','司','雷','炸','山','空','旗']
def abs(n):
    if n<0:return -n
    return n
def check1(x,y):
    if abs(x-y)<2:return True
    return False
def check2(a,b,c,d):
    if a==c:
        if abs(d-b)!=1:return False
        return True
    if d==b:
        if abs(a-c)!=1:return False
        return True
    return False
def cmp1(a,b):
    if b==-2:return 1
    if a==10 or b==10:return 0
    if a==0 and b==9:return 1
    if a>b:return 1
    if a<b:return 2
    if a==b:return 0
def baiqi0():
    if bi[0][1]!=-1 and bi[0][3]!=-1:return False
    for i in range(2,6,1):
        for j in range(5):
            if bi[i][j]==9:return False
    for i in range(5,6,1):
        for j in range(5):
            if bi[i][j]==10:return False
    for i in range(6):
        for j in range(5):
            if pan[i][j]=='o' and bi[i][j]!=-2:return False
    sums=0
    for i in range(6):
        for j in range(5):
            if bi[i][j]==-2:sums+=1
    if sums>5:return False
    global bai0
    bai0=True
    return True
def baiqi1():
    if bi[12][1]!=-1 and bi[12][3]!=-1:return False
    for i in range(7,11,1):
        for j in range(5):
            if bi[i][j]==9:return False
    for i in range(7,8,1):
        for j in range(5):
            if bi[i][j]==10:return False
    for i in range(7,13,1):
        for j in range(5):
            if pan[i][j]=='o' and bi[i][j]!=-2:return False
    sums=0
    for i in range(7,13,1):
        for j in range(5):
            if bi[i][j]==-2:sums+=1
    if sums>5:return False
    global bai1
    bai1=True
    return True
def insert(x,y,c,ids):
    global bi
    global zhen
    if ids=='0':bi[x][y]=qi[c]
    else:bi[12-x][y]=qi[c]
    zhen[x][y]=ids
vis=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
def DFS(x1,y1,x2,y2):
    if x1<0 or y1<0:return -1
    if x1>12 or y1>4:return -1
    if vis[x1][y1]==1:return -1
    if pan[x1][y1]!='*':return -1
    vis[x1][y1]=1
    if x1==x2 and y1==y2:return cmp1(bi[x1][y1],bi[x2][y2])
    for i in range(4):
        if DFS(x1+fx[i],y1+fy[i],x2,y2)!=-1:
            return DFS(x1+fx[i],y1+fy[i],x2,y2)
    return -1
def checks(x1,y1,x2,y2):
    if x1<0 or y1<0 or x2<0 or y2<0:return -1
    if x1>12 or y1>4 or x2>12 or y2>4:return -1
    if x2==6:return -1
    if pan[x1][y1]=='-':return -1
    if bi[x1][y1]==9 or bi[x1][y2]==-1:return -1
    if bi[x1][y1]==-2:return -1
    if zhen[x1][y1]==zhen[x2][y2]:return -1
    if pan[x2][y2]=='o' and bi[x2][y2]!=-2:return -1
    if x1==x2 and y1==y2:return -2
    if pan[x1][y1]=='o' or pan[x2][y2]=='o':
        if check1(x1,x2)==False or check1(y1,y2)==False:return -1
        return cmp1(bi[x1][y1],bi[x2][y2])
    if pan[x1][y1]=='+' or pan[x2][y2]=='+':
        if check2(x1,y1,x2,y2)==False:return -1
        return cmp1(bi[x1][y1],bi[x2][y2])
    if bi[x1][y1]==0:
        global vis
        vis=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        return DFS(x1,y1,x2,y2)
    if x1==x2:
        for i in range(min(y1,y2)+1,max(y1,y2),1):
            if bi[x1][i]!=-2:return -1
            if pan[x1][i]!='*':return -1
        return cmp1(bi[x1][y1],bi[x2][y2])
    if y1==y2:
        for i in range(min(x1,x2)+1,max(x1,x2),1):
            if bi[i][y1]!=-2:return -1
            if pan[i][y1]!='*':return -1
        return cmp1(bi[x1][y1],bi[x2][y2])
def move(x1,y1,x2,y2,a,b):
    k=checks(x1,y1,x2,y2)
    if k==-1 or k==-2:return k
    if k==0:
        bi[x1][y1]=-2
        bi[x2][y2]=-2
        zhen[x1][y1]=0
        zhen[x2][y2]=0
        mp[a]=[-1,-1]
        if b!=1:
            mp[b]=[-1,-1]
    if k==1:
        bi[x2][y2]=bi[x1][y1]
        bi[x1][y1]=-2
        zhen[x2][y2]=zhen[x1][y1]
        zhen[x1][y1]=0
        if b!=-1:
            mp[b]=[-1,-1]
        mp[a]=[x2,y2]
    if k==2:
        bi[x1][y1]=-2
        zhen[x1][y1]=0
        mp[a]=[-1,-1]
    return k
def printf():
    for i in range(13):
        for j in range(5):
            print(names[bi[i][j]],end=' ')
        print()

printf()

app = Flask(__name__)
@app.route("/")
def root():
    return render_template("index.html")

@app.route("/submit",methods=["POST"])
def submit():
    if request.method == "POST":
        ID = x0y0=request.form.get("id")
        x0y0=request.form.get("x0y0")
        x0y1=request.form.get("x0y1")
        x0y2=request.form.get("x0y2")
        x0y3=request.form.get("x0y3")
        x0y4=request.form.get("x0y4")
        x1y0=request.form.get("x1y0")
        x1y1=request.form.get("x1y1")
        x1y2=request.form.get("x1y2")
        x1y3=request.form.get("x1y3")
        x1y4=request.form.get("x1y4")
        x2y0=request.form.get("x2y0")
        x2y1=request.form.get("x2y1")
        x2y2=request.form.get("x2y2")
        x2y3=request.form.get("x2y3")
        x2y4=request.form.get("x2y4")
        x3y0=request.form.get("x3y0")
        x3y1=request.form.get("x3y1")
        x3y2=request.form.get("x3y2")
        x3y3=request.form.get("x3y3")
        x3y4=request.form.get("x3y4")
        x4y0=request.form.get("x4y0")
        x4y1=request.form.get("x4y1")
        x4y2=request.form.get("x4y2")
        x4y3=request.form.get("x4y3")
        x4y4=request.form.get("x4y4")
        x5y0=request.form.get("x5y0")
        x5y1=request.form.get("x5y1")
        x5y2=request.form.get("x5y2")
        x5y3=request.form.get("x5y3")
        x5y4=request.form.get("x5y4")
    insert(5,0,x0y0,ID)
    insert(5,1,x0y1,ID)
    insert(5,2,x0y2,ID)
    insert(5,3,x0y3,ID)
    insert(5,4,x0y4,ID)
    insert(4,0,x1y0,ID)
    insert(4,1,x1y1,ID)
    insert(4,2,x1y2,ID)
    insert(4,3,x1y3,ID)
    insert(4,4,x1y4,ID)
    insert(3,0,x2y0,ID)
    insert(3,1,x2y1,ID)
    insert(3,2,x2y2,ID)
    insert(3,3,x2y3,ID)
    insert(3,4,x2y4,ID)
    insert(2,0,x3y0,ID)
    insert(2,1,x3y1,ID)
    insert(2,2,x3y2,ID)
    insert(2,3,x3y3,ID)
    insert(2,4,x3y4,ID)
    insert(1,0,x4y0,ID)
    insert(1,1,x4y1,ID)
    insert(1,2,x4y2,ID)
    insert(1,3,x4y3,ID)
    insert(1,4,x4y4,ID)
    insert(0,0,x5y0,ID)
    insert(0,1,x5y1,ID)
    insert(0,2,x5y2,ID)
    insert(0,3,x5y3,ID)
    insert(0,4,x5y4,ID)

    printf()
    if ID == "0":
        return {'MMSG': baiqi0()}
    else:return {'MMSG': baiqi1()}
    
@app.route("/bq", methods=["POST"])
def bq():
    if request.method == "POST":
        id = request.form.get("id")
    print(str(bai0) + ' ' + str(bai1))
    if id == "0":
        return {'MMSG': bai1}
    return {'MMSG': bai0}

@app.route("/move", methods=["POST"])
def fuckintmove():
    if request.method == "POST":
        id = request.form.get("id")
        bh = int(request.form.get("bh"))
        x = int(request.form.get("x"))
        y = int(request.form.get("y"))
    print("bh " + str(bh))
    if id == "0":
        x = 11 - x
    if x >= 6:
        x = x + 1
    if id == "0":
        flag = move(mp[bh][0], 4 - mp[bh][1], x, y, bh, -1)
        print(mp[bh][0])
        print(4 - mp[bh][1])
        print(x)
        print(4 - y)
        print(bh)
        if flag == -1 or flag == -2:
            return {'MMSG': -1}
        return {'MMSG': 0}
    elif id == "1":
        flag = move(mp[24 - bh + 25][0], mp[24 - bh + 25][1], x, y, 24 - bh + 25, -1)
        if flag == -1 or flag == -2:
            return {'MMSG': -1}
        return {'MMSG': 0}
    return {'MMSG': -1}

# @app.route("/CJFJ", methods=["GET", "POST"])
# def CJFJ():
#     if request.method == "POST":
#         id = request.form.get("id")

#     print(id + ' 正在创建')

#     g.idtot += 1  # Use the shorthand increment operator

#     return render_template("index.html")


# @app.route("/JR", methods=["GET", "POST"])
# def JR():
#     if request.method == "POST":
#         id = request.form.get("id")
#     print(id)
#     return {'message':"1"}

app.run(host='0.0.0.0', port=8080)