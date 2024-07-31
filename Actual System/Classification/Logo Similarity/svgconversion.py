import cairosvg
from PIL import Image
import io

def svg_to_png(svg_path, png_path, output_width=None, output_height=None):
    # Convert SVG to PNG bytes
    png_bytes = cairosvg.svg2png(url=svg_path)
    
    # Load PNG bytes into PIL Image
    image = Image.open(io.BytesIO(png_bytes))
    

    
    # Save the image to the specified path
    image.save(png_path, 'PNG')
    print(f"Converted {svg_path} to {png_path}")

# Example usage
svg_path = 'logo-1.svg'
png_path = 'example.png'
svg_to_png(svg_path, png_path, output_width=800, output_height=600)
