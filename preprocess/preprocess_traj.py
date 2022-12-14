from antigravity import geohash
import os
import sys
import pandas as pd
from matplotlib.legend_handler import HandlerBase 

sys.path.append('..')

import trajectory.trajectory as trajectory 
from trajectory.utils import loc2hash
from map.load_region import load_r

'''
output data format: id, longitude, latitude, geohash...
'''
def handle_point_df(df):
    def func(x):
        #lat, lon = eval(x['location'])
        lat, lon = x['lat'], x['lon']
        hashcode = loc2hash(lon=lon, lat=lat, precision=5)
        return [lat, lon, hashcode]
    total_loc = list(set(df['location']))
    total_loc = list(map(eval,total_loc))
    print(len(total_loc))
    loc_df = pd.DataFrame(total_loc, columns=['lat','lon'])
    loc_df = loc_df.apply(func, axis=1, result_type='expand')
    print(loc_df.head())
    return loc_df

'''
output data format: id, longitude1, latitude1, longitude2, latitude2, geohash...
'''
def handle_edge_df(graph_path):
    G = load_r(graph_path)     
    data = []
    cnt = 0
    for item in G.edges:
        n_f = G.nodes[item[0]]
        n_t = G.nodes[item[1]]
        g1 = loc2hash(n_f['x'], n_f['y'], precision=5)
        g2 = loc2hash(n_t['x'], n_t['y'], precision=5)
        item = [n_f['x'], n_f['y'], n_t['x'], n_t['y'], g1]
        if g1!=g2:
            g3 = loc2hash((n_f['x']+n_t['x'])/2, (n_f['y']+n_t['y'])/2, precision=5)
            if g3!=g1 and g3!=g2:
                item.append(g3)
                item.append(g2)
                cnt = cnt + 1
            else:
                item.append(g2)
                
        data.append(item)    
    edge_df = pd.DataFrame(data, columns=['lon1','lat1', 'lon2', 'lat2','hash', 'hash1', 'hash2'])   
    print(cnt)
    return edge_df

def preprocess():
    data_root = r'/home/xjm/trajectory/data/'
    trajectory_path = os.path.join(data_root, 'trajectory.csv')
    graph_path = data_root + 'shanghai.xml'
    print(os.path.join(data_root, trajectory_path))
    df = trajectory.get_trajectory_df(trajectory_path, update=False)
    print(df.head())
    loc_df = handle_point_df(df)
    loc_df.to_csv(os.path.join(data_root, "points.csv"))
    edge_df = handle_edge_df(graph_path=graph_path)
    print(edge_df.head())
    edge_df.to_csv(os.path.join(data_root, "edges.csv"))    

if __name__ == '__main__':
    preprocess()