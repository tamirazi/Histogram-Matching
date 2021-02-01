import matplotlib.pyplot as plt
import argparse
import os
import pathlib
from skimage import io, color, util, exposure

# Usage example :python .\main.py -p C:\Desktop\images -r C:\Desktop\images\ref.jpg -d f


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        return None


def histogram_match(src, ref):
    # Open reference and source files
    reference = io.imread(ref)
    image = io.imread(src)
    image_gray = color.rgb2gray(image)

    # Histogram matching
    matched = exposure.match_histograms(image, reference, multichannel=True)
    matched_gray = color.rgb2gray(matched)

    # Calculate the diff between image and matched
    diff = util.compare_images(matched_gray, image_gray, method='diff')
    diff = color.gray2rgb(diff)

    return (image, reference, matched, diff)


def save_proccess_plot(image, reference, matched, diff, name):
    # Configure all the plots
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
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
    plt.savefig('{}'.format(name))
    plt.close()


def args_config():
    parser.add_argument('-p', type=dir_path, nargs=1, required=True, metavar='PATH',
                        help='Folder with the pictures for repair')
    parser.add_argument('-r', type=file_path, nargs=1, required=True, metavar='REFERENCE',
                        help='Reference image')
    parser.add_argument('-d', type=str2bool, metavar='DEBUG',
                        help='Export debug plots', default=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Color balancing script by Tamir Azizi")
    args_config()
    args = parser.parse_args()
    directory = args.p[0]
    directory_name = directory.split("\\")[-1]
    OUT = "\\..\\{}_balanced".format(directory_name)
    DEBUG = "\\..\\{}_debug".format(directory_name)
    reference_image = args.r[0]
    debug_mode = args.d
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file = os.path.join(directory, filename)
            print("Balancing: {}".format(filename))
            image, reference, matched, diff = histogram_match(
                file, reference_image)
            # Create output folder if not exist
            if not os.path.exists(directory + OUT):
                os.makedirs(directory + OUT)
            # Save color balanced image
            io.imsave(directory + OUT +
                      "\\{}".format(filename), matched, quality=100)
            if debug_mode == True:
                # Create debug folder if not exist
                if not os.path.exists(directory + DEBUG):
                    os.makedirs(directory + DEBUG)
                # Save debug plot (src, ref, res, diff)
                save_proccess_plot(image, reference, matched,
                                   diff, directory + DEBUG + "\\d_{}".format(filename))
