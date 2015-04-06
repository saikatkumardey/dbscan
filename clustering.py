import first_level_cluster
import second_level_cluster
import sys
import os
import arguments

local_groups= first_level_cluster.main(arguments.input_directory_name)  #both arguments are directories (input and output, respectively)

second_level_cluster.main(arguments.output_file_name,local_groups) #first argument is the input directory and the second argument is the output file