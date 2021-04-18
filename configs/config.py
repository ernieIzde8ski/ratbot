class Config:
    def __init__(self):
        self.prefix = "r;"  # prefix that bot uses; accepts multiple inputs as tuple of str
        # relevant to cogs.on_message.respuestas
        self.guild_opt_in = [488475203303768065, 526207286067068928, 534875827398246451]
        # guilds which have opted into tenor slaying
        self.SixPP_guilds = [488475203303768065]  # guilds with random bans
        self.SixPP_Chance = 0.0001  # chance of random bans
        # this value defaults to 0.0001,
        # which gives you about a 4.9% chance of getting banned within 500 messages,
        # or 39.3% chance within 5000 messages
        # P(banned in N messages) = 100(1-(1-SixPP_Chance))^N
        self.channels = Channels()  # the channels lol
        self.adminname = "ernie"  # bot admin name - must be lowercase
        self.songs = [  # songs referenced in cogs.help & cogs.randomized via youtube url
            "fjp4thii1WY",
            "i-mWU2JFvUU",
            "alQei8zVMyM",
            "dpZ0wK48qKY",
            "HaM69OVOf74",
            "ng8mh6JUIqY",
            "whhTjySxxYE",
            "tlYU8mxXGnY",
            "U5w7tjrqDlo",
            "YEMEAxlYL04",
            "IoiaAA4vNaI",
            "9iHn_roIApY",
            "YZVJb1dyiV8",
            "MoN3zUJb6tA",
            "aXvG_Lx0Kp4",
            "eLoMej34zvA",
            "OZuW6BH_Vak",
            "4v8KEbQA8kw",
            "O0PV0M6-j9w",
            "mJag19WoAe0",
            "j_JaDDcyIIU",
            "W-0qx0yf_Hg",
            "BJhMjuza_1A",
            "W1LsRShUPtY",
            "Eq7-DsMhLaA",
            "AjZrV4wbdnQ",
            "VkuY33xb6v8",
            "MYKbQVw80mI",
            "4gNR7UDSLXo",
            "bRLML36HnzU",
            "ha0icvcByDs",
            "j_nuOyxMrMQ",
            "S7Jw_v3F_Q0",
            "KXrgF30VplE",
            "hTkW8DLVpwA",
            "tKJwvQfraY8",
            "j9BcQcFVcRM",
            "hCuMWrfXG4E",
            "oe2hdbft5-U",
            "Es5mh7pBeec",
            "aJfgHSUlr-s",
            "eYNMcolpHEM",
            "L3YwMmJgszI",
            "PZc0Dd2n5Js",
            "u8rtCPEL79o",
            "IvVe-uHRD-U",
            "ZJJHeI5izHE",
            "cK3NMZAUKGw",
            "No08DrgSy0Y",
            "alQei8zVMyM",
            "Jxj9w_7JasU",
            "jtgA0jvhp2A",
            "b73BI9eUkjM",
            "ha0icvcByDs",
            "He322O1JWgU",
            "IoiaAA4vNaI",
            "TRUZ0gB_xKY",
            "M0TcB5lxfuY",
            "lrNnMNrKqQc",
            "2KxwqyM7k2s",
            "fYTgJVDYWNs",
            "uGrb-6Vb9Bw",
            "RgsnSg29tBo",
            "E9PHKAV3ATQ"
        ]


class Channels:
    def __init__(self):
        self.status = 708882977202896957  # channel where startup is logged
        self.log = 715297562613121084  # channel where miscellaneous actions [i.e. dm messages to rat] are logged
        self.bm = 762166605458964510  # channel where based meter is stored

    def _get_channels(self, bot):
        self.status = bot.get_channel(self.status)
        self.log = bot.get_channel(self.log)
        self.bm = bot.get_channel(self.bm)
