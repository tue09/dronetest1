import queue
import random
import numpy as np
import math
import copy
#
#Data
#Max_Drone_Flight_Time = 60 minutes = 1 hours.
#Drone_Unloading_Time = 5 minutes = 5/60 hours.
#Drone_Take_Off_Time = 5 minutes = 5/60 hours.
number_customer=20
number_truck=3
number_drone=3
speed_truck=30
speed_drone=45
capacity_drone=3
Max_Drone_Flight_Time=1
Drone_Unloading_Time=5/60
file_object=open('C101_0.5.dat')
data=file_object.readlines()
coordinates=[0]*(number_customer+1)
for i in range(0,len(coordinates)):
    coordinates[i]=[]
time_release=[0]*(number_customer+1)
for i in range(0,number_customer+1):
    coordinates[i].append(int(data[i+5][0:2]))
    coordinates[i].append(int(data[i+5][3:5]))
    time_release[i]=int(data[i+5][18:len(data[i+5])-1])
class cus:
    def __init__(self, coordinates,release_date,weight):
        self.coordinates = coordinates
        self.release_date=release_date/60
        self.weight=weight
depot=coordinates[0]
customer=[0]*(number_customer+1)
customer[0]=cus(coordinates[0],0,0)
for i in range(1,len(customer)):
    customer[i]=cus(coordinates[i],time_release[i],1)
truck_path_array=[1,11,20,5,7,14,0,2,4,6,16,10,3,13,15,0,9,18,19,12,17,8]
x=[0.4,0.45,0.2,0.6,0.9,0.1,0.4,0.6,0.85,0.9,0.15,0.65,0.25,0.05,0.075,0.8,0.8,0.3,0.22,0.1,0.1,0.4]
#
#Function
def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
def change_array(array1,array2,M,N):
    array1=np.array(array1,dtype=list)
    array2=np.array(array2,dtype=list)
    a=[0]*(N)
    a=np.array(a,dtype=list)
    array3=[None]*(M+N-1)
    j=0
    for i in range(M+N-1):
        if array1[i]==0:
            j+=1
            a[j]=i
    a[0]=0
    for j in range(0,M+N-1):
        if 0<=j<a[1]:
            array3[j]=int(array2[j]*(j+2))
    for i in range(1,N-1):
        for j in range(0,M+N-1):
            if a[i]<j<a[i+1]:
                array3[j]=int(array2[j]*(j+1-a[i]))
            elif array1[j]==0:
                array3[j]=None
    for j in range(0,M+N-1):
        if a[N-1]<j:
            array3[j]=int(array2[j]*(j+1-a[N-1]))
        elif array1[j]==0:
            array3[j]=None
    array4=[None]*(M+N-1)
    array4=np.array(array4,dtype=list)
    arraya=[0]*(M+N)
    arraya=np.array(arraya,dtype=list)
    for i in range(0,len(arraya)):
        arraya[i]=[-1]
    for i in range(0,a[1]):
        if array3[i]==0:
            array4[i]=0
        elif array3[i]>=1:
            array4[i]=array1[array3[i]-1]

    for j in range(1,N-1):
        for i in range(a[j]+1,a[j+1]):
            if array3[i]>=1:
                array4[i]=array1[array3[i]+a[j]]
            elif array3[i]==0:
                array4[i]=0
    for i in range(a[N-1]+1,M+N-1):
        if array3[i]==0:
            array4[i]=0
        elif array3[i]!=0:
            array4[i]=array1[array3[i]+a[N-1]]
    array1=np.append(0,array1)
    array4=np.append(-2,array4)
    for i in range(0,len(a)):
        a[i]=a[i]+1

    for i in range(a[0],a[1]):
        if array4[i]==0:
            if arraya[0][0]==-1:
                arraya[0].remove(-1)
            arraya[0].append(array1[i])
    for j in range(1,N-1):
        for i in range(a[j]+1,a[j+1]):
            if array4[i]==0:
                for k in range(a[j],a[j+1]):
                    if array1[k]==0:
                        if arraya[k][0]==-1:
                            arraya[k].remove(-1)
                        arraya[k].append(array1[i])
    for i in range(a[N-1]+1,M+N):
        if array4[i]==0:
            for k in range(a[N-1],M+N):
                if array1[k]==0:
                    if arraya[k][0]==-1:
                        arraya[k].remove(-1)
                    arraya[k].append(array1[i])
    for i in range(1,M+N):
        for j in range(0,M+N):
            if array4[j]==i:
                for k in range(0,M+N):
                    if array1[k]==i:
                        if arraya[k][0]==-1:
                            arraya[k].remove(-1)
                        arraya[k].append(array1[j])
    arr=np.array((array1,arraya))
    return arr
#M=number_customer, N=number_truck
def max_outarray_release_date(array):
    b=[]
    for i in range(0,len(array)):
        b.append(customer[array[i]].release_date)
    c=max(b)
    return c
def sum_outarray_weight(array):
    b=0
    for i in range(0,len(array)):
        b+=customer[array[i]].weight
    return b
def sorted_release_date(array):
    q=queue.PriorityQueue()
    for i in range(0,len(array)):
        q.put((customer[array[i]].release_date,array[i]))
    p=[]
    for i in range(len(array)):
        p.append(q.get()[1])
    return p
def sorted_package_by_weight(array,capacity):
    x=[]
    k=0
    x.append([])
    array1=[]
    for i in range(0,len(array)):
        array1.append(array[i])
    if len(array1)!=0:
        while len(array1)!=0:
            s=0
            for j in range(0,1000):
                if len(array1)!=0:
                    if s+customer[array1[0]].weight<=capacity:
                        x[k].append(array1[0])
                        s+=customer[array1[0]].weight
                        array1.pop(0)
                    elif s+customer[array1[0]].weight>capacity: break
            x.append([])
            k+=1
    for i in range(0,len(x)):
        if len(x[i])==0:
            x.pop(i)
    return x
def split_element_into_2_parts(array,index):
    array1=[]
    array2=[]
    for i in range(0,index):
        array1.append(array[i])
    for i in range(index,len(array)):
        array2.append(array[i])
    array=[array1,array2]
    return array
def Check_y_delivery_in_x(x,y):
    for i in range(0,len(decryption[0])):
        if decryption[0][i]==x:
            for j in range(0,len(decryption[1][i])):
                if decryption[1][i][j]==y:
                    return True
            break
def delivery_location(x):
    for i in range(0,len(decryption[1])):
        for j in range(0,len(decryption[1][i])):
            if decryption[1][i][j]==x:
                a=decryption[0][i]
                break
    return a
def which_truck_package_in(x):
    for i in range(0,len(decryption[0])):
        if decryption[0][i]==x:
            for j in range(0,len(a)-1):
                if a[j]<i<a[j+1]:
                    return j
                if i>a[len(a)-1]:
                    return len(a)-1
decryption=change_array(truck_path_array,x,number_customer,number_truck)
# a is an array satisfying decryption[0][a[i]]=0 for all i in range(0,len(a))
a=[]
for i in range(0,len(truck_path_array)+1):
    if decryption[0,i]==0:
        a.append(i)
last_point_package_queue=[0]*(len(a)-1)
for i in range(0,len(a)-1):
    last_point_package_queue[i]=decryption[0][a[i+1]-1]
last_point_package_queue.append(truck_path_array[len(truck_path_array)-1])
u=[0]*(number_customer+number_truck-1)
for i in range(0,len(u)):
    u[i]=[]
for i in range(0,len(u)):
    if decryption[1][i][0]!=-1:
        u[i]=sorted_release_date(decryption[1][i])
lists=[0]*(number_customer+number_truck-1)
for i in range(0,len(u)):
    lists[i]=[[-1]]
for i in range(0,len(u)):
    if decryption[1][i][0]!=-1:
        lists[i]=sorted_package_by_weight(u[i],capacity_drone)
def Function(s):
    package_queue=[0]*number_truck
    for i in range(0,len(package_queue)):
        package_queue[i]=[]
    for i in range(0,len(package_queue)-1):
        for j in range(a[i]+1,a[i+1]):
            package_queue[i].append([[],truck_path_array[j-1]])
        package_queue[i].append([[999999],999])
    for i in range(a[len(a)-1]+1,len(truck_path_array)+1):
        package_queue[len(package_queue)-1].append([[],truck_path_array[i-1]])
    package_queue[len(package_queue)-1].append([[999999],999])
    drone_queue=queue.PriorityQueue()
    for i in range(0,number_drone):
        drone_queue.put((0,"Drone %i"%i))
    ite=[0]*number_truck
    truck_time=[0]*number_truck
    scp=copy.deepcopy(s)
    Drone_journey=[]
    #
    # Trucks move from depot :
    for i in range(0,len(truck_time)):
        if package_queue[i][ite[i]][1]==999:truck_time[i]=0
        else:
            if decryption[1][a[i]+ite[i]][0]==-1:
                truck_time[i]=truck_time[i]+(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_truck
            else:
                truck_time[i]=max(truck_time[i],max_outarray_release_date(decryption[1][a[i]+ite[i]]))+(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_truck

    p=[0]*len(truck_time)
    for i in range(0,len(p)):
        p[i]=[]
    for i in range(0,len(truck_time)):
        if (a[i]+ite[i]+1)!=number_customer+number_truck:
            if decryption[1][a[i]+ite[i]+1]==[-1]:p[i]=[0]
            else:
                if a[i]+ite[i]+1==number_customer+number_truck-1:
                    p[i]=[0]
                else:
                    for j in range(0,len(scp[a[i]+ite[i]+1])):
                        p[i].append(customer[scp[a[i]+ite[i]+1][j][len(scp[a[i]+ite[i]+1][j])-1]].release_date)
        while len(p[i])!=0:
            if package_queue[i][ite[i]][1]==999:
                package_queue[i][ite[i]][0][0]=999999
                p[i].pop(0)
            else:
                if decryption[1][a[i]+ite[i]+1]==-1:
                    package_queue[i][ite[i]][0].append(truck_time[i]-(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_drone)
                else:
                    package_queue[i][ite[i]][0].append(max(p[i][0],truck_time[i]-(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_drone))
                    p[i].pop(0)

    #
    # trucks and drones move
    for z in range(0,2*(number_customer)+1):
        variable=0
        compare=[]
        v=drone_queue.get()
        for i in range(0,len(package_queue)):
            if package_queue[i][ite[i]][0]!=[]:
                compare.append(max(package_queue[i][ite[i]][0][0],v[0]))
        l=min(compare)
        for i in range(0,len(package_queue)):
            if max(package_queue[i][ite[i]][0][0],v[0])==l:
                h=i
                variable=package_queue[h][ite[h]][0][0]
                package_queue[h][ite[h]][0].pop(0)
                break
        drone_queue.put(v)
        m=0
        for i in range(0,len(package_queue)):
            if compare[i]==999999:
                m+=1
        if m==len(package_queue):
            package_queue[h][ite[h]][0].append(999999)
            break
        if package_queue[h][ite[h]+1][1]!=999:
            element_put_in_drone_queue=0
            if decryption[1][a[h]+ite[h]+1][0]!=-1:
                if variable!=0:
                    timedr=drone_queue.get()
                    drone_queue.put((max(timedr[0],variable)+2*distance(customer[decryption[0][a[h]+ite[h]+1]].coordinates,depot),timedr[1]))
                    element_put_in_drone_queue=(max(timedr[0],variable)+2*distance(customer[decryption[0][a[h]+ite[h]+1]].coordinates,depot))
                    Drone_journey.append([timedr[1],": 0 to",decryption[0][a[h]+ite[h]+1],": package",scp[a[h]+ite[h]+1][0]])
                    scp[a[h]+ite[h]+1].pop(0)

            if package_queue[h][ite[h]][0]==[]:
                ite[h]+=1
                if decryption[1][a[h]+ite[h]][0]==-1:
                    truck_time[h]=truck_time[h]+(distance(customer[package_queue[h][ite[h]-1][1]].coordinates,customer[package_queue[h][ite[h]][1]].coordinates))/speed_truck
                    package_queue[h][ite[h]][0].append(truck_time[h]-(distance(depot,customer[package_queue[h][ite[h]][1]].coordinates))/speed_drone)

                else:
                    truck_time[h]=element_put_in_drone_queue-(distance(customer[decryption[0][a[h]+ite[h]-1]].coordinates,customer[decryption[0][a[h]+ite[h]]].coordinates)/speed_drone)+(distance(customer[package_queue[h][ite[h]-1][1]].coordinates,customer[package_queue[h][ite[h]][1]].coordinates))/speed_truck
                    p=[]
                    if a[h]+ite[h]+1!=number_customer+number_truck-1:
                        for j in range(0,len(scp[a[h]+ite[h]+1])):
                            p.append(customer[scp[a[h]+ite[h]+1][j][len(scp[a[h]+ite[h]+1][j])-1]].release_date)

                        while len(p)!=0:
                            if h<number_truck-1:
                                if (a[h]+ite[h])==a[h+1]:
                                    break
                            else:
                                if (a[h]+ite[h])==number_customer+number_truck:
                                    break
                            package_queue[h][ite[h]][0].append(max(p[0],truck_time[h]-(distance(depot,customer[package_queue[h][ite[h]][1]].coordinates))/speed_drone))
                            p.pop(0)
                    else: ite[h]+=1
        else: ite[h]+=1

    #
    #trucks back to depot
    for i in range(0,number_truck):
        truck_time[i]=truck_time[i]+distance(customer[last_point_package_queue[i]].coordinates,depot)/speed_truck
    Time=max(truck_time)
    Solution=[Drone_journey,Time]
    return Solution
Current_Solution=Function(lists)
print(Current_Solution[0])
drone_journey=[]
for i in range(0,len(Current_Solution[0])):
    drone_journey.append(Current_Solution[0][i][len(Current_Solution[0][i])-1])
for i in range(0,len(drone_journey)):
    drone_journey[i]=sorted_release_date(drone_journey[i])
print("drone_journey is:",drone_journey)
package_queue=[0]*number_truck
for i in range(0,number_truck):
    package_queue[i]=[]
for i in range(0,len(drone_journey)):
    temp=which_truck_package_in(delivery_location(drone_journey[i][0]))
    package_queue[temp].append(drone_journey[i])
print(package_queue)
decryption_fake=copy.deepcopy(decryption)
for i in range(0,len(decryption_fake[1])):
    decryption_fake[1][i]=sorted_release_date(decryption_fake[1][i])
drone_time=[0]*number_drone
truck_time=[0]*number_truck
time_truck_append=[9999999]*(number_customer+1)
truck_location=[0]*number_truck
drone_location=[0]*number_drone
def point_journey(journey):
    journey1=copy.deepcopy(journey)
    point=[0]*len(journey1)
    for i in range(0,len(journey1)):
        point[i]=[journey1[i]]
    for z in range(0,capacity_drone):
        k=0
        for i in range(0,len(point)-1):
            for j in range(i+1,len(point)):
                if delivery_location(point[j][0])==delivery_location(point[i][0]):
                    point[i].append(point[j][0])
                    point[j].pop(0)
                    if point[j]==[]:
                        point.pop(j)
                    k+=1
                    break
            if k==1:break
    return point
def drone_flight_time(journey):
    time=0
    time=time+distance(depot,customer[delivery_location(point_journey(journey)[0][0])].coordinates)/speed_drone
    if len(point_journey(journey))!=1:
        for i in range(0,len(point_journey(journey))-1):
            time=time+distance(customer[delivery_location(point_journey(journey)[i][0])].coordinates,customer[delivery_location(point_journey(journey)[i+1][0])].coordinates)/speed_drone
    time=time+distance(customer[delivery_location(point_journey(journey)[len(point_journey(journey))-1][0])].coordinates,depot)/speed_drone
    return time
def drone_move(a,journey):
#drone a at x in journey to next point
# x in range(0,len(point_journey(journey))+1): x=0:depot
    if drone_location[a]==0:
        drone_time[a]=max(max(drone_time[a],max_outarray_release_date(journey))+Drone_Unloading_Time+distance(depot,customer[delivery_location(point_journey(journey)[drone_location[a]][0])].coordinates)/speed_drone,time_truck_append[delivery_location(point_journey(journey)[0][0])])
        print("Drone",a,"move from: 0 to",delivery_location(point_journey(journey)[drone_location[a]][0]),"bring package",journey,"delivery",point_journey(journey)[drone_location[a]]," || Drone",a,"time is:",drone_time[a])
        drone_location[a]+=1
    elif drone_location[a]!=0:
        if drone_location[a]<len(point_journey(journey)):
            drone_time[a]=max(drone_time[a]+Drone_Unloading_Time+distance(customer[delivery_location(point_journey(journey)[drone_location[a]-1][0])].coordinates,customer[delivery_location(point_journey(journey)[drone_location[a]][0])].coordinates)/speed_drone,time_truck_append[delivery_location(point_journey(journey)[drone_location[a]][0])])
            print("Drone",a,"move from:",delivery_location(point_journey(journey)[drone_location[a]-1][0]),"to",delivery_location(point_journey(journey)[drone_location[a]][0]),"bring package",journey,"delivery",point_journey(journey)[drone_location[a]],"|| Drone",a,"time is:",drone_time[a])
            drone_location[a]+=1
        elif drone_location[a]==len(point_journey(journey)):
            drone_time[a]=drone_time[a]+distance(customer[delivery_location(point_journey(journey)[drone_location[a]-1][0])].coordinates,depot)/speed_drone
            print("Drone",a,"move from:",delivery_location(point_journey(journey)[drone_location[a]-1][0]),"to 0","|| Drone",a,"time is:",drone_time[a])
            drone_location[a]=0
drone_complete_at=[0]*(number_customer+1)
def truck_move(s,x):
#truck s at x to next point
    if x==0:
        truck_time[s]=max_outarray_release_date(decryption[1][a[s]])+distance(depot,customer[decryption[0][a[s]+1]].coordinates)/speed_truck
        time_truck_append[decryption[0][a[s]+1]]=truck_time[s]
        truck_location[s]+=1
        print("Truck",s,"move from: 0 to",decryption[0][a[s]+1],"|| Truck",s,"time is:",truck_time[s])
    if x!=0:
        if a[s]+x+1==number_customer+number_truck:
            truck_time[s]=max(drone_complete_at[decryption[0][a[s]+x]],truck_time[s])+distance(customer[decryption[0][a[s]+x]].coordinates,depot)/speed_truck
            truck_location[s]=0
            print("Truck",s,"move from:",decryption[0][a[s]+x],"to 0","|| Truck",s,"time is:",truck_time[s])
        else:
            if decryption[0][a[s]+x+1]==0:
                truck_time[s]=max(drone_complete_at[decryption[0][a[s]+x]],truck_time[s])+distance(customer[decryption[0][a[s]+x]].coordinates,depot)/speed_truck
                truck_location[s]=0
                print("Truck",s,"move from:",decryption[0][a[s]+x],"to 0","|| Truck",s,"time is:",truck_time[s])
            elif decryption[0][a[s]+x+1]!=0:
                truck_time[s]=max(drone_complete_at[decryption[0][a[s]+x]],truck_time[s])+distance(customer[decryption[0][a[s]+x]].coordinates,customer[decryption[0][a[s]+x+1]].coordinates)/speed_truck
                time_truck_append[decryption[0][a[s]+x+1]]=truck_time[s]
                truck_location[s]+=1
                print("Truck",s,"move from:",decryption[0][a[s]+x],"to",decryption[0][a[s]+x+1],"|| Truck",s,"time is:",truck_time[s])
def reset():
    global drone_time
    global truck_time
    global time_truck_append
    global truck_location
    global drone_location
    global drone_complete_at
    drone_time=[0]*number_drone
    truck_time=[0]*number_truck
    time_truck_append=[9999999]*(number_customer+1)
    truck_location=[0]*number_truck
    drone_location=[0]*number_drone
    drone_complete_at=[0]*(number_customer+1)
def sorted_journey_release_date(journey):
    package_queue1=[0]*number_truck
    for i in range(0,number_truck):
        package_queue1[i]=[]
    for i in range(0,len(journey)):
        temp=which_truck_package_in(delivery_location(journey[i][0]))
        package_queue1[temp].append(journey[i])
    check=[0]*len(package_queue1)
    sort=[]
    for j in range(0,len(journey)):
        for i in range(0,len(package_queue1)):
            if package_queue1[i]==[]:
                check[i]=999999
            else:
                check[i]=max_outarray_release_date(package_queue1[i][0])
        for i in range(0,len(package_queue1)):
            if check[i]==min(check):
                h=i
                break
        sort.append(package_queue1[h][0])
        package_queue1[h].pop(0)
    return sort
drone_journey=sorted_journey_release_date(drone_journey)
def fitness(drone_journey):
    reset()
    drone_journey=sorted_journey_release_date(drone_journey)
    drone_journey1=copy.deepcopy(drone_journey)
    print("drone_journey is:",drone_journey1)
    decryption_fake=copy.deepcopy(decryption)
    for i in range(0,len(decryption_fake[1])):
        decryption_fake[1][i]=sorted_release_date(decryption_fake[1][i])
    #Trucks move from depot
    for i in range(0,number_truck):
        truck_move(i,0)
    #Trucks and drones move
    loading=[0]*number_drone
    for i in range(0,len(loading)):
        loading[i]=[]
    for i in range(0,number_truck):
        if decryption[1][a[i]+truck_location[i]]==[-1]:
            truck_move(i,truck_location[i])
    for g in range(0,number_customer):
        test=0
        for i in range(0,number_truck):
            if truck_location[i]==0:
                test+=1
        if test==number_truck:
            break
        temp=[]
        for i in range(0,len(drone_location)):
            if drone_location[i]==0:
                temp.append(drone_time[i])
        for i in range(0,len(drone_time)):
            if drone_time[i]==min(temp):
                h=i
                break
        loading[h]=drone_journey1[0]
        drone_journey1.pop(0)
        drone_move(h,loading[h])
        for i in range(0,len(point_journey(loading[h])[drone_location[h]-1])):
            for j in range(0,len(decryption_fake[1])):
                for ll in range(0,capacity_drone):
                    for z in range(0,len(decryption_fake[1][j])):
                        if decryption_fake[1][j][z]==point_journey(loading[h])[drone_location[h]-1][i]:
                            decryption_fake[1][j].remove(point_journey(loading[h])[drone_location[h]-1][i])
                            if decryption_fake[1][j]==[]:
                                drone_complete_at[decryption_fake[0][j]]=drone_time[h]
                            break
        if drone_location[h]!=0:
            if drone_location[h]==len(point_journey(loading[h])):
                drone_move(h,loading[h])
            else:
                while time_truck_append[delivery_location(point_journey(loading[h])[drone_location[h]][0])]<9999999:
                    drone_move(h,loading[h])
                    for i in range(0,len(point_journey(loading[h])[drone_location[h]-1])):
                        for j in range(0,len(decryption_fake[1])):
                            for ll in range(0,capacity_drone):
                                for z in range(0,len(decryption_fake[1][j])):
                                    if decryption_fake[1][j][z]==point_journey(loading[h])[drone_location[h]-1][i]:
                                        decryption_fake[1][j].remove(point_journey(loading[h])[drone_location[h]-1][i])
                                        if decryption_fake[1][j]==[]:
                                            drone_complete_at[decryption_fake[0][j]]=drone_time[h]
                                        break
                    if drone_location[h]==len(point_journey(loading[h])):break
                    if drone_location[h]==0:
                        break
        for l in range(0,capacity_drone):
            for i in range(0,number_truck):
                if decryption_fake[1][a[i]+truck_location[i]]==[]:
                    truck_move(i,truck_location[i])
            for i in range(0,number_truck):
                while decryption_fake[1][a[i]+truck_location[i]]==[-1]:
                    truck_move(i,truck_location[i])
            for u in range(0,number_drone):
                if drone_location[u]!=0:
                    if drone_location[u]==len(point_journey(loading[u])):
                        drone_move(u,loading[u])
                    else:
                        while time_truck_append[delivery_location(point_journey(loading[u])[drone_location[u]][0])]<9999999:
                            drone_move(u,loading[u])
                            for i in range(0,len(point_journey(loading[u])[drone_location[u]-1])):
                                for j in range(0,len(decryption_fake[1])):
                                    for ll in range(0,capacity_drone):
                                        for z in range(0,len(decryption_fake[1][j])):
                                            if decryption_fake[1][j][z]==point_journey(loading[u])[drone_location[u]-1][i]:
                                                decryption_fake[1][j].remove(point_journey(loading[u])[drone_location[u]-1][i])
                                                break
                                            if decryption_fake[1][j]==[]:
                                                drone_complete_at[decryption_fake[0][j]]=drone_time[u]
                            if drone_location[u]==len(point_journey(loading[u])):break
                            if drone_location[u]==0:
                                break
                            if drone_location[u]==len(point_journey(loading[u])):
                                drone_move(u,loading[u])
                                break
                    if drone_location[u]==0:
                        loading[u]=[]
        print("drone journey is:",drone_journey1)
    time=max(truck_time)
    print("_______________________________________________________")
    return time
current_solution=fitness(drone_journey)
print("Time is:",current_solution)
test_split=0
test_check=0
number_test_split=0
number_test_check=0
def split(index):
    global drone_journey
    global current_solution
    global test_split
    test_split=0
    if len(drone_journey[index])!=1:
        temp=[0]*(2*(len(drone_journey[index])-1))
        for i in range(0,len(temp)):
            temp[i]=copy.deepcopy(drone_journey)
        for i in range(0,len(drone_journey[index])-1):
            fake=split_element_into_2_parts(temp[i][index],i+1)
            temp[i].pop(index)
            temp[i].insert(index,fake[1])
            temp[i].insert(index,fake[0])
        for i in range(len(drone_journey[index])-1,2*(len(drone_journey[index])-1)):
            temp[i]=copy.deepcopy(temp[i-len(drone_journey[index])+1])
            temp[i][index+1].append(temp[i][index+2][0])
            temp[i][index+2].pop(0)
            if temp[i][index+2]==[]:
                temp[i].pop(index+2)
        check=[0]*len(temp)
        for i in range(0,len(temp)):
            temp[i]=sorted_journey_release_date(temp[i])
            check[i]=fitness(temp[i])
        yy=min(check)
        for i in range(0,len(temp)):
            temp[i]=sorted_journey_release_date(temp[i])
            if fitness(temp[i])==yy:
                h=i
                break
        print("current_solution is:",current_solution)
        if yy<current_solution:
            drone_journey=copy.deepcopy(temp[h])
            current_solution=yy
            test_split+=1
def change(index):
    global drone_journey
    global current_solution
    global test_check
    test_check=0
    k=0
    index=2
    temp=[]
    fake=copy.deepcopy(drone_journey)
    weight=sum_outarray_weight(drone_journey[index+1])
    while weight<=capacity_drone:
        if weight+customer[fake[index][len(fake[index])-1]].weight>capacity_drone:
            break
        else:
            fake[index+1].insert(0,fake[index][len(fake[index])-1])
            if drone_flight_time(fake[index+1])>1:
                break
            weight=weight+customer[fake[index][len(fake[index])-1]].weight
            fake[index].pop(len(fake[index])-1)
            if fake[index]==[]:
                fake.remove([])
                k+=1
            fake_cp=copy.deepcopy(fake)
            temp.append(fake_cp)
            if k==1:
                break
    if len(temp)!=0:
        check=[0]*len(temp)
        for i in range(0,len(temp)):
            temp[i]=sorted_journey_release_date(temp[i])
            check[i]=fitness(temp[i])
        yy=min(check)
        print("yy is:",yy)
        for i in range(0,len(temp)):
            temp[i]=sorted_journey_release_date(temp[i])
            if fitness(temp[i])==yy:
                h=i
                break
        if yy<current_solution:
            drone_journey=copy.deepcopy(temp[h])
            current_solution=yy
            test_check+=1
while number_test_split<=len(drone_journey)-2 or number_test_check<=len(drone_journey)-2:
    number_test_split=0
    number_test_check=0
    for i in range(0,len(drone_journey)-1):
        split(i)
        if test_split==0:number_test_split+=1
        elif test_split==1:break
        change(i)
        if test_check==0:number_test_check+=1
        elif test_check==1:break
fitness(drone_journey)
print("Drone journey is:",drone_journey)
print("Time is",current_solution)





