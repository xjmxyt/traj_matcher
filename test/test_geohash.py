import sys
sys.append("..")
from utils import loc2hash

longitude=116.390705
latitude=39.923201
print(loc2hash(longitude, latitude, 6))