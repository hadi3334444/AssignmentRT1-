# The robot takes the silver tokens next to the golden tokens

It requires Python 2.7 installed, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

To run the code and see the output, you have to write the following command but you have to be in respected directory:

*python2* *run.py* *assignment.py*

![Tux, the Linux mascot](/images/img1.png)


Here is the flowchart or diagram of the code to grab the silver tokens and release them next to the golden tokens. The robot should enter the origin and find a silver token then take it next to the golden token and do the same in total six times, as there are six pair of tokens. 

![Tux, the Linux mascot](/images/flowchart.png)

According to the diagram, the robot first, enter the origin. 

![Tux, the Linux mascot](/images/img2.png)

Then find the silver token and check the distance if the distance is less than the threshold then grabs it

![Tux, the Linux mascot](/images/img3.png)

if not then check the rotation or the angle and turn according to the angle. After grabbing, check for the golden token and check the distance. 

![Tux, the Linux mascot](/images/img4.png)

Move until the distance is less than one and half time of the threshold as the silver token is between the golden and the robot, if not then you have to check the angle and turn according to angle and move till you reach the one and half time of the threshold to release the silver token next to the golden.

![Tux, the Linux mascot](/images/img5.png)




