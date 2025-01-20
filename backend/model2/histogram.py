import numpy as np

class Hist_sp_contrast:
    def __init__(self, img, spec_img):
        self.img = img
        self.spec_img = spec_img
        self.size1 = img.size
        self.size = spec_img.size
        self.shape1 = img.shape
        self.shape = spec_img.shape

    def hist_return(self, image):
        hist, bins = np.histogram(image, bins=256, range=(0, 256))
        return hist, bins
    
    def ip_spec_hist_img(self):
        hist, bins = self.hist_return(self.img)
    
    def spec_hist_img(self):
        hist, bins = self.hist_return(self.spec_img)
    
    def op_spec_hist(self):
        #code for making array of input image
        ip_pixel1 = []  #
        for i in range(self.shape1[0]):  #
            for j in range(self.shape1[1]):  #
                ip_pixel1.append(self.img[i, j])  #
        img_array1 = np.array(ip_pixel1)  #
        img_array1.astype(int)  #

        #code for making array of spcified image
        ip_pixel = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                ip_pixel.append(self.spec_img[i, j])  #
        img_array = np.array(ip_pixel)
        img_array.astype(int)

        #code for hist of spcified image
        hist, bins = self.hist_return(self.spec_img)  #
        norm_hist = []
        histogram = list(hist)
        for i in range(len(histogram)):
            j = histogram[i] / self.size
            norm_hist.append(j)

        trans = []
        for i in range(len(norm_hist)):
            s = []
            for j in range(i + 1):
                s.append(norm_hist[j])
            s1 = int(255 * sum(s))
            trans.append(s1)
        trans_array = np.array(trans)#

        #code for hist of input image
        hist1, bins1 = self.hist_return(self.img)  #
        norm_hist1 = []
        histogram1 = list(hist1)
        for i in range(len(histogram1)):
            j = histogram1[i] / self.size1
            norm_hist1.append(j)

        trans1 = []
        for i in range(len(norm_hist1)):
            s = []
            for j in range(i + 1):
                s.append(norm_hist1[j])
            s1 = int(255 * sum(s))
            trans1.append(s1)
        trans_array1 = np.array(trans1)

        #mapping of pixel values according to specified image to adjust pixel values of input image
        op = list(0 for i in range(256))
        for i in range(len(trans_array1)):
            for j in range(len(trans_array)):
                if trans_array1[i]>trans_array[j]:
                    continue
                else:
                    break
            if j > 0:
                op[i] = trans_array[j-1]
    
        new_img_array1 = np.zeros(len(img_array1))
        for i in range(len(img_array1)):
            new_img_array1[i] = op[img_array1[i]]

        #reshapping to input image shape 
        new_img1 = new_img_array1.reshape(self.shape1[0], self.shape1[1])

        return new_img1
    

