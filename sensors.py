import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

channel_turb = AnalogIn(ads, ADS.P0)
channel_tds = AnalogIn(ads, ADS.P1)
channel_ph = AnalogIn(ads, ADS.P2)


while True:
    print("turb: ", channel_turb.value, "V: ", channel_turb.voltage, "|tds: ", channel_tds.value, "V:", channel_tds.voltage, "ph: ", channel_ph.value, "V: ", channel_ph.voltage)
