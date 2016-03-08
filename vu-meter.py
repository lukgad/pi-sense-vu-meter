# http://blog.blinkenlight.net/experiments/basic-effects/vu-meter/
import alsaaudio
import audioop
import sys
import math
import time

from sense_hat import SenseHat
sense = SenseHat()

input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, device="hw:1,0")
#output = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NONBLOCK, device="hw:0,0")

input.setchannels(1)                          # Mono
input.setrate(8000)                           # 8000 Hz
input.setformat(alsaaudio.PCM_FORMAT_S32_LE)  # 16 bit little endian
input.setperiodsize(320)



lo  = 2000
hi = 32000
 
log_lo = math.log(lo)
log_hi = math.log(hi)



millis = int(round(time.time() * 1000))

def to_sense(limit):
        for x in range(0, 8):
                for y in range(0, 8):
                        sense.set_pixel(y, x, 0, 0, 0)

	for x in range(0, limit):
		sense.set_pixel(x, 0, 255, 30*x, 0)
                for y in range(0, x):
			sense.set_pixel(x, y, 255/x, 30*x, 0)


while True:
#    time.sleep(1/48000)
    len, data = input.read()
#    output.write(data)
#    print(len)	
    if len > 0:
        # transform data to logarithmic scale
        vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
	mm = min(max(int(vu*10),0),7)
	msg = "len %s; vu %s; mm %s \r" % (len, vu, mm)
	print(msg), 
	millis2 = int(round(time.time() * 1000))
	if (millis2 - millis) > 8:
		to_sense(mm)
		millis = int(round(time.time() * 1000))




