# -*- coding: utf-8 -*-

import pytz
import dateutil.parser
from colorconsole import terminal
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from pubnub.pnconfiguration import PNReconnectionPolicy

config = PNConfiguration()
config.subscribe_key = 'sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f'
config.reconnect_policy = PNReconnectionPolicy.LINEAR
pubnub = PubNubTornado(config)
screen = terminal.get_terminal(conEmu=False)

BLACK = 0
GREEN = 2
RED = 1
LIGHT_GRAY = 7
LIGHT_CYAN = 11
WHITE = 15
screen.cprint(LIGHT_CYAN, 0, "<======== Bitflyer FX-BTC/JPY ========>")
screen.reset()
print("")

from tornado import gen

@gen.coroutine
def main(channels):
    class BitflyerSubscriberCallback(SubscribeCallback):

        def __init__(self):
            self.prev_exec_round_time = 0
            self.prev_exec_hour = 0
            self.prev_exec_minute = 0
            self.init_strength_object()
            self.init_execution_check_object()

        def init_strength_object(self):
            self.strength_object = {"BUY": 0, "SELL": 0}

        def init_execution_check_object(self):
            self.execution_check_object = {"BUY": 0, "SELL": 0}

        def cprint_strength_object(self):
            screen.reset()
            screen.cprint(GREEN, BLACK, "BUY: %s\t" % str(self.strength_object["BUY"]).ljust(11))
            screen.cprint(RED, BLACK, "SELL: %s\t" % str(self.strength_object["SELL"]).ljust(11))

            if self.strength_object["BUY"] > self.strength_object["SELL"]:
                screen.cprint(GREEN, BLACK, "[BUY]")
            elif self.strength_object["BUY"] < self.strength_object["SELL"]:
                screen.cprint(RED, BLACK, "[SELL]")
            else:
                screen.cprint(LIGHT_GRAY, BLACK, "[DRAW]")
            screen.reset()
            print("")

        def presence(self, pubnub, presence):
            pass

        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
            elif status.category == PNStatusCategory.PNConnectedCategory:
                pass
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
            elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
                pass

        def message(self, pubnub, message):
            for execution in message.message:
                exec_date = dateutil.parser.parse(execution["exec_date"]).astimezone(pytz.timezone("Asia/Tokyo")).replace(tzinfo=pytz.timezone("Asia/Tokyo"))


                if exec_date.minute != self.prev_exec_minute:
                    print("%s:%s %s" % (exec_date.hour, exec_date.minute, "=" * 50))
                self.prev_exec_hour = exec_date.hour
                self.prev_exec_minute = exec_date.minute

                round_exec_time = round_time(exec_date.second)
                if round_exec_time != self.prev_exec_round_time:
                    self.prev_exec_round_time = round_exec_time
                    self.cprint_strength_object()
                    self.init_strength_object()

                    #if round_exec_time  % 10 == 0:
                    #    screen.cprint(LIGHT_GRAY, BLACK, "直近10秒の裁定判定: ")
                    #    if self.execution_check_object["BUY"] > self.execution_check_object["SELL"]:
                    #        screen.cprint(WHITE, BLACK, "買いです")
                    #    elif self.execution_check_object["BUY"] < self.execution_check_object["SELL"]:
                    #        screen.cprint(WHITE, BLACK, "売りです")
                    #    screen.reset()
                    #    print("")
                    #    self.init_execution_check_object()


                if execution["side"] == "BUY":
                    self.strength_object["BUY"] += execution["size"]
                    self.execution_check_object["BUY"] += execution["size"]
                elif execution["side"] == "SELL":
                    self.strength_object["SELL"] += execution["size"]
                    self.execution_check_object["SELL"] += execution["size"]

    listener = BitflyerSubscriberCallback()
    pubnub.add_listener(listener)
    pubnub.subscribe().channels(channels).execute()

def round_time(time):
    return time - (time % 5)

if __name__ == '__main__':
    channels = [
        'lightning_executions_FX_BTC_JPY',
    ]
    main(channels)
    pubnub.start()

