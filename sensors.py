import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-df4a5d19-f8c6-46f5-be09-a5064404189e'
pnconfig.publish_key = 'pub-c-c99be90c-30aa-4441-8201-41f93d0bb9c6'
pnconfig.user_id = 'jakub_iot_pi_397'
pubnub = PubNub(pnconfig)

#i2c = busio.I2C(board.SCL, board.SDA)

#ds = ADS.ADS1115(i2c)

#channel_turb = AnalogIn(ads, ADS.P0)
#channel_tds = AnalogIn(ads, ADS.P1)
#channel_ph = AnalogIn(ads, ADS.P2)

my_channel = "jakub_sd3a_pi"
#while True:
 #   print("turb: ", channel_turb.value, "V: ", channel_turb.voltage, "|tds: ", channel_tds.value, "V:", channel_tds.voltage, "ph: ", channel_ph.value, "V: ", channel_ph.voltage)

#sensor_data = {
#    'turb_data': channel_turb,
#    'tds_data': channel_tds,
 #   'ph_data': channel_ph
#}
data = {
    "turb_data": 1,
     "tds_data": 2,
      "ph_data": 3
    }


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('my_channel').message(data).pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)

pubnub.add_listener(MySubscribeCallback())
#pubnub.subscribe().channels('my_channel').execute()
#pubnub.publish().channel('my_channel').message(str(data))
pubnub.subscribe().channels('my_channel').execute()
