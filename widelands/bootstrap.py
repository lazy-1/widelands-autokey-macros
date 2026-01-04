# bootstrap.py
"""Simple launcher – can be imported or run directly"""

from .config_editor import ConfigEditor

def launch_editor():
    """Launch the config editor GUI"""
    app = ConfigEditor()
    app.mainloop()

if __name__ == "__main__":
    launch_editor()
