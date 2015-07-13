import numpy as np
from scipy import misc
from math import sin, cos
import png
from tqdm import tqdm
import sys


def makeRay(start,start_power,distance,phi,walls):
	power=start_power
	last_changed = 0
	b=np.zeros(walls.shape, dtype=np.uint16)
	iterations = 0
	inWall = walls[start[0],start[1]]>0
	inWall2 = walls[start[0],start[1]]>0
	r = 0
	start_powers = []
	distances = []
	phis = []
	startX = []
	startY = []

	while (power>1):
		r = r + .3
		iterations +=1
		distance = distance + .3
		x = r * sin(phi)
		y = r * cos(phi)
		x = round(x)
		y = round(y)
		power = start_power / (distance**2)
		newX = start[0]+x
		newY = start[1]+y

		if newX > b.shape[0]-1 or newY > b.shape[1]-1 or newX < 0 or newY < 0:
			power = 0
		else:
			wallValue = walls[newX,newY]
			if wallValue>0 and not inWall and not inWall2:
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
				inWall2 = True
			else:
				if inWall and inWall2:
					inWall2 = False
				elif inWall:
					inWall = False
				elif inWall2:
					inWall2 = False

		try:
			if b[newX,newY]==0 and not inWall:
				b[newX,newY] += power
		except:
			pass
	
	return (b,start_powers,distances,phis,startX,startY)

def run():
	# (height, width)
	a=np.zeros((400,600), dtype=np.uint16)
	walls=np.zeros(a.shape, dtype=np.uint16)
	walls[0:2,0:a.shape[1]]=1
	walls[a.shape[0]-2:a.shape[0],0:a.shape[1]]=1;
	walls[0:a.shape[0],0:2]=2;
	walls[0:a.shape[0],a.shape[1]-2:a.shape[1]]=2;

	walls[140:151,0:a.shape[1]]=1
	walls[140:151,30:80]=0

	walls[0:a.shape[0],300:305]=1
	walls[50:100,300:305]=0

	walls[315:321,0:a.shape[1]]=1
	walls[315:321,100:150]=0

	misc.imsave("filename.tif", walls)
	num = 0
	possible_phis = np.arange(0,2*(3.1415925),0.001)

	for i in tqdm(range(len(possible_phis))): 
		phi_start = possible_phis[i]
		start_powers = [50000000]
		phis = [phi_start]
		startX = [25]
		startY = [25] 
		distances = [0]

		while len(start_powers)>0:
			start = [startX.pop(0),startY.pop(0)]
			start_power=start_powers.pop(0)
			distance = distances.pop(0)
			phi=phis.pop(0)
			
			(b,start_powers2,distances2,phis2,startX2,startY2) = makeRay(start,start_power,distance,phi,walls)
			start_powers += start_powers2
			distances += distances2
			phis += phis2
			startX += startX2
			startY += startY2
			
			a=np.add(a,b)

			num +=1
			
			if num % 1000 == 0:	
				print "saved"
				picture = a;
				picture[np.where(picture==0)]=1
				picture = np.log10(picture)
				picture[np.where(picture==0)]=np.min(picture)
				picture = picture/np.max(picture)*60000
				picture = np.add(picture,walls*2500)
				with open('room.png', 'wb') as f: 
					writer = png.Writer(width=picture.shape[1], height=picture.shape[0], bitdepth=16, greyscale=True)
					writer.write(f, picture)
					
	print "saved"
	picture = a;
	picture[np.where(picture==0)]=1
	picture = np.log10(picture)
	picture[np.where(picture==0)]=np.min(picture)
	picture = picture/np.max(picture)*60000
	picture = np.add(picture,walls*2500)
	with open('room.png', 'wb') as f: 
		writer = png.Writer(width=picture.shape[1], height=picture.shape[0], bitdepth=16, greyscale=True)
		writer.write(f, picture)
		

def run2(offset,cores,rays):
	# (height, width)
	a=np.zeros((400,600), dtype=np.uint16)
	walls=np.zeros(a.shape, dtype=np.uint16)
	walls[0:2,0:a.shape[1]]=1
	walls[a.shape[0]-2:a.shape[0],0:a.shape[1]]=1;
	walls[0:a.shape[0],0:2]=2;
	walls[0:a.shape[0],a.shape[1]-2:a.shape[1]]=2;

	walls[140:151,0:a.shape[1]]=1
	walls[140:151,30:80]=0

	walls[0:a.shape[0],300:305]=1
	walls[50:100,300:305]=0

	walls[315:321,0:a.shape[1]]=1
	walls[315:321,100:150]=0

	misc.imsave("filename.tif", walls)
	num = 0
	phi_increment = 2*(3.1415925) / rays
	possible_phis = np.arange(0+phi_increment*offset,2*(3.1415925),phi_increment*cores)

	for i in tqdm(range(len(possible_phis))): 
		phi_start = possible_phis[i]
		start_powers = [50000000]
		phis = [phi_start]
		startX = [25]
		startY = [25] 
		distances = [0]

		while len(start_powers)>0:
			start = [startX.pop(0),startY.pop(0)]
			start_power=start_powers.pop(0)
			distance = distances.pop(0)
			phi=phis.pop(0)
			
			(b,start_powers2,distances2,phis2,startX2,startY2) = makeRay(start,start_power,distance,phi,walls)
			start_powers += start_powers2
			distances += distances2
			phis += phis2
			startX += startX2
			startY += startY2
			
			a=np.add(a,b)

			num +=1
			
			if num % 10000000 == 0:	
				print "saved"
				picture = a;
				picture[np.where(picture==0)]=1
				picture = np.log10(picture)
				picture[np.where(picture==0)]=np.min(picture)
				picture = picture/np.max(picture)*60000
				picture = np.add(picture,walls*2500)
				with open('room.png', 'wb') as f: 
					writer = png.Writer(width=picture.shape[1], height=picture.shape[0], bitdepth=16, greyscale=True)
					writer.write(f, picture)
					
	print "saved"
	np.save(file('room-%d-%d.npy'%(offset,cores),"wb"),a)
		
		

def load_and_save(cores):
	for i in range(cores):
		temp = np.load(file('room-%d-%d.npy'%(i,cores),"rb"))
		try:
			a = np.add(temp,a)
		except:
			a = temp
	print "saved"
	picture = a;
	picture[np.where(picture==0)]=1
	picture = np.log10(picture)
	picture[np.where(picture==0)]=np.min(picture)
	picture = picture/np.max(picture)*60000
	with open('room.png', 'wb') as f: 
		writer = png.Writer(width=picture.shape[1], height=picture.shape[0], bitdepth=16, greyscale=True)
		writer.write(f, picture)	
		
		
#print sys.argv[1]
#print sys.argv[2]
#run2(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]))
load_and_save(4)
