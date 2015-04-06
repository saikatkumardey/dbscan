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


args = parser.parse_args()

DISTANCE_THRESHOLD, GLOBAL_TRAIL_COVERAGE, input_directory_name, output_file_name = \
args.d, args.c/100.0, args.i, args.o

print "Distance threshold= ",DISTANCE_THRESHOLD, "\nGlobal trail coverage= ", GLOBAL_TRAIL_COVERAGE,"\nInput directory= ", input_directory_name,"\nOutput file name = ", output_file_name
