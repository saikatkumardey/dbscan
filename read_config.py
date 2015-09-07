import sys
import os

DISTANCE_THRESHOLD=0
TIME_START= '09:00:00'
TIME_END = '17:00:00'
INPUT_FILE = ''
OUTPUT_FOLDER = ''
GROUND_TRUTH = ''
TRAIL_ID_RANGE=0


def getvalue(line):
    return line.split('=>')[-1].strip()

def read_config():
    with open('settings.conf','r') as f:
        lines = f.read().split('\n')
        INPUT_FILE = getvalue(lines[0])
        OUTPUT_FOLDER= getvalue(lines[1])
        GROUND_TRUTH = getvalue(lines[2])
        DISTANCE_THRESHOLD = int(getvalue(lines[3]))
        TIME_START = getvalue(lines[4])
        TIME_END= getvalue(lines[5])
        THRESHOLD= getvalue(lines[6])
        TRAIL_ID_RANGE = int(getvalue(lines[7]))

        TIME_START = [int(i) for i in TIME_START.split(':')]
        TIME_END = [int(i) for i in TIME_END.split(':')]
    return INPUT_FILE,OUTPUT_FOLDER,GROUND_TRUTH,DISTANCE_THRESHOLD,TIME_START,TIME_END,THRESHOLD,TRAIL_ID_RANGE
