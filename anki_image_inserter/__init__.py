"""
Image Inserter for Vocabulary Cards - Anki Add-on
Automatically inserts relevant images into vocabulary cards
"""
from aqt import mw, gui_hooks
from aqt.qt import QAction
from aqt.utils import showInfo

# Add-on metadata
__version__ = "1.0.0"


def show_image_inserter_dialog():
    """Show the main Image Inserter dialog"""
    try:
        from .ui_dialog import ImageInserterDialog

        # Load config
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            config = {}

        # Create and show dialog
        dialog = ImageInserterDialog(mw, config)
        dialog.exec()

    except Exception as e:
        showInfo(f"Error opening Image Inserter: {str(e)}\n\nPlease check the error log for details.")
        import traceback
        traceback.print_exc()


def setup_menu():
    """Add menu item to Anki's Tools menu"""
    # Create action
    action = QAction("Image Inserter for Vocabulary", mw)
    action.triggered.connect(show_image_inserter_dialog)

    # Add to Tools menu
    mw.form.menuTools.addAction(action)


# Initialize add-on when Anki is ready
gui_hooks.main_window_did_init.append(setup_menu)
