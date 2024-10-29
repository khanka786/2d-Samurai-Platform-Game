# Utilities File

import os
import pygame

BASE_IMG_PATH = 'data/images/'

# Allow only png files to be imported 
valid_extensions = ['png', 'jpg']

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    base_path = BASE_IMG_PATH + path

    for img_name in sorted(os.listdir(base_path)):
        
        if not img_name.startswith('.') and img_name.split('.')[-1].lower() in valid_extensions:
            print(f"Loading image: {base_path + '/' + img_name}")
            images.append(load_image(path + '/' + img_name))
        else:
            print(f"Ignoring file: {img_name}")

    return images


# Create the player animation & update it in the main.py file
class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0


    # Copies the current animation regardless of the frame and returns the value for images, image_duration, and the current loop
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)


    # Updates the current frame and animation
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            if self.frame < self.img_duration * len(self.images) - 1:
                self.frame += 1
            else:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
