#! /usr/bin/python


from sys import *
from math import *



###############################################
# Globals
###############################################





###############################################
# Functions
###############################################

def append_item(list, index, item):
    if len(list) < index+1:
        list.append(item)
    else:
        list[index] = item
    return list
# End of function.
###############################################


def findatom(fd,natoms,elem,x,y,z,idx,type,\
                 box,pbc,iframe,time,\
                 x0,y0,z0,idx0):

    counter = 1

    if idx0 > 0:
        x0 = x[idx0]
        y0 = y[idx0]
        z0 = z[idx0]

    drsq_min = 1e30
    for i in range(1,natoms+1):

        dx = x0 - x[i]
        if dx<0.0: dx *= -1.0
        if pbc[1]==1 and dx > 0.5*box[1]: dx -= box[1]

        dy = y0 - y[i]
        if dy<0.0: dy *= -1.0
        if pbc[2]==1 and dy > 0.5*box[2]: dy -= box[2]

        dz = z0 - z[i]
        if dz<0.0: dz *= -1.0
        if pbc[3]==1 and dz > 0.5*box[3]: dz -= box[3]

        drsq = dx*dx + dy*dy + dz*dz
        if counter==1 or (counter>1 and drsq < drsq_min):
            counter = counter + 1
            imin = i
            drsq_min = drsq

    return x[imin], y[imin], z[imin], imin, sqrt(drsq_min)
# End of function.
###############################################


def getframe(fd,natoms,elem,x,y,z,idx,type,\
                 box,pbc,iframe,time):


    # print 'At start of getframe(): iframe, len(time) = ', iframe, len(time)

    natoms_old = natoms

    if iframe==0:
        # /* First frame. Read 'natoms' entry explicitly. */
        list = fd.readline().split()
        natoms_pred = int(list[0])
        natoms_saved = 0
        print "Number of atoms for this first frame is %ld." % natoms_pred
    else:
        # /* Not first frame. Use saved copy of the 'natoms' entry belonging to this frame. */
        natoms_pred = natoms

    natoms_try = natoms_pred

    # /* Increment frame counter. */
    iframe = iframe + 1
    time.append(0.0)
    #print 'After iframe increment and time appending: iframe, len(time) = ', iframe, len(time)


    # /* Get data. */
    while True:

        list = fd.readline().split()
        narg = len(list)

        if narg==0:
            # Finalize frame and return to main().
            natoms = iat
            return 0, iframe, natoms, 0
        
        elif narg==1:
            natoms_saved = int(list[0])
            print "Number of atoms for next frame is %ld. Saving this value." % natoms_saved

            # Finalize frame and return to main().
            natoms = iat
            return 1, iframe, natoms, natoms_saved

        elif len(list[0])>2:
            # Process comment line.
            #print "Processing comment line of frame %d." % iframe
            try:
                tmpf = float(list[3])
            except:
                tmpf = 0.0
            time[iframe] = tmpf

            box[1] = float(list[6])
            box[2] = float(list[7])
            box[3] = float(list[8])
            iat = 0

        elif len(list[0])<=2:
            # Process coordinate line.
            iat = iat + 1
            elem = append_item(elem, iat, list[0])
            x    = append_item(x,    iat, float(list[1]))
            y    = append_item(y,    iat, float(list[2]))
            z    = append_item(z,    iat, float(list[3]))
            type = append_item(type, iat, int(list[4]))
            if len(list)>=6: idx = append_item(idx,  iat, int(list[5]))

        else:
            # Line not recognized.
            print 'Line not recognized.'

# End of function.
###############################################






###############################################
###############################################
##               Main function               ##
###############################################
###############################################




# Defaults:
movie = '/dev/null'
pbc = [0,1,1,1]
idx0 = -1
x0, y0, z0 = 0.0, 0.0, 0.0
tol = 1e-15



iframe = 0

time = [0.0]
elem = [0]
x = [0.0]
y = [0.0]
z = [0.0]
idx = [0]
type = [0]
box = [0.0,0.0,0.0,0.0]
pbc = [0,1,1,1]


if len(argv)<=1:
    # Help on usage.
    print "Usage:"
    print "     %s [options]" % argv[0]
    print "Options:"
    print "     movie         Path to md.movie."
    print "                   NOTE: Comment is assumed to contain time stamp in column 4, and box sizes in"
    print "                   columns 7, 8 and 9. Columns start from 1."
    print "     p1 p2 p3      Periodicity of lattice. Default: 1 1 1"
    print "     idx           Find atom closest to this atom index (ignoring the atom corresponding to the index)."
    print "                   Default: -1"
    print "     x y z         Find atom closest to these coordinates. If idx>=0 this is not used."
    print "     tol           Ignore atoms closer than 'value'. Use tol < 0 to ignore this check alltogether. Default: %.10e" % tol
    print ""
    print "Example usage:"
    print "  MdFindClosestAtom.py  pos1.xyz  1 1 1  -1  0.0 0.0 0.0"
    print ""
    exit(0)




# Parse the options.
n = len(argv)
if n>1: movie = argv[1]
if n>4: pbc = [0, int(argv[2]), int(argv[3]), int(argv[4])]
if n>5: idx0 = int(argv[5])
if n>8: x0,y0,z0 = float(argv[6]), float(argv[7]), float(argv[8])
if n>9: tol = float(argv[9])


if movie == '/dev/null':
  print "Error:  You must specify movie file. Exit."
  exit

fd = open(movie, 'r')




# Loop over frames
while True:

    natoms = 0
    natoms_saved = 0

    ret, iframe, natoms, natoms_saved = getframe(fd,natoms,elem,x,y,z,idx,type,\
                                                     box,pbc,iframe,time)


    print "  Returning from frame %d" % iframe
    print "  Number of atoms is %ld" % natoms
    print "  Box size is %.10e  %.10e  %.10e" % (box[1], box[2], box[3])

    print "---------------------------------------------------------------------------------------"
    print "------------------ Going into analysis at time %.10e ------------------" % time[iframe]


    print "Finding closest atom ..."
    x0r,y0r,z0r,idx0r,dr = findatom(fd,natoms,elem,x,y,z,idx,type,\
                                    box,pbc,iframe,time,\
                                    x0,y0,z0,idx0)
    

    print "Closest atom in frame %d at time %.10e idx  %10ld  drmin  %.10f" % \
        (iframe, time[iframe], idx0r, dr)

    print "------------------ Done with analysis at time %.10e ------------------" % time[iframe]
    print "---------------------------------------------------------------------------------------"


    natoms_old = natoms
    natoms = natoms_saved

    if ret==0: break


# Finished reading file.


fd.close()



