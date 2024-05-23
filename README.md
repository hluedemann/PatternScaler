## PatternScaler

This repo provides some simple scripts that facilitate the work with seamless patterns and allow to extract cliparts from images with transparent background.
There are three seperate scripts that provide the following functionality:

1. **pattern_scaler.py**  

    * Scale patterns to the desired resolution
    * Create 2x2 format of the pattern
    * Convert all images into png and jpg format
    ```bash
    python pattern_scaler.py -f "/root/folder/of/patterns"
    ```
2. **pattern_scaler_clipart.py**  
    This script provides similar functionality as `pattern_scaler.py` but is used for patterns where the background is transparent.

    * Scale patterns to teh desired resolution
    * Create 2x2 format and patterns with white, black and transparent background
    * Convert images to png and jpg format
    ```bash
    python pattern_scaler.py -f "/root/folder/of/clipart/patterns"
    ```

3. **split_clipart.py**  
    This script provides the functionality to split different clipart motifs that are inside one single image with transparent background int separate images.

    * Extract all clipart motifs contained inside an image
    ```bash
    python pattern_scaler.py -f "/root/folder/of/clipart/images"
    ```