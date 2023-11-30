#the rquired importss
import numpy as np
import cv2

def histogramEqualizationChannel(channel):
    # calculatte histogram of input channel
    hist, _ = np.histogram(channel, bins=256, range=(0, 256))

    # we have get the cummulatve dist of the 
    cdf = hist.cumsum()

    # nomalizze the cdf and convert it to the type to display the image
    cdf_normalized = cdf * hist.max() / cdf.max()
    cdf_normalized = (cdf_normalized - cdf_normalized.min()) * 255 / (cdf_normalized.max() - cdf_normalized.min())
    cdf_normalized = cdf_normalized.astype(np.uint8)

    # apply the maping using the cdf
    return cdf_normalized[channel]

def histogramEqualizationColor(img):
    # Split the image into its R, G, B channels
    R, G, B = cv2.split(img)

    # Apply histogram equalization to each channel
    R_eq = histogramEqualizationChannel(R)
    G_eq = histogramEqualizationChannel(G)
    B_eq = histogramEqualizationChannel(B)

    # Merge the equalized channels back together
    return cv2.merge((R_eq, G_eq, B_eq))

def main():
    # get image file name from terminal from user
    imageFile = input("Enter the image file name: ")

    # Load the image in color
    orgImage = cv2.imread(imageFile)

    if orgImage is None:
        print("eror: unable to open the image.")
        return

    # rrun histogram equalisation in the function
    newImage = histogramEqualizationColor(orgImage)

    # display the original and resultng images
    cv2.imshow("original image", orgImage)
    cv2.imshow("equalised image", newImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # save the result as a new image
    output_file = "equalized_" + imageFile
    cv2.imwrite(output_file, newImage)

if __name__ == "__main__":
    main()
