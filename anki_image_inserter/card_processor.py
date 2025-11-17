"""
Card processing logic with pause/resume support
Compatible with Anki threading model
"""
import time
import json
import re
from typing import List, Optional
from aqt import mw
from aqt.qt import QTimer
from aqt.utils import tooltip, showInfo
from aqt.operations import QueryOp

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


class CardProcessor:
    """Manages card processing using Anki-safe threading"""

    def __init__(self, dialog, config: dict):
        self.dialog = dialog
        self.config = config
        self.card_ids = []
        self.current_index = 0
        self.success_count = 0
        self.error_count = 0
        self.processing = False
        self.timer = None

        # Initialize managers
        self.search_manager = ImageSearchManager(
            bing_key=self.config.get("bing_api_key", ""),
            unsplash_key=self.config.get("unsplash_api_key", ""),
            pexels_key=self.config.get("pexels_api_key", ""),
            pixabay_key=self.config.get("pixabay_api_key", "")
        )

        self.image_processor = ImageProcessor(
            max_width=self.config.get("max_image_width", 800),
            max_height=self.config.get("max_image_height", 600),
            quality=self.config.get("image_quality", 85)
        )

    def process_cards(self, card_ids: List[int]):
        """Start processing cards"""
        print(f"[CardProcessor] process_cards called with {len(card_ids)} cards")

        self.card_ids = card_ids
        self.current_index = 0
        self.success_count = 0
        self.error_count = 0
        self.processing = True

        print(f"[CardProcessor] Creating QTimer...")
        # Start processing with timer (non-blocking)
        self.timer = QTimer()
        self.timer.timeout.connect(self._process_next_card)
        self.timer.start(100)  # Process every 100ms

        print(f"[CardProcessor] QTimer started successfully, interval=100ms")

    def _process_next_card(self):
        """Process next card (called by timer in main thread)"""
        print(f"[CardProcessor] _process_next_card called, index={self.current_index}/{len(self.card_ids)}")

        # Check if paused
        if self.dialog.paused:
            print(f"[CardProcessor] Processing paused")
            return

        # Check if stopped
        if not self.dialog.processing:
            print(f"[CardProcessor] Processing stopped by user")
            self.stop_processing()
            return

        # Check if done
        if self.current_index >= len(self.card_ids):
            print(f"[CardProcessor] All cards processed!")
            self.stop_processing()
            self.dialog.processing_complete(self.success_count, self.error_count)
            return

        # Process current card
        card_id = self.card_ids[self.current_index]
        print(f"[CardProcessor] Processing card {card_id} ({self.current_index + 1}/{len(self.card_ids)})")

        try:
            self._process_single_card(card_id)
        except Exception as e:
            print(f"[CardProcessor] Error processing card {card_id}: {e}")
            import traceback
            traceback.print_exc()
            self.error_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                f"(Error: {str(e)[:30]})"
            )

        self.current_index += 1
        print(f"[CardProcessor] Card processing complete, moving to next")

    def _process_single_card(self, card_id: int):
        """Process a single card (runs in main thread - safe for mw.col access)"""
        print(f"[CardProcessor] _process_single_card: Starting card {card_id}")

        source_field = self.config.get("source_field", "English")
        target_field = self.config.get("target_field", "Image")
        images_per_card = self.config.get("images_per_card", 6)

        print(f"[CardProcessor] Settings: source={source_field}, target={target_field}, num_images={images_per_card}")

        # Get card and note (SAFE: main thread)
        print(f"[CardProcessor] Getting card from collection...")
        card = mw.col.get_card(card_id)
        note = card.note()
        print(f"[CardProcessor] Got note with fields: {list(note.keys())}")

        # Check if source field exists
        if source_field not in note:
            self.error_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                f"(Error: field '{source_field}' not found)"
            )
            return

        # SKIP if target field already has images!
        if target_field in note:
            existing_content = note[target_field].strip()
            # Check if field has img tags
            if existing_content and '<img' in existing_content:
                print(f"[CardProcessor] SKIPPING card {card_id} - already has images")
                self.success_count += 1
                self.dialog.update_progress(
                    self.current_index + 1,
                    len(self.card_ids),
                    "(Skipped: already has images)"
                )
                return

        # Get search query from source field
        query = note[source_field].strip()
        if not query:
            self.error_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                "(Error: empty source field)"
            )
            return

        # Remove HTML tags from query
        query = re.sub(r'<[^>]+>', '', query)

        # Search for images
        self.dialog.update_progress(
            self.current_index + 1,
            len(self.card_ids),
            f"(Searching: {query})"
        )

        image_results = self.search_manager.search_images(query, images_per_card)

        # DOUBLE CHECK: Ensure we don't get more than requested
        image_results = image_results[:images_per_card]

        if not image_results:
            self.error_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                "(Error: no images found)"
            )
            return

        # Process images
        self.dialog.update_progress(
            self.current_index + 1,
            len(self.card_ids),
            f"(Downloading {len(image_results)} images)"
        )

        processed_images = self.image_processor.process_images(image_results)

        if not processed_images:
            self.error_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                "(Error: image processing failed)"
            )
            return

        # LIMIT to exactly images_per_card (e.g., 6 images)
        processed_images = processed_images[:images_per_card]
        print(f"[CardProcessor] Limited to {len(processed_images)} images (requested: {images_per_card})")

        # Add to Anki media (SAFE: main thread) - PASS images_per_card limit!
        anki_manager = AnkiImageManager(mw.col)
        filenames = anki_manager.add_images_to_media(processed_images, f"vocab_{card_id}_", max_images=images_per_card)

        # Update note (SAFE: main thread)
        if target_field in note:
            # Clear existing images
            anki_manager.clear_field_images(note, target_field)

            # Add new images - PASS images_per_card limit!
            html = anki_manager.format_images_html(filenames, max_images=images_per_card)
            note[target_field] = html
            mw.col.update_note(note)

            self.success_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                f"(Success: {len(filenames)} images)"
            )
        else:
            self.error_count += 1
            self.dialog.update_progress(
                self.current_index + 1,
                len(self.card_ids),
                f"(Error: field '{target_field}' not found)"
            )

    def stop_processing(self):
        """Stop the processing timer"""
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.processing = False

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
