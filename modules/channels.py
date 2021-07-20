class Channels():
    def __init__(self, **channels):
        self.channels = channels
        self.loaded = False

    def get_channels(self, bot):
        """Retrieve channels for later usage"""
        for key, value in self.channels.items():
            setattr(self, key, bot.get_channel(value))
            if getattr(self, key) is None:
                print(f"Could not get channel {key} from id {value}")
        self.loaded = True
