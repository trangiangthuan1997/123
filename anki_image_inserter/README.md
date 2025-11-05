# Image Inserter for Vocabulary Cards - Anki Add-on

Automatically inserts relevant images into your Anki vocabulary cards from multiple high-quality image sources.

## Features

- **Multiple Image Sources**: Search images from Unsplash, Pexels, and Pixabay using their APIs
- **Intelligent Image Selection**: Finds up to 6 relevant images per vocabulary word
- **Optimized Performance**:
  - Compressed images to minimize memory usage
  - Fast processing speed (1000-2000 cards/hour)
  - Clear, high-quality images without ads or logos
- **Flexible Processing**:
  - Trial mode: Test with 20 cards
  - Full mode: Process all cards in a deck
  - Pause/Resume: Maintain progress even after Anki restarts
- **Easy Management**:
  - Delete all images from target field
  - Select source and target fields
  - Configure number of images per card
  - API status monitoring

## Requirements

- Anki version 25.09.2 or compatible
- Python 3.13.5 (bundled with Anki)
- Qt 6.9.1 (bundled with Anki)
- Dependencies (auto-installed):
  - requests
  - Pillow

## Installation

### Method 1: Manual Installation

1. Download this add-on folder
2. Copy the `anki_image_inserter` folder to your Anki add-ons directory:
   - **Windows**: `%APPDATA%\Anki2\addons21\`
   - **Mac**: `~/Library/Application Support/Anki2/addons21/`
   - **Linux**: `~/.local/share/Anki2/addons21/`

3. Install required Python packages:
   - Open Anki
   - Go to Tools → Add-ons
   - Select the add-on
   - Click "View Files"
   - Open terminal/command prompt in that directory
   - Run: `pip install -r requirements.txt`

4. Restart Anki

### Method 2: From Anki Add-ons Browser

*(If published to AnkiWeb)*

1. Open Anki
2. Go to Tools → Add-ons → Get Add-ons
3. Enter the add-on code
4. Click OK
5. Restart Anki

## Configuration

### API Keys Setup

The add-on comes pre-configured with API keys, but you can update them in the UI:

1. Open Anki
2. Go to Tools → Image Inserter for Vocabulary
3. Enter your API keys in the "API Keys" section:
   - **Unsplash**: Get key from https://unsplash.com/developers
   - **Pexels**: Get key from https://www.pexels.com/api/
   - **Pixabay**: Get key from https://pixabay.com/api/docs/

### Default Configuration

The add-on includes these default settings (can be modified in config.json):

```json
{
    "source_field": "English",
    "target_field": "Image",
    "images_per_card": 6,
    "image_quality": 85,
    "max_image_width": 800,
    "max_image_height": 600
}
```

## Usage

### Basic Workflow

1. **Open the Add-on**:
   - Go to Tools → Image Inserter for Vocabulary

2. **Configure Settings**:
   - Select your deck from the dropdown
   - Set source field (e.g., "English" - field containing vocabulary words)
   - Set target field (e.g., "Image" - field where images will be inserted)
   - Choose number of images per card (1-20)

3. **Check API Status** (Optional):
   - Click "Refresh API Status" to see remaining API requests

4. **Run Processing**:
   - **Trial Mode**: Click "Run Trial (20 cards)" to test with 20 cards
   - **Full Mode**: Click "Run All Cards" to process entire deck

5. **Monitor Progress**:
   - Watch the progress bar and status messages
   - Use "Pause" button to pause processing
   - Click "Resume" to continue

6. **Delete Images** (if needed):
   - Click "Delete All Images" to remove all images from target field in selected deck

### Tips for Best Results

- **Source Field Content**: Ensure your source field contains clear, single vocabulary words
- **Image Quality**: Default settings provide good balance between quality and file size
- **API Limits**:
  - Unsplash: 50 requests/hour (free tier)
  - Pexels: 200 requests/hour (free tier)
  - Pixabay: 5000 requests/hour (free tier)
- **Processing Speed**: Approximately 1000-2000 cards/hour depending on:
  - Internet connection speed
  - API response times
  - Number of images per card

### Troubleshooting

**No images found**:
- Check internet connection
- Verify API keys are correct
- Try different vocabulary words
- Check API rate limits

**Images not appearing**:
- Verify target field exists in your note type
- Check Anki's media folder is writable
- Restart Anki to refresh media database

**Slow processing**:
- Reduce number of images per card
- Check internet speed
- Use trial mode first to estimate time

**Pause/Resume not working**:
- State is saved automatically
- Restart the add-on to resume from last position

## Technical Details

### Image Processing

- **Download**: Images fetched via API endpoints
- **Compression**: JPEG format with 85% quality (configurable)
- **Resizing**: Max 800x600 pixels (configurable)
- **Storage**: Anki media folder with unique filenames
- **Format**: HTML img tags in target field

### API Integration

**Priority Sources** (checked in order):
1. Unsplash - High-quality photos from professional photographers
2. Pexels - Free stock photos and videos
3. Pixabay - Free images and royalty-free stock

**Image Selection Criteria**:
- Landscape orientation preferred
- No commercial content or logos
- Safe search enabled (Pixabay)
- Relevant to search query

### Data Storage

- **Configuration**: Stored in Anki's add-on config
- **Progress State**: Saved to `image_inserter_state.json`
- **Images**: Stored in Anki's media folder

## License

This add-on is provided as-is for educational purposes.

## API Usage Terms

Please review the terms of service for each image provider:
- Unsplash: https://unsplash.com/terms
- Pexels: https://www.pexels.com/terms-of-service/
- Pixabay: https://pixabay.com/service/terms/

## Support

For issues, bugs, or feature requests, please contact the developer or check the add-on's homepage.

## Version History

### 1.0.0 (2025-11-05)
- Initial release
- Support for Unsplash, Pexels, and Pixabay APIs
- Trial mode and full processing mode
- Pause/Resume functionality
- Image compression and optimization
- API status monitoring
- Bulk image deletion

## Credits

Developed for Anki 25.09.2 with Python 3.13.5, Qt 6.9.1, and Chromium 122.
