#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os

global cat  # 
global order  # 
global disNum  # 
global filename #LIQi_n.tal
global outfile   #cnf file


def alignstr(number):
    if order < 11:
        return str(number)
    else:
        if number >= 10:
            return str(number)
        if number < 10:
            return '0' + str(number)

def ReadTheFirst(Fnum):
    global filename
    firstfile = open(filename, "rb")
    lines = firstfile.readlines()
    row = 0
    firstL = []
    LatinG = []
    group = 0
    Latin = [['-1' for x in range(order)] for y in range(order)]
    for line in lines:
        if line.find("interpretation") != -1:
            continue
        if line.find("function") != -1:
            continue
        if line.find("%")!=-1:
            continue
        line = line.replace("])]).", ",")
        line = line.replace("]),", ",")
        line = line.replace(" ", "")
        line = line.split(",")
        for i in range(0, order):
            Latin[row][i] = line[i]
        row = (row + 1) % order
        if row == 0:
            LatinG.append(Latin)
            group = (group + 1) % Fnum
            if group == 0:
                firstL.append(LatinG)
                LatinG = []
            Latin = [['-1' for x in range(order)] for y in range(order)]
    return firstL

def writeFirst(number, firstL, Fnum):
    ss = "c " + "First " + str(Fnum) + " Lartin squares\n"
    outfile.write(ss)
    # print firstL[number]
    for fN in range(0, Fnum):
        for x in range(0, order):
            for y in range(0, order):
                s1 = alignstr(fN + 1) + alignstr(x) + alignstr(y) + alignstr(int(firstL[number][fN][x][y])) + " 0\n"
                outfile.write(s1)

def idempotent(Fnum):
    outfile.write("c Idempotent\n")
    for i in range(Fnum, disNum):
        for j in range(0, order):
            s1 = alignstr(i + 1) + alignstr(j) + alignstr(j) + alignstr(j) + " 0\n"
            s2 = ''
            for k in range(0, order):
                if k != j:
                    s2 = s2 + "-" + alignstr(i + 1) + alignstr(j) + alignstr(j) + alignstr(k) + " 0\n"
            outfile.write(s1)
            outfile.write(s2)
    outfile.write("\n")


def dis_order(Fnum):
    outfile.write("c add constrain\n")
    for i in range(Fnum, disNum):
        s1 = alignstr(i + 1) + alignstr(0) + alignstr(1) + alignstr(i + 2) + " 0\n"
        s2 = ''
        for k in range(0, order):
            if k != i + 2:
                s2 = s2 + "-" + alignstr(i + 1) + alignstr(0) + alignstr(1) + alignstr(k) + " 0\n"
        outfile.write(s1)
        outfile.write(s2)
    outfile.write("\n")


def finitdomian(Fnum):
    global clausN
    outfile.write("c finite domain\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    s1 = ""
                    for v in range(0, order):
                        s1 = s1 + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v) + " "
                    s1 = s1 + "0\n"
                    outfile.write(s1)
    outfile.write("\n")


def Lartin(Fnum):
    outfile.write("c quasigroup\n")
    # 行不等
    for i in range(Fnum, disNum):
        for col in range(0, order):
            for row in range(0, order):
                if row == col:  # 第一种情况 col==row对角线上元素
                    for j in range(col + 1, order):
                        s1 = "-" + alignstr(i + 1) + alignstr(row) + alignstr(j) + alignstr(row) + " 0\n"
                        outfile.write(s1)
                else:
                    for j in range(col + 1, order):
                        for v in range(0, order):
                            s1 = "-" + alignstr(i + 1) + alignstr(row) + alignstr(col) + alignstr(v) + " -" + alignstr(
                                i + 1) + \
                                 alignstr(row) + alignstr(j) + alignstr(v) + " 0\n"
                            outfile.write(s1)
    # 列不等
    for i in range(Fnum, disNum):
        for row in range(0, order):
            for col in range(0, order):
                if row == col:  # 第一种情况 col==row对角线上元素
                    for j in range(row + 1, order):
                        s1 = "-" + alignstr(i + 1) + alignstr(row) + alignstr(j) + alignstr(row) + " 0\n"
                        outfile.write(s1)
                else:
                    for j in range(row + 1, order):
                        for v in range(0, order):
                            s1 = "-" + alignstr(i + 1) + alignstr(row) + alignstr(col) + alignstr(v) + " -" + \
                                 alignstr(i + 1) + alignstr(j) + alignstr(col) + alignstr(v) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty1(Fnum):  # (assert (= (fi (fi x y) (fi y x)) x))
    outfile.write("c identity 1\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if v1 == v2 and x != v1:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(y) + alignstr(x) + \
                                     alignstr(v2) + " 0\n"
                            else:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(y) + alignstr(x) + \
                                     alignstr(v2) + " " + alignstr(i + 1) + alignstr(v1) + alignstr(v2) + alignstr(
                                    x) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty2(Fnum):  # (assert (= (fi (fi y x) (fi x y)) x))
    outfile.write("c identity 2\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if v1 == v2 and x != v1:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(y) + alignstr(x) + alignstr(v2) + " 0\n"
                            else:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(y) + alignstr(x) + alignstr(v2) + " " + \
                                     alignstr(i + 1) + alignstr(v2) + alignstr(v1) + alignstr(x) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty3(Fnum):  # fi(fi(fi(x,y),y),y)=x
    outfile.write("c identity 3\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if v1 == y and v2 != v1:
                                continue
                            elif v2 == y:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " 0\n"
                            else:

                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " " + \
                                     alignstr(i + 1) + alignstr(v2) + alignstr(y) + alignstr(x) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty4(Fnum):  # (assert (= (fi x (fi x y)) (fi y x)))
    outfile.write("c identity 4\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if x == v1 and v2 != v1:
                                continue
                            else:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(x) + alignstr(v1) + alignstr(v2) + " " + \
                                     alignstr(i + 1) + alignstr(y) + alignstr(x) + alignstr(v2) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty5(Fnum):  # (assert (= (fi (fi (fi y x) y) y) x))
    outfile.write("c identity 5\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if v1 == y and v2 != v1:
                                continue
                            elif v2 == y:
                                s1 = "-" + alignstr(i + 1) + alignstr(y) + alignstr(x) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " 0\n"
                            else:
                                s1 = "-" + alignstr(i + 1) + alignstr(y) + alignstr(x) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " " + \
                                     alignstr(i + 1) + alignstr(v2) + alignstr(y) + alignstr(x) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty6(Fnum):  # (assert (= (fi (fi y x) y) (fi x (fi y x)))
    outfile.write("c identity 6\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if v1 == y and v2 != v1:
                                continue
                            elif x == v1 and v2 != v1:
                                s1 = "-" + alignstr(i + 1) + alignstr(y) + alignstr(x) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " 0\n"
                            else:
                                s1 = "-" + alignstr(i + 1) + alignstr(y) + alignstr(x) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " " + \
                                     alignstr(i + 1) + alignstr(x) + alignstr(v1) + alignstr(v2) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def IQproperty7(Fnum):  # (assert (= (fi (fi x y) y) (fi x (fi x y)))
    outfile.write("c identity 7\n")
    for i in range(Fnum, disNum):
        for x in range(0, order):
            for y in range(0, order):
                if x != y:
                    for v1 in range(0, order):
                        for v2 in range(0, order):
                            if v1 == y and v2 != v1:
                                continue
                            elif x == v1 and v2 != v1:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " 0\n"
                            else:
                                s1 = "-" + alignstr(i + 1) + alignstr(x) + alignstr(y) + alignstr(v1) + " -" + alignstr(
                                    i + 1) + alignstr(v1) + alignstr(y) + alignstr(v2) + " " + \
                                     alignstr(i + 1) + alignstr(x) + alignstr(v1) + alignstr(v2) + " 0\n"
                            outfile.write(s1)
    outfile.write("\n")


def Disjoint():  # (assert (not (= (f1 i j) (f2 i j))))
    outfile.write("c disjoint\n")
    for f1 in range(1, disNum + 1):
        for f2 in range(f1 + 1, disNum + 1):
            for i in range(0, order):
                for j in range(0, order):
                    if i != j:
                        for v in range(0, order):
                            s1 = "-" + alignstr(f1) + alignstr(i) + alignstr(j) + alignstr(v) + " -" + alignstr(
                                f2) + alignstr(i) + alignstr(j) + alignstr(v) + " 0\n"
                            outfile.write(s1)

def GenCNF(CNFfileName,vtime,firstL,Fnum):
    global outfile
    outfile = open(CNFfileName, "wb")
    writeFirst(vtime, firstL, Fnum)
    idempotent(Fnum)
#    dis_order(Fnum)
    finitdomian(Fnum)
    if cat == 1:
        IQproperty1(Fnum)
    elif cat == 2:
        IQproperty2(Fnum)
    elif cat == 3:
        IQproperty3(Fnum)
    elif cat == 4:
        IQproperty4(Fnum)
    elif cat == 5:
        IQproperty5(Fnum)
    elif cat == 6:
        IQproperty6(Fnum)
    elif cat == 7:
        IQproperty7(Fnum)
    else:
        print "cat erro!"
    Lartin(Fnum)
    Disjoint()
    outfile.close()

if __name__=="__main__":
    type=sys.getfilesystemencoding()
    global filename
    global cat #
    global order # 
    global disNum
    vtime=0
    filename=sys.argv[1]
    cat=int(filename[3])
    order=int(filename.split("_")[1].split(".")[0])
    Fnum=int(filename.split("_")[1].split(".")[1].split("a")[1])
    max = Fnum
    outfilename="LIQ"+str(cat)+"_"+str(order)+".cnf"
    firstL=ReadTheFirst(Fnum)
    firstlen=len(firstL)
    print "#cat " + str(cat).decode('utf-8').encode(type)
    print "#order " + str(order).decode('utf-8').encode(type)
    print "#the total number of C("+str(cat)+")("+str(order)+"):" + str(firstlen).decode('utf-8').encode(type)

    for vtime in range(firstlen):
        print "============================================="
        print "For " + str(vtime) + "/" + str(firstlen - 1) + " of C"
        for disNum in range(Fnum + 1, order - 1):
            print "Try to find " + str(disNum) + " disjoint Lartin square..."
            GenCNF(outfilename, vtime, firstL, Fnum)
            exc = ".\/glucose -verb=0 -no-model " + outfilename + " > LIQ_result"
            os.system("%s" % exc)
            resultfile = open("LIQ_result", "rb")
            re = resultfile.readlines()
            if re[-1].find("s SATISFIABLE") != -1:
                if disNum > max:
                    max = disNum
                print "when l=" + str(disNum) + "   " + str(vtime) + "/" + str(firstlen - 1) + "：SAT"
                print "max="+str(max)
            if re[-1].find("s UNSATISFIABLE") != -1:
                print "when l=" + str(disNum) + "   " + str(vtime) + "/" + str(firstlen - 1) + "：UNSAT"
                break
        if max==order-2:
            print "The LIQ" + str(cat) + "_" + str(order) + " is EXISTENT"
            sys.exit()
    print "The LIQ"+str(cat)+"_"+str(order)+" is NONEXISTENT"
    print "The maxinum of disjoint IQ is max="+str(max)
