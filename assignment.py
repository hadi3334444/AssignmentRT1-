from __future__ import print_function
import time
from sr.robot import *
# robot object
R = Robot() 
# t for time
t = 1 
# angle threshold
a_th = 4.0 
# distance threshold
d_th = 0.4 
# array to store collected silver tokens
collctdTokens = [] 
# array to store visited gold tokens
visitedPoints = [] 
# lambda to delay actions
delay = lambda x : time.sleep(x) 

# move forward or backward the robot
def drive(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	delay(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

# turn the robot clockwise/anti clockwise
def turn(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	delay(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

# find a token not marked and return the distance and angle and code 
def find_token(token_type, visited_tokens):
	distance = 1000
	rot_y = 0
	token_code = -1

	for token in R.see():
		if (token.dist < distance) and (token.info.marker_type is token_type) and (token.info.code not in visited_tokens):
			distance = token.dist
			token_code = token.info.code
			rot_y = token.rot_y

	if distance >= 1000:
		print('No token in range')
		return -1, -1, token_code
	else:
		return distance, rot_y, token_code

# update the position of the robot with respect to the marked token
def update_pos(target_code):
	for token in R.see():
		if token.info.code == target_code:
			return token.dist, token.rot_y
	return -1, -1

# carry the silver token to a golden one
def bring_to_checkpoint(token_code):
	checkpoint = False
	lock = False
	checkpoint_code = -1
	a = 1
	
	while not checkpoint:
		if not lock:
			distance, rot_y, pointCode = find_token(MARKER_TOKEN_GOLD, visitedPoints)
			# if token was not found, move and turn until one is found
			while distance == -1 or pointCode == -1:
				#turn clockwise
				turn(30+a, t)
				#go forward
				drive(30+a, t)
				distance, rot_y, pointCode = find_token(MARKER_TOKEN_GOLD, visitedPoints)
				if pointCode != -1:
					print('Locked gold token')
				else:
					print('No gold token in range')
				a += 5
				delay(1)
		else:
			print('Delivering to gold token')
			distance, rot_y = update_pos(pointCode)
		lock = True
		a=0
		# if close enough to the gold token, release the silver token and mark it as visited
		# distance threshold should be far than the actual distance threshold because it has grabbed a silver token 
		if distance < d_th * 1.5 :
			checkpoint = True
			R.release()
			collctdTokens.append(token_code)
			visitedPoints.append(pointCode)
			lock = False
		elif rot_y < -a_th:
			turn(-2, t)
		elif rot_y > a_th:
			turn(2, t)
		else:
			drive(30, t)

# main code or main function
remaining_tokens=6
# enter the rigion
drive(40, t*3)
delay(1)
lock = False
token_code = -1
a=0
# while loop to collect all tokens 
while remaining_tokens > 0:
	if not lock:
		distance, rot_y, token_code = find_token(MARKER_TOKEN_SILVER, collctdTokens)
		# if token was not found, move and turn until one is found
		while distance == -1 or token_code == -1:
			turn(30+a, t)
			drive(30+a, t)
			distance, rot_y, token_code = find_token(MARKER_TOKEN_SILVER, collctdTokens)
			if token_code != -1:
				print('Locked token')
			else:
				print('No silver token in range')
			delay(1)
			a += 5
	else:
		distance, rot_y = update_pos(token_code)
	lock = True
	a=0
	# if the threshold distance is reached grab the silver token
	if distance < d_th:
		if R.grab():
			print('Grabbed token')
			delay(0.5)
			print('Delivering token...')
			#going backward
			drive(-30, t)
			turn(30, t)
			bring_to_checkpoint(token_code)
			#decrement the remaining silver tokens
			remaining_tokens -= 1
			#going backward
			drive(-30, t)
			#turn clockwise
			turn(45, t)#45
			lock = False
		else:
			print('[ERROR] Unable to grab token!')
			exit()
	elif rot_y < -a_th:
		turn(-2, t)
	elif rot_y > a_th:
		turn(2, t)
	else:
		drive(30, t)
print('All tokens delivered successfully!')
exit()
