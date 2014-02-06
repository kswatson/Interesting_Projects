import math
import sys
from datetime import datetime

class Space:
    def __init__(self,var):
        self.v = var
        self.D = [1,2,3,4,5,6,7,8,9]

def setDomains(V,E):
    for e in E:
        row = e[0]
        column = e[1]
        '''--Check row--'''
        for col in range(9):
            if (V[row][col].v > 0 and V[row][column].D.count(V[row][col].v) > 0):
                V[row][column].D.remove(V[row][col].v)
               
        '''--Check column--'''
        for r in range(9):
            if(V[r][column].v > 0 and V[row][column].D.count(V[r][column].v) > 0):
                V[row][column].D.remove(V[r][column].v)
                
        '''--Check region--'''
        for Crow in getRegion(int(row/3),int(column/3)):
            for Ccol in Crow:
                r = Ccol[0]
                c = Ccol[1]
                if(V[r][c].v > 0 and V[row][column].D.count(V[r][c].v) > 0):
                    V[row][column].D.remove(V[r][c].v)
        
def getRegion(row, column):
    return[[[row*3,column*3], [row*3,column*3+1], [row*3,column*3+2]],
           [[row*3+1,column*3], [row*3+1,column*3+1], [row*3+1,column*3+2]],
           [[row*3+2,column*3], [row*3+2,column*3+1], [row*3+2,column*3+2]]]
    
def consistent (row, column, var, V):
    '''--Check row--'''
    for Vcolumn in V[row]:
        if (Vcolumn.v == var):
            return False
            
    '''--Check column--'''
    for i in range(9):
        if(V[i][column].v == var):
            return False
    '''--Check region--'''
    
    for Crow in getRegion(int(row/3),int(column/3)):
        for Ccol in Crow:
            if(V[Ccol[0]][Ccol[1]].v == var):
                return False
    
    return True

def forwardCheck (row, column, var, V):
    checkedSpaces = []
    '''--Check row--'''
    for col in range(9):
        if (V[row][col].v == 0 and V[row][col].D.count(var) > 0):
            V[row][col].D.remove(var)
            checkedSpaces.append([row,col])
            if(len(V[row][col].D) == 0):
                for checkedSpace in checkedSpaces:
                    V[checkedSpace[0]][checkedSpace[1]].D.append(var)
                return [-1]
    '''--Check column--'''
    for r in range(9):
        if(V[r][column].v == 0 and V[r][column].D.count(var) > 0):
            V[r][column].D.remove(var)
            checkedSpaces.append([r,column])
            if(len(V[r][column].D) == 0):
                for checkedSpace in checkedSpaces:
                    V[checkedSpace[0]][checkedSpace[1]].D.append(var)
                return [-1]
            
    '''--Check region--'''
    for Crow in getRegion(int(row/3),int(column/3)):
        for Ccol in Crow:
            r = Ccol[0]
            c = Ccol[1]
            if(V[r][c].v == 0 and V[r][c].D.count(var) > 0):
                V[r][c].D.remove(var)
                checkedSpaces.append([r,c])
                if(len(V[r][c].D) == 0):
                    for checkedSpace in checkedSpaces:
                        V[checkedSpace[0]][checkedSpace[1]].D.append(var)
                    return [-1]
                    
    return checkedSpaces
    
def getConstrainingValues (row, column, var, V):
    constrainingValues = 0
    '''--Check row--'''
    for col in range(9):
        if (V[row][col].v == 0 and V[row][col].D.count(var) > 0):
            constrainingValues += 1
    '''--Check column--'''
    for r in range(9):
        if(V[r][column].v == 0 and V[r][column].D.count(var) > 0):
            constrainingValues += 1
            
    '''--Check region--'''
    for Crow in getRegion(int(row/3),int(column/3)):
        for Ccol in Crow:
            r = Ccol[0]
            c = Ccol[1]
            if(V[r][c].v == 0 and V[r][c].D.count(var) > 0):
                constrainingValues += 1
                    
    return constrainingValues

def getConstrainedVariables (row, column, V):
    constrainedVariables = 0
    '''--Check row--'''
    for col in range(9):
        if (V[row][col].v == 0):
            constrainedVariables += 1
    '''--Check column--'''
    for r in range(9):
        if(V[r][column].v == 0):
            constrainedVariables += 1
            
    '''--Check region--'''
    for Crow in getRegion(int(row/3),int(column/3)):
        for Ccol in Crow:
            r = Ccol[0]
            c = Ccol[1]
            if(V[r][c].v == 0):
                constrainedVariables += 1
                    
    return constrainedVariables

def printSudoku(V, o):
    for row in V:
        for column in row:
            o.write(str(column.v)+" ");
        o.write("\n");
    
def recursiveBacktrackSearch (V, E): 
    global o;
    if(len(E) == 0):
        printSudoku(V, o);
        return True
    
    minEl = min(E,key=lambda el:len(V[el[0]][el[1]].D))
    minE = []
    for el in E:
        if(len(V[el[0]][el[1]].D) == len(V[minEl[0]][minEl[1]].D)):
            minE.append(el)
    if(len(minE) > 1):
        e = max(minE,key=lambda el:getConstrainedVariables(el[0],el[1],V))
    else:
        e = minEl
    E.remove(e)
    row = e[0]
    column = e[1]
    V[row][column].D.sort(key=lambda d:getConstrainingValues(row, column, d, V))
    for var in V[row][column].D:
        if(consistent(row,column,var,V)):
            V[row][column].v = var
            fc = forwardCheck(row,column,var,V)
            if(fc.count(-1) == 0):
                if(recursiveBacktrackSearch(V, E)):
                    return True
            V[row][column].v = 0
            if(fc.count(-1) == 0):
                for checkedSpace in fc:
                    V[checkedSpace[0]][checkedSpace[1]].D.append(var)
    E.append([row,column])
    return False
#Main
file = sys.argv[1]
f = open(file, 'r')
o = open("solved_sudoku_"+file+".txt",'w')

o.write("Running file: "+file+"\n")

iV = []
for line in f:
    iV.append([Space(int(line[0])), Space(int(line[1])), Space(int(line[2])),
               Space(int(line[3])), Space(int(line[4])), Space(int(line[5])),
               Space(int(line[6])), Space(int(line[7])), Space(int(line[8]))])

iE = []
for i in range(9):
    for k in range(9):
        if(iV[i][k].v == 0):
            iE.append([i,k])
setDomains(iV,iE)

start = datetime.now()
o.write("Start: "+str(start)+"\n")
recursiveBacktrackSearch(iV,iE)
end = datetime.now()
o.write("End: "+str(end)+"\n")
o.write("Time Taken: "+str(end-start)+"\n")

f.close()
o.close()