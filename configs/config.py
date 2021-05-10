class Config:
    def __init__(self):
        self.prefix = "r."  # prefix that bot uses; accepts multiple inputs as tuple of str
        # relevant to cogs.on_message.respuestas
        self.guild_opt_in = [488475203303768065, 526207286067068928, 534875827398246451]
        # guilds which have opted into tenor slaying
        self.SixPP_guilds = [488475203303768065]  # guilds with random bans
        self.SixPP_Chance = 0.00002  # chance of random bans
        # this value defaults to 0.00002,
        # which gives you about a 0.1% chance of getting banned within 500 messages,
        # or 9.5% chance within 5000 messages
        # P(banned in N messages) = 1 - (1-SixPP_Chance) ^ N
        self.channels = Channels()  # the channels lol
        self.adminname = "ernie"  # bot admin name - must be lowercase
        self.corrections = {  # cogs.on_message.corrections
            "bano": "Baño",
            "senor": "Señor",
            "senora": "Señora",
            "jalapeno": "Jalapeño",
            "canada": "Cañada",
            "canadian": "Cañadian",
            "retard": "Ratard",
            "ExampleSlur": "Armenium"
        }
        # songs referenced in cogs.core.[help/info] & cogs.randomized via youtube url
        self.songs = {
            "fjp4thii1WY": "ROSÉ - 'Gone'",
            "i-mWU2JFvUU": "Blade of Immortal Steel",
            "alQei8zVMyM": "Kroonk",
            "dpZ0wK48qKY": "Elvenking - Petalstorm [HD Audio]",
            "HaM69OVOf74": "Arch Enemy - As the Pages Burn",
            "ng8mh6JUIqY": "BABYMETAL - BxMxC (OFFICIAL)",
            "whhTjySxxYE": "BABYMETAL- -シンコペーション ｜ Syncopation",
            "tlYU8mxXGnY": "When The Moon Shines Red",
            "U5w7tjrqDlo": "Rise of Evil",
            "YEMEAxlYL04": "The Beatles - While My Guitar Gently Weeps",
            "IoiaAA4vNaI": "Stay",
            "9iHn_roIApY": "휘파람 (Whistle) (Acoustic Version)",
            "YZVJb1dyiV8": "Ans Ende der Welt",
            "MoN3zUJb6tA": "Ruf' doch mal an '06",
            "aXvG_Lx0Kp4": "Queen - I Want To Break Free (cover by Selo i Ludy)",
            "eLoMej34zvA": "Heart - Dreamboat Annie",
            "OZuW6BH_Vak": "Heart-Crazy On You",
            "4v8KEbQA8kw": "Take It Easy",
            "O0PV0M6-j9w": "Layla",
            "mJag19WoAe0": "Maxwell's Silver Hammer",
            "j_JaDDcyIIU": "Yellow Submarine",
            "W-0qx0yf_Hg": "Old Time Religion",
            "BJhMjuza_1A": "Rock-a-My Soul in the Bosom of Abraham",
            "W1LsRShUPtY": "Old Time Rock & Roll",
            "Eq7-DsMhLaA": "Night of Winterlight",
            "AjZrV4wbdnQ": "Katyusha (Катюша) - Aleksandr Marshal & Valeria Kurnushkina",
            "VkuY33xb6v8": "There Ain't Nobody Gonna Miss Me When I'm Gone",
            "MYKbQVw80mI": "Seen and Not Heard",
            "4gNR7UDSLXo": "Emmanuel - Esa Triste Guitarra",
            "bRLML36HnzU": "Monster Mash",
            "ha0icvcByDs": "The Greater Good",
            "j_nuOyxMrMQ": "Come Out Ye Black & Tans",
            "S7Jw_v3F_Q0": "The Kingston Trio - M.T.A.",
            "KXrgF30VplE": "Cats In the Cradle",
            "hTkW8DLVpwA": "The Flaming Lips - Yoshimi Battles The Pink Robots Pt. 1",
            "tKJwvQfraY8": "Bad Moon Rising",
            "j9BcQcFVcRM": "You Ain't Seen Nothing Yet",
            "hCuMWrfXG4E": "Billy Joel - Uptown Girl",
            "oe2hdbft5-U": "I Shot The Sheriff (1973) - Bob Marley & The Wailers",
            "Es5mh7pBeec": "Homestuck: [S] Collide Track 4 - Heir of Grief",
            "aJfgHSUlr-s": "Yakety Yak",
            "eYNMcolpHEM": "Wasted Youth",
            "L3YwMmJgszI": "Let There Be Night",
            "PZc0Dd2n5Js": "Moonbeam Stone Circle",
            "u8rtCPEL79o": "Really (Reggae Version)",
            "IvVe-uHRD-U": "smells like nirvana but only the gargling",
            "ZJJHeI5izHE": "뚜두뚜두 (DDU-DU DDU-DU) (Remix) (Live)",
            "cK3NMZAUKGw": "BABYMETAL - メギツネ - MEGITSUNE",
            "No08DrgSy0Y": "23 - Dr. Pepper - Cool and new Volume V",
            "Jxj9w_7JasU": "The Nameless",
            "jtgA0jvhp2A": "Dubioza kolektiv \"No Escape (from Balkan)\"",
            "b73BI9eUkjM": "JENNIE - 'SOLO' M/V",
            "He322O1JWgU": "Really",
            "TRUZ0gB_xKY": "Towards the Shores",
            "M0TcB5lxfuY": "Nightfall",
            "lrNnMNrKqQc": "Symphony of the Enchanted Lands",
            "2KxwqyM7k2s": "The Winter Wake (Acoustic Version)",
            "fYTgJVDYWNs": "Twilight of Magic",
            "uGrb-6Vb9Bw": "Dünedain - Por los siglos de los siglos",
            "RgsnSg29tBo": "Thank You, Pain.",
            "E9PHKAV3ATQ": "Waiting out the Winter",
            "8nWLZaijTbk": "Another Holy War"
        }


class Channels:
    def __init__(self):
        self.status = 708882977202896957  # channel where startup is logged
        self.log = 715297562613121084  # channel where miscellaneous actions [i.e. dm messages to rat] are logged
        self.bm = 762166605458964510  # channel where based meter is stored

    def _get_channels(self, bot):
        self.status = bot.get_channel(self.status)
        self.log = bot.get_channel(self.log)
        self.bm = bot.get_channel(self.bm)
