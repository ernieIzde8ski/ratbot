guildOptIn = [488475203303768065, 526207286067068928, 534875827398246451]
ratmin_id = 302956027656011776
statusChannel = 708882977202896957
logChannel = 715297562613121084
enabledcogs = ["cogs.admin", "cogs.misc", "cogs.star trek", "cogs.on_message.dms", "cogs.on_message.PIPI",
               "cogs.on_message.corrections", "cogs.on_message.ratsponding"]
# line when responding to my name - must be lowercase
adminname = "ernie"
spokesperson = "i am his spokesperson, what do you want of him"


def removeStrangeChars(s): return "".join(i for i in s if ord(i) < 384)
