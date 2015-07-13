import numpy as np
from scipy import misc
from math import sin, cos
import png
# (height, width)
a=np.zeros((400,300), dtype=np.uint16)
walls=np.zeros(a.shape, dtype=np.uint16)
walls[0:2,0:a.shape[1]]=1
walls[a.shape[0]-2:a.shape[0],0:a.shape[1]]=1;
walls[0:a.shape[0],0:2]=2;
walls[0:a.shape[0],a.shape[1]-2:a.shape[1]]=2;

walls[148:151,0:a.shape[1]]=1
walls[148:151,30:40]=0

walls[318:321,0:a.shape[1]]=1
walls[318:321,100:150]=0

misc.imsave("filename.tif", walls)

for phi_start in np.arange(1.4,2*(3.1415925),10): 
	start_powers = [500000000]
	phis = [phi_start]
	startX = [25]
	startY = [25] 
	distances = [0]
	num = 0
	while len(start_powers)>0:
		start = [startX.pop(0),startY.pop(0)]
		start_power=start_powers.pop(0)
		distance = distances.pop(0)
		phi=phis.pop(0)
		r = 0
		power=start_power
		last_changed = 0
		b=np.zeros(a.shape, dtype=np.uint16)
		iterations = 0
		inWall = walls[start[0],start[1]]>0

		while (power>0.01):
			r = r + .1
			iterations +=1
			distance = distance + .1
			x = r * sin(phi)
			y = r * cos(phi)
			x = round(x)
			y = round(y)
			power = start_power / (distance**2)
			newX = start[0]+x
			newY = start[1]+y

			try:
				wallValue = walls[newX,newY]
				if wallValue>0 and not inWall:
					print wallValue
					inWall = True
					startX.append(newX)
					startY.append(newY)
					start_powers.append(start_power/2)
					distances.append(distance)
					if wallValue == 1:
						phis.append(0-phi)
					elif wallValue == 2:
						phis.append(3.1415925-phi)
					start_power = start_power / 2
				elif wallValue > 0:
					inWall = True
				else:
					inWall = False
			except:
				# outside now
				print "problem"
				power = 0
				
			if newX > a.shape[0] or newY > a.shape[1] or newX < 0 or newY < 0:
				power = 0

			try:
				if b[newX,newY]==0 and not inWall:
					b[newX,newY] += power
			except:
				pass
				
		a=np.add(a,b)

		num +=1
		
		if num % 100 == 0:	
			print "saved"
			picture = a;
			picture[np.where(picture==0)]=1
			picture = np.log10(picture)
			picture[np.where(picture==0)]=np.min(picture)
			picture = np.add(picture,walls*np.max(picture)/2)
			with open('room.png', 'wb') as f: 
				writer = png.Writer(width=picture.shape[1], height=picture.shape[0], bitdepth=16, greyscale=True)
				writer.write(f, picture)
	print "saved"
	picture = a;
	picture[np.where(picture==0)]=1
	picture = np.log10(picture)
	picture[np.where(picture==0)]=np.min(picture)
	picture = np.add(picture,walls*np.max(picture)/2)
	with open('room.png', 'wb') as f: 
		writer = png.Writer(width=picture.shape[1], height=picture.shape[0], bitdepth=16, greyscale=True)
		writer.write(f, picture)
	