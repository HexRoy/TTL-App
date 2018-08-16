# Time To Lift - TTL-App :muscle:
## 	- Geoffroy Penny
### App to keep track of your workouts, and progresion over time

#### Python Version
* 3.6.5

# To run this on your windows machine use:
* python -m pip install --upgrade pip wheel setuptools
* python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
* python -m pip install kivy.deps.gstreamer
* pip install -r requirements.txt
 
 
 ## Menu Screen
 ### Everything working; Routines button and the Settings button
 ### Todo:
	* Create nicer images for the buttons and background
 ![alt text](https://github.com/HexRoy/TTL-App/blob/master/Images/ui/1%20Menu.png)

 
 ## Your Routines Screen
 ### Scrollable interface that displays each routine and the last time it was used/updated
 ### Todo:
	* Fix the sizing of each routine in the scroll view (3 or less items looks bad, too streched)
	* Create a background
	* Add button backgrounds
	* Implement the delete routine button
 ![alt text](https://github.com/HexRoy/TTL-App/blob/master/Images/ui/2%20Your%20Routines.png)
 
 
 ## Add Routine Screen
 ### Everything working, able to create a routine and save it to a csv file 
 ### Todo: 
	* Create background
	* filter the name to only allow letters?
	* Button backgrounds
 ![alt text](https://github.com/HexRoy/TTL-App/blob/master/Images/ui/3%20Add%20Routine.png)
 
 
 ## Display Routine Screen
 ### For looking at your routine and selecting which exercise you want to complete next
 ### Todo:
	* fix the spacing between the prgress bar and the exercises
	* implement the edit button
	* Correctly implement the color changing 
	* Create background
	* Create button backgrounds
 ![alt text](https://github.com/HexRoy/TTL-App/blob/master/Images/ui/4%20Display%20Routine.png)
 
 
 ## Display Exercise Screen
 ### Displays your previous weight/reps from the last time you used this routine.
 ### Can also complete the exercise and enter data
 ### Todo:
	* Create background
	* Create button backgrounds
	* Fix spacing and pretty it upgrade
 ![alt text](https://github.com/HexRoy/TTL-App/blob/master/Images/ui/5%20Display%20Exercise.png)
 
 
 ## Settings Screen
 ### All buttons are clickable but non functioning
 ### Todo:
	* Create background
	* Create button backgrounds
	* implement notifications
	* implement auto increase weight
	* implement quotes
	* implement color scheme
 ![alt text](https://github.com/HexRoy/TTL-App/blob/master/Images/ui/6%20Settings.png)