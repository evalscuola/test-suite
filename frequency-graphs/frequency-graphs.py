import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#vn= [2,3,6,6,7,8,9,9,10,7]
#vu= [1,1,2,3,6,7,7,7,8,9]

df = pd.read_csv("analysis.csv", sep='\t', header = None, \
    names = ['item', 'difficulty', 'discrimination', \
    'keys', 'A', 'B', 'C', 'D', 'empty'])
#df = pd.DataFrame({'vn': vn, 'vu': vu})

print(df)

plt.rcParams["figure.figsize"]=8,6

g=sns.histplot(data=df.difficulty, bins=10, edgecolor='black')
g.set(xlabel = 'Difficulty Index [%]\n ← Difficult Item      Easy Item →', ylabel = 'Number of Items')
#High Difficulty      Low Difficulty
plt.savefig("difficulty.png", dpi=400)

plt.clf()

#plt.show()

g1=sns.histplot(data=df.discrimination, bins=10, edgecolor='black') #stat="density",
g1.set(xlabel = 'Discrimination Index [%]\n ← Weak      Good →', ylabel = 'Number of Items')

plt.savefig("discrimination.png", dpi=400)
# show the graph
#plt.show()
