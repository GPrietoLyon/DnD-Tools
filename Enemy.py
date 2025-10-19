import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

class Enemy:
    def __init__(self,Name, HP,AC):
        self.HP = HP
        self.AC = AC


    def LoadHitRolls(self,HitRolls):
        self.Itnum = len(HitRolls[0])
        self.HitRolls = np.array(HitRolls)
        self.AttackNumber = len(self.HitRolls)
    def LoadDamageRolls(self,DamageRolls):
        self.DamageRolls = np.array(DamageRolls)


    def PassAC(self):
        HitMasks=[]
        for i in range(0,self.AttackNumber):
            HitNumber=self.HitRolls[i]
            HitMask= ((HitNumber>=self.AC) & (HitNumber!=min(HitNumber)) )| (HitNumber==max(HitNumber))
            HitPercentage = len(HitNumber[HitMask]) / len(HitNumber) * 100   
            HitMasks.append(HitMask)
            print("Attack Number "+str(i+1)+ " Hit Chance : ",np.round(HitPercentage))
        return HitMasks

    def DamageSim(self,showTotal=False, showIndividual=False):
        self.HPSim=[self.HP]*self.Itnum
        TotalDamage=[]
        HitMasks=self.PassAC()
        for i in range(0,self.AttackNumber):
            HitMask=HitMasks[i]
            DamageNumber=self.DamageRolls[i]
            EffDamage=DamageNumber
            EffDamage[~HitMask]=0
            if showIndividual:
                fig, ax = plt.subplots()
                ax.hist(EffDamage, density=True, bins=range(min(EffDamage), max(EffDamage) + 2))
                ax.set_ylabel("Probability")
                ax.set_xlabel("Damage of Individual Attack")
                ax.axvline(x=np.median(EffDamage), color='black', linestyle='dashed', linewidth=2)
                plt.show()
                
            TotalDamage.append(EffDamage)
        self.IndividualDamage = TotalDamage
        self.TotalDamage = np.sum(TotalDamage,axis=0)
        if showTotal:                    
            fig, ax = plt.subplots()
            ax.hist(self.TotalDamage, bins=range(min(self.TotalDamage), max(self.TotalDamage) + 1), density=True)
            ax.set_ylabel("Probability")
            ax.set_xlabel("Damage of All Attacks Combined")
            ax.axvline(x=np.median(self.TotalDamage), color='black', linestyle='dashed', linewidth=2)
            ax.text(0.8, 0.9, f"Median Damage: {np.median(self.TotalDamage)}", ha='center', va='center', transform=ax.transAxes)
            plt.show()
            