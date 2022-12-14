import pandas as pd 
import os
import matplotlib.pyplot as plt

def get_single_route(vehicle,root='/home/xjm/trajectory/data'):
    df = pd.read_csv(os.path.join(root, 'final.csv'), index_col=0)
    get_single_route(vehicle, df)

def get_single_route(vehicle, df):
    df = df[df['vehicle_id']==vehicle]
    df = df[df['speed']!=0]
    return list(df['eid'])  
  
def eid_analyse(df, root='/home/xjm/trajectory/data'):
    df = df[df['speed']!=0]
    df1 = df['eid'].value_counts()
    print(df1.head())
    df1.to_csv(os.path.join(root, 'eid_analyse.csv'))
    plt.plot(list(range(len(df1))), df1)
    plt.savefig('out.png')
    
    
    
root='/home/xjm/trajectory/data'
df = pd.read_csv(os.path.join(root, 'final.csv'), index_col=0)
#route = get_single_route(2034, df)
#print(route)
eid_analyse(df)
    
    