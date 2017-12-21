# -*- coding: utf-8 -*-

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
screen.cprint(LIGHT_CYAN, 0, "<======== Bitflyer FX-BTC/JPY ========>")

from tornado import gen

@gen.coroutine
def main(channels):
    class BitflyerSubscriberCallback(SubscribeCallback):

        def __init__(self):
            self.prev_best_ask = 0

        def presence(self, pubnub, presence):
            pass  # handle incoming presence data

        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass  # This event happens when radio / connectivity is lost

            elif status.category == PNStatusCategory.PNConnectedCategory:
                pass
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
            elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
                pass

        def message(self, pubnub, message):
            # Handle new message stored in message.message
            # メインの処理はここで書きます
            # 登録したチャンネルからメッセージ(価格の変化など)がくるたび、この関数が呼ばれます
            current_best_ask = int(message.message['best_ask'])
            if self.prev_best_ask > current_best_ask:
                screen.cprint(RED, BLACK, "[best_ask] %s\n" % message.message['best_ask'])
            elif self.prev_best_ask < current_best_ask:
                screen.cprint(GREEN, BLACK, "[best_ask] %s\n" % message.message['best_ask'])
            else:
                screen.cprint(LIGHT_GRAY, BLACK, "[best_ask] %s\n" % message.message['best_ask'])
            screen.reset()
            self.prev_best_ask = current_best_ask

    listener = BitflyerSubscriberCallback()
    pubnub.add_listener(listener)
    pubnub.subscribe().channels(channels).execute()

if __name__ == '__main__':
    channels = [
        'lightning_ticker_FX_BTC_JPY',
    ]
    main(channels)
    pubnub.start()

