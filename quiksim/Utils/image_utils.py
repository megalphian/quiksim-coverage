# Convert to bw
def convert_rgb_to_bw(img, thresh = 225, bin=True):

    # Source: https://stackoverflow.com/a/50090612/13808688

    fn = lambda x : 255 if x >= thresh else 0
    if(bin):
        img = img.convert('L').point(fn, mode='1')

    return img

def invert_bin_image(img):
    fn = lambda x : 0 if x == 255 else 255
    img = img.point(fn, mode='1')

    return img
