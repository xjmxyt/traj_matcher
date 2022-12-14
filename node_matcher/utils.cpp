#include <iostream>
#include "utils.h"


int to_int(std::string &s){
    return atoi(s.c_str());
}
double to_double(std::string &s){
    return atof(s.c_str());
}