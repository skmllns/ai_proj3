'''
TSP and Greedy Search
CECS 545
Sarah Mullins
Fall 2014
'''

import calcs
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ion()
plt.show()

#input data
#file_name = raw_input("Please enter the file name: ")
file_name = "Random5.tsp"

#begin clock
start_time = time.clock()

#extract point information from file
all_points = calcs.getPoints(file_name)

#assign point information to a list of objects
point_objects = calcs.assignPoints(all_points)

for curr_point in point_objects:
    plt.plot([curr_point.x],[curr_point.y], 'ro')
    plt.annotate("%d" % curr_point.num, xy=(curr_point.x, curr_point.y))
    plt.draw()


#pick an arbitrary start point
start_point = point_objects[0]

#create a list for storing placed points
placed_points = list()
placed_points.append(start_point)

#find the point closest to the start point
#to start with, compare minimum distance to an arbitrary large number
min_dist = [0, 9999999]
for pt in point_objects:
    if pt not in placed_points:
        dist = calcs.calcDistance(start_point.x, start_point.y, pt.x, pt.y)
        if dist < min_dist[1]:
            min_dist[0] = pt.num
            min_dist[1] = dist

#create a list to contain a list of edges
#they will be stored according to the standard form equation of a line:
#ax + by + c = 0
edge_list = list()

#add 2nd point to the list of placed points
curr_point = calcs.findPoint2(point_objects, min_dist[0])
placed_points.append(curr_point)

#add edge b/w first 2 points to list
a, b, c = calcs.getLine(placed_points[0].x, placed_points[0].y, placed_points[1].x, placed_points[1].y)
calcs.plotLine(placed_points[0], placed_points[1])
edge_list.append([placed_points[0].num, placed_points[1].num, a, b, c])

#set first edge
edge = edge_list[0]
a = edge[2]
b = edge[3]
c = edge[4]

#manually insert 3rd point, to set up the 3 initial edges
min_dist = [0, 999999]
for pt in point_objects:

    if pt not in placed_points:             #but only look if it hasn't been placed yet
        pt2edge_dist = calcs.getPtLineDist(point_objects, edge, pt.x, pt.y)
        if pt2edge_dist < min_dist[1]:      #if it's the shortest, make it the new shortest
            min_dist, pt_a, pt_b = calcs.setShortest(min_dist, pt, pt2edge_dist, point_objects, edge)
            print "new min dist is", min_dist, ", between ", pt_a.num, " and ", pt_b.num
#
#add point to list of placed points
curr_point = calcs.findPoint2(point_objects, min_dist[0])
placed_points.append(curr_point)

#create edges between the new point and the points that make up the edge it just attached to
a, b, c = calcs.getLine(pt_a.x, pt_a.y, curr_point.x, curr_point.y)
d, e, f = calcs.getLine(curr_point.x, curr_point.y, pt_b.x, pt_b.y)

edge_list.append([pt_a.num, curr_point.num, a, b, c])
calcs.plotLine(pt_a, curr_point)

edge_list.append([curr_point.num, pt_b.num, d, e, f])
calcs.plotLine(curr_point, pt_b)

#create a copy of the edge list
placed_edges = edge_list[:]

while len(placed_points) < len(point_objects):
    edge_list = placed_edges   #refresh edge list
    min_dist = [0, 9999999]
    pt_a = None
    pt_b = None
    for pt in point_objects:
        if pt not in placed_points:
            for edge in edge_list:       #check it against every edge in the list, calculating their proximity to each other
                pt2edge_dist = calcs.getPtLineDist(point_objects, edge, pt.x, pt.y)
                if pt2edge_dist < min_dist[1]:                               #if it's the shortest, make it the new shortest
                    min_dist, pt_a, pt_b = calcs.setShortest(min_dist, pt, pt2edge_dist, point_objects, edge)
                    min_dist[0] = pt.num
                    min_dist[1] = min_dist


    #add given point to list of placed points, remove it from the list of eligible points
    curr_point = calcs.findPoint2(point_objects, min_dist[0])

    #add current point to the list of placed points
    placed_points.append(curr_point)

    #create edges between the new point and the points that make up the edge it just attached to
    a, b, c = calcs.getLine(pt_a.x, pt_a.y, curr_point.x, curr_point.y)
    d, e, f = calcs.getLine(curr_point.x, curr_point.y, pt_b.x, pt_b.y)

    #add new edges
    placed_edges.append([pt_a.num, curr_point.num, a, b, c])
    calcs.plotLine(pt_a, curr_point)

    placed_edges.append([curr_point.num, pt_b.num, d, e, f])
    calcs.plotLine(curr_point, pt_b)

    #find edge to be removed, and remove it!
    rem_edge = calcs.findEdge(edge_list, pt_a.num, pt_b.num)

    pt_label = str(pt_a.num) + str(pt_b.num)
    line = [line for line in ax.lines if line.get_label() == pt_label]

#screen stays open for x amount of seconds
time.sleep(20)
