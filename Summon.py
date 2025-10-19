import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

class Summon:
    def __init__(self,Name,AttackNumber,Hit,Damage,DamageMod,Itnum=100):
        self.Itnum=Itnum
        self.AttackNumber = AttackNumber
        self.Hit = Hit
        self.Damage = [Damage[i] for i in range(AttackNumber)]
        self.Name = Name
        self.DamageMod = DamageMod

        assert self.AttackNumber == len(self.Hit), "Hit array length does not match AttackNumber"
        assert self.AttackNumber == len(self.DamageMod), "Damage array length does not match AttackNumber"
        assert self.AttackNumber == len(self.Damage), "Damage array length does not match AttackNumber"


    def RollHit(self,hasAdvantage=False,ShowPlot=False):
        self.HitRolls = [ np.random.randint(1,21,self.Itnum)+self.Hit[i]  
                          for i in range(0,self.AttackNumber)]
        if hasAdvantage:
            self.HitRolls = [np.maximum(self.HitRolls[i],np.random.randint(1,21,self.Itnum)+self.Hit[i]) 
                             for i in range(0,self.AttackNumber)]

        self.Critsmask = [self.HitRolls[i] == 20+self.Hit[i]  for i in range(0,self.AttackNumber)]
        
        if ShowPlot:
            for i,rolls in enumerate(self.HitRolls):
                plt.hist(rolls, density=True,bins=range(min(rolls),max(rolls)+2))
                plt.title("Attack "+str(i+1)+ ". Lowest: "+str(min(rolls))+" Highest: "+str(max(rolls))+" Advantage: "+str(hasAdvantage))
                plt.ylabel("Probability")
                plt.xlabel("Hit Roll")
                plt.show()


    def RollDamage(self,ShowPlot=False):
        self.DamageRolls = []
        Keys=["d4","d6","d8","d10","d12"]
        att=0
        for Dice,mod in zip(self.Damage,self.DamageMod):
            mask=np.array(list(Dice.values()))!=0
            DiceKeys = np.array(Keys)[mask][0]
            DiceValues = np.array(list(Dice.values()))[mask][0]
            DamageEach=[np.random.randint(1,int(DiceKeys[1:])+1,self.Itnum) for i in range(0,DiceValues)] 
            TotalDamage=np.sum(DamageEach,axis=0)
            TotalDamage+=mod
            
            CritDamage=[]
            for C in self.Critsmask[att]:
                if C==False:
                    crit=0
                if C==True:
                    crit=np.array([np.random.randint(1,int(DiceKeys[1:])+1) for i in range(0,DiceValues)])
                    crit=np.sum(crit)
                CritDamage.append(crit)
            TotalDamage+=np.array(CritDamage)
            self.DamageRolls.append(TotalDamage)
            att+=1


            if ShowPlot:
                plt.hist(TotalDamage, density=True,bins=range(min(TotalDamage),max(TotalDamage)+1))
                plt.ylabel("Probability")
                plt.title("Damage Roll. Lowest: "+str(min(TotalDamage))+" Highest: "+str(max(TotalDamage)))
                plt.xlabel("Damage Roll")
                plt.show()

