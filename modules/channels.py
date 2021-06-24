class Channels():
    def __init__(self, **channels):
        self.channels = channels
        self.loaded = False

    def get_channels(self, bot):
        self.k = {}
        for key in self.channels.keys():
            self.k[key] = bot.get_channel(self.channels[key])
            if not self.k[key]:
                print(f"Could not get channel {key}")
        self.loaded = True
