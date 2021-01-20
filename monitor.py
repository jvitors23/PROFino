import serial

try:
	arduino = serial.Serial("/dev/ttyACM0",timeout=1)
except:
	print('Please check the port')

def receive_message(msg):
	print('jose')

def clean(L):#L is a list
	newl=[] #initialising the new list
	for i in range(len(L)):
		temp=L[i][2:]
		newl.append(temp[:-5])
	return newl

while True:
	rawdata=[]
	rawdata.append(str(arduino.readline()))
	msg = clean(rawdata)[0]
	receive(msg)


	





