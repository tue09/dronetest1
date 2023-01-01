import queue
import random
import numpy as np
import math
#
#Data
number_customer=20
number_truck=3
number_drone=3
speed_truck=30
speed_drone=45
capicity_drone=3
file_object=open('C101_0.5.dat')
data=file_object.readlines()
coordinates=[0]*(number_customer+1)
for i in range(0,len(coordinates)):
    coordinates[i]=[]
time_release=[0]*(number_customer+1)
for i in range(0,21):
    coordinates[i].append(int(data[i+5][0:2]))
    coordinates[i].append(int(data[i+5][3:5]))
    time_release[i]=int(data[i+5][18:len(data[i+5])-1])
class cus:
    def __init__(self, coordinates,release_date,weight):
        self.coordinates = coordinates
        self.release_date=release_date
        self.weight=weight
depot=coordinates[0]
customer=[0]*(number_customer+1)
customer[0]=cus(coordinates[0],0,0)
for i in range(1,len(customer)):
    customer[i]=cus(coordinates[i],time_release[i],1)
truck_path_array=[1,3,5,7,8,0,2,4,10,11,13,15,0,9,18,20,19,6,12,17,16,14]
x=[0.4,0.5,0.8,0.75,0.15,0.9,0.3,0.25,0.65,0.7,0.13,0.45,0.1,0.2,0.5,0.11,0.25,0.36,0.19,0.78,0.89,0.9]
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
def sorted_package_by_weight(array,capicity):
    x=[]
    k=0
    x.append([])
    array1=[]
    for i in range(0,len(array)):
        array1.append(array[i])
    if len(array1)!=0:
        while len(array1)!=0:
            s=0
            for j in range(0,100):
                if len(array1)!=0:
                    if s+customer[array1[0]].weight<=capicity:
                        x[k].append(array1[0])
                        s+=customer[array1[0]].weight
                        array1.pop(0)
                    elif s+customer[array1[0]].weight>capicity: break
            x.append([])
            k+=1
    for i in range(0,len(x)):
        if len(x[i])==0:
            x.pop(i)
    return x
decryption=change_array(truck_path_array,x,20,3)
# a is an array satisfying decryption[a[i]]=0 for all i in range(0,len(a))
a=[]
for i in range(0,len(truck_path_array)+1):
    if decryption[0,i]==0:
        a.append(i)
package_queue=[0]*number_truck
for i in range(0,len(package_queue)):
    package_queue[i]=[]
for i in range(0,len(package_queue)-1):
    for j in range(a[i]+1,a[i+1]):
        package_queue[i].append([0,truck_path_array[j-1]])
    package_queue[i].append([999999,999])
for i in range(a[len(a)-1]+1,len(truck_path_array)+1):
    package_queue[len(package_queue)-1].append([0,truck_path_array[i-1]])
package_queue[len(package_queue)-1].append([999999,999])
drone_queue=queue.PriorityQueue()
for i in range(0,number_drone):
    drone_queue.put(0)
ite=[0]*number_truck
truck_time=[0]*number_truck
#
# Trucks move from depot :
for i in range(0,len(truck_time)):
    if decryption[1][a[i]+ite[i]][0]==-1:
        truck_time[i]=truck_time[i]+(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_truck
        print("Truck %i : 0"%i,"to %i"%truck_path_array[a[i]+ite[i]])
    else:
        truck_time[i]=truck_time[i]+max_outarray_release_date(decryption[1][a[i]+ite[i]])+(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_truck
        print("Truck %i : 0"%i,"to %i"%truck_path_array[a[i]+ite[i]])
for i in range(0,len(truck_time)):
    if decryption[1][a[i]+ite[i]+1][0]==-1:
        package_queue[i][ite[i]][0]=truck_time[i]-(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_drone
    else:
        package_queue[i][ite[i]][0]=max(max_outarray_release_date(decryption[1][a[i]+ite[i]+1]),truck_time[i]-(distance(depot,customer[package_queue[i][ite[i]][1]].coordinates))/speed_drone)
#
# trucks and drones move
for z in range(0,number_customer+1):
    compare=[]
    v=drone_queue.get()
    for i in range(0,len(package_queue)):
        compare.append(max(package_queue[i][ite[i]][0],v))
    l=min(compare)
    for i in range(0,len(package_queue)):
        if max(package_queue[i][ite[i]][0],v)==l:
            h=i
            ite[i]+=1
            break
    m=0
    for i in range(0,len(package_queue)):
        if compare[i]==999999:
            m+=1
    if m==len(package_queue):
        break
    drone_queue.put(v)
    if package_queue[h][ite[h]][1]!=999:
        if decryption[1][a[h]+ite[h]][0]!=-1:
            u=sorted_release_date(decryption[1][a[h]+ite[h]])
            p=sorted_package_by_weight(u,capicity_drone)
            element_put_in_drone_queue=[0]*len(p)
            for i in range(0,len(p)):
                timedr=drone_queue.get()
                drone_queue.put(max(timedr,package_queue[h][ite[h]-1][0])+2*distance(customer[decryption[0][a[h]+ite[h]]].coordinates,customer[decryption[0][a[h]+ite[h]-1]].coordinates))
                element_put_in_drone_queue[i]=(max(timedr,package_queue[h][ite[h]-1][0])+2*distance(customer[decryption[0][a[h]+ite[h]]].coordinates,customer[decryption[0][a[h]+ite[h]-1]].coordinates))

        if decryption[1][a[h]+ite[h]][0]==-1:
            truck_time[h]=truck_time[h]+(distance(customer[package_queue[h][ite[h]][1]].coordinates,customer[package_queue[h][ite[h]-1][1]].coordinates))/speed_truck
            print("Truck",h,":",truck_path_array[a[h]+ite[h]-1],"to",truck_path_array[a[h]+ite[h]])
        else:
            truck_time[h]=element_put_in_drone_queue[len(p)-1]-(distance(customer[decryption[0][a[h]+ite[h]-1]].coordinates,customer[decryption[0][a[h]+ite[h]]].coordinates)/speed_drone)+(distance(customer[package_queue[h][ite[h]-1][1]].coordinates,customer[package_queue[h][ite[h]][1]].coordinates))/speed_truck
            print("Truck",h,":",truck_path_array[a[h]+ite[h]-1],"to",truck_path_array[a[h]+ite[h]])
        if decryption[1][a[h]+ite[h]+1][0]==-1:
            package_queue[h][ite[h]][0]=truck_time[h]-(distance(depot,customer[package_queue[h][ite[h]][1]].coordinates))/speed_drone
        else:
            package_queue[h][ite[h]][0]=max(max_outarray_release_date(decryption[1][a[h]+ite[h]+1]),truck_time[h]-(distance(customer[package_queue[h][ite[h]-1][1]].coordinates,customer[package_queue[h][ite[h]][1]].coordinates))/speed_drone)
#
#trucks back to depot
last_point_package_queue=[]
for i in range(0,len(a)-1):
    last_point_package_queue.append(a[i+1]-1)
last_point_package_queue.append(truck_path_array[len(truck_path_array)-1])
for i in range(0,number_truck):
    truck_time[i]=truck_time[i]+distance(customer[last_point_package_queue[i]].coordinates,depot)/speed_truck
    print("Truck %i :"%i,last_point_package_queue[i],"to 0")
Time=max(truck_time)
print("Time is: ",Time)
