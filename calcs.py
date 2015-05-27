'''
Class & function definitions for TSP DFS and BFS program
CECS 545
Sarah Mullins
Fall 2014
'''

import csv      #extract data from a csv file
import math     #calculate distance between two points
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#each point object contains its number id, x coord and y coord
class Point:
    def __init__(self, num, x, y, next1=None, next2=None, next3=None, prev=None):
        self.num = num
        self.x = x
        self.y = y

#import point information from file into a list
def getPoints(csv_file):
    prelim_list = list()
    with open(csv_file, "r") as f:
        file_reader = csv.reader(f, delimiter=' ')
        for row in file_reader:
            if row[0] == "1":
                prelim_list.append(row)
                for second_row in file_reader:
                    prelim_list.append(second_row)
    return prelim_list


#create Point objects from list
def assignPoints(orig_list):
    point_list = list()
    for item in orig_list:
        point = Point(int(item[0]), float(item[1]), float(item[2]))
        point_list.append(point)
    return point_list


#calculate the distance between two points
def calcDistance(x1, y1, x2, y2):
    return math.sqrt((x2 -x1)**2+(y2 - y1)**2)


#find a point given its assigned number
def findPoint2(point_objects, val):
    for obj in point_objects:
        if obj.num == val:
            return obj

def findEdge(edge_list, pt_a, pt_b):
    for edge in edge_list:
        if edge[0] == pt_a:
            if edge[1] == pt_b:
                return edge

def getLine(x1, y1, x2, y2):

    #find slope-intercept equation
    #y = mx + d
    m = (y2-y1)/(x2-x1)
    d = y1 - m*x1


    #ax+by+c=0
    a = m
    b = -1
    c = d

    return a, b, c

def getPtLineDist(point_objects, edge, x, y):

    print edge[0], edge[1]
    a = edge[2]
    b = edge[3]
    c = edge[4]

    pt1 = findPoint2(point_objects, edge[0])
    pt2 = findPoint2(point_objects, edge[1])

    x1 = pt1.x
    y1 = pt1.y

    x2 = pt2.x
    y2 = pt2.y

    dist = abs(a*x + b*y + c)/math.sqrt(a**2+b**2)

    x3 = (b*(b*x - a*y) - a*c)/math.sqrt(a**2+b**2)
    y3 = (a*(-b*x + a*y) - b*c)/math.sqrt(a**2+b**2)

    #make sure closest point is actually on the edge
    if (x1 < x3 < x2 or x2 < x3 < x1) and (y1 < y3 < y2 or y2 < y3 < y1):
        return dist
    else:
        d1 = calcDistance(x1, y1, x3, y3)
        d2 = calcDistance(x2, y2, x3, y3)
        return min(d1, d2)

def plotLine(pt1, pt2):

    plt.plot([pt1.x, pt2.x], [pt1.y, pt2.y], label="%d%d" % (pt1.num, pt2.num))
    plt.draw()
    time.sleep(1)

def setShortest(min_dist, pt, pt2edge_dist, point_objects, edge):
        min_dist[0] = pt.num
        min_dist[1] = pt2edge_dist

        pt_a = findPoint2(point_objects, edge[0])
        pt_b = findPoint2(point_objects, edge[1])

        return min_dist, pt_a, pt_b