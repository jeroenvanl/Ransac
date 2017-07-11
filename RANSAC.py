# Script to derive planes from unstructured point cloud using the RANSAC (Random Sampling Consensus) technique


import rhinoscriptsyntax as rs
import math 
import ghpythonlib.components as ghcomp
import Rhino.Geometry as geo

from random import randint

if(run):
    # set meta parameters
    c = len(pointCloud)-1
    planes=[]
    amount = int(iterations)
    surfaces=[]
    amountPoints=[]
    allPoints=[]
    # loop multiple times
    for i in range(amount):
        # create plane from random three points
        pointList = []
        pointList.append(pointCloud[randint(0,c)])
        closestPoints,indexes,distances = ghcomp.ClosestPoints(pointList[0],pointCloud,3)
        pointList.append(closestPoints[1])
        pointList.append(closestPoints[2])
        avgPoint = rs.AddPoint((pointList[0].X+pointList[1].X+pointList[2].X)/3,(pointList[0].Y+pointList[1].Y+pointList[2].Y)/3,(pointList[0].Z+pointList[1].Z+pointList[2].Z)/3)
        plane = rs.PlaneFitFromPoints(pointList)
        movedPlane = rs.MovePlane(plane,avgPoint)
        # check whether normal plane aligns any orthogonal direction
        normal = abs(movedPlane.ZAxis[2])
        normal = min(1-normal,normal)
        normalX = abs(movedPlane.ZAxis[0])
        normalX = min(1-normalX,normalX)
        normalY = abs(movedPlane.ZAxis[1])
        normalY = min(1-normalY,normalY)
        if(normal<zValue and normalX<zValue and normalY<zValue):
            # count how many points fit this random plane
            pointCount = 0
            pts = []
            for pt in pointCloud:
                dist = abs(rs.DistanceToPlane(plane,pt))
                if(dist<maxDist):
                    pointCount+=1
                    pts.append(pt)
            # if enough points fit the plane
            if(pointCount>=minAmount):
                # add points and size
                for p in pts:
                    allPoints.append(p)
                amountPoints.append(pointCount)
                # add plane
                planes.append(movedPlane)