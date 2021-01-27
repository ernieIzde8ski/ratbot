from discord import AllowedMentions

none = AllowedMentions.none()
all = AllowedMentions.all()
everyone = AllowedMentions(everyone=True, users=False, roles=True)
users = AllowedMentions(everyone=False, users=True, roles=False)
roles = AllowedMentions(everyone=False, users=False, roles=True)

# message from myer: why the fuck
