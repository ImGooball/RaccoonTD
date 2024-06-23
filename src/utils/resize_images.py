from PIL import Image

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(output_path)

# Resize tower image
resize_image('tower.png', 'tower_resized.png', (64, 64))

# Resize enemy image
resize_image('enemy.png', 'enemy_resized.png', (64, 64))
