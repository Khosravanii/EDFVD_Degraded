import random as r
from math import gcd
import sys
from os import system, name 

# define our clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
clear()    
    
#Reading Task Set
def Task_Set():
    Temp=[]
    Task_Set=[]
    Tasks=[]
    #Reading file to a list
    data = open('Tasks.txt','r')
    data.seek(22)#Doesn't consider first line of file
    tasks= data.readlines()
    for line in tasks:
        stripped_task=line.strip('\n')
        Temp.append(stripped_task)
    #split item
    for i in Temp:
        li = list(i.split(","))
        Tasks.append( li)
    #Convert every item in task set to integer
    for task in Tasks:
        Task_Set.append(list(map(int, task)))
    # Add Task ID for Each Task
    i=0
    while (i < len(Task_Set)):
           Task_Set[i].insert(0,i+1)
           Task_Set[i].insert(6,int(0)) # Release Time
           Task_Set[i].insert(4,Task_Set[i][3]) # Period=Deadline
           i+=1
    return Task_Set
tasks= Task_Set()
tasks_show=Task_Set()
n=len(tasks)
#print(Len_Task_Set)


#Calculating X
def X(tasks,n):
    u_lo_lo,u_hi,u_lo_hi,u_lo_total=0,0,0,0

    for i in range(n):
        if tasks[i][5]==0:
            u_lo_lo +=tasks[i][1]/tasks[i][4]

        elif tasks[i][5]==1:
            u_hi +=tasks[i][2]/tasks[i][4]
            u_lo_hi +=tasks[i][1]/tasks[i][4]
        else:
            break
    u_lo_total=u_lo_lo + u_lo_hi
    #ensuring that EDF-VD successfully schedules all LO-criticality behaviors
    X = u_lo_hi / (1-u_lo_lo)
    #ensuring that EDF-VD successfully schedules all HI -criticality behaviors
    chk = X * u_lo_lo + u_hi
    if chk <=1:
        return round(X,2)
    else:
        return 1
    print("X is : %s"%round(X,2))
X=X(tasks,n)


def show_Tasks(Task_show,n,X):
    
    for i in range(n):
        if tasks_show[i][5] >0:
            tasks_show[i].append(X * tasks[i][3])
        else:
            tasks_show[i].append('-')
    return tasks_show
show=show_Tasks(tasks_show,n,X)
print("TID\tC(LO)\tC(HI)\tD\tP\tL\tRT\tVD")
for i in show:
    print("")
    for j in i:
        print(j, end = '\t')
print("\n")

def tasks_HI():
    tasks=Task_Set()
    n=len(tasks)
    tasks_HI=[]
    for i in range(n):
        if tasks[i][5]==1:
            tasks_HI.append(tasks[i])
        else:
            tasks_HI.append(0)
    return tasks_HI
tasks_HI=tasks_HI()

def tasks_LO(X):
    tasks=Task_Set()
    n=len(tasks)
    tasks_LO=[]
    for i in range(n):
        tasks_LO.append(tasks[i])
        if tasks_LO[i][5]==1:
            tasks_LO[i][3]= X*tasks_LO[i][3]
            #tasks_LO[i][2]=tasks_LO[i][3]
    return tasks_LO
tasks_LO=tasks_LO(X)
#print("\nQLO:",tasks_LO)
#print("QHI:",tasks_HI)

#Calculating Hyper Perios as LCM
def LCM(Task_Set):
    P=[]
    for i in range(n):
        P.append(tasks[i][4])
    lcm = P[0]
    for i in P[1:]:
        lcm =int( lcm*i/gcd(lcm, i))
    return lcm
lcm=LCM(Task_Set)
print("Hyper Period is: ",lcm)
print("X-parameter is : %s"%(X))

def utilization(Task_Set,Len_Task_Set):
    u_lo_lo,u_hi,u_lo_hi,u_lo_total=0,0,0,0
    for i in range(n):
        if tasks[i][5]==0:
            u_lo_lo +=tasks[i][1]/tasks[i][4]
        elif tasks[i][5]==1:
            u_hi +=tasks[i][2]/tasks[i][4]
            u_lo_hi +=tasks[i][1]/tasks[i][4]
        else:
            break
    u_lo_total=u_lo_lo + u_lo_hi
    print("Utilization in Low Criticality mode: %s"%round(u_lo_total,2))
    print("Utilization in High Criticality mode: %s"%round(u_hi,2))
    if u_hi <=1 and u_lo_total <=1:
        return 1
    else:
        return 2
util=utilization(tasks,n)
#print('utilization of task set is %s'%util,end='\n')
print()
def TimeLeft(Task_Set,Len_Task_Set):
    time_left=[]
    for i in range (Len_Task_Set):
        if Task_Set[i][6]==0:
            time_left.append(Task_Set[i][1])
        else:
             time_left.append(int(0))
    return time_left
timeLeft=TimeLeft(tasks,n)
#print('\nTime left set:\n%s\n\n'%timeLeft)

def array_sort(instances,index=1):
    for i in range(len(instances)):
        tmp = instances[i].copy()
        k = i
        while k > 0 and tmp[index] < instances[k-1][index]:
            instances[k] = instances[k - 1].copy()
            k -= 1
        instances[k] = tmp.copy()
    return instances
    
def EDF_VD(tasks,n,lcm,util):
    i=0
    instances=[]
    for i in range(n):
        j=0
        while 1:
            if j*tasks[i][3]<lcm:
                instances.append([tasks[i],j*tasks[i][3]])
                j+=1
            else:
                break

    instances = array_sort(instances)
    #for x in range(len(instances)):
        #print(instances[x])
    timeLine=[]
    time=0
    while(time <lcm):
        if util ==1:            
            sig=1
            last_criticality = criticality = 0
            while time<lcm:
                for i in range(n):
                    if (time>1 and ((time%tasks[i][3]==0 and time>tasks[i][6]) or
                    time==tasks[i][6])) or (last_criticality!=criticality and timeLeft[i]==tasks[i][1]):
                        if criticality==1:
                            timeLeft[i]=tasks[i][2]
                        elif criticality==0:
                            timeLeft[i]=tasks[i][1]
                last_criticality=criticality 
                anyrun=0
                for j in range(len(instances)):
                    is_break = False
                    is_pop = False
                    time_spend=0
                    for k in range(len(timeLine)-1,0,-1):
                        if instances[j][0][0]==timeLine[k][0] and timeLine[k][1]!="X":
                            time_spend+=1
                        else:
                            break
                    if timeLeft[instances[j][0][0]-1]>0:
                        for k in range(j+1,len(instances)):    
                            if j<len(instances)-1 and \
                                (instances[j][1]==instances[k][1] or (time>=instances[k][1] and (instances[j][0][5]<instances[k][0][5] \
                                or (instances[j][0][5]==1 and instances[k][0][5]==1)))) and ((criticality==0 and \
                                instances[k][1]+tasks_LO[instances[k][0][0]-1][3]<instances[j][1]+tasks_LO[instances[j][0][0]-1][3]) or \
                                (criticality==1 and instances[k][1]+instances[k][0][3]<instances[j][1]+instances[j][0][3])):
                                
                                instances[j],instances[k]=instances[k],instances[j] 
                                
                        if criticality==1 and instances[j][0][5]==0:
                            criticality=0
                        if criticality==0 or (criticality==1 and instances[j][0][5]>0):
                            if time+timeLeft[instances[j][0][0]-1]>instances[j][1]+instances[j][0][3]:
                                timeLine.append(['%s X'%instances[j][0][0],criticality])
                                if time+1==instances[j][1]+instances[j][0][3]:
                                    timeLeft[instances[j][0][0]-1]=1
                            else:
                                timeLine.append([instances[j][0][0],criticality])
                            timeLeft[instances[j][0][0]-1]-=1
                            anyrun=1
                            if timeLeft[instances[j][0][0]-1]==0:
                                is_pop = True
                            is_break = True
                    #Overrun Mode
                    if anyrun==1 and instances[j][0][5]>0 and timeLeft[instances[j][0][0]-1]==0 and criticality ==0:
                        #signal=int(input("Task ("+str(instances[j][0][0])+") Time ("+str(time)+") signal %d/0:"%(sig)))
                        signal =r.randint(1, 100000)
                        if sig==signal:
                            print('No Completion Signal for Task %s at %s'%(instances[j][0][0],time+1))
                            timeLeft[instances[j][0][0]-1]=(instances[j][0][2]-instances[j][0][1])
                            temp=1
                            for k in range(j+1,len(instances)):
                                if instances[k][0][0]== instances[j][0][0]:
                                    temp=k
                                    break
                            for k in range(len(instances)-1,j,-1):
                                if instances[k][0][5]==0 and instances[k][1]>=instances[j][1] and instances[k][1] <= instances[temp][1]:
                                    timeLeft[instances[k][0][0]-1]=0
                                    instances.pop(k)
                        
                                    if is_pop and k==j:
                                        is_pop = False

                            criticality=1
                            is_pop = False
                            is_break = True
                    
                    if is_pop:
                        instances.pop(j)
                    if is_break:
                        break                 
                if anyrun==0:
                    timeLine.append(['-','I'])
                    criticality = 0
                time+=1    
            mn=0
            mx=0
            
            print('Starting Scheduling Task Set:',end='\n')
            print('*********************************************************************')
            print("* Start Time\t","End Time\t", "Task ID\t","System Criticality *")
            for i in range(lcm):
                if i>0 and (timeLine[i][0]!=timeLine[i-1][0] or timeLine[i][1]!=timeLine[i-1][1]):
                    mx=i
                    print("*",mn,"\t\t",mx,"\t\t", "["+str(timeLine[i-1][0])+"]\t\t\t",  timeLine[mn][1],"\t    *")
                    
                    mn=i
                if i==lcm-1:
                    mx=lcm
                    print("*",mn,"\t\t",mx,"\t\t", "["+str(timeLine[i][0])+"]\t\t\t",  timeLine[mn][1],"\t    *")
            print('*********************************************************************')
        else:
            print('Task set is not feasible.(Utilization Must be <=1.)')
            break
#for x in range(100):        
EDF_VD(tasks,n,lcm,util)
