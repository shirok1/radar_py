import time

import numpy as np

import mvs_driver
import cv2 as cv

print("SDK Version: ", mvs_driver.get_sdk_version_str())

devices = mvs_driver.enum_devices()
print("Device count: ", len(devices))
if len(devices) == 0:
    raise RuntimeError("Not enough devices!")
for device_info in devices:
    print(device_info.special_info["chModelName"])
first_device_info = devices[0]
print("Opening device: ", first_device_info)
handle = first_device_info.create_handle()

device = handle.open_device()


def print_int_value(name):
    print(name, device.get_int_value(name))


print_int_value("Height")
print_int_value("Width")
print_int_value("PayloadSize")
device.set_float_value("ExposureTime", 1500)
device.set_float_value("Gain", 20)
device.set_enum_value("PixelFormat", 17301513)

device.start_grabbing()

# img = device.get_image_buffer()
t1 = time.time()
count_fps = 0
count_s = 0
count_max = 35
height = device.get_int_value("Height")
width = device.get_int_value("Width")
shape = (height, width)
frame = np.empty(shape, dtype=np.uint8)
while True:
    img = device.get_image_to_buffer(frame, 1000)
    t2 = time.time()
    count_fps += 1
    img: np.ndarray
    img = cv.cvtColor(img, cv.COLOR_BAYER_BG2BGR)
    print(img.shape)
    cv.imshow("Image", frame)
    if t2 - t1 >= 8:
        fps = count_fps / (t2 - t1)
        count_fps = 0
        t1 = time.time()
        print(f"fps {fps}")
    if cv.waitKey(1) == ord('q'):
        break

device.stop_grabbing()

device.close()

handle.destroy()
