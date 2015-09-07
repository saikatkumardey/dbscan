import argparse

parser = argparse.ArgumentParser(
	description=
	'''example, python prog_name -d 100 -c 50 -i up -o bus_stops.txt
	'''
	)

parser.add_argument('-d',type=float,default=100.0, help="threshold distance")
parser.add_argument('-c',type=float,default=50.0, help="global trail coverage percentage")
parser.add_argument('-i',type=str,default='up', help="the input file name, (eg, up)")
parser.add_argument('-o',type=str,default='bus_stops.txt', help= "the output file name (eg, bus_stops.txt)")
parser.add_argument('-s',type=str,default='00:00:00', help= "start time of the log hh:mm:ss (24 hour clock)")
parser.add_argument('-e',type=str,default='23:00:00', help= "end time of the log hh:mm:ss (24 hour clock) ")
parser.add_argument('-t',type=str,default='one',help="get result with 0 threshold by default, type all to get for 0 to 100")

args = parser.parse_args()

DISTANCE_THRESHOLD, GLOBAL_TRAIL_COVERAGE, input_directory_name, output_file_name = \
args.d, args.c/100.0, args.i, args.o

TIME_START = [int(i) for i in args.s.split(':')]
TIME_END = [int(i) for i in args.e.split(':')]

threshold= args.t
#START_TIME, END_TIME = int(args.s.split(':')[0]), int(args.e.split(':')[0])
#print START_TIME, END_TIME
print TIME_START,TIME_END
print "Distance threshold= ",DISTANCE_THRESHOLD,"\nInput directory= ", input_directory_name,"\nOutput file name = ", output_file_name
