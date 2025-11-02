from pathlib import Path
from os import chdir



class Context:
    current_directory: Path

    HOME = Path.home()
    HISTORY_PATH = HOME / '.history'
    TRASH_DIR_PATH = HOME / ".trash"

    def __init__(self):
        self.current_directory = Context.HOME
        chdir(self.current_directory)