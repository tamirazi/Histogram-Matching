import matplotlib.pyplot as plt
import cv2
from skimage import exposure
from skimage.exposure import match_histograms


def histogram_match(src, ref):
    # Open reference and source files
    reference = cv2.imread(ref, 1)
    reference = cv2.cvtColor(reference, cv2.COLOR_BGR2RGB)
    image = cv2.imread(src, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Histogram matching
    matched = match_histograms(image, reference, multichannel=True)
    matched_gray = cv2.cvtColor(matched, cv2.COLOR_BGR2GRAY)

    # Calculate the diff between image and matched
    diff = cv2.absdiff(matched_gray, image_gray)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2RGB)

    return (image, reference, matched, diff)


def save_proccess_plot(image, reference, matced, diff, name):
    # Configure all the plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    for aa in (ax1, ax2, ax3, ax4):
        aa.set_axis_off()

    ax1.imshow(image)
    ax1.set_title('Source')
    ax2.imshow(reference)
    ax2.set_title('Reference')
    ax3.imshow(matched)
    ax3.set_title('Matched')
    ax4.imshow(diff)
    ax4.set_title('Diff')

    plt.tight_layout()
    plt.savefig('{}.png'.format(name))


image, reference, matched, diff = histogram_match(
    './/imgs//0004.jpg', './/imgs//0003.jpg')
save_proccess_plot(image, reference, matched, diff, 'test')
