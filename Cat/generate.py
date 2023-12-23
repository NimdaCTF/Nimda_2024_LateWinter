from PIL import Image, ImageDraw, ImageFont
import os
from random import choice
import sys
import hmac

PREFIX = "nimda_Lo0K_@t_YoUr$elf_"
SECRET = b"drums-donkey-jam-tetris-beat-meat-king-kong"
SALT_SIZE = 12


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[2]

    frames_dir = 'frames/'
    frame_files = [f for f in os.listdir(frames_dir) if f.endswith('.png')]
    frame_files.sort(key=lambda x: int(x.split('_')[1]))

    frames = []

    for frame_file in frame_files:
        frame = Image.open(os.path.join(frames_dir, frame_file))
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')

        frames.append(frame)

    poisoned = choice(frames[50:])

    draw = ImageDraw.Draw(poisoned)
    font = ImageFont.load_default()
    text = get_flag()

    draw.text((150, 150), text, fill=(255, 0, 0), font=font)

    output_gif = os.path.join(target, 'result.gif')

    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[0:],
        optimize=True,
        duration=100000,
        loop=0
    )


if __name__ == '__main__':
    generate()
