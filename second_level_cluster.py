import os
import sys
from math import *
from lib import *
from datetime import datetime
import pickle
from pprint import pprint


def get_standard_deviation(values):
	mean = sum(values)/len(values)
	deviation_sq = map(lambda x:(x-mean)**2, values)
	variance = sum(deviation_sq)/len(deviation_sq)
	sd = variance**(0.5)
	return sd

class Second_level_cluster():
	
	def __init__(self,local_groups):		
		self.all_trails=[]
		self.all_trails=local_groups #contains all the trails along with local-leader points in each trail
		self.all_global_groups={} #contains all global-groups
		self.global_group_leaders=[] #contains global group leaders chosen from each group depending on their wait-time and proximity to other points in the same group
		self.bus_stops=[]
		self.sorted_clusters=[]
		self.bus_stop_count=0
		self.total_number_of_trails=len(local_groups)

	def process_trails(self):
		""" Add an additional field for global_group_number to each point 
		in each trail"""

		for each_trail_index in xrange(0,len(self.all_trails)):
			trail=[]
			for each_point in self.all_trails[each_trail_index]:
				if each_point == None:
					continue
				point = each_point
				point += [0] 
				trail.append(point)
			self.all_trails[each_trail_index]= trail


	def algorithm(self,DISTANCE_THRESHOLD,threshold,num_trails):
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

		##pickle all the groups
		# pickle_data_file = open('raw_group_data.pkl','wb')
		# pickle.dump(new_group,pickle_data_file)


		#remove all groups occupying less than (GLOBAL_TRAIL_COVERAGE) % of the total trails
		for i in new_group.keys():
			#iterate over all the keys of the new_group dictionary
			# print "benchmark: ",(threshold/100.0) * num_trails,
			# print "present: ",len(new_group[i]),
			if len(new_group[i])< ((threshold/100.0) * num_trails):
				# print "deleting it"
				del self.all_global_groups[i]
			# print

		print len(self.all_global_groups.keys()),"clusters"

		self.temporal_sorting()
		# print len(self.all_global_groups)
		# pprint(self.all_global_groups)
		# self.temporal_sort_single_cluster(self.all_global_groups[1])


	def temporal_sort_single_cluster(self,cluster):
		
		for i in xrange(0,len(cluster)):
			for j in xrange(i+1,len(cluster)):
				point_a= cluster[i]
				point_b= cluster[j]
				if point_a[4] == point_b[4] and datetime.strptime(point_a[2],DATE_FORMAT)>datetime.strptime(point_b[2],DATE_FORMAT):
					cluster[i],cluster[j] = cluster[j], cluster[i]


	def temporal_sorting(self):
		'''
		input: global_group_details dictionary containing the clusters
		output: temporally sorted clusters 
		'''
		c_list= self.all_global_groups.items()
		cluster_list = c_list[:]
		DATE_FORMAT = '%H:%M:%S'
		print len(cluster_list)
		for i in xrange(0,len(cluster_list)):
			for j in xrange(i+1,len(cluster_list)):
				flag= False
				for point_a in cluster_list[i][1]:
					for point_b in cluster_list[j][1]:
						if point_a[4] == point_b[4] and datetime.strptime(point_a[2],DATE_FORMAT)>datetime.strptime(point_b[2],DATE_FORMAT):
							flag= True
							break
				if flag==True:
					cluster_list[i],cluster_list[j] = cluster_list[j], cluster_list[i]
		
		#get group_heads
		group_heads=[]
		for cluster in cluster_list:
			head = get_group_leader(cluster[1])
			total_wait_time = 0
			for i in cluster[1]:
				total_wait_time+= int(i[3])
			head[3]= total_wait_time
			dist= self.get_spatial_spread(cluster[1])
			head= head[:5]+[str(dist)]+head[5:]
			group_heads.append(head)
		f= open('group_heads','w')
		for head in group_heads:
			head=[str(i) for i in head]
			f.write(','.join(head)+"\n")
		f.close()
		#update the sorted_clusters and bus_stops
		self.sorted_clusters= cluster_list[:]
		self.bus_stops= group_heads[:]


		##dump the sorted clusters
		pickle_data_file = open('pickle_data.pkl','wb')
		pickle.dump(self.sorted_clusters,pickle_data_file)




	def bus_stop_details(self):
		
		bus_details = open('bus_stop_details','w')
		stop_number=1
		
		for values in self.all_global_groups.values():
			#bus_details.write("stop number "+str(stop_number)+"\n")
			for i in values:
				i=[str(j) for j in i]
				bus_details.write(','.join(i)+'\n')
			stop_number+=1
		


	def get_spatial_spread(self,group):
		dist=0
		if len(group)==0:
			return dist

		for current_point in xrange(0,len(group)):
			for point in xrange(current_point+1,len(group)):
				dist=max(dist,get_spherical_distance(float(group[current_point][0]),float(group[point][0]),float(group[current_point][1]),float(group[point][1])))
		#print dist
		return dist


	def write_bus_stops(self,output_file):
		output_file= open(output_file,'w')
		output_file.write('latitude,longitude,timestamp,total_wait_time,trail_number,spatial_spread,local_group_number,global_group_no\n')

		for stop in self.bus_stops:
			stop=[str(j) for j in stop ]
			output_file.write(','.join(stop)+'\n')	

		output_file.close()

	def write_global_group_details(self,OUTPUT_FOLDER,num_trails,threshold):
		#log file
		# stop number, total points, number of trails in the stop, point contribution of each trail in the stop

		## 3 plots required
		# 1> Trail Contribution % vs Stops
		# 2> No of stops vs Trail Contribution Threshold
		# 3> Mean Weight vs No of Stops

		output_file= open(OUTPUT_FOLDER+"/"+str(threshold)+"/trail_vs_stops.csv",'w')
		output_file.write('stop_number,total_points,trails,global_group_no,mean_wt_time,standard_deviation,each_trail_contrib\n')

		class Output_log(object):
			"""docstring for Output_log"""
			def __init__(self,stop_number,total_contrib,trails,global_group_number,each_trail_contrib):
				self.stop_number = stop_number
				self.total_contrib = total_contrib
				self.trails = trails
				self.num_of_trails = len(trails)
				self.each_trail_contrib = each_trail_contrib
				self.global_group_number= global_group_number

		stop_number = 0
		stoppage_list=[]

		trails_present = set()

		##temporary
		stoppages_at_each_trail={}

		for i,cluster in self.sorted_clusters:

			total_contrib=0
			trails= set()
			each_trail_contrib={}
			global_group_number = cluster[0][-1]
			for j in self.all_global_groups[i]:
				j= [str(k) for k in j]
				wait_time = float(j[3])
				trail_number = int(j[4])
				total_contrib += wait_time
				trails.add(trail_number)
				trails_present.add(trail_number)
				each_trail_contrib[trail_number]= wait_time
			
			obj = Output_log(stop_number, total_contrib, trails,global_group_number,each_trail_contrib)
			stoppage_list.append(obj)
			stop_number+=1
			for i in each_trail_contrib.keys():
				if i not in stoppages_at_each_trail:
					stoppages_at_each_trail[i]=[]
				stoppages_at_each_trail[i].append(stop_number)
		
		# s_at_each= open('stoppage_trails_detail.csv','w')
		# for i in stoppages_at_each_trail:
		# 	k= stoppages_at_each_trail[i]
		# 	k=[str(j) for j in k]
		# 	k= ','.join(k)
		# 	s_at_each.write(str(i)+"==>"+k+"\n")
			#print i,"=>",stoppages_at_each_trail[i]



		print "trails_present ",trails_present, len(trails_present)

		#create a bucket
		threshold_dict = {}

		for i in stoppage_list:
			# i.trails= (len(i.trails)*100.0)/len(trails_present)
			i.trails= (len(i.trails)*100.0)/num_trails

			if int(i.trails%10 == 0):
				nearest_dec = int(i.trails)
			else:
				nearest_dec = int(i.trails) - int(i.trails)%10 + 10

			if nearest_dec in threshold_dict:
				threshold_dict[nearest_dec]+=1
			else:
				threshold_dict[nearest_dec]=1


		num_of_stops = len(stoppage_list)
		print "num stops: ",num_of_stops

		for i in threshold_dict:
			threshold_dict[i] = threshold_dict[i]*100.0/num_of_stops

		#delete > 100% threshold
		if 100 in threshold_dict:
			del threshold_dict[100]
		#change in algorithm
		#instead of the interval in the bucket
		#keep a single threshold into which all
		#stoppages greater than the threshold will be stored
		total_pct = 100
		for i in sorted(threshold_dict.keys()):
			threshold_dict[i] = total_pct - threshold_dict[i]
			total_pct= threshold_dict[i]

		print "Threshold: ",sorted(threshold_dict.items())

		threshold_list = sorted(threshold_dict.items())
		threshold_csv = open(OUTPUT_FOLDER+"/"+str(threshold)+"/stops_vs_threshold.csv","w")
		threshold_csv.write("threshold,stops\n")
		
		for i in threshold_list:
			threshold_csv.write(str(i[0])+","+str(i[1])+"\n")

		for i in stoppage_list:
			output_file.write(str(i.stop_number)+","+str(i.total_contrib)+","+str(i.trails)+","+str(i.global_group_number)+","+str(i.total_contrib*1.0/i.num_of_trails)+","+str(get_standard_deviation(i.each_trail_contrib.values()))+","+str(i.each_trail_contrib)+"\n")

		# # write the mean_wt vs stops csv
		# mean_wt_csv = open(OUTPUT_FOLDER+"/"+str(threshold)+"/mean_wt_vs_stops.csv","w")
		# mean_wt_csv.write("stop_number,global_group_no,mean_wt\n")
		# for i in stoppage_list:
		# 	mean_wt_csv.write(str(i.stop_number)+","+str(i.global_group_number)+","+str(i.total_contrib*1.0/i.num_of_trails)+"\n")



def main(OUTPUT_FOLDER,output_file_name,local_groups,threshold,num_trails,DISTANCE_THRESHOLD):
	obj= Second_level_cluster(local_groups)
	obj.algorithm(DISTANCE_THRESHOLD,threshold,num_trails)
	obj.write_bus_stops(OUTPUT_FOLDER+'/'+str(threshold)+'/'+output_file_name)
	# obj.write_global_group_details_prev('details/global_group_details.txt')
	obj.write_global_group_details(OUTPUT_FOLDER,num_trails,threshold)
	obj.bus_stop_details()