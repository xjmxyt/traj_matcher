# 轨迹数据预处理
## 数据
- shanghai.xml：上海的点和边构成的图
- trajectory.csv：出租车的轨迹
- edges.csv：eid, 边的起点，终点和geohash
- points.csv：pid, 出租车所有经过点的坐标
- match.csv：对于points.csv中每一个点，找到pid对应的eid的编号，以及pid, eid的坐标和距离
- vehicle.csv：车辆对应的eid编号

## 文件和作用
- node_matcher: 将gps坐标和最近的边进行匹配
- map: 获取上海的地图并进行处理
- trajectory: trajectory.py将车辆数据合并成为df

```bash
python trajectory/trajectory.py
python preprocess/preprocess_traj.py
```
```bash
cd node_matcher
g++ main.cpp dist.cpp utils.cpp -std=c++11 -g -o main
./main
cp ./data/match.csv ../data/match.csv
```
```bash
cd ..
python preprocess/handle_traj.py
```