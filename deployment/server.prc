# While dev.prc contains settings for both the dev server and client, the
# live server separates these. The client settings go in config/public_client.prc
# and server settings go here. Don't forget to update both if necessary.

# Resource settings
vfs-mount resources/phase_3 /phase_3
vfs-mount resources/phase_3.5 /phase_3.5
vfs-mount resources/phase_4 /phase_4
vfs-mount resources/phase_5 /phase_5
vfs-mount resources/phase_5.5 /phase_5.5
vfs-mount resources/phase_6 /phase_6
vfs-mount resources/phase_7 /phase_7
vfs-mount resources/phase_8 /phase_8
vfs-mount resources/phase_9 /phase_9
vfs-mount resources/phase_10 /phase_10
vfs-mount resources/phase_11 /phase_11
vfs-mount resources/phase_12 /phase_12
vfs-mount resources/phase_13 /phase_13
model-path /
default-model-extension .bam


# Server settings
want-dev #f
want-cheesy-expirations #t
cogsuit-hack-prevent #t


# DC Files
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toon.dc
dc-file config/otp.dc


# Shared secret for CSMUD
# ##### NB! Update config/public_client.prc too! #####
# csmud-secret Yv1JrpTUdkX6M86h44Z9q4AUaQYdFnectDgl2I5HOQf8CBh7LUZWpzKB9FBD


# Beta Modifications
# Temporary modifications for unimplemented features go here.
want-bbhq #f
want-pets #t
want-parties #t
want-accessories #f
want-golf #f
want-gardening #f
want-gifting #f
want-keep-alive #f

# Chat Settings
blacklist-sequence-url https://s3.amazonaws.com/cdn.toontownrewritten.com/misc/tsequence.dat
want-whitelist #f
want-blacklist-sequence #f


# Holidays and Events
want-mega-invasions #f
mega-invasion-cog-type tm


# Working (Custom) Addons!
want-toonfest #t
want-doomsday #f