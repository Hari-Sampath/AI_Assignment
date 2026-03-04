import random
import string

from PIL import Image, ImageDraw, ImageFont


def generate_captcha(text=""):
    if not text:
        text = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Create a blank image with a light background
    img = Image.new("RGB", (200, 60), color=(240, 240, 240))
    d = ImageDraw.Draw(img)

    for _ in range(10):  # adding noise
        d.line(
            [
                (random.randint(0, 200), random.randint(0, 60)),
                (random.randint(0, 200), random.randint(0, 60)),
            ],
            fill=(0, 0, 0),
            width=1,
        )

    d.text((40, 15), text, fill=(50, 50, 250))

    img.save("captcha.png")
    img.show()
    print(f"CAPTCHA generated! (Secret: {text})")
    return text


# Example Usage
secret_code = generate_captcha()
user_input = input("Enter the code you see in captcha.png: ")

if user_input.upper() == secret_code:
    print("Verification Successful. You are human.")
else:
    print("Verification Failed.")
