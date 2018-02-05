#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pickle
global cat #种类
global order # 阶数
global disNum #不相交拉丁方个数
global outfile
clausN=0
global filename
def preprocess():
    Inline = raw_input("Please input the category, order and the number of disjoint IQ.\n（Example：LIQ(4)(9) want to find 6 disjoint IQs you can input:4 9 6\n")
    para = Inline.split(" ")
    cat = int(para[0])
    order = int(para[1])
    disNum = int(para[2])
    filename = "LIQ" + str(cat) + '_' + str(order) + ".cnf"
    outfile = open(filename, "wb")
    return filename,outfile, cat, order, disNum

def idempotent():
    global  clausN
    outfile.write("c 幂等性质\n")
    for i in range(0,disNum):
        for j in range(0,order):
            s1=alignstr(i+1)+alignstr(j)+alignstr(j)+alignstr(j)+" 0\n"
            s2=''
            for k in range(0,order):
                if k!=j:
                    s2=s2+"-"+alignstr(i+1)+alignstr(j)+alignstr(j)+alignstr(k)+" 0\n"
            outfile.write(s1)
            outfile.write(s2)
            clausN=clausN+order
    outfile.write("\n")

def dis_order():
    global clausN
    outfile.write("c 指定不相交拉丁方顺序（消除等价解）\n")
    for i in range(0, disNum):
        s1=alignstr(i+1)+alignstr(0)+alignstr(1)+alignstr(i+2)+" 0\n"
        s2=''
        for k in range(0,order):
            if k!=i+2:
                s2=s2+"-"+alignstr(i+1)+alignstr(0)+alignstr(1)+alignstr(k)+" 0\n"
        outfile.write(s1)
        outfile.write(s2)
        clausN = clausN + order
    outfile.write("\n")




def finitdomian():
    global clausN
    outfile.write("c 有限域的限定\n")
    for i in range(0,disNum):
        for x in range(0,order):
            for y in range(0,order):
                if x!=y:
                    if x==0 and y==1:
                        continue
                    s1=""
                    for v in range(0,order):
                        s1=s1+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v)+" "
                    s1=s1+"0\n"
                    outfile.write(s1)
                    clausN = clausN + 1
    outfile.write("\n")

def Lartin():
    global clausN
    outfile.write("c 拟群的性质（拉丁方性质）\n")
    # 行不等
    for i in range(0, disNum):
        for col in range(0, order):
            for row in range(0, order):
                if row==col:            #第一种情况 col==row对角线上元素
                    for j in range(col + 1, order):
                        s1="-"+alignstr(i+1)+alignstr(row)+alignstr(j)+alignstr(row)+" 0\n"
                        outfile.write(s1)
                        clausN = clausN + 1
                elif row==0 and col==1: #第二种情况f(0,1)
                    for j in range(col + 1, order):
                        s1="-"+alignstr(i+1)+alignstr(row)+alignstr(j)+alignstr(i+2)+" 0\n"
                        outfile.write(s1)
                        clausN = clausN + 1
                else:
                    for j in range(col + 1, order):
                        for v in range(0,order):
                            s1="-"+alignstr(i+1)+alignstr(row)+alignstr(col)+alignstr(v)+" -"+alignstr(i+1)+\
                               alignstr(row)+alignstr(j)+alignstr(v)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    #列不等
    for i in range(0,disNum):
        for row in range(0, order):
            for col in range(0, order):
                if row == col:  # 第一种情况 col==row对角线上元素
                    for j in range(row + 1, order):
                        s1="-"+alignstr(i+1)+alignstr(row)+alignstr(j)+alignstr(row)+" 0\n"
                        outfile.write(s1)
                        clausN = clausN + 1
                elif row==0 and col==1: #第二种情况f(0,1)
                    for j in range(row + 1, order):
                        s1 = "-" + alignstr(i + 1) + alignstr(j) + alignstr(col) + alignstr(i + 2) + " 0\n"
                        outfile.write(s1)
                        clausN = clausN + 1
                else:
                    for j in range(row + 1, order):
                        for v in range(0,order):
                            s1="-"+alignstr(i+1)+alignstr(row)+alignstr(col)+alignstr(v)+" -"+\
                               alignstr(i+1)+alignstr(j)+alignstr(col)+alignstr(v)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def IQproperty1():         #(assert (= (fi (fi x y) (fi y x)) x))
    global clausN
    outfile.write("c IQ的类别1性质\n")
    for i in range(0,disNum):
        for x in range(0,order):
            for y in range(0,order):
                if x!=y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if v1==v2 and x!=v1:
                                s1 = "-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i + 1) + alignstr(y) + alignstr(x) + \
                                     alignstr(v2) +" 0\n"
                            else:
                                s1="-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(y)+alignstr(x)+\
                                alignstr(v2)+" " +alignstr(i+1) + alignstr(v1) + alignstr(v2) + alignstr(x)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def IQproperty2():    #(assert (= (fi (fi y x) (fi x y)) x))
    global clausN
    outfile.write("c IQ的类别2性质\n")
    for i in range(0, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x!=y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if v1 == v2 and x != v1:
                                s1 = "-"+alignstr(i+1)+alignstr(y)+alignstr(x)+alignstr(v1)+" -"+alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v2) +" 0\n"
                            else:
                                s1="-"+alignstr(i+1)+alignstr(y)+alignstr(x)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v2)+" " +\
                                alignstr(i+1) + alignstr(v1) + alignstr(v2) + alignstr(x)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def IQproperty3():                               #fi(fi(fi(x,y),y),y)=x
    global clausN
    outfile.write("c IQ的类别3性质\n")
    for i in range(0,disNum):
        for x in range(0,order):
            for y in range(0,order):
                if x!=y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if v1==y and v2!=v1:
                                continue
                            elif v2==y :
                                s1 = "-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" 0\n"
                            else:

                                s1="-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" " +\
                                alignstr(i+1) + alignstr(v2) + alignstr(y) + alignstr(x)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")


def IQproperty4():  # (assert (= (fi x (fi x y)) (fi y x)))
    global clausN 
    outfile.write("c IQ的类别4性质\n")
    for i in range(0, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if x==v1 and v2!=v1:
							    continue
                            else:
                                s1="-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(x)+alignstr(v1)+alignstr(v2)+" " +\
                                alignstr(i+1) + alignstr(y) + alignstr(x) + alignstr(v2)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def IQproperty5():                  #(assert (= (fi (fi (fi y x) y) y) x))
    global clausN
    outfile.write("c IQ的类别5性质\n")
    for i in range(0, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if v1==y and v2!=v1:
                                continue
                            elif v2==y:
                                s1 = "-"+alignstr(i+1)+alignstr(y)+alignstr(x)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" 0\n"
                            else:
                                s1="-"+alignstr(i+1)+alignstr(y)+alignstr(x)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" " +\
                                alignstr(i+1) + alignstr(v2) + alignstr(y) + alignstr(x)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def IQproperty6():                 #(assert (= (fi (fi y x) y) (fi x (fi y x)))
    global clausN
    outfile.write("c IQ的类别6性质\n")
    for i in range(0, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if v1==y and v2!=v1:
                                continue
                            elif x==v1 and v2!=v1:
                                s1 ="-"+alignstr(i+1)+alignstr(y)+alignstr(x)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" 0\n"
                            else:
                                s1="-"+alignstr(i+1)+alignstr(y)+alignstr(x)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" " +\
                                alignstr(i+1) + alignstr(x) + alignstr(v1) + alignstr(v2)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def IQproperty7():                 #(assert (= (fi (fi x y) y) (fi x (fi x y)))
    global clausN
    outfile.write("c IQ的类别7性质\n")
    for i in range(0, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0,order):
                        for v2 in range(0,order):
                            if v1==y and v2!=v1:
                                continue
                            elif x==v1 and v2!=v1:
                                s1 ="-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" 0\n"
                            else:
                                s1="-"+alignstr(i+1)+alignstr(x)+alignstr(y)+alignstr(v1)+" -"+alignstr(i+1)+alignstr(v1)+alignstr(y)+alignstr(v2)+" " +\
                                alignstr(i+1) + alignstr(x) + alignstr(v1) + alignstr(v2)+" 0\n"
                            outfile.write(s1)
                            clausN = clausN + 1
    outfile.write("\n")

def Disjoint():                      #(assert (not (= (f1 i j) (f2 i j))))
    global clausN
    outfile.write("c不相交性质\n")
    for f1 in range(1,disNum+1):
        for f2 in range(f1+1,disNum+1):
            for i in range(0,order):
                for j in range(0,order):
                    if i==0 and j==1:
                        continue
                    if i!=j:
                        for v in range(0,order):
                            s1="-"+alignstr(f1)+alignstr(i)+alignstr(j)+alignstr(v)+" -"+alignstr(f2)+alignstr(i)+alignstr(j)+alignstr(v)+" 0\n"
                            outfile.write(s1)
                            clausN=clausN+1

def alignstr(number):
    if order < 11 :
        return str(number)
    else:
        if number >= 10:
            return str(number)
        if number < 10:
            return '0'+str(number)

def SATopt():
    linN=0
    optcode=1
    lineopt=''
    readfile=open(filename,"rb")
    ss=filename.split(".")
    optfilename=ss[0]+"_opt."+ss[1]
    optfile=open(optfilename,"wb")
    dic={}
    for i in range(0, disNum):
        for x in range(0, order):
            for y in range(0, order):
                for v in range(0, order):
                    key = alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v)
                    dic[key] = str(optcode)
                    optcode = optcode + 1
                    if key[0]=='0':
                        keyy=key[1:]
                        dic[keyy] = str(optcode)
    dicpath=ss[0]+".dic"
    dicfile=open(dicpath,"wb")
    pickle.dump(dic,dicfile)
    while 1:
        line = readfile.readline()
        if not line:
            break
        if line[0] == 'c':
            optfile.write(line)
        elif line=="\n":
            optfile.write(line)
        else:
            line = line.split(" ")
            lineopt = ''
            linN=linN+1
            for l in line:
                if l[0] == '-':
                    lineopt = lineopt + '-' + dic[l.split('-')[1]] + " "
                elif l[0]=='0' and l[1]=='\n':
                    lineopt = lineopt + l
                else:
                    lineopt = lineopt + dic[l] + " "
            optfile.write(lineopt)






if __name__=="__main__":
    filename,outfile,cat,order,disNum=preprocess()
    idempotent()
    dis_order()
    finitdomian()
    if cat==1:
        IQproperty1()
    elif cat==2:
        IQproperty2()
    elif cat==3:
        IQproperty3()
    elif cat==4:
        IQproperty4()
    elif cat==5:
        IQproperty5()
    elif cat==6:
        IQproperty6()
    elif cat==7:
        IQproperty7()
    else:
        print "cat erro!"
    Lartin()
    Disjoint()
    outfile.close()
    SATopt()
    print (order*order-order)*order+order," ",clausN
