#introduce the point structure

try:
    import simpleguitk as simplegui
except ImportError:
    import simplegui
import math
import random

#fix the size of the Grassmannian manifold Gr(N,M) structure first

N=3
M=7

#The coodinates chosen for the plotting
#The size scalling is modified by some constants SCALE

radius=5
textsize=12
SCALE=350
#give the location of a digit_set
location=[]
for k in range(M):
    location.append(((SCALE+30*(3*N-6))/N*math.cos(-2*math.pi*(k+2)/M)+10.0/N*math.sin(2*k)+SCALE/N, \
                     (SCALE+30*(3*N-6))/N*math.sin(-2*math.pi*(k+2)/M)+10.0/N*math.cos(2*k)+SCALE/N))

def loc(listortuple):
    sum_x=0
    sum_y=0
    for i in listortuple:
        sum_x +=location[i-1][0]
        sum_y +=location[i-1][1]
    return (sum_x,sum_y)

def locoftiles(tile):
    loc_pt=[]
    for set in tile:
        loc_pt.append(loc(set))
    return loc_pt

def loc2(listortuple):
    sum_x=0
    sum_y=0
    for i in listortuple:
        sum_x +=location[i-1][0]
        sum_y +=location[i-1][1]
    return (sum_x+495,sum_y)

def locoftiles2(tile):
    loc_pt=[]
    for set in tile:
        loc_pt.append(loc2(set))
    return loc_pt


#define the boundary set
boundary=[]
for i in range(M):
    digits=[]
    for j in range(N):
        digits.append((i+j)%M+1)
    digits.sort()    
    boundary.append(tuple(digits))

#check a digit_set is a boundary point or not.
def unbdry(set):
    if set in boundary:
        return False
    else:
        return True

#check the click position inside a circle or not
def insidept(digit, pos):
    if (loc(digit)[0] - pos[0])**2+(loc(digit)[1]-pos[1])**2 \
        < radius ** 2:
        return True
    else:
        return False

#define the point class
#initially, we provide all black triangle tiles attached to the point



#pt(digit, neighbors,...)   make a dict for pts, and a dict for tiles.



class wscwithblacktiles():
    def __init__(self, dict_pts={}, dict_blacktiles={}):
        self.dict_pts = dict_pts
        self.dict_blacktiles = dict_blacktiles
        self.sorted()

    def addpts(self, t, nbr=[]):
        self.dict_pts[t] = nbr

    def addtiles(self, t, tiles):
        self.dict_blacktiles[t] = tiles

    def drawtiles(self, canvas):
        for blacktile in self.dict_blacktiles.values():
            canvas.draw_polygon(locoftiles(blacktile), 1,"Gray", "Gray")

    def draw_pointcircle(self, canvas):
        for pt in self.dict_pts:
            canvas.draw_circle(loc(pt), radius, 1, "Green", "White")
            canvas.draw_text(str(pt),  (loc(pt)[0]-10*N/2, loc(pt)[1]-13), textsize, "Black")

    def drawtiles2(self, canvas):
        for blacktile in self.dict_blacktiles.values():
            canvas.draw_polygon(locoftiles2(blacktile), 1,"Black", "Black")

    def draw_pointcircle2(self, canvas):
        for pt in self.dict_pts:
            canvas.draw_circle(loc2(pt), radius ,1, "Green", "White")
            canvas.draw_text(str(pt),  (loc2(pt)[0]-10*N/2, loc2(pt)[1]+3), textsize, "Black")

    def mutation(self, pos):
        for pt in self.dict_pts.items():
            if ((len(pt[1]) == 4) and insidept(pt[0], pos)):
                nb = []
                tunb=[]
                for i in range(4):
                    tunb.append(pt[1][i])
                    nb.append(set(tunb[i]))
                black=[True,True]
                white=[True,True]
                black[0] = len(self.dict_blacktiles[tuple(nb[0].union(nb[1]))]) >=4
                black[1] = len(self.dict_blacktiles[tuple(nb[2].union(nb[3]))]) >=4
                white[0] = (tuple(nb[0].union(nb[3])) in self.dict_blacktiles.keys())
                white[1] = (tuple(nb[1].union(nb[2])) in self.dict_blacktiles.keys())
                common_dig=nb[0].intersection(nb[2])
                alist=list((nb[0].union(nb[2])).difference(set(pt[0]).difference(common_dig)))
                alist.sort()
                new = tuple(alist)

                if unbdry(tunb[0]):
                    l=len(self.dict_pts[tunb[0]])
                    inx = self.dict_pts[tunb[0]].index(pt[0])
                    pre = (inx-1) %l
                    nex = (inx+1) %l
                    if black[0] and white[0]:
                        (self.dict_pts[tunb[0]][inx], self.dict_pts[tunb[0]][nex])= (tunb[1],new)
                    if black[0] and (not white[0]):
                        self.dict_pts[tunb[0]][inx:inx+1] = [tunb[1], new, tunb[3]]
                    if (not black[0]) and white[0]:
                        if nex==0:
                            self.dict_pts[tunb[0]][0] = new
                            self.dict_pts[tunb[0]].pop(l-1)
                            self.dict_pts[tunb[0]].pop(l-2)
                        elif pre==l-1:
                            self.dict_pts[tunb[0]][l-1] = new
                            self.dict_pts[tunb[0]].pop(1)
                            self.dict_pts[tunb[0]].pop(0)
                        else:
                            self.dict_pts[tunb[0]][inx] = new
                            self.dict_pts[tunb[0]].pop(nex)
                            self.dict_pts[tunb[0]].pop(pre)
                    if (not black[0]) and (not white[0]):
                        (self.dict_pts[tunb[0]][pre], self.dict_pts[tunb[0]][inx])= (new, tunb[3])

                if unbdry(tunb[2]):
                    l=len(self.dict_pts[tunb[2]])
                    inx = self.dict_pts[tunb[2]].index(pt[0])
                    pre = (inx-1) %l
                    nex = (inx+1) %l
                    if black[1] and white[1]:
                        (self.dict_pts[tunb[2]][inx], self.dict_pts[tunb[2]][nex])= (tunb[3],new)
                    elif black[1] and (not white[1]):
                        self.dict_pts[tunb[2]][inx:inx+1] = [tunb[3], new, tunb[1]]
                    elif (not black[1]) and white[1]:
                        if nex==0:
                            self.dict_pts[tunb[2]][0] = new
                            self.dict_pts[tunb[2]].pop(l-1)
                            self.dict_pts[tunb[2]].pop(l-2)
                        elif pre==l-1:
                            self.dict_pts[tunb[2]][l-1] = new
                            self.dict_pts[tunb[2]].pop(1)
                            self.dict_pts[tunb[2]].pop(0)
                        else:
                            self.dict_pts[tunb[2]][inx] = new
                            self.dict_pts[tunb[2]].pop(nex)
                            self.dict_pts[tunb[2]].pop(pre)
                    elif (not black[1]) and (not white[1]):
                        (self.dict_pts[tunb[2]][pre], self.dict_pts[tunb[2]][inx])= (new, tunb[1])

                if unbdry(tunb[1]):
                    l=len(self.dict_pts[tunb[1]])
                    inx = self.dict_pts[tunb[1]].index(pt[0])
                    pre = (inx-1) %l
                    nex = (inx+1) %l
                    if black[0] and white[1]:
                        (self.dict_pts[tunb[1]][pre], self.dict_pts[tunb[1]][inx])= (new, tunb[0])
                    elif black[0] and (not white[1]):
                        self.dict_pts[tunb[1]][inx:inx+1] = [tunb[2], new, tunb[0]]
                    elif (not black[0]) and (white[1]):
                        if nex==0:
                            self.dict_pts[tunb[1]][0] = new
                            self.dict_pts[tunb[1]].pop(l-1)
                            self.dict_pts[tunb[1]].pop(l-2)
                        elif pre==l-1:
                            self.dict_pts[tunb[1]][l-1] = new
                            self.dict_pts[tunb[1]].pop(1)
                            self.dict_pts[tunb[1]].pop(0)
                        else:
                            self.dict_pts[tunb[1]][inx] = new
                            self.dict_pts[tunb[1]].pop(nex)
                            self.dict_pts[tunb[1]].pop(pre)
                    elif (not black[0]) and (not white[1]):
                        (self.dict_pts[tunb[1]][inx], self.dict_pts[tunb[1]][nex])= (tunb[2], new)

                if unbdry(tunb[3]):
                    l=len(self.dict_pts[tunb[3]])
                    inx = self.dict_pts[tunb[3]].index(pt[0])
                    pre = (inx-1) %l
                    nex = (inx+1) %l
                    if black[1] and white[0]:
                        (self.dict_pts[tunb[3]][pre], self.dict_pts[tunb[3]][inx])= (new, tunb[2])
                    elif black[1] and (not white[0]):
                        self.dict_pts[tunb[3]][inx:inx+1] = [tunb[0], new, tunb[2]]
                    elif (not black[1]) and (white[0]):
                        if nex==0:
                            self.dict_pts[tunb[3]][0] = new
                            self.dict_pts[tunb[3]].pop(l-1)
                            self.dict_pts[tunb[3]].pop(l-2)
                        elif pre==l-1:
                            self.dict_pts[tunb[3]][l-1] = new
                            self.dict_pts[tunb[3]].pop(1)
                            self.dict_pts[tunb[3]].pop(0)
                        else:
                            self.dict_pts[tunb[3]][inx] = new
                            self.dict_pts[tunb[3]].pop(nex)
                            self.dict_pts[tunb[3]].pop(pre)
                    elif (not black[1]) and (not white[0]):
                        (self.dict_pts[tunb[3]][inx], self.dict_pts[tunb[3]][nex])= (tunb[0], new)

                if black[0]:
                    alist=list(nb[0].union(nb[1]))
                    alist.sort()
                    self.dict_blacktiles[tuple(alist)].remove(pt[0])
                else:
                    alist=list(nb[0].union(nb[1]))
                    alist.sort()                  
                    del self.dict_blacktiles[tuple(alist)]
                if black[1]:
                    alist=list(nb[2].union(nb[3]))
                    alist.sort()
                    self.dict_blacktiles[tuple(alist)].remove(pt[0])
                else:
                    alist=list(nb[2].union(nb[3]))
                    alist.sort()                    
                    del self.dict_blacktiles[tuple(alist)]
                if white[0]:
                    alist=list(nb[0].union(nb[3]))
                    alist.sort()                   
                    self.dict_blacktiles[tuple(alist)].append(new)
                else:
                    alist=list(nb[0].union(nb[3]))
                    alist.sort()                    
                    self.dict_blacktiles[tuple(alist)]=[tunb[0],new,tunb[3]]
                if white[1]:
                    alist=list(nb[1].union(nb[2]))
                    alist.sort()                    
                    self.dict_blacktiles[tuple(alist)].append(new)
                else:
                    alist=list(nb[1].union(nb[2]))
                    alist.sort()                    
                    self.dict_blacktiles[tuple(alist)]=[tunb[1],new,tunb[2]]

                del self.dict_pts[pt[0]]
                self.dict_pts[new]=[tunb[1],tunb[2],tunb[3],tunb[0]]
        self.sorted()


    def sorted(self):
        for tile in self.dict_blacktiles.items():
            tile[1].sort()


#create a wsc at the negative infinity time

def create0(N,M):

    ptinfo={}
    tileinfo={}

    pts={N+1: []}

    for i in range(1,N+2):
        pt_dig=tuple(range(1,i)+range(i+1,N+2))
        pts[N+1].append(pt_dig)


    t_dig=tuple(range(1,N+2))
    tileinfo[t_dig]=pts[N+1]



    pt_dig=tuple(range(3,N+3))
    pts[N+2]=[]
    pts[N+2].append(pt_dig)


    for k in range(2,N+1):
        pt_dig=tuple(range(1,k)+range(k+2,N+3))
        pts[N+2].append(pt_dig)
        t_dig=tuple(range(1,k)+range(k+1,N+3))
        ptinfo[pts[N+1][k-1]]=[pts[N+2][k-2],pts[N+2][k-1],pts[N+1][k],pts[N+1][k-2]]
        tileinfo[t_dig]=[pts[N+1][k-1],pts[N+2][k-2],pts[N+2][k-1]]

    for m in range(N+3,M+1):
        pt_dig=tuple(range(m-N+1,m+1))
        pts[m]=[]
        pts[m].append(pt_dig)
        for k in range(2,N):
            pt_dig=tuple(range(1,k)+range(k+m-N,m+1))
            pts[m].append(pt_dig)
            t_dig=tuple(range(1,k)+range(k+m-N-1,m+1))
            ptinfo[pts[m-1][k-1]]=[pts[m][k-2],pts[m][k-1],\
                                   pts[m-1][k],pts[m-2][k],\
                                   pts[m-2][k-1],pts[m-1][k-2]]
            tileinfo[t_dig]=[pts[m-1][k-1],pts[m][k-2],pts[m][k-1]]

        pt_dig=tuple(range(1,N)+[m])
        pts[m].append(pt_dig)
        t_dig=tuple(range(1,N)+range(m-1,m+1))
        ptinfo[pts[m-1][N-1]]=[pts[m][N-2],pts[m][N-1],\
                               pts[m-2][N-1],pts[m-1][N-2]]
        tileinfo[t_dig]=[pts[m-1][N-1],pts[m][N-2],pts[m][N-1]]

    return wscwithblacktiles(ptinfo,tileinfo)


#deep copy a wsc without quote the original info
def copy(wsc):
    ptinfo2 = {}
    for pt in wsc.dict_pts:
        ptinfo2[pt]=[]
        for v in wsc.dict_pts[pt]:
            ptinfo2[pt].append(v)

    tileinfo2 = {}
    for ti in wsc.dict_blacktiles:
        tileinfo2[ti]=[]
        for v in wsc.dict_blacktiles[ti]:
            tileinfo2[ti].append(v)

    return wscwithblacktiles(ptinfo2,tileinfo2)


def reverse_dig(tupleorlist):
    newlist=[]
    for i in tupleorlist:
        newlist.append(M+1-i)
    newlist.sort()
    return tuple(newlist)

def reverse(wsc):
    ptinfo2 = {}
    for pt in wsc.dict_pts:
        ptinfo2[reverse_dig(pt)]=[]
        for v in wsc.dict_pts[pt]:
            ptinfo2[reverse_dig(pt)].append(reverse_dig(v))

    tileinfo2 = {}
    for ti in wsc.dict_blacktiles:
        tileinfo2[reverse_dig(ti)]=[]
        for v in wsc.dict_blacktiles[ti]:
            tileinfo2[reverse_dig(ti)].append(reverse_dig(v))

    return wscwithblacktiles(ptinfo2,tileinfo2)
    



#randomly mutate the initial point to a new position
def randmutate(awsc,n):
    for i in range(n):
        one = random.choice(awsc.dict_pts.keys())
        awsc.mutation(loc(one))

wsc=create0(N,M)


n=random.randint(M*N,M*N+4)
#randmutate(wsc,n)

wsc2=reverse(wsc)

m=random.randint(M,M+4)

#randmutate(wsc2,m)



#Event handlers, draw handlers and click handler

def mutationonclick(pos):
    wsc.mutation(pos)

#circular the boundary to draw the polyline for the boundary
cir_bdry=boundary+[range(1,N+1)]

def draw(canvas):
    #wsc.drawtiles(canvas)
    canvas.draw_polyline(locoftiles(cir_bdry), 1,"Gray")
    #wsc.draw_pointcircle(canvas)
    for aset in boundary:
        pt=tuple(aset)
        canvas.draw_circle(loc(pt), radius ,1, "Green", "White")
        canvas.draw_text(str(pt), (loc(pt)[0]-10*N/2, loc(pt)[1]-13), textsize, "Black")

    #wsc2.drawtiles2(canvas)
    #canvas.draw_polyline(locoftiles2(cir_bdry), 1,"Black")
    #wsc2.draw_pointcircle2(canvas)
    #for aset in boundary:
        #pt=tuple(aset)
        #canvas.draw_circle(loc2(pt), radius ,2, "Green", "White")
        #canvas.draw_text(str(pt), (loc2(pt)[0]-10*N/2, loc2(pt)[1]+3), textsize, "Black")


#Frame

frame=simplegui.create_frame("mutation process", 4*SCALE , 2*SCALE )
frame.set_canvas_background('White')


#Register Event Handlers

frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mutationonclick)

#start

frame.start()