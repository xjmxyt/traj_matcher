#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <time.h>
#include "dist.h"
#include "utils.h"

#define HASH
//#define DEBUG

#define INF 2e9

using namespace std;

vector<Edge> edges;
vector<Point> points;
Edge nullEdge(-1, -1, -1, -1,-1);

#ifdef HASH
unordered_map<string, vector<Edge*>> h2e;
unordered_map<string, vector<Point*>> h2p;
#endif

ostream& operator<<(ostream& os, const Point& p){
    //return os << "lon: " << p.lon << " lat: " << p.lat << "goe: " << p.geoHash << "pid: " << p.pid;
    return os << p.lon << "," << p.lat;
}
ostream& operator<<(ostream& os, const Edge& e){
    os <<"###node from:###"<< e.p_from << endl;
    os <<"###node to:###"<< e.p_to << endl;
    return os;
}
/*
input data format: id, longitude1, latitude1, longitude2, latitude2, geohash...
*/
void load_edges(vector<Edge>&edges, string filename){
    ifstream fp(filename); //定义声明一个ifstream对象，指定文件路径
    string line;
    getline(fp,line); //跳过列名，第一行不做处理
    while (getline(fp,line)){ //循环读取每行数据
        vector<string> data_line;
        string number;
        istringstream readstr(line); //string数据流化
        //将一行数据按'，'分割
        for(int j = 0;j < 8;j++){ //可根据数据的实际情况取循环获取
            getline(readstr,number,','); //循环读取数据
            data_line.push_back(number); //字符串传long
        }
        int eid = to_int(data_line[0]);
        Edge e(to_double(data_line[1]), to_double(data_line[2]), to_double(data_line[3]), to_double(data_line[4]), eid);
        for(int i=5; i<data_line.size(); i++){
            e.addHash(data_line[i]);
        }
        edges.push_back(e); //插入到vector中
    }
}

/*
input data format: id, longitude, latitude, geohash...
*/
void load_points(vector<Point>&points, string filename){
    ifstream fp(filename); //定义声明一个ifstream对象，指定文件路径
    string line;
    getline(fp,line); //跳过列名，第一行不做处理
    while (getline(fp,line)){ //循环读取每行数据
        vector<string> data_line;
        string number;
        istringstream readstr(line); //string数据流化
        //将一行数据按'，'分割
        for(int j = 0;j < 4;j++){ //可根据数据的实际情况取循环获取
            getline(readstr,number,','); //循环读取数据
            //data_line.push_back(atol(number.c_str())); //字符串传long
            data_line.push_back(number);
        }
        Point p(to_double(data_line[2]), to_double(data_line[1]), to_int(data_line[0]));
        p.addHash(data_line[3]);
        points.push_back(p); //插入到vector中
    }    
}

void gen_hash_ind(unordered_map<string, vector<Edge*>> &h2e, unordered_map<string, vector<Point*>> &h2p){
    for(Edge &e: edges){
        for(string code: e.geoHash){
            if(h2e.find(code)!=h2e.end()) h2e[code].push_back(&e);
            else h2e[code] = {&e};
        }
    }
    for(Point &p: points){
        if(h2p.find(p.geoHash)!=h2p.end()) h2p[p.geoHash].push_back(&p);
        else h2p[p.geoHash] = {&p};
    }
}

/*
*/
DistR find_near_edge(Point &p, vector<Edge> &edges){
    double min_dist = INF;
    Edge *min_e = nullptr;
#ifndef HASH
    for(Edge &e: edges){
        double dist = getNearestDistance(p, e);
        if(dist < min_dist){
            min_dist = dist;
            min_e = e;
        }        
    }
#endif
#ifdef HASH
    for(Edge* e: h2e[p.geoHash]){
        double dist = getNearestDistance(p, *e);
        if(dist < min_dist){
            min_dist = dist;
            min_e = e;
        }
    }
#endif
    return DistR{min_e, min_dist};
}

void handle(){
    ofstream f;
    f.open("./data/match.csv", ios::out|ios::trunc);
    f << "pid,p_lon,p_lat,eid,e1_lon,e1_lat,e2_lon,e2_lat,dist" << endl;
    int cnt = 0;
    for(Point &p: points){
        DistR r = find_near_edge(p, edges);
        //handle nullprt
        if(r.e==nullptr) r.e = &nullEdge;
#ifdef DEBUG
        cout << "Point " << p << endl;
        cout << r.e->eid << " " << *r.e << " " << r.dist << endl;
        cnt ++;
        if(cnt > 1000) break;
#endif
        f << p.pid << "," << p << ",";
        f << r.e->eid <<"," << r.e->p_from << "," << r.e->p_to << "," << r.dist << endl;
    }
    f.close();
    cout << "writing finished!!!" << endl;
}

int main(){
    clock_t start, end;
    string edge_file = "./data/edges.csv";
    string point_file = "./data/points.csv";
    load_edges(edges,edge_file);
    load_points(points,point_file);
    cout << "######points size: " << points.size() << endl;
    cout << "######edges size: " << edges.size() << endl;
    cout << "#########load successfully###########" << endl;
#ifdef HASH
    gen_hash_ind(h2e, h2p);
    cout << "gen hash ind successfully" << endl;
#endif
    start = clock();
    handle();
    end = clock();
    cout<<"运行时间"<<(double)(end-start)/CLOCKS_PER_SEC<<endl;
}