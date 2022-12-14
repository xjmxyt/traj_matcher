#include "dist.h"
/*
ref: https://blog.csdn.net/ufoxiong21/article/details/46487001
*/
using namespace std;

double getDistanceBtwP(double LonA, double LatA,double LonB, double LatB)//根据两点经纬度计算距离,X经度，Y纬度
{
    double radLng1 = LatA * M_PI / 180.0;
    double radLng2 = LatB * M_PI / 180.0;
    double a = radLng1 - radLng2;
    double b = (LonA - LonB) * M_PI/ 180.0;
    double s = 2 * asin(sqrt(pow(sin(a / 2), 2)+ cos(radLng1) * cos(radLng2) * pow(sin(b / 2), 2))) * 6378.137;	//返回单位为公里
    return s;
}


//点PCx,PCy到线段PAx,PAy,PBx,PBy的距离
double getNearestDistance(double PAx, double PAy,double PBx, double PBy,double PCx, double PCy)
{     
	double a,b,c;  
	a=getDistanceBtwP(PAy,PAx,PBy,PBx);//经纬坐标系中求两点的距离公式
	b=getDistanceBtwP(PBy,PBx,PCy,PCx);//经纬坐标系中求两点的距离公式
	c=getDistanceBtwP(PAy,PAx,PCy,PCx);//经纬坐标系中求两点的距离公式
	if(b*b>=c*c+a*a)return c;   
	if(c*c>=b*b+a*a)return b;  
	double l=(a+b+c)/2;     //周长的一半   
	double s=sqrt(l*(l-a)*(l-b)*(l-c));  //海伦公式求面积 
	return 2*s/a;   
}

//点P到边e的距离
double getNearestDistance(Point &p, Edge &e){
    return getNearestDistance(e.p_from.lon, e.p_from.lat, e.p_to.lon, e.p_to.lat, p.lon, p.lat);
}