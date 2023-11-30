import numpy as np
import cv2


#we need to cal cumli sum
def calculateCumulativeSum(hist):
    cdf = np.zeros_like(hist)
    cum_sum = 0
    for i in range(len(hist)):
        cum_sum += hist[i]
        cdf[i] = cum_sum
    return cdf

def calculateHistogram(channel):
     # calculatte histogram of input channel
    hist = np.zeros(256)
    for pixel in np.nditer(channel):
        hist[pixel] += 1
    return hist



def histogramEqualizationColor(img):
    # split the image into rgba
    R, G, B = cv2.split(img)

    # apply tio each chanel
    R_eq = histogramEqualizationChannel(R)
    G_eq = histogramEqualizationChannel(G)
    B_eq = histogramEqualizationChannel(B)

    # merge the equlized channels back
    return cv2.merge((R_eq, G_eq, B_eq))


def histogramEqualizationChannel(channel):
    #the histogram chanel has to be changed maiually
    hist = calculateHistogram(channel)

    #  calculate cumul distri of the histogrm
    cdf = calculateCumulativeSum(hist)

    # we need to make sure the cdf is nortmal
    cdf_min = cdf.min()
    cdf_max = cdf.max()
    cdf_normalized = (cdf - cdf_min) * 255 / (cdf_max - cdf_min)
    cdf_normalized = cdf_normalized.astype(np.uint8)

    # use cdf mapping
    equalized_channel = np.array([cdf_normalized[pixel] for pixel in channel.flatten()])
    return equalized_channel.reshape(channel.shape)


def main():
    imageFile = input("Enter the image file name: ")
    orgImage = cv2.imread(imageFile)

    if orgImage is None:
        print("Error: unable to open the image.")
        return

    newImage = histogramEqualizationColor(orgImage)

    # display the original and resultng images
    cv2.imshow("Original Image", orgImage)
    cv2.imshow("Equalized Image", newImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

     # save the result as a new image
    output_file = "equalized_" + imageFile
    cv2.imwrite(output_file, newImage)

if __name__ == "__main__":
    main()

