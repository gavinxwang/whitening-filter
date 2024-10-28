import numpy as np
import dwt

def waveletlike(x, sigma_r, sigma_w, zeropad=False):
    """Calculates the log likelihood for a vector described by sigma_r and sigma_w."""
    gamma = 1
    
    d = np.copy(x)
    els = len(d)
    pow_2 = int(np.ceil(np.log2(els)))

    if 2**pow_2 != els and zeropad:
        diff = 2**pow_2 - els
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
    
    total_sum = 0.0
    
    gamma = 1
    g_gamma = 1 / (2 * np.log(2))  # g(gamma) = 1 / (2 * ln(2))

    index = 0

    # Level 1: Process the first 2 coefficients
    n0 = 2  # Initial size of the first level (2 coefficients)
    sigma_S2 = sigma_r**2 * 2**(-gamma) * g_gamma + sigma_w**2  # Eq. (34)

    # Add log-likelihood terms for level 1 coefficients
    level_1_coefficients = wv[index : index + n0]  # Extract coefficients for level 1
    total_sum += np.sum(
        -0.5 * np.log(2 * np.pi * sigma_S2) - (level_1_coefficients ** 2) / (2 * sigma_S2)
    )
    index += n0  # Update the index

    # Loop over levels m = 2 to J
    for m in range(2, J + 1):
        num_coefficients = 1 * 2**(m - 1)  # Number of coefficients at level m
        sigma_W2 = sigma_r**2 * 2**(-gamma * m) + sigma_w**2  # Eq. (33)

        # Extract the coefficients for the current level
        level_m_coefficients = wv[index : index + num_coefficients]

        # Add log-likelihood terms for level m coefficients
        total_sum += np.sum(
            -0.5 * np.log(2 * np.pi * sigma_W2) - (level_m_coefficients ** 2) / (2 * sigma_W2)
        )
        index += num_coefficients  # Update the index
    # print("Last index:", index)
    return total_sum

'''
# Example usage:

x = [1.,2.,3.,4.,5.,6.,7.,8.]
sigma_r = 1.0
sigma_w = 0.5
result = waveletlike(x, sigma_r, sigma_w, zeropad=True)
print("Log Likelihood:", result)
'''
