import os
import sys
from math import *
from lib import *
from arguments import DISTANCE_THRESHOLD, GLOBAL_TRAIL_COVERAGE


class Second_level_cluster():
	
	def __init__(self,local_groups):		
		self.all_trails=[]
		self.all_trails=local_groups #contains all the trails along with local-leader points in each trail
		self.all_global_groups={} #contains all global-groups
		self.global_group_leaders=[] #contains global group leaders chosen from each group depending on their wait-time and proximity to other points in the same group
		self.bus_stop_count=0
		self.total_number_of_trails=len(local_groups)

	def process_trails(self):
		""" Add an additional field for global_group_number to each point 
		in each trail"""

		for each_trail_index in xrange(0,len(self.all_trails)):
			trail=[]
			for each_point in self.all_trails[each_trail_index]:
				point = each_point
				point += [0] 
				trail.append(point)
			self.all_trails[each_trail_index]= trail


	def algorithm(self):
		"""
		input: Set of trails containing local leader points (latitude, longitude, timestamp, wait_time, local_group_number)
		output: All bus Stops (latitude,longitude,timestamp, wait_time,local_group_number,global_group_number)
		"""

		self.process_trails() #process the trails to have an additional field : global group leader
		total_trails= self.total_number_of_trails
		#print total_trails
		new_group={}  #create global groups and store them in the dictionary
		
		#for each leader point for each trail 
		for each_trail_index in xrange(0,total_trails):
			for each_leader_point in self.all_trails[each_trail_index]:
				#if global_group_no for the current leader point = 0
				if each_leader_point[-1]==0:
					self.bus_stop_count+=1  #increment bus_stop_count
					new_group[self.bus_stop_count]=[] # (key: value) => bus_stop_count: []
					new_group[self.bus_stop_count].append(each_leader_point) #append each_leader_point to the group with key bus_stop_count
					each_leader_point[-1]=self.bus_stop_count #assign global_group_no to each_leader_point
					
					#for each leader point in each of the subsequent trails
					for next_trail_index in xrange(each_trail_index+1,total_trails):
						for next_leader_point in self.all_trails[next_trail_index]:
							#if global_group_no for the next_leader_point = 0
							if next_leader_point[-1]==0:
								#calculate distance
								distance= get_spherical_distance(float(each_leader_point[0]),float(next_leader_point[0]),float(each_leader_point[1]),float(next_leader_point[1]))
								if distance<= DISTANCE_THRESHOLD:
									#add the next_leader_point to the same global group
									next_leader_point[-1]= each_leader_point[-1]
									new_group[each_leader_point[-1]].append(next_leader_point)
									break


		#make a copy of the global groups and store it into all_global_groups attribute
		self.all_global_groups= dict(new_group)

		#now, new_group and all_global_groups contain the same info
		#we kept the same info into two dictionaries so as to remove (key:value) pairs from the dictionary
		#corresponding to certain condition and we cannot iterate a list and delete elements from it at
		#the same time

		#remove all groups occupying less than 50% of the total trails
		for i in new_group.keys():
			#iterate over all the keys of the new_group dictionary
			if len(new_group[i])< GLOBAL_TRAIL_COVERAGE * self.total_number_of_trails:
				del self.all_global_groups[i]

		print len(self.all_global_groups.keys()),"bus stops"

		#store all global group leaders in a list
		for key in self.all_global_groups.keys():
			self.global_group_leaders.append(get_group_leader(new_group[key]))


	def write_bus_stops(self,output_file):
		output_file= open(output_file,'w')
		output_file.write('latitude,longitude,timestamp,total_wait_time,local_group_number,global_group_no\n')
		for i in self.global_group_leaders:
			i=[str(j) for j in i ]
			output_file.write(','.join(i)+'\n')
		output_file.close()



def main(output_file_name,local_groups):
	obj= Second_level_cluster(local_groups)
	obj.algorithm()
	obj.write_bus_stops(output_file_name)