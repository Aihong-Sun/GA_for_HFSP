import random
import matplotlib.pyplot as plt
from Instance import Job,State,Machine,PT
import numpy as np


class Item:
    def __init__(self):
        self.start=[]
        self.end=[]
        self._on=[]
        self.T=[]
        self.last_ot=0
        self.L=0

    def update(self,s,e,on,t):
        self.start.append(s)
        self.end.append(e)
        self._on.append(on)
        self.T.append(t)
        self.last_ot=e
        self.L+=t

class Scheduling:
    def __init__(self,J_num,Machine,State,PT):
        self.M=Machine
        self.J_num=J_num
        self.State=State
        self.PT=PT
        self.Create_Job()
        self.Create_Machine()
        self.fitness=0

    def Create_Job(self):
        self.Jobs=[]
        for i in range(self.J_num):
            J=Item()
            self.Jobs.append(J)

    def Create_Machine(self):
        self.Machines=[]
        for i in range(len(self.M)):    #突出机器的阶段性，即各阶段有哪些机器
            State_i=[]
            for j in range(self.M[i]):
                M=Item()
                State_i.append(M)
            self.Machines.append(State_i)

    #每个阶段的解码
    def Stage_Decode(self,CHS,Stage):
        for i in CHS:
            last_od=self.Jobs[i].last_ot
            last_Md=[self.Machines[Stage][M_i].last_ot for M_i in range(self.M[Stage])] #机器的完成时间
            last_ML = [self.Machines[Stage][M_i].L for M_i in range(self.M[Stage])]     #机器的负载
            M_time=[self.PT[Stage][M_i][i] for M_i in range(self.M[Stage])]             #机器对当前工序的加工时间
            O_et=[last_Md[_]+M_time[_] for _ in range(self.M[Stage])]
            if O_et.count(min(O_et))>1 and last_ML.count(last_ML)>1:
                Machine=random.randint(0,self.M[Stage])
            elif O_et.count(min(O_et))>1 and last_ML.count(last_ML)<1:
                Machine=last_ML.index(min(last_ML))
            else:
                Machine=O_et.index(min(O_et))
            s, e, t=max(last_od,last_Md[Machine]),max(last_od,last_Md[Machine])+M_time[Machine],M_time[Machine]
            self.Jobs[i].update(s, e,Machine, t)
            self.Machines[Stage][Machine].update(s, e,i, t)
            if e>self.fitness:
                self.fitness=e

    #解码
    def Decode(self,CHS):
        for i in range(self.State):
            self.Stage_Decode(CHS,i)
            Job_end=[self.Jobs[i].last_ot for i in range(self.J_num)]
            CHS = sorted(range(len(Job_end)), key=lambda k: Job_end[k], reverse=False)

    #画甘特图
    def Gantt(self):
        fig = plt.figure()
        M = ['red', 'blue', 'yellow', 'orange', 'green', 'moccasin', 'purple', 'pink', 'navajowhite', 'Thistle',
             'Magenta', 'SlateBlue', 'RoyalBlue', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
             'navajowhite','navy', 'sandybrown']
        M_num=0
        for i in range(len(self.M)):
            for j in range(self.M[i]):
                for k in range(len(self.Machines[i][j].start)):
                    Start_time=self.Machines[i][j].start[k]
                    End_time=self.Machines[i][j].end[k]
                    Job=self.Machines[i][j]._on[k]
                    plt.barh(M_num, width=End_time - Start_time, height=0.8, left=Start_time, \
                             color=M[Job], edgecolor='black')
                    plt.text(x=Start_time + ((End_time - Start_time) / 2 - 0.25), y=M_num - 0.2,
                             s=Job+1, size=15, fontproperties='Times New Roman')
                M_num += 1
        plt.yticks(np.arange(M_num + 1), np.arange(1, M_num + 2), size=20, fontproperties='Times New Roman')

        plt.ylabel("机器", size=20, fontproperties='SimSun')
        plt.xlabel("时间", size=20, fontproperties='SimSun')
        plt.tick_params(labelsize=20)
        plt.tick_params(direction='in')
        plt.show()
#
# Sch=Scheduling(J_num,Machine,State,PT)

