import numpy as np
from scipy import misc
from math import sin, cos
import png

a=np.zeros((500,500), dtype=np.uint16)
walls=np.zeros(a.shape, dtype=np.uint16)
walls[0:2,0:a.shape[0]]=1
walls[a.shape[0]-2:a.shape[0],0:a.shape[0]]=1;
walls[0:a.shape[0],0:2]=2;
walls[0:a.shape[0],a.shape[0]-2:a.shape[0]]=2;

walls[148:151,0:a.shape[0]]=1
walls[148:151,30:40]=0

walls[318:321,0:a.shape[0]]=1
walls[318:321,300:400]=0

misc.imsave("filename.tif", walls)

for phi_start in np.arange(.1,2*(3.1415925),10): 
	start_powers = [500000000]
	phis = [phi_start]
	startX = [25]
	startY = [25] 
	distances = [0]
	rs = [0]

	num = 0
	while len(start_powers)>0:
		print (rs,start_powers,startX)

		start = [startX.pop(0),startY.pop(0)]
		start_power=start_powers.pop(0)
		distance = distances.pop(0)
		phi=phis.pop(0)
		r = rs.pop(0)

		power=start_power
		last_changed = 0
		b=np.zeros(a.shape, dtype=np.uint16)
		iterations = 0
		while (power>1):
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
			pastWalls = False
			pastHorizontal = False
			pastVertical = False
			if newX > walls.shape[0]-1 or newX < 1:
				pastWalls = True
				pastHorizontal = True

			if newY > walls.shape[1]-1 or newY < 1:
				pastWalls = True
				pastVertical = True
				
				
			try:
				if iterations > 100 and (pastVertical or walls[start[0]+x,start[1]+y]==1):
					if not pastVertical and (newX<a.shape[0]-1 and newY<a.shape[1]-1 and newX > 0 and newY > 0):
						startX.append(start[0])
						startY.append(start[1])
						start_powers.append(start_power/2)
						distances.append(distance)
						phis.append(phi)
						rs.append(r)
						
					newX = round(start[0]+ x)
					newY = round(start[1]+ y)
							
					if (newX<a.shape[0]-1 and newY<a.shape[1]-1 and newX > 0 and newY > 0):
						startX.append(newX)
						startY.append(newY)
						start_powers.append(start_power/2)
						distances.append(distance)
						phis.append(0-phi)
						rs.append(0)
					power = 0
				elif iterations > 100 and (pastHorizontal or walls[start[0]+x,start[1]+y]==2):
					newX = round(start[0]+ x)
					newY = round(start[1]+ y)
					if not pastHorizontal:
						if (newX<a.shape[0]-1 and newY<a.shape[1]-1 and newX > 0 and newY > 0):
							startX.append(start[0])
							startY.append(start[1])
							start_powers.append(start_power/2)
							distances.append(distance)
							phis.append(phi)
							rs.append(r)
					
					if (newX<a.shape[0]-1 and newY<a.shape[1]-1 and newX > 0 and newY > 0):
						startX.append(newX)
						startY.append(newY)
						start_powers.append(start_power/2)
						distances.append(distance)
						phis.append(3.141-phi)
						rs.append(0)
					power = 0
			except:
				pass

				
			try:
				if b[start[0]+x,start[1]+y]==0:
					b[start[0]+x,start[1]+y] += power
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

	