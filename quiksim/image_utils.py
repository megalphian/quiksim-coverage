# Convert to bw
def convert_rgb_to_bw(img, thresh = 225, bin=True):

    # Source: https://stackoverflow.com/a/50090612/13808688

    fn = lambda x : 255 if x >= thresh else 0
    if(bin):
        img = img.convert('L').point(fn, mode='1')

    return img