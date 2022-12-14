#ifndef __DIST__
#define __DIST__

#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

struct Point{
    double lon;
    double lat;
    string geoHash;
    int pid;
    Point() {}
    Point(double lon, double lat, int pid)
        :lon(lon), lat(lat), pid(pid) {}
    void addHash(string &hash){
        geoHash = hash;
    }
};
struct Edge{
    Point p_from;
    Point p_to;
    std::vector<string> geoHash;
    int eid;
    Edge() {}
    Edge(double PAx, double PAy,double PBx, double PBy, int eid){
        p_from.lon = PAx;
        p_from.lat = PAy;
        p_to.lon = PBx;
        p_to.lat = PBy;
        this->eid = eid;
    }
    Edge(Point p_from,Point p_to, int eid)
        :p_from(p_from), p_to(p_to), eid(eid){}

    void addHash(std::vector<string>& hash){
        for(auto item: hash){
            geoHash.push_back(item);
        }
    }
    void addHash(string hash){
        geoHash.push_back(hash);
    }
};
struct DistR{
    Edge *e;
    double dist;
    DistR() {}
    DistR(Edge *e, double dist) :e(e), dist(dist) {}
};
//根据两点经纬度计算距离,X经度，Y纬度
double getDistanceBtwP(double LonA, double LatA,double LonB, double LatB);
//点PCx,PCy到线段PAx,PAy,PBx,PBy的距离
double getNearestDistance(double PAx, double PAy,double PBx, double PBy,double PCx, double PCy);
//点P到边e的距离
double getNearestDistance(Point &p, Edge &e);

#endif