#Usage:

Modify settings.conf and run the program

```
#!python

python clustering.py

```

##MODULES:

* first_level_cluster.py	#contains code for first level clustering algorithm
* second_level_cluster.py	#contains code for the second level clustering algorithm
* lib.py    #lib.py contains common functions and variables used by both first_level_cluster.py and second_level_cluster.py, as well as info extracted from config.txt
* groundtruth.py #contains code for comparing algorithm's output with actual stoppages, calculate false positive and false negatives


