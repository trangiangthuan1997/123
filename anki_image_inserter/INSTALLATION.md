# Installation Guide - Image Inserter for Vocabulary Cards

## Quick Installation Steps

### Step 1: Install the Add-on

1. **Locate your Anki add-ons folder**:
   - Open Anki
   - Go to Tools → Add-ons
   - Click "View Files" button
   - This opens your add-ons folder

2. **Copy the add-on**:
   - Copy the entire `anki_image_inserter` folder into the add-ons directory
   - The path should look like: `.../addons21/anki_image_inserter/`

### Step 2: Install Dependencies

The add-on requires two Python packages: `requests` and `Pillow`.

#### Option A: Automatic Installation (Recommended)

Most modern Anki installations bundle these packages. Try running the add-on first; if it works, you're done!

#### Option B: Manual Installation

If you get import errors, install dependencies manually:

**On Windows:**
```bash
cd "%APPDATA%\Anki2\addons21\anki_image_inserter"
python -m pip install -r requirements.txt
```

**On Mac:**
```bash
cd ~/Library/Application\ Support/Anki2/addons21/anki_image_inserter
python3 -m pip install -r requirements.txt
```

**On Linux:**
```bash
cd ~/.local/share/Anki2/addons21/anki_image_inserter
python3 -m pip install -r requirements.txt
```

### Step 3: Restart Anki

1. Close Anki completely
2. Reopen Anki
3. Check that "Image Inserter for Vocabulary" appears in Tools menu

### Step 4: Configure API Keys

1. Open the add-on: Tools → Image Inserter for Vocabulary
2. The add-on comes with pre-configured API keys
3. (Optional) Enter your own API keys if you have them:
   - Unsplash: https://unsplash.com/developers
   - Pexels: https://www.pexels.com/api/
   - Pixabay: https://pixabay.com/api/docs/

### Step 5: Test the Add-on

1. Select a deck with vocabulary cards
2. Set source field (e.g., "English")
3. Set target field (e.g., "Image")
4. Click "Run Trial (20 cards)"
5. Watch the progress bar

## Troubleshooting Installation

### Add-on doesn't appear in Tools menu

- Check folder structure: the files should be in `addons21/anki_image_inserter/`
- Verify files exist: `__init__.py`, `manifest.json`, etc.
- Restart Anki
- Check Anki console (Tools → Add-ons → select add-on → "View Files" → check for errors)

### Import errors (requests or Pillow)

Install dependencies manually (see Step 2, Option B above)

### Permission errors

- Run Anki with administrator/sudo privileges
- Check file permissions on add-ons folder
- Ensure antivirus isn't blocking installation

### API errors

- Verify internet connection
- Check API keys are entered correctly
- Refresh API status to check rate limits
- Try different vocabulary words

## Verification Checklist

- [ ] Add-on folder copied to correct location
- [ ] Dependencies installed (requests, Pillow)
- [ ] Anki restarted
- [ ] "Image Inserter for Vocabulary" appears in Tools menu
- [ ] Dialog opens without errors
- [ ] API status shows available requests
- [ ] Trial mode processes cards successfully

## Getting Help

If you encounter issues:

1. Check the README.md for detailed documentation
2. Verify all installation steps completed
3. Check Anki version compatibility (25.09.2 or similar)
4. Review error messages in Anki's console
5. Ensure Python version is 3.13.5 or compatible

## Pre-configured API Keys

The add-on comes with the following pre-configured API keys:

- **Unsplash**: OtEMymIeSCu1lPVusDbWdMW0pqTB3xkMvc6PlYGF-Z4
- **Pexels**: KgzxcRtVKNlbNAHsNphj25g0tJJSR7k6qbF2nS0R2BqBXkyedLe57pDw
- **Pixabay**: 52801659-83850f13953d17e2275f05b6b

These keys are embedded in the `config.json` file and will work immediately after installation.

## Next Steps

After successful installation:

1. Read the README.md for usage instructions
2. Try trial mode with 20 cards
3. Review the results
4. Adjust settings as needed
5. Process your full deck

Enjoy automatic image insertion for your vocabulary cards!
