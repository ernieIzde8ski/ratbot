# guilds which have opted into tenor slaying
# only relevant if you load cogs.on_message.respuestas
guildOptIn = [488475203303768065, 526207286067068928, 534875827398246451]
# bot admin user id, mostly extant by now
ratmin_id = 302956027656011776
# channel where startup is logged
statusChannel = 708882977202896957
# channel where miscellaneous actions [i.e. dm messages to rat] are logged
logChannel = 715297562613121084
# cogs that load alongside the bot
enabledcogs = ["cogs.admin", "cogs.misc", "cogs.star trek", "cogs.on_message.dms", "cogs.on_message.PIPI",
               "cogs.on_message.corrections", "cogs.on_message.ratsponding", "cogs.uncategorized"]
# bot admin name - must be lowercase
adminname = "ernie"
# line when responding to bot admin name
spokesperson = "i am his spokesperson, what do you want of him"
# songs referenced in cogs.uncategorized via youtube url
songs = ["i-mWU2JFvUU", "alQei8zVMyM", "dpZ0wK48qKY", "HaM69OVOf74", "ng8mh6JUIqY", "whhTjySxxYE", "tlYU8mxXGnY",
         "U5w7tjrqDlo", "YEMEAxlYL04", "IoiaAA4vNaI", "9iHn_roIApY", "YZVJb1dyiV8", "MoN3zUJb6tA", "aXvG_Lx0Kp4",
         "eLoMej34zvA", "OZuW6BH_Vak", "4v8KEbQA8kw", "O0PV0M6-j9w", "mJag19WoAe0", "j_JaDDcyIIU", "W-0qx0yf_Hg",
         "BJhMjuza_1A", "W1LsRShUPtY", "Eq7-DsMhLaA", "AjZrV4wbdnQ", "VkuY33xb6v8", "MYKbQVw80mI", "4gNR7UDSLXo",
         "bRLML36HnzU", "ha0icvcByDs", "j_nuOyxMrMQ", "S7Jw_v3F_Q0", "KXrgF30VplE", "hTkW8DLVpwA", "tKJwvQfraY8",
         "j9BcQcFVcRM", "hCuMWrfXG4E", "oe2hdbft5-U", "Es5mh7pBeec", "aJfgHSUlr-s", "eYNMcolpHEM", "L3YwMmJgszI"
         "PZc0Dd2n5Js", "u8rtCPEL79o", "IvVe-uHRD-U", "ZJJHeI5izHE", "cK3NMZAUKGw", "No08DrgSy0Y", "alQei8zVMyM"
         "Jxj9w_7JasU"]


def removeStrangeChars(s): return "".join(i for i in s if ord(i) < 384)
