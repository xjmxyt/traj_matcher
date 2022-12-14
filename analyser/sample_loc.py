import pandas as pd
import numpy as np

from utils import draw_gps, locstr2loc

def sample_loc(locations, nums=5000):
    inds = [i for i in range(len(locations))]
    sample_inds = np.random.choice(inds, nums, replace=False)
    return locations[sample_inds]
    
if __name__ == '__main__':
    data_root = r'./data/'
    trajectory_path = data_root + 'trajectory.csv'   
    df = pd.read_csv(trajectory_path).iloc[:]
    df['lat'] = df['location'].apply(lambda x:locstr2loc(x)[0])
    df['lon'] = df['location'].apply(lambda x:locstr2loc(x)[1])
    addr = np.array(list(zip(df['lat'], df['lon'])))
    samples = sample_loc(addr,nums=5000).tolist()
    bound = [[31.41,121.31], [31.03,121.31], [31.03,121.65], [31.41,121.65], [31.41,121.31]]
    draw_gps(samples, 'red', 'point', bound=bound)