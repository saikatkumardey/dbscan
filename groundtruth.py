import math
class Point:
    def __init__(self):
        self.Lat=0.00
        self.Lon=0.00
        self.timestamp = 0
        self.total_wait_time=0
        self.trail_no=-1
        self.local_group_no=0
        self.globalgroupId = 0
        self.nbd=-1
        #self.visted=False
        #self.nbdDist=10000000

def retrivefile(filename):
    f = open(filename,'r')
    lines = f.readlines()
    data = []
    for row in lines:
        line = row.rstrip('\n').split(',')
        if len(line)<2:
            continue
        data.append(line)
    data.pop(0)

    return data

def storing(data):
    objlist=[]
    for row in data:
        obj=Point()
        obj.Lat=row[0]
        obj.Lon=row[1]
        obj.timestamp=row[2]
        obj.globalgroupId=int(eval(row[-1]))
        objlist.append(obj)
    return objlist

def storing2(data):
    objlist=[]
    prev=data[0]
    iobjlist=[]
    for row in data:
        obj=Point()
        obj.Lat=row[0]
        obj.Lon=row[1]
        obj.timestamp=row[2]
        obj.total_wait_time = row[3]
        obj.trail_no= row[4]
        obj.local_group_no = row[5]
        obj.globalgroupId=int(eval(row[-1]))
        if prev[-1]==row[-1]:
            iobjlist.append(obj)
        else:
            objlist.append(iobjlist)
            iobjlist=[]
            iobjlist.append(obj)
        prev=row
    objlist.append(iobjlist)
    return objlist

def caldistance(a,b,c,d):
    Coords1=[]
    Coords2=[]
    Coords1.append(a)
    Coords1.append(b)
    Coords2.append(c)
    Coords2.append(d)
    
    Coords1[0]=math.radians(float(Coords1[0]))
    Coords1[1]=math.radians(float(Coords1[1]))
    Coords2[0]=math.radians(float(Coords2[0]))
    Coords2[1]=math.radians(float(Coords2[1]))
    if Coords1!=Coords2:
        
        distance=math.acos(math.sin(Coords1[0])*math.sin(Coords2[0])+math.cos(Coords1[0])*math.cos(Coords2[0])*math.cos(Coords1[1]-Coords2[1]))*6371*1000
    else:
        distance=0
    return distance

def compare_ground_truth(ground_truth_file, bus_stop_file,OUTPUT_FOLDER,threshold):
    #filename1 = raw_input("Enter the fixed filename:")  #Actual Stop List
    data1 = retrivefile(ground_truth_file)
    objlist1 = storing(data1)
    #filename2 = raw_input("Enter the filename which is going to be compared:")  #Experiment Stop List
    data2 = retrivefile(bus_stop_file)
    
    if data1==[] or data2==[]:
        return [None,None]

    #stores all the ground points as list
    objlist2 = storing2(data2)

    detected_stoppages=[]

    for i in objlist2:
        for j in i:
           detected_stoppages.append(j)

    prevminDist=1000000000000
    for p1 in objlist1:
        for p2 in objlist2:
            storeDist=[]
            for r in p2:
                storeDist.append(caldistance(p1.Lat,p1.Lon,r.Lat,r.Lon))
            minDist=min(storeDist)
            if minDist<=30 and minDist<prevminDist:
                if p1.nbd != -1:
                    for p3 in objlist2:
                        tmp=p3[0]
                        if tmp.nbd==p1.globalgroupId:
                            for r in p3:
                                r.nbd=-1
                        
                for r in p2:
                    r.nbd=p1.globalgroupId
                    p1.nbd=r.globalgroupId
            prevminDist=minDist
    try:
        fn=open(OUTPUT_FOLDER+"/"+str(int(threshold))+"/False_Negative.csv",'w')
        fn.write("Latitude,Longitude,GlobalGroupId\n")
    except:
        print "no "+OUTPUT_FOLDER+"/"+str(int(threshold))+"/False_Negative.csv"+" file found"
 
    no_fn=0
    for p1 in objlist1:
        if p1.nbd == -1:
            no_fn+=1
            fn.write(p1.Lat+','+p1.Lon+','+str(p1.globalgroupId)+'\n')
    fn.close()
    try:
        fp=open(OUTPUT_FOLDER+"/"+str(int(threshold))+"/False_Positive.csv",'w')
        fp.write("latitude,longitude,timestamp,total_wait_time,trail_number,local_group_number,global_group_no\n")
    except:
        print "no "+OUTPUT_FOLDER+"/"+str(int(threshold))+"/False_Positive.csv"
    
    no_fp=0
    for p2 in objlist2:
        tmp=p2[0]
        if tmp.nbd==-1:
            for r in p2:
                no_fp+=1
                detected_stoppages.remove(r)
                fp.write(str(r.Lat)+','+str(r.Lon)+','+str(r.timestamp)+','+
                    str(r.total_wait_time)+','+str(r.trail_no)+','+str(r.local_group_no)+','+str(r.globalgroupId)+'\n')
    fp.close()

    print "actual stops: ",len(objlist1),"fn ",no_fn," fp: ",no_fp," detected: ",len(detected_stoppages)

    detected = open(OUTPUT_FOLDER+"/"+str(int(threshold))+"/detected_stoppages.csv",'w')
    detected.write("latitude,longitude,timestamp,total_wait_time,trail_number,local_group_number,global_group_no\n")

    for r in detected_stoppages:
        detected.write(str(r.Lat)+','+str(r.Lon)+','+str(r.timestamp)+','+
                     str(r.total_wait_time)+','+str(r.trail_no)+','+str(r.local_group_no)+','+str(r.globalgroupId)+'\n')

    detected.close()

    #calculate fp% and fn%
    fp_pct= no_fp*100.0/len(data2)
    fn_pct = no_fn*100.0/len(data1)

    return fp_pct, fn_pct
     
if __name__=='__main__':
    main()
    
