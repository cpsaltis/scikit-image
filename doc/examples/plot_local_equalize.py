"""
===============================
Local Histogram Equalization
===============================

This examples enhances an image with low contrast, using a method called
*local histogram equalization*, which "spreads out the most frequent intensity
values" in an image .
The equalized image [1]_ has a roughly linear cumulative distribution function for each pixel neighborhood.
The local version [2]_ of the histogram equalization emphasized every local graylevel variations.

.. [1] http://en.wikipedia.org/wiki/Histogram_equalization
.. [2] http://en.wikipedia.org/wiki/Adaptive_histogram_equalization

"""

from skimage import data
from skimage.util.dtype import dtype_range
from skimage import exposure
from skimage.morphology import disk

import matplotlib.pyplot as plt

import numpy as np
from skimage.filter import rank


def plot_img_and_hist(img, axes, bins=256):
    """Plot an image along with its histogram and cumulative histogram.

    """
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(img, cmap=plt.cm.gray)
    ax_img.set_axis_off()

    # Display histogram
    ax_hist.hist(img.ravel(), bins=bins)
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')

    xmin, xmax = dtype_range[img.dtype.type]
    ax_hist.set_xlim(xmin, xmax)

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(img, bins)
    ax_cdf.plot(bins, img_cdf, 'r')

    return ax_img, ax_hist, ax_cdf


# Load an example image
img = data.moon()

# Contrast stretching
p2 = np.percentile(img, 2)
p98 = np.percentile(img, 98)
img_rescale = exposure.equalize_hist(img)

# Equalization
selem = disk(30)
img_eq = rank.equalize(img, selem=selem)


# Display results
f, axes = plt.subplots(2, 3, figsize=(8, 4))

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img, axes[:, 0])
ax_img.set_title('Low contrast image')
ax_hist.set_ylabel('Number of pixels')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_rescale, axes[:, 1])
ax_img.set_title('Global equalise')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_eq, axes[:, 2])
ax_img.set_title('Local equalize')
ax_cdf.set_ylabel('Fraction of total intensity')


# prevent overlap of y-axis labels
plt.subplots_adjust(wspace=0.4)
plt.show()
