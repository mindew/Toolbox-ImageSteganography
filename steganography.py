"""A program that encodes and decodes hidden messages in images through LSB steganography"""

from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    red_pixels = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    # create new image with the mode of "RGB" with size of encoded_image.size
    pixels = decoded_image.load()

    for a in range(x_size):
        for b in range(y_size):
            if bin(red_pixels[a, b])[-1] == '1':
                # convert an integer number to a binary string
                pixels[a, b] = (255, 255, 255)
            else:
                pixels[a, b] = (0, 0, 0)

    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    image = Image.open(template_image)
    # set x and y size of the image
    x_size = image.size[0]
    y_size = image.size[1]

    text_image = write_text(text_to_encode, image.size)
    secret_pixels = text_image.load()
    pixels = image.load()
    # set pixels of encoded_image

    encoded_image = Image.new("RGB", image.size)
    encoded_pixels = encoded_image.load()

    for a in range(x_size):
        for b in range(y_size):
            if secret_pixels[a, b][0] > 0:
                if bin(pixels[a, b][0])[-1] == '0':
                    encoded_pixels[a, b] = (pixels[a, b][0] | 1, pixels[a, b][1], pixels[a, b][2])
                else:
                    encoded_pixels[a, b] = (pixels[a, b][0], pixels[a, b][1], pixels[a, b][2])

            else:
                if bin(pixels[a, b][0])[-1] == '1':
                    encoded_pixels[a, b] = (pixels[a, b][0] & ~1, pixels[a, b][1], pixels[a, b][2])
                else:
                    encoded_pixels[a, b] = (pixels[a, b][0], pixels[a, b][1], pixels[a, b][2])
    # save the encoded_image
    encoded_image.save('images/encoded_image.png')


if __name__ == '__main__':

    print("Encoding the image...")
    encode_image("Apple is delicious")

    print("Decoding the image...")
    decode_image('images/encoded_image.png')
