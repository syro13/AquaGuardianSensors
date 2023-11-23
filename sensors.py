import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
import time

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-df4a5d19-f8c6-46f5-be09-a5064404189e'
pnconfig.publish_key = 'pub-c-c99be90c-30aa-4441-8201-41f93d0bb9c6'
pnconfig.user_id = 'jakub_iot_pi_397'
pubnub = PubNub(pnconfig)

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

channel_turb = AnalogIn(ads, ADS.P0)
channel_tds = AnalogIn(ads, ADS.P1)
channel_ph = AnalogIn(ads, ADS.P2)

turb_a_total = 0
turb_v_total = 0
tds_a_total = 0
tds_v_total = 0
ph_a_total = 0
ph_v_total = 0

count = 0

my_channel = "jakub_sd3a_pi"
max_time = 5
start_time = time.time()
user_input = int(input("to run press 1: "))
if(user_input == 1):
    while (time.time() - start_time) < max_time:
        #print("turb: ", channel_turb.value, "V: ", channel_turb.voltage, "|tds: ", channel_tds.value, "V:", channel_tds.voltage, "ph: ", channel_ph.value, "V: ", channel_ph.voltage)
        turb_a_total += channel_turb.value
        turb_v_total += channel_turb.voltage
        tds_a_total += channel_tds.value
        tds_v_total += channel_tds.voltage
        ph_a_total += channel_ph.value
        ph_v_total += channel_ph.voltage
        count += 1
    
turb_results_a = turb_a_total/count
turb_results_v = turb_v_total/count
tds_results_a = tds_a_total/count
tds_results_v = tds_v_total/count
ph_results_a = ph_a_total/count
ph_results_v = ph_v_total/count

data = {
    "turb_data": {
            "analog_in": turb_results_a,
            "voltage_in" : turb_results_v
        },
     "tds_data": {
            "analog_in": tds_results_a,
            "voltage_in" : tds_results_v
        },
      "ph_data": {
            "analog_in": ph_results_a,
            "voltage_in" : ph_results_v
        }
    }


def my_publish_callback(envelope, status):
    if not status.is_error():
        print("Data sent")
    else:
        print("Not Send")
        pass  

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  

        elif status.category == PNStatusCategory.PNConnectedCategory:
            pubnub.publish().channel('aqua_guardian_channel').message(data).pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print("Data received:")
        print(message.message)

pubnub.add_listener(MySubscribeCallback())
#pubnub.subscribe().channels('my_channel').execute()
#pubnub.publish().channel('my_channel').message(str(data))
pubnub.subscribe().channels('aqua_guardian_channel').execute()
