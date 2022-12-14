import datetime
from sys import flags
import folium
import os
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from collections import defaultdict
import tqdm
import numpy as np
import geohash

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36")  #放ua

def draw_gps(locations1, color1, type='line', bound=None):
    """
    绘制gps轨迹图
    :param locations: list, 需要绘制轨迹的经纬度信息，格式为[[lat1, lon1], [lat2, lon2], ...]
    :param output_path: str, 轨迹图保存路径
    :param file_name: str, 轨迹图保存文件名
    :return: None
    """
    m1 = folium.Map(locations1[0], zoom_start=15, attr='default')  # 中心区域的确定
    if type == 'line':
        folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
            locations1,  # 将坐标点连接起来
            weight=3,  # 线的大小为3
            color=color1,  # 线的颜色为橙色
            opacity=0.8  # 线的透明度
        ).add_to(m1)  # 将这条线添加到刚才的区域m内
        # 起始点，结束点
        folium.Marker(locations1[0], popup='<b>Starting Point</b>').add_to(m1)
    else:
        for loc in locations1:
            folium.CircleMarker(loc, radius=3).add_to(m1)
    if bound:
        print(bound)
        folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
            bound,  # 将坐标点连接起来
            weight=8,  # 线的大小为3
            color="black",  # 线的颜色为黑色
            opacity=0.8  # 线的透明度
        ).add_to(m1)  # 将这条线添加到刚才的区域m内        
    m1.save('MAP1.HTML') # 将结果以HTML形式保存到指定路径


def get_time(time_string='2007-02-20 05:26:04'):
    dateTime_p = datetime.datetime.strptime(time_string,'%Y-%m-%d %H:%M:%S')
    return int(dateTime_p.hour)*60 + int(dateTime_p.minute)


def draw_velocity(speeds):
    plt.plot(speeds)
    plt.xlabel("time")
    plt.ylabel("velocity")
    plt.title("speed in a day")
    plt.savefig("speeds.png", dpi=200)


def get_region_by_pos(lat, lon, level=-1):
    '''
    :param lat: str or float
    :param lon: str or float
    :param level: int: -1 for all, 1 for country, 2 for city, 3 for district
    :return: string: address of the region
    e.g. 'Shanghai Fish Inn East Nanjing Road, 4, 宁波路, 外滩街道, 黄浦区, 上海市, 200001, 中国'    '''
    print(lat, lon)
    location = geolocator.geocode(",".join([str(lat), str(lon)]))  #根据查相关信息
    address = location.address
    if level == -1:
        return address
    elif level == 1:
        return address.split(",")[-1].strip()
    elif level == 2:
        return address.split(",")[-3].strip()
    elif level == 3:
        return address.split(",")[-4].strip()
    else: return address

def get_loc(line):
    '''
    The first field is the identificaion of this particular taxi, which has been for privacy reasons; 
    the second is the timestamp when this report is sent out; 
    the third and fourth fields are the logitude and latitude of the current location of this taxi, respectively; 
    the fifth is the instantaneous speed of the taxi at this moment; 
    the sixth is the angle from the north in clockwise direction with a unit of 2 degrees, for example, "157" as shown in the above example would be 314 degrees from the north in clockwise direction; 
    the last field is the current status of this taxi, "0" indicates the taxi is vacant, "1" indicates that the taxi has taken passengers for delivery, and all other figures are assigned for vague purposes.
    '''
    id, timestamp, logitude, latitude, speed, angle, state = line.split(',')
    return id, timestamp, float(logitude), float(latitude), int(speed)

def read(file):
    '''
    :return:
        id: string
        location: (latitude: float, longitude:float) 
        speeds: float
    '''
    f = open(file, 'r')
    lines = f.readlines()
    locations = []
    speeds = []
    cnt = 0
    for line in lines:
        id, timestamp, logitude, latitude, speed = get_loc(line)
        minute = get_time(timestamp)
        if cnt <= minute:
            while(cnt <= minute):
                locations.append([float(latitude), float(logitude)])
                speeds.append(speed)   
                cnt = cnt + 1             
    while cnt < 1440:
        locations.append([float(latitude), float(logitude)])
        speeds.append(0)   
        cnt = cnt + 1          
    f.close()
    return id, locations, speeds

def get_bbox_by_loc(locations):
    '''
    :param
        locations: list of location: (latitude: float, longitude:float) 
    :return:
        bbox:(north, south, east, west)
    '''
    loc_cp = locations.copy()
    loc_cp = sorted(loc_cp, key=lambda x: x[0])
    north = loc_cp[-1][0]
    south = loc_cp[0][0]
    loc_cp = sorted(loc_cp, key=lambda x: x[0])
    east = loc_cp[0][1]
    west = loc_cp[-1][1]
    return north, south, east, west

def get_region_by_file(file):
    '''
    :return:
        region_dict: defaultdict: {region: num_count}
        region: list: [region]
    '''
    _, locations, _ = read(file)
    locations = list(set([(x, y) for x, y in locations]))
    regions_dict = defaultdict(int)
    bar = tqdm.tqdm(list(range(len(locations))))
    for ind in bar:
        loc = locations[ind]
        region = get_region_by_pos(*loc, level=3)
        bar.set_description(f"process location {loc}: {region}")
        regions_dict[region] = regions_dict[region] + 1
    return regions_dict, regions_dict.keys()


def get_region_by_dir(root):
    total_dict = defaultdict(int)
    for file in os.listdir(root):
        file = os.path.join(root, file) 
        region_dict, region = get_region_by_dir(file)
        for key in region:
            total_dict[key] += region_dict[key]
    return total_dict, region_dict.keys()


def dir_walk(root, proc, *args, **kargs):
    r = []
    for file in os.listdir(root):
        file = os.path.join(root, file)     
        r.append(proc(file, *args, **kargs))
    return r

def get_bbox_from_file(file):
    _, loc, _ = read(file)
    return get_bbox_by_loc(loc)

def locstr2loc(s):
    return list(map(float, s[1:-1].split(',')))

def loc2hash(lon, lat, precision=6):
    code = geohash.encode(longitude=lon,latitude=lat, precision=precision)
    return code

if __name__ == '__main__':
    print(get_time())
    print(get_region_by_pos(31.241300, 121.480600, level=3))
    file = r'/Users/xiejinman/Downloads/Taxi_070220/Taxi_99780'
    #print(get_region_by_file(file))
    _, locations, _ = read(file)
    print(get_bbox_by_loc(locations))
    r = dir_walk(r'/Users/xiejinman/Downloads/Taxi_070220/', get_bbox_from_file)
    r = np.array(r)
    #(north, south, east, west)
    print(np.max(r, axis=0), np.min(r, axis=0), np.max(r, axis=1), np.min(r, axis=1))



