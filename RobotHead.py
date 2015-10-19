import rhinoscriptsyntax as rs

base = 0

def createBase(centerpoint = 20, width = 8, height = 10, depth = 5):
    

    center = ' 0,0,'+str(centerpoint)
    lengthRadius= ' 0,0,'+str(centerpoint-height)
    widthRadius = ' '+str(width)+',0,0'
    depthRadius = ' 0,'+str(depth)+',0'
    
    rs.Command("_Ellipsoid"+center+lengthRadius+widthRadius+depthRadius)
    global base 
    base = rs.AllObjects()[0]


def createEyes(cutout = False, radius = 1.5):
    
    rightPos = (3, -3.5, 20)
    rightEye = addEye(rightPos, radius = radius)
    
    leftPos = (-3,-3.5,20)
    leftEye = addEye(leftPos, radius = radius)
    if(cutout):
        rs.BooleanDifference([base],[rightEye, leftEye])
        global base
        base = rs.AllObjects()[0]


def addEye(pos, radius = 1.5):
    rs.AddSphere(pos, radius)
    return rs.AllObjects()[0]

def createMouth(smile = True, cutout = False, centerx = 0, centery = -3.5, centerz = 14, height = 0.5, width = 3, depth = 1):
    center = toPos(centerx, centery, centerz)
    heightRadius = toPos(centerx, centery, centerz+height)
    widthRadius = toPos(centerx+width, centery, centerz)
    depthRadius = toPos(centerx, centery+depth, centerz)
    
    
    rs.Command("_Ellipsoid"+center+heightRadius+widthRadius+depthRadius)
    mouthGUID = rs.AllObjects()[0]
    
    if(smile):
        smileFactor = 0.1
        rs.SelectObject(mouthGUID)
        rightEnd = widthRadius
        rightLift = toPos(centerx+width, centery, centerz+smileFactor)
        leftEnd = toPos(centerx-width, centery, centerz)
        leftLift = toPos(centerx-width, centery, centerz+smileFactor)
        
        rs.Command("_Bend"+center+rightEnd+rightLift)
        rs.Command("_Bend"+center+leftEnd+leftLift)
        rs.UnselectAllObjects()
        
        
    if(cutout):
        print "todo"
        rs.BooleanDifference([base],[mouthGUID])
        global base
        base = rs.AllObjects()[0]

def createNose(centerx = 0, centery = -4, centerz = 18, height = 2, width = 1, depth = 2):
    center = toPos(centerx, centery, centerz)
    heightRadius = toPos(centerx, centery, centerz+height)
    widthRadius = toPos(centerx+width, centery, centerz)
    depthRadius = toPos(centerx, centery+depth, centerz)
    
    rs.Command("_Ellipsoid"+center+heightRadius+widthRadius+depthRadius)

def toPos(x, y, z):
    return ' '+str(x)+','+str(y)+','+str(z)


def createHead(eyes, mouth, nose, **kwargs):
    """ args: 
    eyes: 0/1
    mouth: 0/1
    nose: 0/1
    kwargs (optional):
    cutoutEyes: 0/1
    cutoutMouth: 0/1
    smile: 0/1
    """
    
    
    width = 8
    height = 10
    depth = 5
    centerpoint = 20
    if('horizontalHead' in kwargs):
        if kwargs['horizontalHead']:
            width = 10
            height = 8

    createBase(centerpoint, width, height, depth)
    
    cutout = False
    if(eyes):
        if('cutoutEyes' in kwargs):
            cutout = kwargs['cutoutEyes']
        
        createEyes(cutout = cutout)
     
     
    if(mouth):
        cutout = kwargs['cutoutMouth']
        if('smile' in kwargs):
            smile= kwargs['smile']
        else:
            smile = False
            
        createMouth(smile = smile, cutout=cutout)
    
    
    if(nose):
        createNose()
    

kwargs = {'cutoutEyes': 0, 'cutoutMouth': 0, 'smile':1, 'horizontalHead':0}
createHead(False, True, False, **kwargs)

#createBase()

#createEyes(cutout=True)
#createMouth(cutout=True)
#createNose()