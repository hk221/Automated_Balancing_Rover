from PIL import Image
import io

# Load the PNG image using PIL/Pillow
image = Image.open('image.png')

# Convert the image to byte stream
byte_stream = io.BytesIO()
image.save(byte_stream, format='PNG')
byte_stream.seek(0)

# Read the byte stream
byte_data = byte_stream.read()

# Close the byte stream
byte_stream.close()

