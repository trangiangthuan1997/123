"""
Card processing logic with pause/resume support
"""
import time
import json
from typing import List, Optional
from aqt import mw
from aqt.qt import QThread, pyqtSignal
from aqt.utils import tooltip

from .image_api import ImageSearchManager
from .image_processor import ImageProcessor, AnkiImageManager


class ProcessingState:
    """Manages processing state for pause/resume"""

    STATE_FILE = "image_inserter_state.json"

    def __init__(self):
        self.deck_id = None
        self.card_ids = []
        self.current_index = 0
        self.config = {}

    def save(self):
        """Save state to file"""
        state_data = {
            "deck_id": self.deck_id,
            "card_ids": self.card_ids,
            "current_index": self.current_index,
            "config": self.config
        }

        try:
            addon_dir = mw.addonManager.addonsFolder(__name__)
            state_path = f"{addon_dir}/{self.STATE_FILE}"
            with open(state_path, 'w') as f:
                json.dump(state_data, f)
        except Exception as e:
            print(f"Error saving state: {e}")

    @classmethod
    def load(cls):
        """Load state from file"""
        state = cls()
        try:
            addon_dir = mw.addonManager.addonsFolder(__name__)
            state_path = f"{addon_dir}/{cls.STATE_FILE}"

            with open(state_path, 'r') as f:
                state_data = json.load(f)

            state.deck_id = state_data.get("deck_id")
            state.card_ids = state_data.get("card_ids", [])
            state.current_index = state_data.get("current_index", 0)
            state.config = state_data.get("config", {})

        except FileNotFoundError:
            pass  # No saved state
        except Exception as e:
            print(f"Error loading state: {e}")

        return state

    def clear(self):
        """Clear saved state"""
        try:
            addon_dir = mw.addonManager.addonsFolder(__name__)
            state_path = f"{addon_dir}/{self.STATE_FILE}"
            import os
            if os.path.exists(state_path):
                os.remove(state_path)
        except Exception as e:
            print(f"Error clearing state: {e}")


class CardProcessorThread(QThread):
    """Background thread for processing cards"""

    progress_update = pyqtSignal(int, int, str)
    processing_complete = pyqtSignal(int, int)
    error_occurred = pyqtSignal(str)

    def __init__(self, card_ids: List[int], config: dict, dialog):
        super().__init__()
        self.card_ids = card_ids
        self.config = config
        self.dialog = dialog
        self.success_count = 0
        self.error_count = 0

    def run(self):
        """Process cards in background thread"""
        try:
            # Initialize managers
            search_manager = ImageSearchManager(
                self.config.get("unsplash_api_key", ""),
                self.config.get("pexels_api_key", ""),
                self.config.get("pixabay_api_key", "")
            )

            image_processor = ImageProcessor(
                max_width=self.config.get("max_image_width", 800),
                max_height=self.config.get("max_image_height", 600),
                quality=self.config.get("image_quality", 85)
            )

            anki_manager = AnkiImageManager(mw.col)

            source_field = self.config.get("source_field", "English")
            target_field = self.config.get("target_field", "Image")
            images_per_card = self.config.get("images_per_card", 6)

            # Process each card
            for i, card_id in enumerate(self.card_ids):
                # Check if paused
                while self.dialog.paused:
                    time.sleep(0.5)
                    if not self.dialog.processing:
                        return  # Stopped

                try:
                    # Get card and note
                    card = mw.col.get_card(card_id)
                    note = card.note()

                    # Check if source field exists
                    if source_field not in note:
                        self.error_count += 1
                        self.progress_update.emit(i + 1, len(self.card_ids), f"(Error: field '{source_field}' not found)")
                        continue

                    # Get search query from source field
                    query = note[source_field].strip()
                    if not query:
                        self.error_count += 1
                        self.progress_update.emit(i + 1, len(self.card_ids), "(Error: empty source field)")
                        continue

                    # Remove HTML tags from query
                    import re
                    query = re.sub(r'<[^>]+>', '', query)

                    # Search for images
                    self.progress_update.emit(i + 1, len(self.card_ids), f"(Searching: {query})")
                    image_results = search_manager.search_images(query, images_per_card)

                    if not image_results:
                        self.error_count += 1
                        self.progress_update.emit(i + 1, len(self.card_ids), "(Error: no images found)")
                        continue

                    # Process images
                    self.progress_update.emit(i + 1, len(self.card_ids), f"(Processing {len(image_results)} images)")
                    processed_images = image_processor.process_images(image_results)

                    if not processed_images:
                        self.error_count += 1
                        self.progress_update.emit(i + 1, len(self.card_ids), "(Error: image processing failed)")
                        continue

                    # Add to Anki media
                    filenames = anki_manager.add_images_to_media(processed_images, f"vocab_{card_id}_")

                    # Update note
                    if target_field in note:
                        # Clear existing images
                        anki_manager.clear_field_images(note, target_field)

                        # Add new images
                        html = anki_manager.format_images_html(filenames)
                        note[target_field] = html
                        mw.col.update_note(note)

                        self.success_count += 1
                        self.progress_update.emit(i + 1, len(self.card_ids), f"(Success: {len(filenames)} images)")
                    else:
                        self.error_count += 1
                        self.progress_update.emit(i + 1, len(self.card_ids), f"(Error: field '{target_field}' not found)")

                    # Rate limiting - small delay between cards
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Error processing card {card_id}: {e}")
                    self.error_count += 1
                    self.progress_update.emit(i + 1, len(self.card_ids), f"(Error: {str(e)[:30]})")

            # Processing complete
            self.processing_complete.emit(self.success_count, self.error_count)

        except Exception as e:
            self.error_occurred.emit(str(e))


class CardProcessor:
    """Manages card processing"""

    def __init__(self, dialog, config: dict):
        self.dialog = dialog
        self.config = config
        self.thread: Optional[CardProcessorThread] = None

    def process_cards(self, card_ids: List[int]):
        """Start processing cards"""
        # Create and start thread
        self.thread = CardProcessorThread(card_ids, self.config, self.dialog)
        self.thread.progress_update.connect(self.dialog.update_progress)
        self.thread.processing_complete.connect(self.dialog.processing_complete)
        self.thread.start()

    def delete_all_images(self, deck_id: int) -> int:
        """Delete all images from target field in deck"""
        target_field = self.config.get("target_field", "Image")
        deck_name = mw.col.decks.name(deck_id)
        query = f'deck:"{deck_name}"'

        card_ids = mw.col.find_cards(query)
        anki_manager = AnkiImageManager(mw.col)
        count = 0

        for card_id in card_ids:
            try:
                card = mw.col.get_card(card_id)
                note = card.note()

                if target_field in note and note[target_field]:
                    anki_manager.clear_field_images(note, target_field)
                    mw.col.update_note(note)
                    count += 1

            except Exception as e:
                print(f"Error deleting images from card {card_id}: {e}")

        return count
