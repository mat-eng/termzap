import screen_brightness_control as sbc
import sys

delta = int(sys.argv[1])
brightness = sbc.get_brightness()
brightness[0] += delta
if brightness[0] >= 100:
    brightness[0] = 100
if brightness[0] <= 0:
    brightness[0] = 0
print(f"New brightness value: {brightness[0]}")
sbc.set_brightness(brightness[0])
