from image_utils import convert_rgb_to_bw, invert_bin_image

from PIL import Image
import PIL.ImageOps
import PIL.ImageChops

import matplotlib.pyplot as plt

base_dir = 'Map-9'

original_env = convert_rgb_to_bw(Image.open(base_dir + '/' + 'original_map.png'))
observed_env = convert_rgb_to_bw(Image.open(base_dir + '/' + 'observed_map.png'))

original_env_inv = invert_bin_image(original_env)
observed_env_inv = invert_bin_image(observed_env)

new_obstacles = PIL.ImageChops.subtract(observed_env_inv, original_env_inv)

plt.imshow(new_obstacles)
plt.show()

