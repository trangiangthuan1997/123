"""
Config Dialog Module
Giao diện cấu hình cho Piper TTS Add-on
"""

import os
from typing import List, Optional
from aqt import mw
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QCheckBox,
    QFileDialog,
    QLineEdit,
    QGroupBox,
    QMessageBox,
    QWidget,
    QDoubleSpinBox
)


class PiperTTSConfigDialog(QDialog):
    """Dialog cấu hình cho Piper TTS"""

    def __init__(self, parent=None, config: dict = None):
        """
        Khởi tạo dialog

        Args:
            parent: Widget cha
            config: Dictionary chứa cấu hình hiện tại
        """
        super().__init__(parent)
        self.config = config or {}
        self.selected_note_type = None
        self.selected_source_field = None
        self.selected_target_field = None
        self.selected_model_path = None
        self.overwrite_existing = False

        self.setWindowTitle("Piper TTS - Cấu hình")
        self.setMinimumWidth(600)
        self.setup_ui()
        self.load_config()

        # Trigger populate fields cho note type đã chọn
        if self.note_type_combo.currentIndex() >= 0:
            self._on_note_type_changed(self.note_type_combo.currentIndex())

    def setup_ui(self):
        """Thiết lập giao diện"""
        layout = QVBoxLayout()

        # Group 1: Note Type Selection
        note_type_group = self._create_note_type_group()
        layout.addWidget(note_type_group)

        # Group 2: Field Selection
        field_group = self._create_field_group()
        layout.addWidget(field_group)

        # Group 3: Model Selection
        model_group = self._create_model_group()
        layout.addWidget(model_group)

        # Group 4: Options
        options_group = self._create_options_group()
        layout.addWidget(options_group)

        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _create_note_type_group(self) -> QGroupBox:
        """Tạo group chọn Note Type"""
        group = QGroupBox("1. Chọn Note Type")
        layout = QVBoxLayout()

        # Label hướng dẫn
        help_label = QLabel("Chọn loại thẻ (Note Type) mà bạn muốn xử lý:")
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        # ComboBox chọn Note Type
        self.note_type_combo = QComboBox()
        layout.addWidget(self.note_type_combo)

        # Populate note types (trước khi connect signal để tránh trigger sớm)
        self._populate_note_types()

        # Connect signal sau khi populate
        self.note_type_combo.currentIndexChanged.connect(self._on_note_type_changed)

        group.setLayout(layout)
        return group

    def _create_field_group(self) -> QGroupBox:
        """Tạo group chọn trường"""
        group = QGroupBox("2. Chọn Trường (Fields)")
        layout = QVBoxLayout()

        # Source field
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Trường nguồn (chứa văn bản):"))
        self.source_field_combo = QComboBox()
        source_layout.addWidget(self.source_field_combo)
        layout.addLayout(source_layout)

        # IPA field (optional)
        self.use_ipa_checkbox = QCheckBox("Sử dụng trường IPA (phát âm chuẩn hơn)")
        self.use_ipa_checkbox.toggled.connect(self._on_use_ipa_toggled)
        layout.addWidget(self.use_ipa_checkbox)

        ipa_layout = QHBoxLayout()
        ipa_layout.addWidget(QLabel("Trường IPA (tùy chọn):"))
        self.ipa_field_combo = QComboBox()
        self.ipa_field_combo.setEnabled(False)  # Disabled by default
        ipa_layout.addWidget(self.ipa_field_combo)
        layout.addLayout(ipa_layout)

        # Help text for IPA
        ipa_help = QLabel(
            "⚠️ Experimental: IPA có thể không hoạt động tốt với hầu hết models. "
            "Khuyến nghị: TẮT và để Piper tự phân tích text thường (chính xác hơn)."
        )
        ipa_help.setWordWrap(True)
        ipa_help.setStyleSheet("color: #d9534f; font-size: 9pt; padding: 5px; font-weight: bold;")
        layout.addWidget(ipa_help)

        # Target field
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Trường đích (chứa âm thanh):"))
        self.target_field_combo = QComboBox()
        target_layout.addWidget(self.target_field_combo)
        layout.addLayout(target_layout)

        group.setLayout(layout)
        return group

    def _create_model_group(self) -> QGroupBox:
        """Tạo group chọn model"""
        group = QGroupBox("3. Chọn Model Giọng nói Piper")
        layout = QVBoxLayout()

        # Help text
        help_label = QLabel(
            "Chọn file model giọng nói (.onnx). "
            "Đề xuất: en_US-lessac-medium.onnx cho giọng Anh-Mỹ chất lượng cao."
        )
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        # Model path input and browse button
        model_layout = QHBoxLayout()
        self.model_path_input = QLineEdit()
        self.model_path_input.setPlaceholderText("Nhấn 'Browse' để chọn file model...")
        model_layout.addWidget(self.model_path_input)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._browse_model_file)
        model_layout.addWidget(browse_button)

        layout.addLayout(model_layout)

        # Download instructions link
        download_label = QLabel(
            '<a href="https://github.com/rhasspy/piper/releases">Tải model tại đây</a>'
        )
        download_label.setOpenExternalLinks(True)
        layout.addWidget(download_label)

        group.setLayout(layout)
        return group

    def _create_options_group(self) -> QGroupBox:
        """Tạo group tùy chọn"""
        group = QGroupBox("4. Tùy chọn")
        layout = QVBoxLayout()

        # Overwrite checkbox
        self.overwrite_checkbox = QCheckBox(
            "Ghi đè lên âm thanh đã có (mặc định: bỏ qua thẻ đã có âm thanh)"
        )
        layout.addWidget(self.overwrite_checkbox)

        # Speed control
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Tốc độ đọc:")
        speed_layout.addWidget(speed_label)

        self.length_scale_spinbox = QDoubleSpinBox()
        self.length_scale_spinbox.setMinimum(0.5)  # Nhanh nhất (200% tốc độ)
        self.length_scale_spinbox.setMaximum(4.0)  # Chậm nhất (25% tốc độ)
        self.length_scale_spinbox.setValue(2.0)    # Mặc định: 50% tốc độ
        self.length_scale_spinbox.setSingleStep(0.1)
        self.length_scale_spinbox.setDecimals(1)
        self.length_scale_spinbox.setSuffix("x")
        speed_layout.addWidget(self.length_scale_spinbox)

        speed_help = QLabel("(1.0 = Bình thường, 2.0 = Chậm 50%, 0.5 = Nhanh 200%)")
        speed_help.setStyleSheet("color: gray; font-size: 9pt;")
        speed_layout.addWidget(speed_help)
        speed_layout.addStretch()

        layout.addLayout(speed_layout)

        group.setLayout(layout)
        return group

    def _create_buttons(self) -> QHBoxLayout:
        """Tạo các nút điều khiển"""
        layout = QHBoxLayout()

        # Start button
        self.start_button = QPushButton("Bắt đầu")
        self.start_button.clicked.connect(self._on_start)
        self.start_button.setDefault(True)
        layout.addWidget(self.start_button)

        # Cancel button
        cancel_button = QPushButton("Hủy")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        return layout

    def _populate_note_types(self):
        """Điền danh sách Note Types"""
        if not mw or not mw.col:
            return

        note_types = mw.col.models.all_names_and_ids()
        self.note_type_combo.clear()

        for note_type in note_types:
            self.note_type_combo.addItem(note_type.name, note_type.id)

        # Chọn note type đã lưu trước đó (nếu có)
        if self.config.get('last_note_type'):
            index = self.note_type_combo.findText(self.config['last_note_type'])
            if index >= 0:
                self.note_type_combo.setCurrentIndex(index)

    def _on_use_ipa_toggled(self, checked: bool):
        """Xử lý khi checkbox IPA được bật/tắt"""
        self.ipa_field_combo.setEnabled(checked)

    def _on_note_type_changed(self, index: int):
        """Xử lý khi note type thay đổi"""
        if index < 0:
            return

        # Kiểm tra field combo đã được tạo chưa (tránh lỗi khi khởi tạo)
        if not hasattr(self, 'source_field_combo') or not hasattr(self, 'target_field_combo'):
            return

        # Lấy fields của note type
        note_type_name = self.note_type_combo.currentText()
        note_type_id = self.note_type_combo.currentData()

        if not mw or not mw.col:
            return

        model = mw.col.models.get(note_type_id)
        if not model:
            return

        field_names = [field['name'] for field in model['flds']]

        # Populate source field combo
        self.source_field_combo.clear()
        self.source_field_combo.addItems(field_names)

        # Tự động chọn "English" nếu có
        if 'English' in field_names:
            self.source_field_combo.setCurrentText('English')
        elif self.config.get('source_field') in field_names:
            self.source_field_combo.setCurrentText(self.config['source_field'])

        # Populate target field combo
        self.target_field_combo.clear()
        self.target_field_combo.addItems(field_names)

        # Tự động chọn "Audio" nếu có
        if 'Audio' in field_names:
            self.target_field_combo.setCurrentText('Audio')
        elif self.config.get('target_field') in field_names:
            self.target_field_combo.setCurrentText(self.config['target_field'])

        # Populate IPA field combo (if exists)
        if hasattr(self, 'ipa_field_combo'):
            self.ipa_field_combo.clear()
            self.ipa_field_combo.addItems(field_names)

            # Tự động chọn "IPA" hoặc field có chứa "ipa" (case insensitive)
            ipa_found = False
            for field in field_names:
                if field.lower() == 'ipa' or 'ipa' in field.lower():
                    self.ipa_field_combo.setCurrentText(field)
                    ipa_found = True
                    break

            # Nếu không tìm thấy field IPA, dùng config đã lưu
            if not ipa_found and self.config.get('ipa_field') in field_names:
                self.ipa_field_combo.setCurrentText(self.config['ipa_field'])

    def _browse_model_file(self):
        """Mở dialog chọn file model"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file model Piper (.onnx)",
            "",
            "ONNX Model Files (*.onnx);;All Files (*.*)"
        )

        if file_path:
            self.model_path_input.setText(file_path)

    def load_config(self):
        """Tải cấu hình đã lưu"""
        # Model path
        if self.config.get('model_path'):
            self.model_path_input.setText(self.config['model_path'])

        # Overwrite option
        self.overwrite_checkbox.setChecked(self.config.get('overwrite_existing', False))

        # Length scale (speed)
        self.length_scale_spinbox.setValue(self.config.get('length_scale', 2.0))

        # IPA option
        self.use_ipa_checkbox.setChecked(self.config.get('use_ipa', False))

    def _validate_config(self) -> tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của cấu hình

        Returns:
            tuple[bool, str]: (hợp lệ, thông báo lỗi)
        """
        # Kiểm tra note type
        if self.note_type_combo.currentIndex() < 0:
            return False, "Vui lòng chọn Note Type"

        # Kiểm tra source field
        if self.source_field_combo.currentIndex() < 0:
            return False, "Vui lòng chọn trường nguồn"

        # Kiểm tra target field
        if self.target_field_combo.currentIndex() < 0:
            return False, "Vui lòng chọn trường đích"

        # Kiểm tra model path
        model_path = self.model_path_input.text().strip()
        if not model_path:
            return False, "Vui lòng chọn file model giọng nói"

        if not os.path.exists(model_path):
            return False, f"File model không tồn tại: {model_path}"

        if not model_path.endswith('.onnx'):
            return False, "File model phải có định dạng .onnx"

        # Kiểm tra file config (.onnx.json)
        config_path = model_path + '.json'
        if not os.path.exists(config_path):
            return False, (
                f"Không tìm thấy file config: {config_path}\n\n"
                f"File config phải có cùng tên với model và thêm .json\n"
                f"Ví dụ: en_US-lessac-medium.onnx.json"
            )

        return True, ""

    def _on_start(self):
        """Xử lý khi nhấn nút Bắt đầu"""
        # Validate
        is_valid, error_msg = self._validate_config()
        if not is_valid:
            QMessageBox.warning(self, "Lỗi cấu hình", error_msg)
            return

        # Lưu các giá trị đã chọn
        self.selected_note_type = self.note_type_combo.currentText()
        self.selected_source_field = self.source_field_combo.currentText()
        self.selected_target_field = self.target_field_combo.currentText()
        self.selected_model_path = self.model_path_input.text().strip()
        self.overwrite_existing = self.overwrite_checkbox.isChecked()
        self.selected_length_scale = self.length_scale_spinbox.value()
        self.use_ipa = self.use_ipa_checkbox.isChecked()
        self.selected_ipa_field = self.ipa_field_combo.currentText() if self.use_ipa else None

        # Lưu config
        self._save_config()

        # Accept dialog
        self.accept()

    def _save_config(self):
        """Lưu cấu hình"""
        self.config['model_path'] = self.selected_model_path
        self.config['source_field'] = self.selected_source_field
        self.config['target_field'] = self.selected_target_field
        self.config['overwrite_existing'] = self.overwrite_existing
        self.config['last_note_type'] = self.selected_note_type
        self.config['length_scale'] = self.selected_length_scale
        self.config['use_ipa'] = self.use_ipa
        self.config['ipa_field'] = self.selected_ipa_field

    def get_config(self) -> dict:
        """
        Lấy cấu hình đã chọn

        Returns:
            dict: Cấu hình
        """
        return {
            'note_type': self.selected_note_type,
            'source_field': self.selected_source_field,
            'target_field': self.selected_target_field,
            'model_path': self.selected_model_path,
            'overwrite_existing': self.overwrite_existing,
            'length_scale': self.selected_length_scale,
            'use_ipa': self.use_ipa,
            'ipa_field': self.selected_ipa_field
        }
