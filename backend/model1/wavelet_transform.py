import numpy as np
import pywt
import cv2

class Wavelet_Transform():
    def __init__(self, pan_image, rgb_image, wavelet='db1'):
        self.pan_image = pan_image
        self.rgb_image = rgb_image
        self.size1 = pan_image.size
        self.size = rgb_image.size
        self.shape1 = pan_image.shape
        self.shape = rgb_image.shape
        self.wavelet = wavelet

    def rgb_to_hsi(self):
 
        b, g, r = cv2.split(self.rgb_image)
        b, g, r = b/255, g/255, r/255
        numerator = r + g + b

        with np.errstate(divide='ignore', invalid='ignore'):
            h = np.arccos((0.5 * ((r - g) + (r - b))) / (np.sqrt((r - g) ** 2 + (r - b) * (g - b))+0.000001))
            h = np.degrees(h)
            h = np.where(b <= g, h, 360 - h)
            s = np.where(numerator == 0, 0, 1 - 3 * np.minimum(r, g, b) / numerator)
            i = numerator / 3

        return h, s, i, r, g, b

    def hist_return(self, image):
        hist, bins = np.histogram(image, bins=256, range=(0, 256))
        return hist, bins

    def ip_spec_hist_img(self):
        hist, bins = self.hist_return(self.pan_image)

    def spec_hist_img(self):
        hue,sat,ins, r, g, b = self.rgb_to_hsi()
        ins = ins*255
        hist, bins = self.hist_return(ins)

    def op_spec_hist(self):
        hue,sat,ins, r, g, b = self.rgb_to_hsi()
        
        ip_pixel = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                ip_pixel.append(255*ins[i, j])  
        img_array = np.array(ip_pixel)
        img_array = img_array.astype(int)
    
        ip_pixel1 = []  
        for i in range(self.shape1[0]):  
            for j in range(self.shape1[1]):  
                ip_pixel1.append(self.pan_image[i, j])  
        img_array1 = np.array(ip_pixel1)  
        img_array1 = img_array1.astype(int)  

        #Histogram Equalization for intensity image
        hist, bins = self.hist_return(255*ins)  
        norm_hist = []
        histogram = list(hist)
        for i in range(len(histogram)):
            j = histogram[i] / self.size1
            norm_hist.append(j)

        trans = []
        for i in range(len(norm_hist)):
            s = []
            for j in range(i + 1):
                s.append(norm_hist[j])
            s1 = int(255 * sum(s))
            trans.append(s1)
        trans_array = np.array(trans)
        
        #Histogram Equalization for pan image
        hist1, bins1 = self.hist_return(self.pan_image)  
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

        #trans1_array for pan
        #tran_array for ins
        #Histogram matching
        op = list(0 for i in range(256))
        for i in range(len(trans_array1)):
            for j in range(len(trans_array)):
                if trans_array1[i]>trans_array[j]:
                    continue
                else:
                    break
            if j >= 0:
                op[i] = trans_array[j]
        
        
        new_img_array1 = np.zeros(len(img_array1))
        for i in range(len(img_array1)):
            new_img_array1[i] = op[img_array1[i]]

        new_img1 = new_img_array1.reshape(self.shape1[0], self.shape1[1])
        return new_img1
        
    def wavelets(self):
        new_image1 = self.op_spec_hist()
        hue,sat,ins, r, g, b = self.rgb_to_hsi()
        
        coeffs = pywt.dwt2(255*ins, self.wavelet)
        iA, (iH, iV, iD) = coeffs
        coeffs_level2 = pywt.dwt2(iA, self.wavelet)
        iA2, (iH2, iV2, iD2) = coeffs_level2

        coeffs1 = pywt.dwt2(new_image1, self.wavelet)
        pA, (pH, pV, pD) = coeffs1
        coeffs1_level2 = pywt.dwt2(pA, self.wavelet)
        pA2, (pH2, pV2, pD2) = coeffs1_level2

        reconstructed_image1 = pywt.idwt2((iA2, (pH2, pV2, pD2)), self.wavelet)
        reconstructed_image1 = cv2.resize(reconstructed_image1, (pH.shape[1], pH.shape[0]))
        reconstructed_image = pywt.idwt2((reconstructed_image1, (pH, pV, pD)), self.wavelet)
        reconstructed_image = reconstructed_image/np.max(reconstructed_image)
        return reconstructed_image
    
    def hsi_to_rgb(self):
        h, s, i, r, g, b = self.rgb_to_hsi()
        reconstructed_image = self.wavelets()
        i = reconstructed_image
        r = np.zeros_like(h)
        g = np.zeros_like(h)
        b = np.zeros_like(h)

        for k in range(r.shape[0]):
            for l in range(r.shape[1]):
                if (h[k,l]>=0 and h[k,l]<120):
                    b[k,l] = i[k,l] * (1 - s[k,l])
                    r[k,l] = i[k,l] * (1 + (s[k,l] * np.cos(np.pi*h[k,l]/180)) / np.cos(np.pi*(60 - h[k,l])/180))
                    g[k,l] = 3 * i[k,l]- (r[k,l] + b[k,l])
                elif (h[k,l]>=120 and h[k,l]<240):
                    h[k,l]=h[k,l]-120
                    r[k,l] = i[k,l] * (1 - s[k,l])
                    g[k,l] = i[k,l] * (1 + (s[k,l] * np.cos(np.pi*h[k,l]/180)) / (np.cos(np.pi*(60 - h[k,l])/180)))
                    b[k,l] = 3 * i[k,l]- (r[k,l] + g[k,l])
                else:
                    h[k,l]=h[k,l]-240
                    g[k,l] = i[k,l] * (1 - s[k,l])
                    b[k,l] = i[k,l] * (1 + (s[k,l] * np.cos(np.pi*h[k,l]/180)) / (np.cos(np.pi*(60 - h[k,l])/180)))
                    r[k,l] = 3 * i[k,l] - (g[k,l] + b[k,l])     

        pan_sharpen_output = np.stack((r, g, b), axis=-1)
        
        
        return pan_sharpen_output