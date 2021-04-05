import pygame
import os

'''
cooldown_tick(cooldowns, delta, callbacks={})
cooldowns - словарь {имя : текущее время}
delta - текущая разница во времени (то, что надо отнять от всех КД)
callbacks - словарь {имя : функция}, вызвать функцию, если соответствующий таймер стал равным 0
'''
def cooldown_tick(cooldowns, delta, callbacks={}):
	for name in cooldowns:
		if cooldowns[name] > 0:
			cooldowns[name] -= delta
			if cooldowns[name] <= 0:
				cooldowns[name] = 0
				if name in callbacks:
					callbacks[name]()

def load_images_by_dir(directory):
	image_names =  os.listdir(directory)
	image_list = []
	for file in image_names:
		if ".png" in file:
			image_list.append(pygame.image.load(directory+"/"+file))
	return image_list

def load_images_by_dir_right(directory):
	image_names =  os.listdir(directory)
	image_list = [[],[]]
	for file in image_names:
		if ".png" in file:
			im_right = pygame.image.load(directory+"/"+file)
			im_left = pygame.transform.flip(im_right, True, False)
			image_list[0].append(im_left)
			image_list[1].append(im_right)
	return image_list

