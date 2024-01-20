# Is ISS Overhead? Skyeler's Approach

## Step 1: What does it mean to be overhead?
I defined 'overhead' as being visible from sea level, given ideal conditions, from a specific location. Note that ISS is visible only from dusk to dawn, according to [NASA](https://spotthestation.nasa.gov/faq.cfm#:~:text=The%20space%20station%20is%20visible,or%20dusk%20at%20your%20location). 
## Step 2: What does it mean to be visible from sea level? 
This is a more complicated process. I referred to a few different physics and astronomy pages online: https://physics.stackexchange.com/questions/129317/how-much-of-the-sky-is-visible-from-a-particular-location


I decided to calculate the 'circle of view' (in terms of latitude and longitude) of the sky (so then the astronomical objects like ISS) that can be seen from a given point.
Here is a [diagram](https://github.com/scmcqueen/WhereIsISS/blob/main/ISS_Diagram.svg) of the earth, ISS's orbit, and my process for deriving theta, the angle of visibility. 

In my code, I convert theta from radians to degrees using the formula theta/(2pi)x360 which is equivalent to theta/pi x 180.

Once theta is in degrees, these correspond to latitude/longitude differences. We are looking to see when ISS falls within the [circle](https://i.stack.imgur.com/CLZNr.png) around the coordinates of the user. To do this, we can use the formula for a circle! 
Here is another [diagram](https://github.com/scmcqueen/WhereIsISS/blob/main/Field_of_View.svg) showing the the field of view from the user's coordinates. 

To recap, I made the following assumptions:
1. The user is standing at sea-level. 
2. ISS is overhead when it is visible. 

Using these assumptions, I calculated a formula to find the angle theta of visibility, relative to a user's coordinates. This can be used to find a circle or field of visibility (the circle equation) and then we can calculate whether or not ISS is within the field of view. Now, I can program these calculations using the data (ISS coordinates, viewer coordinates, Earth's radius, height of ISS's orbit).

## Step 3: Write some code!

I knew that I wanted to make a shell program that would allow a user to put in their coordinates or use Ann Arbor. 

To do this, I wrote a few different functions. 

**get_iss_location()**: This functions gets the current latitude and longitude of ISS. 

**validate_coords()**: This function validates that the user input coordinates are valid latitude and longitude values.

**get_user_location()**: Allows the user to indicate if they are in Ann Arbor or put in their own coordinates. If they indicate that they are in Ann Arbor, we will use the coordinates for North Quadrangle building (found from Google Maps). This function uses validate_coords() to ensure that the user coordinates are true latitude,longitude. If not, we will use the coordinates for Hell, Michigan (found from Google Maps).

**can_you_see()**: This functions asks the user whether it is dusk or dawn or another time of day. This isn't strictly necessary to determine whether or not ISS is overhead, but the user might be interested to know if they could actually see ISS. 

**get_visibility_range()**: Calculates the angle theta (referenced in step 2) that corresponds to the radius of the field of view. In otherwords, this tells us the radius of how much of the night sky someone can see from a specific position. For this function, we used 248 miles as height of ISS's orbit as supplied by [NASA](https://www.nasa.gov/wp-content/uploads/2018/06/stemonstrations_orbits.pd) and 3,959 miles as Earth's radius, as supplied by [NASA](https://science.nasa.gov/earth/facts/).

**iss_coords_in_range()**: This function returns True if ISS is within the field of view calculated in the get_visibility_range() function and False if not. TL;DR this is the function that calculates whether or not ISS is overhead.

The main function puts all of these functions together to create an interactive terminal program. 

## Running the Program
Run the Week1.py file and input your responses in the terminal. 

## Testing the Program 

Aside from the typical testing to ensure that my code worked as intended and there were no bugs (e.g. type issues), I wanted to test that ISS was trult visible at certain coordinates when my program said it was.

While I was running the program, at one point it said that ISS was overhead of Ann Arbor! To verify this, I used the [Live Space Station Tracking Map](https://spotthestation.nasa.gov/tracking_map.cfm). The green circle around the space station indicates where on Earth the station is visible and at the time, Southern Michigan was in the visible area. 

I used the Tracking Map to test a few more times - using the coordinates of cities that I could tell where in the bounds of the visibility zone. It worked! This is anecdotal evidence, but helps me to feel confident in my code. 
