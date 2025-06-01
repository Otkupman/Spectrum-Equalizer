# Spectrum Equalizer: Color Gradient Divider

## Description
Spectrum Equalizer is a compact, user-friendly tool for dividing color spectrums into any number of shades. The program visualizes smooth color transitions, provides precise color values in major color models, and allows direct code usage.
![Spectral Imaging](https://github.com/Otkupman/Spectrum-Equalizer/blob/main/Spectral%20Imaging.png)

## Features
✔ Flexible spectrum division — Any number of colors (from 2 to ∞)  
✔ Gradient visualization — Intuitive spectrum display  
✔ Detailed color codes — Precise values in:
   - RGB (Red, Green, Blue)
   - HEX (Hexadecimal)
   - HSV/HSB (Hue, Saturation, Value/Brightness)
   - HSL/I (Hue, Saturation, Lightness/Intensity)
   - CMYK (Cyan, Magenta, Yellow, Key/Black)  

✔ Algorithm choice:
   - Linear interpolation through HSV space
     ![Linear interpolation screenshot](https://github.com/Otkupman/Spectrum-Equalizer/blob/main/Demo%20Linear.png)
   - Circular interpolation (shortest path around color wheel)
     ![Circular interpolation screenshot](https://github.com/Otkupman/Spectrum-Equalizer/blob/main/Demo%20Circular.png)

✔ Convenient copying:
   - Right-click context menu
   - Double-click for quick HEX copy  

✔ Full palette export — "Copy all" button for complete color transfer  

## Target Users
🎨 Designers — Creating harmonious color schemes  
👩‍🎨 Digital Artists — Studying smooth transitions for painting  
👨‍💻 Web Developers — Quick HEX generation for CSS  
📊 Data Analysts — Visualizing data with color scales  
🌈 Colorimetrists — Calculating color coordinates, quantization evaluation, pseudocolor creation  

## Technical Specifications
🔹 Python 3 implementation using Tkinter  
🔹 Clipboard support via pyperclip  
🔹 Responsive UI with compact element arrangement  

## Quick Start
1. Download portable Windows executable (~11MB) from [Releases](https://github.com/Otkupman/Spectrum-Equalizer/releases)  
2. Select preferred algorithm  
3. Choose start/end colors  
4. Enter desired divisions count  
5. Click "Generate" or press Enter  
