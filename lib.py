import os
from math import *

def get_spherical_distance(lat1,lat2,long1,long2):
        """
        Get spherical distance any two points given their co-ordinates (latitude, longitude)
        """
        q=radians(lat2-lat1)
        r=radians(long2-long1)
        lat2r=radians(lat2)
        lat1r=radians(lat1)
        a=sin(q/2)*sin(q/2)+cos(lat1r)*cos(lat2r)*sin(r/2)*sin(r/2)
        c=2*atan2(sqrt(a),sqrt(1-a))
        R=6371*1000
        d=R*c
        return d


def get_group_leader(group):
        """ returns the group_leader point for a particular group of points"""
       
        if group == []:
            return
        wait_per_distance= [] #contains the summation of wait_time/distance from one point to all other point, for every point in the group
        total_wait_time=0  #would contain the total wait time of the group, we sum up the 'count' field of all the points
        for each_point in group:
            wait_time= int(each_point[3])  #each_point= [latitude,longitude,timestamp,count,local_group_number]
            temp=0   #temp would contain wait_time* (1/d1 + 1/d2 + 1/d3 + .....) where d1,d2,d3...dn are distances from one point to all other points
            for other_point in group:
                #get distance from each_point to other_point, d1,d2,d3.... etc
                distance= get_spherical_distance(float(each_point[0]),float(other_point[0]),float(each_point[1]),float(other_point[1]))
                temp+= 1/(distance+1)  # here, temp= (1/d1 + 1/d2 + 1/d3 + .....)
            temp= wait_time*temp        #now, temp= wait_time* (1/d1 + 1/d2 + 1/d3 + ....)
            wait_per_distance.append(temp)  #append temp to the list
            total_wait_time+=wait_time 
        
        max_index=0

        max_wait_per_distance= max(wait_per_distance) #get the maximum value from the list
 
        #get the index of the point having maximum wait_per_distance
        for index in xrange(0,len(wait_per_distance)):
           if max_wait_per_distance == wait_per_distance[index]:
               max_index= index
               break

        group[max_index][3]= total_wait_time  #replace 'count' field with total_wait_time.

        return group[max_index]  #return the group leader point