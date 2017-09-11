import sensor, image, time, pyb
from pyb import UART
uart = UART(3, 57600)#timeout_char =10
from pyb import Pin
p8_pin = pyb.Pin.board.P8
p8_pin.init(Pin.IN,Pin.PULL_UP)

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.GRAYSCALE) # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用 QQVGA 速度快一些
sensor.set_auto_whitebal(False)
clock = time.clock() # 追踪帧率
a=1
position_X=80
position_Y=60
new_point_ready = 0
detect_mode = 1#   1黑色   0彩色

def led_blink(x):
    led = pyb.LED(x)
    led.on()
    time.sleep(5)
    led.off()

def send_position():
    if (new_point_ready == 1):
        uart.writechar(0xFF)
        uart.writechar(position_X)
        uart.writechar(position_Y)
        
        if (detect_mode == 0):
            uart.writechar(0xFD)
            led_blink(3)
        else:
            led_blink(2)
    else:
        if (detect_mode == 0):
            uart.writechar(0xFE)

tim4 = pyb.Timer(4)              # create a timer object using timer 4
tim4.init(freq=50)                # trigger at 50Hz
tim4.callback(lambda t:send_position())

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob
while(True):
    if p8_pin.value()==0:
        detect_mode = 1
        blob_thresholds(0, 54, -15, 17, 5, 24)#黑色

    else:
        detect_mode = 0
        blob_thresholds=(14, 73, -70, -21, -5, 53)#绿色

    img = sensor.snapshot() # 从感光芯片获得一张图像
    clock.tick() # Track elapsed milliseconds between snapshots().

    blobs = img.find_blobs([blob_thresholds])
    if blobs:
        new_point_ready = 1
        b=find_max(blobs)
 #       if b.pixels()/(b.w()*b.h())<0.60:
  #          continue
        img.draw_rectangle(b[0:4],color=(0,0,255)) # rect
        #用矩形标记出目标颜色区域
        img.draw_cross(b[5], b[6]) # cx, cy
        #在目标颜色区域的中心画十字形标记
        print ("黑点位置X= %d,Y=%d" %(b[5], b[6]))
        position_X=b[5]
        position_Y=b[6]
    else:
        new_point_ready = 0

    print(clock.fps())

