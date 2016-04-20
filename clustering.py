import first_level_cluster
import second_level_cluster
import groundtruth
import sys
import os
import read_config

threshold_fp_fn={}



INPUT_FILE,OUTPUT_FOLDER,GROUND_TRUTH,DISTANCE_THRESHOLD,TIME_START,TIME_END,THRESHOLD, TRAIL_ID_RANGE\
= read_config.read_config()

print INPUT_FILE,OUTPUT_FOLDER,GROUND_TRUTH,DISTANCE_THRESHOLD,TIME_START,TIME_END,THRESHOLD,TRAIL_ID_RANGE

local_groups,num_trails= first_level_cluster.main(INPUT_FILE,DISTANCE_THRESHOLD,TIME_START,TIME_END,TRAIL_ID_RANGE)  #both arguments are directories (input and output, respectively)

print "Num trails: ",num_trails

def run_program(threshold):

    print "THRESHOLD ",threshold


    if OUTPUT_FOLDER not in os.listdir('.'):
        os.mkdir(OUTPUT_FOLDER)
    
    if str(threshold) not in os.listdir(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER+"/"+str(int(threshold)))


    second_level_cluster.main(OUTPUT_FOLDER, "bus_stops.csv",local_groups,threshold,num_trails,DISTANCE_THRESHOLD) #first argument is the input directory and the second argument is the output file

    # file_name = arguments.input_directory_name.split('_')[-1]
    
    #UNCOMMENT TO GET GROUND-TRUTH COMPARISON
    
    fp,fn = groundtruth.compare_ground_truth(GROUND_TRUTH,OUTPUT_FOLDER+"/"+str(threshold)+'/bus_stops.csv',OUTPUT_FOLDER,threshold)
    threshold_fp_fn[threshold]= [fp,fn]


if '-' in THRESHOLD:
    interval = THRESHOLD.split('-')
    first = int(interval[0])
    last = int(interval[1])

    for i in xrange(first,last+1,10):
        run_program(i)
    #merge 0-thresholds (stops_vs_threshold) and individual threshold's fp/fn
    f = open(OUTPUT_FOLDER+"/0/stops_vs_threshold.csv","r")
    f_new = open(OUTPUT_FOLDER+"/0/stops_vs_threshold_merged.csv","w")

    f_new.write("threshold%,stops%,false_positive%,false_negative%\n")

    #read data from stops_vs_threshold and store it in a list of the form [[a,b],[c,d],..]
    f_data = dict([[int(i.split(',')[0]),float(i.split(',')[1])] for i in f.read().split()[1:]])

    for i,j in sorted(threshold_fp_fn.items()):

        if i in f_data:
            if j[0]== None:
                j[0]= 0
            if j[1]== None:
                j[1]= 100
            f_new.write(str(i)+","+str(f_data[i])+","+str(j[0])+","+str(j[1])+"\n")

else:
    run_program(int(THRESHOLD))