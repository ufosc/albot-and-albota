# Misc
ERROR_REPORT_URL = 'https://github.com/ufosc/albot-and-albot'
BOT_NAME = 'ALBot'

# Embed colors
EMBED_COLOR_STANDARD = 0x00529b
EMBED_COLOR_ERROR = 0x913232

# Message reaction types
# 'CONFLICT' means that this reaction type MUST be unique, or at least
# not be the same as another CONFLICT-type reaction, as the program
# could potentially use this reaction as a user-input button.
REACTION_DELETE = '\U0001f6ae'  # CONFLICT
REACTION_NEW = '\u2733'         # CONFLICT
REACTION_EXPAND = '\U0001f521'  # CONFLICT
REACTION_DENY = '\u26d4'        #
REACTION_ERROR = '\u26a0'       #
REACTION_NOT_FOUND = '\u2139'   # Same as REACTION_INFO
REACTION_INFO = '\u2139'        # Same as REACTION_NOT_FOUND

# Common Times (in seconds)
WEEK = 604680  # 2 minutes less than a week for the reminders
DAY = 86400
HOUR = 3600
MIN = 60

# Similar words for open projects
ALUMNUS = ["alumni", "alumnus", "alumna", "alum", "stultus", "stulta"]
ALMUNI_ROLE = "alumnus"
MUDDY = ["muddy", "muddy swamp", "muddyswamp", "muddy-swamp", "MUD"]
MUDDY_ROLE = "muddy-swamp"
WEBSITE = ["website", "club site", "club website", "clubwebsite", "clubsite"]
WEBSITE_ROLE = "club-website"
MVW = ["mvw", "marstonvswest", "marston vs west", "marston v west"]
MVW_ROLE = "marston-vs-west"
ALBOT = ["bot", "albot"]
BOT_ROLE = "bot-dev"

PROJECT_ROLES = [MUDDY_ROLE, WEBSITE_ROLE, MVW_ROLE, BOT_ROLE]
