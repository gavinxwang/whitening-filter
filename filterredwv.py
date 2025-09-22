import numpy as np
import dwt

def filterredwv(x, sigma_r, sigma_w, zeropad=False):
    """Extracts the 1/f component from a data vector x."""
    gamma = 1
    d = np.copy(x)
    els = len(d)
    pow_2 = int(np.ceil(np.log2(els)))
    
    # Pad data to the next power of two, if needed
    if 2 ** pow_2 != els and zeropad:
        diff = 2 ** pow_2 - els
        left = diff // 2
        right = diff - left
        x = np.concatenate([np.zeros(left), d, np.zeros(right)])
    else:
        x = d

    J = np.log2(len(x))
    if not J.is_integer():
        raise ValueError("Data length must be a power of two")
    J = int(J)

    # Perform wavelet decomposition
    wv = dwt.call_wt1(x, 1)
    
    # Save wavelet coefficients to CSV
    # with open('wv_data.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     for coeff in wv:
    #         writer.writerow([coeff])
    
    # Calculate scaling factors
    sm2 = sigma_r ** 2 / (2.0 * np.log(2.0)) + sigma_w ** 2

    # Adjust the wavelet coefficients
    wv[0] *= 1 - (sigma_w ** 2) / sm2

    k = 1
    for i in range(1, J + 1):
        sm2 = sigma_r ** 2 * 2 ** (-gamma * i) + sigma_w ** 2
        for _ in range(2 ** (i - 1)):
            wv[k] *= 1 - (sigma_w ** 2) / sm2
            k += 1
    
    # Write the new coeffs to a file
    # np.savetxt('wv_coeffs.dat', wv)
    
    # Reconstruct the red component (inverse wavelet transform)
    redcomp = dwt.call_wt1(wv, -1)
    
    if zeropad and (left > 0 or right > 0):
        redcomp = redcomp[left : left + els]
    
    return redcomp

'''
# Example usage

x = np.random.normal(0, 5, 16)
sigma_r = 0.5 # arbitrary values
sigma_w = 2.0

print("Original signal:", x)
result = filterredwv(x, sigma_r, sigma_w, zeropad=True)
print("Filtered 1/f component:", result)
'''
