"""
Main UI dialog for Image Inserter add-on
"""
from typing import Optional, List
from aqt import mw
from aqt.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QLineEdit, QTextEdit, QGroupBox,
    QProgressBar, QFormLayout, Qt, QMessageBox
)
from aqt.utils import showInfo, tooltip


class ImageInserterDialog(QDialog):
    """Main dialog for the Image Inserter add-on"""

    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config or {}
        self.processing = False
        self.paused = False
        self.current_position = 0
        self.total_cards = 0
        self.processor = None  # Keep reference to processor

        self.setWindowTitle("Image Inserter for Vocabulary Cards")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)

        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout()

        # API Keys Section
        api_group = QGroupBox("API Keys")
        api_layout = QFormLayout()

        self.unsplash_key_input = QLineEdit()
        self.unsplash_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("Unsplash API Key:", self.unsplash_key_input)

        self.pexels_key_input = QLineEdit()
        self.pexels_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("Pexels API Key:", self.pexels_key_input)

        self.pixabay_key_input = QLineEdit()
        self.pixabay_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("Pixabay API Key:", self.pixabay_key_input)

        self.google_key_input = QLineEdit()
        self.google_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("Google API Key:", self.google_key_input)

        self.google_cx_input = QLineEdit()
        self.google_cx_input.setPlaceholderText("Custom Search Engine ID")
        api_layout.addRow("Google CX:", self.google_cx_input)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # API Status Section
        status_group = QGroupBox("API Status")
        status_layout = QVBoxLayout()

        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(80)
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)

        refresh_btn = QPushButton("Refresh API Status")
        refresh_btn.clicked.connect(self.refresh_api_status)
        status_layout.addWidget(refresh_btn)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Deck and Field Selection
        selection_group = QGroupBox("Deck and Field Selection")
        selection_layout = QFormLayout()

        self.deck_combo = QComboBox()
        self.load_decks()
        selection_layout.addRow("Select Deck:", self.deck_combo)

        self.source_field_input = QLineEdit()
        self.source_field_input.setText("English")
        selection_layout.addRow("Source Field:", self.source_field_input)

        self.target_field_input = QLineEdit()
        self.target_field_input.setText("Image")
        selection_layout.addRow("Target Field:", self.target_field_input)

        self.images_per_card_spin = QSpinBox()
        self.images_per_card_spin.setMinimum(1)
        self.images_per_card_spin.setMaximum(20)
        self.images_per_card_spin.setValue(6)
        selection_layout.addRow("Images per Card:", self.images_per_card_spin)

        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)

        # Progress Section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("Ready")
        progress_layout.addWidget(self.progress_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Action Buttons
        btn_layout1 = QHBoxLayout()

        self.trial_btn = QPushButton("Run Trial (20 cards)")
        self.trial_btn.clicked.connect(self.run_trial)
        btn_layout1.addWidget(self.trial_btn)

        self.run_all_btn = QPushButton("Run All Cards")
        self.run_all_btn.clicked.connect(self.run_all)
        btn_layout1.addWidget(self.run_all_btn)

        layout.addLayout(btn_layout1)

        btn_layout2 = QHBoxLayout()

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setEnabled(False)
        btn_layout2.addWidget(self.pause_btn)

        self.delete_images_btn = QPushButton("Delete All Images")
        self.delete_images_btn.clicked.connect(self.delete_all_images)
        btn_layout2.addWidget(self.delete_images_btn)

        layout.addLayout(btn_layout2)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def load_decks(self):
        """Load available decks into combo box"""
        self.deck_combo.clear()
        decks = sorted(mw.col.decks.all_names_and_ids(), key=lambda d: d.name)
        for deck in decks:
            self.deck_combo.addItem(deck.name, deck.id)

    def load_config(self):
        """Load configuration into UI"""
        if "unsplash_api_key" in self.config:
            self.unsplash_key_input.setText(self.config["unsplash_api_key"])
        if "pexels_api_key" in self.config:
            self.pexels_key_input.setText(self.config["pexels_api_key"])
        if "pixabay_api_key" in self.config:
            self.pixabay_key_input.setText(self.config["pixabay_api_key"])
        if "google_api_key" in self.config:
            self.google_key_input.setText(self.config["google_api_key"])
        if "google_cx" in self.config:
            self.google_cx_input.setText(self.config["google_cx"])
        if "source_field" in self.config:
            self.source_field_input.setText(self.config["source_field"])
        if "target_field" in self.config:
            self.target_field_input.setText(self.config["target_field"])
        if "images_per_card" in self.config:
            self.images_per_card_spin.setValue(self.config["images_per_card"])

    def save_config(self):
        """Save current configuration"""
        self.config["unsplash_api_key"] = self.unsplash_key_input.text()
        self.config["pexels_api_key"] = self.pexels_key_input.text()
        self.config["pixabay_api_key"] = self.pixabay_key_input.text()
        self.config["google_api_key"] = self.google_key_input.text()
        self.config["google_cx"] = self.google_cx_input.text()
        self.config["source_field"] = self.source_field_input.text()
        self.config["target_field"] = self.target_field_input.text()
        self.config["images_per_card"] = self.images_per_card_spin.value()

        # Save to Anki config
        mw.addonManager.writeConfig(__name__, self.config)

    def refresh_api_status(self):
        """Refresh and display API status"""
        from .image_api import ImageSearchManager

        self.save_config()
        self.status_text.setText("Checking API status...")

        try:
            manager = ImageSearchManager(
                unsplash_key=self.unsplash_key_input.text(),
                pexels_key=self.pexels_key_input.text(),
                pixabay_key=self.pixabay_key_input.text(),
                google_key=self.google_key_input.text(),
                google_cx=self.google_cx_input.text()
            )

            # Perform a test search to get rate limit info
            # Use a simple word to avoid wasting quota
            manager.search_images("test", num_images=1)

            status = manager.get_api_status()
            status_text = "API Rate Limit Status:\n"

            for service, remaining in status.items():
                if remaining is not None:
                    status_text += f"{service}: {remaining} requests remaining\n"
                else:
                    status_text += f"{service}: Connected (rate limit unknown)\n"

            self.status_text.setText(status_text)

        except Exception as e:
            self.status_text.setText(f"Error checking API status:\n{str(e)}")

    def get_selected_deck_id(self) -> Optional[int]:
        """Get the currently selected deck ID"""
        return self.deck_combo.currentData()

    def get_cards_for_deck(self, deck_id: int, limit: Optional[int] = None) -> List[int]:
        """Get card IDs for the selected deck"""
        deck_name = mw.col.decks.name(deck_id)
        query = f'deck:"{deck_name}"'

        if limit:
            query += f' -is:suspended'

        card_ids = mw.col.find_cards(query)

        if limit:
            card_ids = card_ids[:limit]

        return card_ids

    def run_trial(self):
        """Run trial mode with 20 cards"""
        self.save_config()
        self.start_processing(limit=20)

    def run_all(self):
        """Run on all cards in deck"""
        self.save_config()
        self.start_processing()

    def start_processing(self, limit: Optional[int] = None):
        """Start processing cards"""
        print(f"[DEBUG] start_processing called with limit={limit}")

        deck_id = self.get_selected_deck_id()
        print(f"[DEBUG] Selected deck_id: {deck_id}")

        if not deck_id:
            showInfo("Please select a deck")
            return

        # Validate API keys
        if not self.unsplash_key_input.text() and not self.pexels_key_input.text() and not self.pixabay_key_input.text():
            showInfo("Please enter at least one API key")
            return

        print(f"[DEBUG] API keys validated")

        # Get cards
        card_ids = self.get_cards_for_deck(deck_id, limit)
        print(f"[DEBUG] Found {len(card_ids) if card_ids else 0} cards")

        if not card_ids:
            showInfo("No cards found in selected deck")
            return

        self.total_cards = len(card_ids)
        self.current_position = 0
        self.processing = True
        self.paused = False

        # Update UI
        self.trial_btn.setEnabled(False)
        self.run_all_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.pause_btn.setText("Pause")

        self.progress_bar.setMaximum(self.total_cards)
        self.progress_bar.setValue(0)

        print(f"[DEBUG] Creating CardProcessor...")

        # Start processing - KEEP REFERENCE TO PROCESSOR!
        from .card_processor import CardProcessor
        self.processor = CardProcessor(self, self.config)

        print(f"[DEBUG] Starting card processing...")
        self.processor.process_cards(card_ids)

        print(f"[DEBUG] Processing started successfully")

    def toggle_pause(self):
        """Toggle pause/resume"""
        if self.processing:
            self.paused = not self.paused
            if self.paused:
                self.pause_btn.setText("Resume")
                self.progress_label.setText("Paused")
            else:
                self.pause_btn.setText("Pause")
                self.progress_label.setText("Processing...")

    def update_progress(self, current: int, total: int, message: str = ""):
        """Update progress bar and label"""
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"Processing: {current}/{total} {message}")

    def processing_complete(self, success_count: int, error_count: int):
        """Called when processing is complete"""
        self.processing = False
        self.paused = False

        # Update UI
        self.trial_btn.setEnabled(True)
        self.run_all_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setText("Pause")

        self.progress_label.setText(f"Complete! Success: {success_count}, Errors: {error_count}")

        showInfo(f"Processing complete!\n\nSuccessfully processed: {success_count} cards\nErrors: {error_count} cards")

    def delete_all_images(self):
        """Delete all images from target field in selected deck"""
        deck_id = self.get_selected_deck_id()
        if not deck_id:
            showInfo("Please select a deck")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete all images from the target field?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            from .card_processor import CardProcessor
            processor = CardProcessor(self, self.config)
            count = processor.delete_all_images(deck_id)
            showInfo(f"Deleted images from {count} cards")
