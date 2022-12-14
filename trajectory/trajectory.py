import os
import re
from traceback import format_exception_only
import pandas as pd
from trajectory.utils import read 
from tqdm import tqdm
from time import sleep

def get_df_from_file(path)->pd.DataFrame:
    id, locations, speeds = read(path)
    vehicle_id = path.split('/')[-1]
    columns=['vehicle_id', 'location', 'speed']
    df = pd.DataFrame(dict(zip(columns, [[id for i in range(len(speeds))], locations, speeds])))
    df['timestamp'] = range(len(df))
    return df 


def load_trajectory_data(root)->pd.DataFrame:
    '''
        :param 
            root: trajectory root path
        :return 
            trajectory_df
    '''
    vehicle_df = pd.DataFrame(columns=['vehicle_id', 'location', 'speed', 'timestamp'])
    path_list = os.listdir(root)
    for dir in tqdm(path_list):
        df = get_df_from_file(os.path.join(root, dir))
        vehicle_df = pd.concat([vehicle_df, df], ignore_index=True, axis=0) #按行拼接
        sleep(0.01)
    return vehicle_df

def get_trajectory_df(filename, root=None, update=True)->pd.DataFrame:
    '''
        if update is True: 
            update file using data in root dir 
            will save data in filename
            @requires
                root is not None
        else:
            load data from file
        :param
            filename: the trajectory df data 
            root: the root directory
            update: whether to update the trajectory df
        :return: 
            the trajectory df data
    '''
    if os.path.exists(filename) and update==False:
        df = pd.read_csv(filename, index_col=0)
        return df  
    else:
        if root is None:
            raise ValueError("root must be specified")
        else:
            df = load_trajectory_data(root)
            df.to_csv(filename)
            return df 
    
def get_vehicles(root):
    '''
        :param 
            root: trajectory root path

    '''
    total_vehicles = []
    for dir in os.listdir(root):
        pattern = re.compile(r'_\d+')
        vehicle_id = pattern.findall(dir)[0][1:]
        total_vehicles.append(vehicle_id)
    return total_vehicles


if __name__ == '__main__':
    root = r'/Users/xiejinman/Downloads/Taxi_070220/'
    data_root = r'/Users/xiejinman/Documents/AI_22/data/'
    trajectory_path = data_root + 'trajectory.csv'
    total_vehicles = get_vehicles(root=root)
    print(total_vehicles[:3], len(total_vehicles))
    df = get_trajectory_df(trajectory_path, root) 
    print(df.head())


