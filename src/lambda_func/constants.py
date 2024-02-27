from datetime import date
from pathlib import Path


START_DATE = date(2024, 3, 3)
"""First day message will be printed, should be a day corresponding to the top row for the 
github contribution dot-matrix (as of Feb 2024, this is a Sunday)"""

DATA_DIR = Path.cwd() / "data"

OUTPUT_DIR = Path.cwd() / "output"

INPUT_MESSAGE_FILE = DATA_DIR / "message_raw.txt"
"""Raw message string to be encoded"""

ENCODED_MESSAGE_FILE = DATA_DIR / "message_encoded.npy"
"""Store of the full raw message encoded as pixels"""

FULL_PIXELLATED_MESSAGE_FILE = DATA_DIR / "message_pixellated.txt"

MESSAGE_RECORD_FILE = OUTPUT_DIR / "message_record.txt"
"""Path to the file in which the message printed in the github dot matrix so far will be recorded in"""

MSG_FILLED_PIXEL = "⬛"
"""Default filled pixel to be printed in the output message file"""

MSG_EMPTY_PIXEL = "⬜"
"""Default empty pixel to be printed in the output message file"""

GITHUB_USERNAME = "glyn-stevens"
"""Username of the github account that the PAT belongs to"""

GITHUB_PAT_ENV_VAR = "GITHUB_PERSONAL_ACCESS_TOKEN"
"""Name of the environment variable in the lambda storing the Github PAT
Store PAT as environment variable for security"""

GITHUB_REPO = "gitlab-scrolling-message"
"""Name of the git repo that the commit will be made in and that the message record file is in"""
