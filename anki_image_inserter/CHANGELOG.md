# Changelog

All notable changes to the Image Inserter for Vocabulary Cards add-on will be documented in this file.

## [1.0.0] - 2025-11-05

### Added
- Initial release of Image Inserter for Vocabulary Cards
- Multi-source image search (Unsplash, Pexels, Pixabay)
- API integration with authentication
- Image compression and optimization
- Trial mode (20 cards) for testing
- Full processing mode for entire decks
- Pause/Resume functionality
- Progress tracking and status display
- API rate limit monitoring
- Bulk image deletion from target field
- Configurable source and target fields
- Adjustable images per card (1-20)
- User-friendly Qt-based interface
- Menu integration in Anki Tools menu
- Pre-configured API keys for immediate use
- State persistence across Anki restarts
- HTML image formatting for Anki fields
- Error handling and logging
- Comprehensive documentation

### Features
- Fast processing: 1000-2000 cards/hour
- Smart image compression: 85% JPEG quality
- Automatic resizing: max 800x600 pixels
- Clean images without ads or logos
- Landscape orientation preference
- Safe search enabled
- Rate limiting to respect API quotas
- Background processing with Qt threading
- Real-time progress updates

### Compatibility
- Anki version: 25.09.2
- Python: 3.13.5
- Qt: 6.9.1
- Chromium: 122

### Dependencies
- requests >= 2.31.0
- Pillow >= 10.0.0

### Documentation
- README.md with comprehensive usage guide
- INSTALLATION.md with step-by-step setup
- Inline code documentation
- Troubleshooting guide
- API usage information

## [Unreleased]

### Planned Features
- Google Images integration
- DuckDuckGo search support
- Bing Images integration
- Custom image filters
- Batch processing optimization
- Image preview before insertion
- Multiple image layout options
- Field mapping presets
- Export/import configurations
- Enhanced error recovery
- Offline image cache
- Image quality comparison

### Known Issues
- None reported yet

---

## Version History

The version numbering follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backward compatible)
- PATCH version for bug fixes (backward compatible)

## Feedback

Please report bugs, request features, or provide feedback through the add-on's homepage or contact the developer directly.
