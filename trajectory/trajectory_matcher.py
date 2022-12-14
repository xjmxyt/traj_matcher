from joblib import Parallel, delayed
import osmnx as ox
import pandas as pd
from trajectory.trajectory import get_trajectory_df
from map.load_region import load_r
import time 
import warnings

warnings.filterwarnings("ignore")

def edges_r(b, G):
    '''
        :param 
            b: pandas.series
            G: graph
    '''
    warnings.filterwarnings("ignore")
    # dicty=defaultdict(int)
    # for i in range(0,len(b)):
    loc = list(map(float, b['location'][1:-1].split(',')))
    #loc = eval(b['location'])
    X = float(loc[1])
    Y = float(loc[0])
    c, dist = ox.distance.nearest_edges(G, X, Y, return_dist=True)
    (u, v, key) = c
    return *b.values, (u, v, key), dist

def get_bbox_from_df(df):
    df_temp = df.copy()
    df_temp['lat'] = df_temp['location'].apply(lambda x: list(map(float, x[1:-1].split(',')))[0])
    df_temp['log'] = df_temp['location'].apply(lambda x: list(map(float, x[1:-1].split(',')))[1])
    return df_temp['lat'].min(), df_temp['lat'].max(), df_temp['log'].min(), df_temp['log'].max()

def match_edge(G, df:pd.DataFrame)->pd.DataFrame:
    tasks = [delayed(edges_r)(df.iloc[i], G) for i in range(len(df))]
    multi_work =  Parallel(n_jobs=-1, verbose=10)
    res = multi_work(tasks)
    cols = list(df.columns)
    cols.extend(["road_id","dist"])
    return pd.DataFrame(res, columns=cols)


def location_match(trajectory_path, graph_path, limit=-1):
    trajectory_df = get_trajectory_df(trajectory_path, update=False)
    pos_df = get_diff_points(trajectory_df)
    G = load_r(graph_path, bbox=[31.41, 31.03, 121.31, 121.65])
    if limit>0:
        trajectory_df = pos_df.iloc[:limit]
    df = match_edge(G, trajectory_df)
    return df    
        

def trajectory_match(trajectory_path, graph_path, limit=-1):
    '''
        match location of trajectory to graph edges 
        :param
            trajectory_path: path of trajectory.csv
            graph_path: path of graph.xml
    '''
    trajectory_df = get_trajectory_df(trajectory_path, update=False)
    print("size of trajectory: ", len(trajectory_df))
    G = load_r(graph_path, bbox=[31.41, 31.03, 121.31, 121.65])
    if limit>0:
        trajectory_df = trajectory_df.iloc[:limit]
    df = match_edge(G, trajectory_df)
    return df

def get_diff_points(df):
    '''
        get different locations from df
    '''
    locs = list(set(list(df['location'])))
    return pd.DataFrame(locs, columns=['location'])

if __name__ == "__main__":
    # 121.37,31.34   121.65,31.15
    data_root = r'../data/'
    trajectory_path = data_root + 'trajectory.csv'    
    graph_path = data_root + 'shanghai.xml'
    begin_time = time.time()
    df = location_match(trajectory_path=trajectory_path, graph_path=graph_path, limit=1000)
    df.to_csv(data_root+r"temp.csv")
    '''
    print("graph_path:", graph_path)
    df = trajectory_match(trajectory_path=trajectory_path, graph_path=graph_path, limit=1000)
    print(df.head())
    print("time used: ", time.time() - begin_time)
    df.to_csv("temp.csv")
    '''
    #print(get_bbox_from_df(get_trajectory_df(trajectory_path, update=False)))



