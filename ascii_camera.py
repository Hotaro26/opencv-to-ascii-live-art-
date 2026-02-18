import cv2
import numpy as np
import os
import sys

# Tiny ASCII characters from dark to light - minimal detail
ASCII_CHARS = ['@', '#', '%', '?', '*', '+', ':', ',', '.', ' ']

def resize_to_square(image, new_width=70):
    """Crop to square and resize"""
    height, width = image.shape[:2]
    # Create square by cropping
    size = min(height, width)
    y_offset = (height - size) // 2
    x_offset = (width - size) // 2
    square_image = image[y_offset:y_offset+size, x_offset:x_offset+size]
    
    # Resize for ASCII display (smaller)
    new_height = int(new_width * 0.55)  # Account for character aspect ratio
    resized = cv2.resize(square_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized

def enhance_image(image):
    """Enhance image for better detail"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Light bilateral filter for smoothing
    enhanced = cv2.bilateralFilter(enhanced, 5, 50, 50)
    
    # Normalize
    enhanced = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
    
    return enhanced

def image_to_ascii(image, new_width=70):
    """Convert image to compact ASCII art"""
    try:
        # Resize to square
        image = resize_to_square(image, new_width)
        
        # Enhance for better details
        enhanced = enhance_image(image)
        
        # Convert to ASCII
        height, width = enhanced.shape
        ascii_art = ""
        
        for y in range(height):
            line = ""
            for x in range(width):
                pixel_value = int(enhanced[y, x])
                pixel_value = max(0, min(255, pixel_value))
                # Map to ASCII
                char_index = int(pixel_value * (len(ASCII_CHARS) - 1) / 255)
                char_index = max(0, min(len(ASCII_CHARS) - 1, char_index))
                line += ASCII_CHARS[char_index]
            ascii_art += line + "\n"
        
        return ascii_art
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main function for ASCII camera"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print(" Error: Could not open camera")
        print("   - Check if camera is connected")
        print("   - Check if another app is using it")
        return
    
    # Camera settings
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✓ ASCII Camera Started")
    print("=" * 75)
    print("CONTROLS: q=quit | s=save | c=more contrast | x=less contrast | r=reset")
    print("=" * 75 + "\n")
    
    frame_count = 0
    contrast_level = 50
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Mirror effect
            frame = cv2.flip(frame, 1)
            
            # Apply contrast
            frame = cv2.convertScaleAbs(frame, alpha=1 + (contrast_level - 50) / 100, beta=0)
            
            # Convert to ASCII
            ascii_art = image_to_ascii(frame, new_width=70)
            
            if ascii_art:
                clear_screen()
                print(ascii_art)
                status = f"Frame: {frame_count:04d} | Contrast: {contrast_level:3d} | 'h'=help"
                print(status)
            
            # Keyboard input
            key = cv2.waitKey(50) & 0xFF
            
            if key == ord('q'):
                break
            
            elif key == ord('s'):
                filename = f"ascii_face_{frame_count:04d}.txt"
                try:
                    with open(filename, 'w') as f:
                        f.write(ascii_art)
                    print(f"\n✓ Saved: {filename}")
                    input("Press Enter...")
                except Exception as e:
                    print(f" Error: {e}")
            
            elif key == ord('c'):
                contrast_level = min(contrast_level + 5, 100)
            
            elif key == ord('x'):
                contrast_level = max(contrast_level - 5, 0)
            
            elif key == ord('r'):
                contrast_level = 50
            
            elif key == ord('h'):
                print("\n" + "="*75)
                print("CONTROLS:")
                print("  q - Quit")
                print("  s - Save current frame")
                print("  c - Increase contrast")
                print("  x - Decrease contrast")
                print("  r - Reset to default")
                print("="*75)
                input("Press Enter to continue...")
            
            frame_count += 1
    
    except KeyboardInterrupt:
        print("\n✓ Stopped by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Camera closed")

if __name__ == "__main__":
    main()


