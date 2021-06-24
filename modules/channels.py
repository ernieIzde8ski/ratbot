class Channels():
    def __init__(self, **channels):
        self.channels = channels
        self.loaded = False

    def get_channels(self, bot):
        for key, value in self.channels.items():
            setattr(self, key, bot.get_channel(value))
            if not getattr(self, key):
                print(f"Could not get channel {key} from id {value}")
        self.loaded = True
