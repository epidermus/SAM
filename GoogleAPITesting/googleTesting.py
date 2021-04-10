lat = 43.62000000
long = -116.0000000
out = ""
for x in range(100):
    lat = lat + .0005
    long = long + .005
    out += (str(lat) + "," + str(long) + "/")
print(out)
