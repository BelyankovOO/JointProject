import pygame
import os
import math


def cooldown_tick(cooldowns, delta, callbacks={}):
    """
    Decrease cooldown and if cooldown equal zero call function.

    :param cooldowns: dict
    :param delta: decrease from all cooldown
    :param callback: callback function
    """
    for name in cooldowns:
        if cooldowns[name] > 0:
            cooldowns[name] -= delta
            if cooldowns[name] <= 0:
                cooldowns[name] = 0
                if name in callbacks:
                    if callbacks[name] is not None:
                        callbacks[name]()


def load_images_by_dir(directory):
    """
    Load images in one direction.

    :param directory: directiory with image
    """
    image_names = os.listdir(directory)
    image_list = []
    for file in image_names:
        if ".png" in file:
            image_list.append(pygame.image.load(directory + "/" + file))
    return image_list


def load_images_by_dir_right(directory):
    """
    Load images in two direction (left and right).

    :param directory: directiory with image
    """
    image_names = os.listdir(directory)
    image_list = [[], []]
    for file in image_names:
        if ".png" in file:
            im_right = pygame.image.load(directory + "/" + file)
            im_left = pygame.transform.flip(im_right, True, False)
            image_list[0].append(im_left)
            image_list[1].append(im_right)
    return image_list


def vector_normalization(vector):
    """
    Normalize vector.

    :param vector: current vector
    """
    module = math.sqrt(vector[0]**2 + vector[1]**2)
    normalized_vector = (vector[0] / module, vector[1] / module)
    return normalized_vector
