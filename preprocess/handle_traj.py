from operator import index
import pandas as pd
import os

def handle(root='/home/xjm/trajectory/data'):
    match_file = os.path.join(root, "match.csv")
    point_file = os.path.join(root, "points.csv")
    edge_file = os.path.join(root, "edges.csv")
    traj_file = os.path.join(root, "trajectory.csv")
    # load csv
    match_df = pd.read_csv(match_file, usecols=['pid', 'eid', 'dist'])
    point_df = pd.read_csv(point_file, index_col=0)
    point_df['pid'] = point_df.index
    point_df.columns = ['lat', 'lon', 'hash', 'pid']
    
    edge_df = pd.read_csv(edge_file, index_col=0)
    edge_df['eid'] = edge_df.index
    
    traj_df = pd.read_csv(traj_file, index_col=0)
    traj_df['lon'] = traj_df['location'].apply(lambda x: eval(x)[-1])
    traj_df['lat'] = traj_df['location'].apply(lambda x: eval(x)[0])
    traj_df = traj_df.drop(['location'], axis=1)
    print(match_df.head())
    print(point_df.head())
    print(edge_df.head())
    print(traj_df.head())
    df = pd.merge(traj_df, point_df, on=['lon', 'lat'], how='left')
    df = pd.merge(df, match_df, on=['pid'], how='left')
    df = pd.merge(df, edge_df, on=['eid'], how='left')
    df.to_csv(os.path.join(root, 'final.csv'))
    print(df.head())

handle()