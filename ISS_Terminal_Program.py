# ISS current location: http://api.open-notify.org/iss-now.json
# Live view of ISS https://www.youtube.com/watch?v=P9C25Un7xaM 

import requests
import math

def get_iss_location()->dict:
    ''' Returns the coordinates of ISS in a dictionary, where the keys are 'latitude' and 'longitude 
    and the values are floats.
    '''
    iss_request = requests.get('http://api.open-notify.org/iss-now.json')
    coordinates = iss_request.json()['iss_position']
    coordinates['latitude']=float(coordinates['latitude'])
    coordinates['longitude']=float(coordinates['longitude'])
    return(coordinates)

def validate_coords(coord:list)->bool:
    ''' Validates whether or not the coordinates supplied are valid latitude and longitude. 
    Returns True if they are valid, False otherwise. 
    '''
    if len(coord)!=2:
        return False
    try:
        test = float(coord[1])
        test2=float(coord[0])
    except:
        return False
    if abs(float(coord[0])) <=90 and abs(float(coord[0]))>=0 and abs(float(coord[1])) <=180 and abs(float(coord[1]))>=0:
        return True
    return False

def get_user_location()->dict:
    '''Returns the coordinates for user's location, where the keys are 'latitude' and 'longitude 
    and the values are floats.
    If the user is in Ann Arbor, returns preset coordinates for North Quadrangle building. 
    If the user inputs invalid coordinates, returns preset coordinates for Hell, MI. 
    '''
    in_aa = input('Are you in Ann Arbor? Y or N:  ').lower()
    if 'y' in in_aa:
        return {'longitude': -83.7404, 'latitude': 42.2806} #of north quad, from google
    location = input('Please input your location in the form "latitude,longitude", e.g. "42.2806,-83.7404":  ')
    coords = location.split(',')
    if not validate_coords(coords): #if invalid
        print('The coordinates you supplied are inaccurate. Let\'s pretend you are at 42.4338,-83.9948. ')
        return {'longitude': -83.9948, 'latitude': 42.4338}
    return {'longitude': float(coords[1]), 'latitude': float(coords[0])}

def can_you_see()->bool:
    ''' Returns a boolean indicating whether the user reports it being dusk or dawn, or another 
    time of day. 
    '''
    return 'y' in input('Is it dusk or dawn? Y or N:  ').lower()

def get_visibility_range()->float:
    ''' Returns the angle theta (in degrees) of visibility. Refer to markdown file for more notes
    on this process. 
    '''
    iss_orbit = 248 #iss height is 248 miles - https://www.nasa.gov/wp-content/uploads/2018/06/stemonstrations_orbits.pdf
    earth_radius = 3959 #earth radius is 3,959 miles - https://science.nasa.gov/earth/facts/
    theta = math.acos(earth_radius/(earth_radius+iss_orbit))*180/math.pi #converted to degrees
    return theta

def iss_coords_in_range(iss_location:dict,your_location:dict,theta:float)->bool:
    ''' Checks whether or not the ISS is in the field of view of the user. In simpler terms, this 
    function returns True if the ISS is visible in the night sky from the user's latitude,longitude
    or False if not.

    Keyword Arguments
    iss_location -- dictionary containing latitude and longitude of ISS
    your_location -- dictionary containing latitude and longitude of user
    theta -- the radius of the field of view of the sky
    '''
    lat_diff = abs(iss_location['latitude'] -your_location['latitude']) #calculate the latitude difference
    long_diff = min(abs(iss_location['longitude'] -your_location['longitude']),360-abs(iss_location['longitude'] -your_location['longitude']))
    #the above line calculates the longitude difference. Note that because longitude goes from [-180,180], we have to also consider the case in
    #   which involves modulus. For example, 170 - (-175) = 345 which implies a distance of 245 when they are only  15 apart. Hence, taking the
    #   minimum of (360-(iss_long-your_long)) and iss_long-your_long.
    return (lat_diff**2 + long_diff**2 <= theta**2)

def main():
    user_coords=get_user_location() 
    iss_coords = get_iss_location()
    theta = get_visibility_range()
    iss_overhead = iss_coords_in_range(iss_coords,user_coords,theta)
    visible = can_you_see()
    if iss_overhead:
        print('ISS is overhead! Look up!')
        if not visible:
            print('JK! ISS is only visible at dusk or dawn as to see it, the sun\'s light must reflect off of the spacecraft.')
    else:
        print(f'ISS is not overhead. It is currently at {str(iss_coords["latitude"])},{str(iss_coords["longitude"])}.')
        if not visible:
            print('But it doesn\'t matter! ISS is only visible at dusk or dawn as to see it, the sun\'s light must reflect off of the spacecraft.')

if __name__ == '__main__':
    main()
