"""AI Wardrobe development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (
    b'\x11\xff\x9d{\xd1G\x9e\xe7\x97\x08@Q-\x8c\x82\xfb{[\x96K\xc3+'
    b'\xde\xd1'
)
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
WARDROBE_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = WARDROBE_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/wardrobe.sqlite3
DATABASE_FILENAME = WARDROBE_ROOT/'var'/'wardrobe.sqlite3'
