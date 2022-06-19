"""
This script basically solves the onion peeling problem. This is my implementation that I did as a programming exercise, 
and it failed with "time limit exceeded" error, so there is much to improve in this code.

Here is a description of the problem as I recall it : 
Somebody somewhere for some reason is interested in the layered structures at cross sections of onions.
He stores these layered structures by storing the 2D coordinates of points in the boundaries of the layers. 
Later he reconstructs these layered structures from the 2D coordinates. How the heck does he do this?

This script receives as input a set of 2D points representing the layered structure of a cross section of an onion.
It receives the number of points in the first line and then the x and y coordinates, separated by spaces, 
of each point in a separate line. Then it finds the outermost convex hull of the set of points,
removes the points belonging to the outermost convex hull from the set, and repeats this process with the remaining points. 
It returns the number of layers found for the specific set of points given as input.

The algorithm used in this script to find the convex hull of a set of 2D points is similar to the gift wrapping algorithm. 
It starts with a reference point known to belong to the convex hull (the leftmost one for example) and a reference vector 
(initially the y-axis basis vector), defines a vector from this point to every other point and finds the one with largest 
cosine with the reference vector (largest normalized inner product), then it continues this process with the new point and 
the new vector found.

https://en.wikipedia.org/wiki/Convex_layers

https://en.wikipedia.org/wiki/Gift_wrapping_algorithm

https://br.spoj.com/problems/CEBOLA.pdf
"""


# def vis(coordinates,hull):

#     import cv2
#     import numpy as np
    
#     img_w = 200
#     img_h = 200
#     img = np.zeros((img_h,img_w,3))
#     for x,y in [coordinates[i] for i in hull]:
#         x = int(img_w*x + img_w/2)
#         y = int(img_h*y + img_h/2)
#         img = cv2.circle(img, (x,y), 5, [0,0,255], 5)

#     cv2.imshow("test",img)
#     cv2.waitKey()
#     cv2.destroyAllWindows()

import math

def vnorm(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def vcos(v1,v2):
    return (v1[0]*v2[0] + v1[1]*v2[1]) / (vnorm(v1) * vnorm(v2))

def vdiff(v1,v2):
    return [v1[0]-v2[0],v1[1]-v2[1]]

def convex_hull(coord):

    c = min(coord,key=lambda x: x[0])
    ref = [0,1]
    hull = [coord.index(c)]
    while ((hull[0] != hull[-1]) or (len(hull) == 1)):
        vcs=[vcos(vdiff(pt,c),ref) if pt != c else -math.inf for pt in coord]
        hull.append(vcs.index(max(vcs))) 
        p = coord[hull[-2]]
        c = coord[hull[-1]]
        ref = vdiff(c,p)
    return hull

def convex_polygons(coord, count):
    L = len(coord)
    if L > 0:
        hull = convex_hull(coord)
        count+=1
        # vis(coord,hull)
        return convex_polygons([coord[i] for i in range(L) if i not in hull],count)
    else:
        return count

n = int(input().rstrip())

orig_coord = []
for _ in range(n):
    orig_coord.append(list(map(int, input().rstrip().split())))

result = convex_polygons(orig_coord, 0)
print(result)

