TOKEN = "your token"
shutUp = ['shut up liberal', 'what do you want', 'i am your god who the hell do you think you are', 'wot', 'wut', 'WHAT DO YOU WANT', 'wot you want, pathetic mortal', 'lower your shields and surrender your ships because this is the end for your civilization', 'death to capitalism & you', 'do you have nothing better with your life to do right now', 'what', 'что', 'look i don\'t know what you think is a productive use of time but this is not it', 'how HIGH do you even have to BE', 'do you ever think of the utterly meaningless impact your messages right here will ever have', 'couldn\'t you be out there being productive rn', 'I DONT CARE ABOUT YOU', 'you look your best away from the keyboard; never forget', 'https://en.wikipedia.org/wiki/Shut_up', 'https://www.youtube.com/watch?v=KRB-iHGHSqk', 'https://www.youtube.com/watch?v=RwC9CP_2YKE', 'this is explicitly a bot admin command what do you want from me', '']
guildOptIn = [488475203303768065, 526207286067068928, 534875827398246451]
guildOptOut = [516604644793778177]
ratmin_id = 302956027656011776
statusChannel = 708882977202896957
logChannel = 715297562613121084
enabledcogs = ["cogs.admin", "cogs.misc", "cogs.star trek", "cogs.on_message.dms", "cogs.on_message.PIPI", "cogs.on_message.corrections"]
api_key = "ed428f1c-3aac-457f-afcf-09ed85cef8e5"
#line when responding to my name
adminname= "Ernie"
spokesperson = "i am his spokesperson, what do you want of him"

def removeStrangeChars(s): return "".join(i for i in s if ord(i)<384)
def SlursExist(content: str):
    content = removeStrangeChars(content)
    for i in content.split(" "):
        if i.lower() in slursList: return True
    return False
def cleantext(content: str):
    content = removeStrangeChars(content)
    if not content:
        return False
    for i in content.split(" "):
        if i.lower() in slursList: return False
    return str(content)
