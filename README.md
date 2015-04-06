**UPDATE:

* Removed config.txt
* Added argument parsing capablity.

**RUN THE FOLLOWING COMMANDS IN THE TERMINAL:

```
#!python

python clustering.py --help  #to see a list of options for running the program

python clustering.py -d 100 -c 50 -i up -o bus_stops.txt  #run the command like this.
														  # to see what -d, -c, -i , -o stands for
														  # type python clustering.py --help

```


**MODULES:**

* first_level_cluster.py	#contains code for first level clustering algorithm
* second_level_cluster.py	#contains code for the second level clustering algorithm
* lib.py    #lib.py contains common functions and variables used by both first_level_cluster.py and second_level_cluster.py, as well as info extracted from config.txt
* arguments.py #contains argument parsing capability


**OUTPUT:**

'output_file_name' specified in command-line after the -i flag.
