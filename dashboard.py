from PIL import Image
import requests
import os
import random
import glob
from PIL import ImageDraw
from PIL import ImageFilter

# URL of the image to download
image_url = "http://profilepics.cf.kik.com/rUHAExq1aGWSH7hvuUDzwoshOgY/orig.jpg"
# Path to the folder where the image will be saved
folder_path = "c:/Users/holyk/Desktop/code/kikbot-blackjackbot/images/temp"


def get_user_profile(folder_path, image_url):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Send a GET request to download the image
    response = requests.get(image_url)

    # Extract the filename from the URL
    filename = os.path.basename(image_url)

    # Save the image to the specified folder
    image_path = os.path.join(folder_path, filename)
    with open(image_path, "wb") as file:
        file.write(response.content)
    return Image.open(image_path)

def create_and_paste_image():
    image_files = glob.glob("images/backgrounds/*.jpg")

    random_image_file = random.choice(image_files)
    random_image = Image.open(random_image_file)
    random_image = random_image.filter(ImageFilter.BLUR())

    hex_guide = Image.open("images/guides/Untitled96_20240218160236.png")
    hex_guide = hex_guide.resize((300, 300))

    profile_picture = get_user_profile(folder_path, image_url)
    new_image = profile_picture.resize((300, 300)).convert("RGBA")

    # Crop the image to a 1:1 ratio
    width, height = random_image.size
    if width > height:
        left = (width - height) // 2
        right = left + height
        top = 0
        bottom = height
    else:
        top = (height - width) // 2
        bottom = top + width
        left = 0
        right = width

    cropped_image = random_image.crop((left, top, right, bottom))

    # Resize the cropped image to 1000x1000
    resized_image = cropped_image.resize((1000, 1000)).convert("RGBA")
    resized_image.save("images/final_products/resized_image.png")

    # Open the original image
    # mask = Image.new('RGBA', (300, 300), )
    
    if new_image.size == hex_guide.size:
        new_image.paste(hex_guide, (0, 0), mask=hex_guide)
        # Convert all white pixels to transparent
        new_image = new_image.convert("RGBA")
        data = new_image.getdata()
        new_data = []
        for item in data:
            # Set the alpha value to 0 for white pixels
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        new_image.putdata(new_data)
        new_image.save("images/final_products/new_image.png")
    else:
        print("Error: Images do not have the same dimensions.")


    x = (resized_image.width - new_image.width) - 50
    y = 50

    # Paste the resized image in the center of the new image
    resized_image.paste(new_image, (x, y), mask=new_image)
    # new_image.paste(resized_image, (x, y))

    # Save the new image
    resized_image.save("images/final_products/final_image.png")

    draw = ImageDraw.Draw(resized_image)
    border_color = (127, 0, 255, 50)
    border_width = 10
    border_radius = 20

    # Calculate the coordinates of the box
    x1 = 30
    y1 = 230

    for i in range(7):
        x2 = x1 + 450
        y2 = y1 + 60

        # Draw the rounded rectangle
        draw.rounded_rectangle([(x1, y1), (x2, y2)], fill=border_color , outline=border_color, width=border_width, radius=border_radius)
        y1+= 100
    # Save the modified image
        draw.rounded_rectangle([(550, 400), (950, 900)], fill=border_color , outline=border_color, width=border_width, radius=border_radius)
    
    resized_image.save("images/final_products/final_image_with_box.png")





# Call the function with the image_path variable
create_and_paste_image()

# Now you can use the image_path variable to work with the downloaded image