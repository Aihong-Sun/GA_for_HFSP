import random
import numpy as np
import copy
from Scheduling import Scheduling as Sch
from Instance import Job,State,Machine,PT
import matplotlib.pyplot as plt

class GA:
    def __init__(self,J_num,State,Machine,PT):
        self.State=State
        self.Machine=Machine
        self.PT=PT
        self.J_num=J_num
        self.Pm=0.2
        self.Pc=0.9
        self.Pop_size=100

    # 随机产生染色体
    def RCH(self):
        Chromo = [i for i in range(self.J_num)]
        random.shuffle(Chromo)
        return Chromo

    # 生成初始种群
    def CHS(self):
        CHS = []
        for i in range(self.Pop_size):
            CHS.append(self.RCH())
        return CHS

    #选择
    def Select(self, Fit_value):
        Fit = []
        for i in range(len(Fit_value)):
            fit = 1 / Fit_value[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        idx = np.random.choice(np.arange(len(Fit_value)), size=len(Fit_value), replace=True,
                               p=(Fit) / (Fit.sum()))
        return idx

    # 交叉
    def Crossover(self, CHS1, CHS2):
        T_r = [j for j in range(self.J_num)]
        r = random.randint(2, self.J_num)  # 在区间[1,T0]内产生一个整数r
        random.shuffle(T_r)
        R = T_r[0:r]  # 按照随机数r产生r个互不相等的整数
        # 将父代的染色体复制到子代中去，保持他们的顺序和位置
        H1=[CHS1[_] for _ in R]
        H2=[CHS2[_] for _ in R]
        C1=[_ for _ in CHS1 if _ not in H2]
        C2=[_ for _ in CHS2 if _ not in H1]
        CHS1,CHS2=[],[]
        k,m=0,0
        for i in range(self.J_num):
            if i not in R:
                CHS1.append(C1[k])
                CHS2.append(C2[k])
                k+=1
            else:
                CHS1.append(H2[m])
                CHS2.append(H1[m])
                m+=1
        return CHS1, CHS2

    # 变异
    def Mutation(self, CHS):
        Tr = [i_num for i_num in range(self.J_num)]
        # 机器选择部分
        r = random.randint(1, self.J_num)  # 在变异染色体中选择r个位置
        random.shuffle(Tr)
        T_r = Tr[0:r]
        K=[]
        for i in T_r:
            K.append(CHS[i])
        random.shuffle(K)
        k=0
        for i in T_r:
            CHS[i]=K[k]
            k+=1
        return CHS

    def main(self):
        BF=[]
        x=[_ for _ in range(self.Pop_size+1)]
        C=self.CHS()
        Fit=[]
        for C_i in C:
            s=Sch(self.J_num,self.Machine,self.State,self.PT)
            s.Decode(C_i)
            Fit.append(s.fitness)
        best_C = None
        best_fit=min(Fit)
        BF.append(best_fit)
        for i in range(self.Pop_size):
            C_id=self.Select(Fit)
            C=[C[_] for _ in C_id]
            for Ci in range(len(C)):
                if random.random()<self.Pc:
                    _C=[C[Ci]]
                    CHS1,CHS2=self.Crossover(C[Ci],random.choice(C))
                    _C.extend([CHS1,CHS2])
                    Fi=[]
                    for ic in _C:
                        s = Sch(self.J_num, self.Machine, self.State, self.PT)
                        s.Decode(ic)
                        Fi.append(s.fitness)
                    C[Ci]=_C[Fi.index(min(Fi))]
                    Fit.append(min(Fi))
                elif random.random()<self.Pm:
                    CHS1=self.Mutation(C[Ci])
                    C[Ci]=CHS1
            Fit = []
            Sc=[]
            for C_i in C:
                s = Sch(self.J_num, self.Machine, self.State, self.PT)
                s.Decode(C_i)
                Sc.append(s)
                Fit.append(s.fitness)
            if min(Fit)<best_fit:
                best_fit=min(Fit)
                best_C=Sc[Fit.index(min(Fit))]
            BF.append(best_fit)
        plt.plot(x,BF)
        plt.show()
        best_C.Gantt()

if __name__=="__main__":
    g=GA(Job,State,Machine,PT)
    g.main()
