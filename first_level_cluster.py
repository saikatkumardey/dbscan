import os
import sys
from lib import *
from arguments import DISTANCE_THRESHOLD

local_groups=[] #store all the local group leaders per group per trail in a file

class First_level_cluster():
    
    def __init__(self):
        self.data_lines=[]         #contains latitude, longitude, time-stamp
        self.zero_speed_data=[]    # contains latitude, longitude, time-stamp, count
        self.local_group_data=[]   # contains latitude, longitude, time-stamp, count, local_group_number
        self.local_group_leader=[] # contains latitude, longitude, time-stamp, total_wait_time, local_group_number
        #self.distance_threshold= 100

    def read_data(self,file_name):
        """ reads the file named file_name and stores it in data_lines """
        input_file= open(file_name,'r')
        self.data_lines= input_file.readlines()[1:]
        input_file.close()

    def print_data(self, data_list):
        """ prints the data_list. For test purposes only. """
        j=1
        for i in data_list:
            print j,i
            j+=1

    def process_line(self,raw_data):
        """ Takes a line of raw gps data and returns latitude,longitude and timestamp """

        line= raw_data.split(',')
        latitude, longitude, timestamp = line[0],line[1], line[2].split()[0]
        return latitude,longitude, timestamp

    def get_zero_speed_data(self):
        """ 
            stores the duplicate contiguous points in a list. 
            compare each line of gps data with the next one, group them if they are same
            and store them in the list zero_speed_data once a different line of data has been
            found and start a new group.
            the list zero_speed_data contains only the first point of each group and contains
            an additional attribute count to store the number of duplicate contiguous points present (excluding itself).

            output list: latitude,longitude,timestamp,count,local_group_number
                         where count= number of duplicate contiguous points
        
        """

        count=0
        #get the first point from the raw trail data
        current_latitude, current_longitude, current_timestamp = self.process_line(self.data_lines[0])
        
        for next_line in self.data_lines[1:]:
            #get the next point
            next_latitude, next_longitude, next_timestamp= self.process_line(next_line)
            #if current and next points are same, duplicate points found, increment count
            if (current_latitude,current_longitude) == (next_latitude,next_longitude):
                count+=1
            else:
                #if there is at least one additional duplicate point
                if count>0:
                    #add the first point of the group to the zero_speed_list
                    self.zero_speed_data.append([current_latitude,current_longitude,current_timestamp,count])
                    count=0 #reset count so as to mark the beginning of a new group
                current_latitude, current_longitude, current_timestamp = next_latitude, next_longitude, next_timestamp
                #assign the next point to be the current point, ie, it is probably the first point of a next zero-speed group


    def get_local_groups(self):
        """
        assign local group number to each point
        """
        #assign first point of zero_speed_data to be in local group 1
        local_group_no=1
        current_point = self.zero_speed_data[0]+[local_group_no]
        self.local_group_data.append(current_point)
        
        #for each point in the zero_speed_data list
        for each_point in self.zero_speed_data[1:]:
            #get distance between the current_point and each_point
            distance= get_spherical_distance(float(current_point[0]),float(each_point[0]),float(current_point[1]),float(each_point[1]))
            
            if distance > DISTANCE_THRESHOLD:
                #create a new group
                local_group_no+=1
            #assign each point to local_group_no
            #point to note: local_group_no doesn't change if the distance between two points is <= distance_threshold.
            
            each_point+=[local_group_no] #append the local_group_no (changed/unchanged) to the next point
            self.local_group_data.append(each_point)
            current_point= each_point #assign each_point to the current_point


    def get_local_group_leaders(self):
        
        """ get all of the local group leader points for all groups in a trail
            we store the group leader points for a trail in local_group_leader[]
        """

        #group the points based on local group_number and store the local group leader of each group


        #attach a dummy variable to the end of local_group_data
        #we'll remove it after operation
        #significance: to append the new group formed after the operation on last element of the list
        #since we add a new group only when we find a change in the local_group_number between consecutive
        #elements, we need to make sure that we have a dummy variable to check the last element of the list with.
        #and form the last group
        
        self.local_group_data.append([-12])

        group=[] #stores a group of points temporarily
        group_number=1
        for each_point in self.local_group_data:
            #check the local group number for each point, if it is equal to  group_number append it to group
            if each_point[-1] == group_number:
                group.append(each_point)
            else:
                #get the group leader of the current group
                group_leader= get_group_leader(group)
                #and append it to local_group_leader[]
                self.local_group_leader.append(group_leader)
                group_number+=1 #create a new group
                group=[] #reset group[]
                group.append(each_point) #add the current point to the new group
        self.local_group_data.pop() # removing the dummy variable

    def write_data(self,file_name):
        """write the local group leader data to file_name"""
        write_trail= open(file_name,'w')
        for data_line in self.local_group_leader:
            data_line= [str(el) for el in data_line]
            write_trail.write(','.join(data_line)+"\n")
        write_trail.close()


#############          End of class definition     #############################


def get_file_names(path):
    """ Helper function: returns all the files in a directory named path 

    For example:
    if path= 'up/'
    then this function returns all the file names present inside the directory 'up/'
    """
    names= os.listdir(path)
    return names

def get_output_file_name(path,name):
    """returns output file name depending on the trail"""
    out_name= path+'/'+name.split('.')[0]+'_out.txt'
    return out_name

def comp(a):
    """comparison function to sort the file_names lexicographically.... eg, up_1 comes before up_2"""
    a= a.split('_')
    a= int(a[1].split('.')[0])
    return a



def main(directory):
    """ First-level-clustering algorithm  
    Input: set of trails containing points (latitude,longitude, altitude, timestamp)
    output: leader points (latitude, longitude, timestamp, wait_time, local_group_number) for all groups in each trail
    """    
    call_algo= First_level_cluster()

    #get all the file_names in the directory into a list and sort them up lexicographically  
    trails= sorted(get_file_names(directory),key=comp)
    print "LEN: ",len(trails)
        
    #for each file in the list trails
    for trail in trails:
        input_trail= directory +'/'+ trail #get the path of the input file | for example, up/up_1.txt
        call_algo.read_data(input_trail) #read all the points in the input_trail and store it in data_lines[]
        call_algo.get_zero_speed_data()  #get all the zero-speed points and store it in zero_speed_data[]
        call_algo.get_local_groups()     #get all local groups from zero-speed points and store in local_group_data[]
        call_algo.get_local_group_leaders() #get all local group leaders from local_group_data and store in local_group_leader[]
        local_groups.append(call_algo.local_group_leader)
        call_algo.__init__();  #re-initialize all attributes of the object call_algo for the next trail

    #uncomment the lines to write all the local-group leaders to a file
    # f_out= open('localgroup','w')
    # for i in local_groups:
    #     for j in i:
    #         j=[str(k) for k in j]
    #         f_out.write(','.join(j)+'\n')
    # f_out.close()

    return local_groups
