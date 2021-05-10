class Config:
    def __init__(self):
        self.prefix = "r;"  # prefix that bot uses; accepts multiple inputs as tuple of str
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
            "AjZrV4wbdnQ": "Aleksandr Marshal & Valeria Kurnushkina — Katyusha (Катюша)",
            "RgsnSg29tBo": "The Agonist — Thank You, Pain.",
            "E9PHKAV3ATQ": "The Agonist — Waiting out the Winter",
            "HaM69OVOf74": "Arch Enemy — As the Pages Burn",
            "ng8mh6JUIqY": "BABYMETAL — BxMxC",
            "cK3NMZAUKGw": "BABYMETAL — メギツネ | MEGITSUNE",
            "whhTjySxxYE": "BABYMETAL — シンコペーション ｜ Syncopation",
            "j9BcQcFVcRM": "Bachman Turner Overdrive — You Ain't Seen Nothing Yet",
            "YEMEAxlYL04": "The Beatles — While My Guitar Gently Weeps",
            "mJag19WoAe0": "The Beatles — Maxwell's Silver Hammer",
            "j_JaDDcyIIU": "The Beatles — Yellow Submarine",
            "hCuMWrfXG4E": "Billy Joel — Uptown Girl",
            "ZJJHeI5izHE": "BLACKPINK — 뚜두뚜두 | DDU-DU DDU-DU (Remix) (Live)",
            "u8rtCPEL79o": "BLACKPINK — Really (Reggae Version)",
            "IoiaAA4vNaI": "BLACKPINK — Stay",
            "9iHn_roIApY": "BLACKPINK — 휘파람 | Whistle (Acoustic Version)",
            "8nWLZaijTbk": "Blind Guardian — Another Holy War",
            "M0TcB5lxfuY": "Blind Guardian — Nightfall",
            "bRLML36HnzU": "Bobby Pickett — Monster Mash",
            "oe2hdbft5-U": "Bob Marley & The Wailers — I Shot The Sheriff (1973)",
            "W1LsRShUPtY": "Bob Seger — Old Time Rock & Roll",
            "No08DrgSy0Y": "Cool and New Music Team — Dr. Pepper",
            "tKJwvQfraY8": "Creedence Clearwater Revival — Bad Moon Rising",
            "jtgA0jvhp2A": "Dubioza kolektiv — No Escape (from Balkan)",
            "uGrb-6Vb9Bw": "Dünedain — Por los siglos de los siglos",
            "aJfgHSUlr-s": "The Coasters — Yakety Yak",
            "4v8KEbQA8kw": "The Eagles — Take It Easy",
            "alQei8zVMyM": "Elina Ohanessian — Kroonk",
            "Jxj9w_7JasU": "Eluveitie — The Nameless",
            "PZc0Dd2n5Js": "Elvenking — Moonbeam Stone Circle",
            "dpZ0wK48qKY": "Elvenking — Petalstorm",
            "TRUZ0gB_xKY": "Elvenking — Towards the Shores",
            "fYTgJVDYWNs": "Elvenking — Twilight of Magic",
            "2KxwqyM7k2s": "Elvenking — The Winter Wake (Acoustic Version)",
            "4gNR7UDSLXo": "Emmanuel — Esa Triste Guitarra",
            "O0PV0M6-j9w": "Eric Clapton — Layla",
            "IvVe-uHRD-U": "ernieIzde8ski — smells like nirvana but only the gargling",
            "hTkW8DLVpwA": "The Flaming Lips — Yoshimi Battles The Pink Robots Pt. 1",
            "OZuW6BH_Vak": "Heart — Crazy On You",
            "eLoMej34zvA": "Heart — Dreamboat Annie",
            "Es5mh7pBeec": "Homestuck: [S] Collide Track 4 — Heir of Grief",
            "b73BI9eUkjM": "JENNIE — SOLO",
            "VkuY33xb6v8": "The Kentucky Colonels — There Ain't Nobody Gonna Miss Me When I'm Gone",
            "S7Jw_v3F_Q0": "The Kingston Trio — M.T.A.",
            "eYNMcolpHEM": "Meat Loaf — Wasted Youth",
            "W-0qx0yf_Hg": "Mormon Tabernacle Choir — Old Time Religion",
            "BJhMjuza_1A": "Mormon Tabernacle Choir — Rock-a-My Soul in the Bosom of Abraham",
            "MYKbQVw80mI": "Petra — Seen and Not Heard",
            "L3YwMmJgszI": "Powerwolf — Let There Be Night",
            "tlYU8mxXGnY": "Powerwolf — When The Moon Shines Red",
            "lrNnMNrKqQc": "Rhapsody — Symphony of the Enchanted Lands",
            "fjp4thii1WY": "ROSÉ — Gone",
            "U5w7tjrqDlo": "Sabaton — Rise of Evil",
            "aXvG_Lx0Kp4": "Selo i Ludy — I Want To Break Free",
            "ha0icvcByDs": "Styx — The Greater Good",
            "i-mWU2JFvUU": "Twilight Force — Blade of Immortal Steel",
            "Eq7-DsMhLaA": "Twilight Force — Night of Winterlight",
            "YZVJb1dyiV8": "Wise Guys — Ans Ende der Welt",
            "MoN3zUJb6tA": "Wise Guys — Ruf' doch mal an '06",
            "j_nuOyxMrMQ": "The Wolfe Tones — Come Out Ye Black & Tans"
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
