from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent / 'db.sqlite'

connection = sqlite3.connect(DB_PATH)