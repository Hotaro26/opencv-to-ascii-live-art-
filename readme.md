
# ASCII Camera live art

Convert live camera feed into real-time ASCII art.

## Features

- **Live ASCII Conversion**: Real-time conversion of camera input to ASCII art
- **Terminal Display**: View ASCII art directly in your terminal
- **Save Frames**: Save ASCII art frames to text files
- **Simple Controls**: Press 'q' to quit, 's' to save current frame

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python ascii_camera.py
```

## Usage

Once the script is running:

- **Terminal display** will show live ASCII art representation of your camera feed
- Press **'s'** to save the current ASCII frame to a text file
- Press **'q'** to quit the application
- Adjust terminal width/font size for better ASCII art display

## Controls

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `s` | Save current frame as ASCII art to text file |

## Notes

- Works best in a terminal with dark background
- For best results, use a monospace font (e.g., Courier, Consolas)
- ASCII frames are saved with timestamps in the format: `ascii_frame_XXXX.txt`
- The camera feed is flipped horizontally for mirror effect
- Processing is optimized for 80-character width display

## Troubleshooting

- **Camera not opening**: Ensure your camera is connected and not in use by other applications
- **Garbled display**: Try resizing your terminal window
- **Slow performance**: Reduce terminal width or use a lower resolution camera





## Example Output

 https://github.com/user-attachments/assets/bcbdad51-c9be-4904-a91a-ba260d2c9c20




