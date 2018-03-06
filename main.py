import pynmea2
from numpy import pi, cos, sin, arctan2, sqrt, square, radians


def haversine(lat1, lat2, lon1, lon2):
    """
    haversine(lat1, lat2, lon1, lon2)

    Method to calculate the (long) distance over a sphere with the haversine formula.
    input: two gps coordinates (radians) defined by lat and long coordinates
    output: distance between the two points in meters
    """
    # radius of earth (m)
    r_earth = 6371e3

    dlat = float(lat2) - float(lat1)  # change in latitude
    dlon = float(lon2) - float(lon1)  # change in longitude

    # distance over a sphere using the Haversine formula
    # https://www.movable-type.co.uk/scripts/latlong.html
    a = square(sin(dlat/2)) + cos(lat1)*cos(lat2)*square(sin(dlon/2))
    c = 2*arctan2(sqrt(a), sqrt(1-a))
    d = r_earth * c

    return d


def distBetweenGPSPoints(lat1, lat2, lon1, lon2):
    """
    distBetweenGPSPoints(lat1, lat2, lon1, lon2)

    Method to calculate the straight-line approximation between two gps coordinates.
    input: two gps coordinates (radians) defined by lat and long coordinates
    output: distance between the two points in meters
    """
    r_earth = 6371e3  # radius of earth (m)
    dlat = lat2 - lat1  # change in latitude
    dlon = lon2 - lon1  # change in longitude

    dlat *= (pi/180)
    dlon *= (pi/180)

    dx = r_earth*dlon*cos((lat1+lat2)/2)
    dy = r_earth*dlat

    dist = sqrt(square(dx)+square(dy))  # straight line approximation

    return dist


def GPStoRad(gpsData):
    """
    GPStoRad(gpsData)

    Method to parse GPS data and determine angular positon using the pynmea2 library.
    input: gpsData in GPGGA format
    output: gpsFloat [latitude, longditude] in radians
    """
    nmeaObj = pynmea2.parse(gpsData)  # create nmea object
    lat = radians(nmeaObj.latitude)  # degrees->radians
    lon = radians(nmeaObj.longitude)  # degrees->radians
    gpsFloat = [float(lat), float(lon)]

    # print for debugging
    print("GPS Coordinates in Radians: [%f, %f]" % (gpsFloat[0], gpsFloat[1]))
    return gpsFloat


def calcHeading(prevLocation, currLocation, goalLocation):
    """
    calcHeading(prevLocation, currLocation, goalLocation)

    Method to calculate the heading of the car based on current, previous location of the
    car with respect to the goal location. Will only work if robot moved between steps.
    input: previous, current, goal location [lat, long] (radians)
    output: heading from current location to goal (radians)
    """
    # TODO: compare performance with buying a compass module...

    return heading


if __name__ == '__main__':
    # test GPGGA sentence parsing
    data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
    dataFloat = GPStoRad(data)
    print("\n")

    # Test the distance between two gps coordinates
    PetronasTwinTowers = [3.157884, 101.712166]  # lat, long
    lat1 = radians(PetronasTwinTowers[0])
    lon1 = radians(PetronasTwinTowers[1])

    sevenElevenTaiping = [4.842704, 100.740181]
    lat2 = radians(sevenElevenTaiping[0])
    lon2 = radians(sevenElevenTaiping[1])

    dist_h = haversine(lat1, lat2, lon1, lon2)
    dist = distBetweenGPSPoints(lat1, lat2, lon1, lon2)
    print("Haversine: %f km" % (dist_h/1000))
    print("Straight-line approx: %f km" % (dist/1000))
    print("Google Maps: 216.16 km")
    print("\n")


    # Sidney's data test
    # data from stream
    data1 = "$GPGGA,003957.00,3252.88385,N,11714.01269,W,1,06,1.52,129.2,M,-33.8,M,,*6D"
    data2 = "$GPGGA,003958.00,3252.88368,N,11714.01211,W,1,04,4.25,129.1,M,-33.8,M,,*6A"

    # parse gps data
    [lat1, lon1] = GPStoRad(data1)
    [lat2, lon2] = GPStoRad(data2)

    # compare the haversine vs straight-line approximation
    dist_h = haversine(lat1, lat2, lon1, lon2)
    dist = distBetweenGPSPoints(lat1, lat2, lon1, lon2)
    print("Haversine: %f m" % (dist_h/1000))
    print("Straight-line approx: %f m" % (dist))
