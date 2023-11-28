#!/usr/bin/env python3

from a_star import AStar
astar =  AStar()

if __name__ == "__main__":
	while True:
		ja = input("go forward?\n")
		speed = int(200)
		if ja == "ja":
			while True:
				print("goin...")
				astar.motors(speed,speed)
