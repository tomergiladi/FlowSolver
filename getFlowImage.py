import cv2
import numpy as np
import networkx as nx
import os
imgname = 'flow-8mania-2.png'
img = cv2.imread(imgname)
img_orig = img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,90,150,apertureSize = 3)
cv2.imshow('',edges)

lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100, minLineLength=0,maxLineGap=20)
crc = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=25, minRadius=3, maxRadius=30)


lines=lines.reshape(-1,4)



vlines=lines[lines[:,0]==lines[:,2]]
hlines=lines[lines[:,1]==lines[:,3]]

vlines_len = np.abs(vlines[:,3]-vlines[:,1])
hlines_len = np.abs(hlines[:,2]-hlines[:,0])

vlines = vlines[:,0]
hlines = hlines[:,1]
 
vlines=vlines[vlines_len>0.95*(max(hlines)-min(hlines))]
hlines=hlines[hlines_len>0.95*(max(vlines)-min(vlines))]

# for l in vlines:

#     cv2.line(img, (l[0], l[1]), (l[2], l[3]), (255, 0, 255), 3, cv2.LINE_AA)
# for r in vlines:
#     cv2.line(img, (r, 0), (r, img.shape[0]), (255, 0, 255), 3, cv2.LINE_AA)

# cv2.imshow('',img)
# cv2.waitKey(0)



vlines=np.sort(vlines)
hlines=np.sort(hlines)

vlines_diff = vlines[1:]-vlines[:-1]
vlines_diff=np.append(vlines_diff,100)
vlines=vlines[:][vlines_diff>5]
hlines_diff = hlines[1:]-hlines[:-1]
hlines_diff= np.append(hlines_diff,100)
hlines=hlines[:][hlines_diff>5]
vmids=(vlines[:-1]+vlines[1:])/2
hmids=(hlines[:-1]+hlines[1:])/2
vmids=vmids.astype(int)
hmids=hmids.astype(int)


# for x in vmids:
#     for y in hmids:
#         cv2.circle(img, (x,y), 10, (120,255,255), 10)
for r in vlines:
    cv2.line(img, (r, 0), (r, img.shape[0]), (255, 0, 255), 3, cv2.LINE_AA)
for c in hlines:
    cv2.line(img, (0, c), (img.shape[1],c), (255, 0, 0), 3, cv2.LINE_AA)

cv2.imshow('',img)

colors = {}
terminals = []
if crc is not None:

    # Convert the coordinates and radius of the circles to integers
    crc = np.round(crc[0, :]).astype("int")

    # For each (x, y) coordinates and radius of the circles
    ind = 0
    for (x, y, r) in crc:

        # Draw the circle
        cv2.circle(img, (x, y), r, (0, 255, 0), 4)   
        i=(y>hlines).sum()-1
        j=(x>vlines).sum()-1
        color = tuple(img[y,x])
        if color not in colors:
            colors[color]=ind
            terminals.append([])
            ind += 1
        terminals[colors[color]].append((i,j))

mid_hlines  = (hlines[:-1]+hlines[1:])/2
mid_vlines  = (vlines[:-1]+vlines[1:])/2

mid_hlines = mid_hlines.astype(int)
mid_vlines = mid_vlines.astype(int)

edges = []
for j,vline in enumerate(vlines[1:-1]):
    for i,mhline in enumerate(mid_hlines):
        
        color = tuple(img_orig[mhline,vline])
        if color not in colors:
            continue    
        edges.append((colors[color],(i,j),(i,j+1)))

for i,hline in enumerate(hlines[1:-1]): 
    for j,mvline in enumerate(mid_vlines):
        color = tuple(img_orig[hline,mvline])
        if color not in colors:
            continue
        edges.append((colors[color],(i,j),(i+1,j)))

edges.sort()
print(terminals)
print(edges)

#make grid graph with size hlines-1, vlines-1

G = nx.grid_2d_graph(hlines.shape[0]-1,vlines.shape[0]-1)
G=nx.digraph.DiGraph(G)

#set the colot attribute of all nodes and edges to be -1
for n in G.nodes:
    G.nodes[n]['color'] = -1
for e in G.edges:
    G.edges[e]['color'] = -1

#set the attributes of the nodes that match the terminals
for i in range(len(terminals)):
    for t in terminals[i]:
        G.nodes[t]['color'] = i  

#set the attributes of the edges that match the edges
for e in edges: 
    G.edges[e[1],e[2]]['color'] = e[0]  


#reverse values and keys of a dictionary
colors= dict((colors[k],k) for k in colors)

G.colors = colors
#make list of list into tuple of tuples
terminals = [tuple(t) for t in terminals]
G.terminals = tuple(terminals)
# store the graph in a file
try :
    os.mkdir(f"data/{imgname.split('.')[0]}")
except:
    pass
nx.write_gpickle(G, f"data/{imgname.split('.')[0]}/sol.gpickle")
    

cv2.imshow('',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
