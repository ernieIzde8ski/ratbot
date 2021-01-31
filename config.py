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
               "cogs.on_message.corrections", "cogs.on_message.ratsponding"]
# bot admin name - must be lowercase
adminname = "ernie"
# line when responding to bot admin name
spokesperson = "i am his spokesperson, what do you want of him"


def removeStrangeChars(s): return "".join(i for i in s if ord(i) < 384)
