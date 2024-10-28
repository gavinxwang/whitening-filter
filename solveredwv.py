import numpy as np
from waveletlike import waveletlike
from scipy.optimize import minimize
from filterredwv import filterredwv

def solveredwv(x, silent=False, zeropad=False):
    """
    This function finds the best-fit model describing the data 
    as 1/f noise + white noise.

    Parameters:
    - x: Input data vector
    - silent: Suppresses output if True.
    - zeropad: If True, pads the data to the next power of two.

    Returns:
    - redcomp: Best fit 1/f component.
    - whitecomp: Best fit white component.
    - alpha: RMS ratio of the 1/f component to the white component.
    - sol: List of [sigma_r, sigma_w].
    """
    gamma = 1  # Default gamma value
    d = np.copy(x)
    els = len(d)

    # Pad data to the next power of two, if needed
    pow_2 = int(np.ceil(np.log2(els)))
    if (2 ** pow_2 != els) and zeropad:
        diff = 2 ** pow_2 - els
        left = diff // 2
        right = diff - left
        x = np.concatenate((np.zeros(left), d, np.zeros(right)))
    #     np.savetxt('x.txt', x)
    else:
        x = np.array(d, dtype=float)
    
    # Perform optimizing with scipy optimize function
    # We want to minimize -1*waveletlike(x, sigma_r, sigma_w)
    
    initial_guess = [500.0, 1.0]
    initial_guess = [0.1, 1.0]

    def objective(params, x):
        sigma_r, sigma_w = params
        return -waveletlike(x, sigma_r, sigma_w, zeropad = zeropad)

    result = minimize(objective, initial_guess, args=(x,), method='Nelder-Mead', 
                  bounds=[(0.0, 1000), (0.0, 10)])

    if result.success:
        sigma_r, sigma_w = result.x
        print(f"Optimized sigma_r: {sigma_r}")
        print(f"Optimized sigma_w: {sigma_w}")
    else:
        print("Optimization failed:", result.message)
    
    # Compute the red and white components using the optimized parameters
    redcomp = filterredwv(x, sigma_r, sigma_w, zeropad = zeropad)
    whitecomp = x - redcomp
    
    # Calculate RMS values
    rms_white = np.std(whitecomp)
    rms_red = np.std(redcomp)

    alpha = rms_red / rms_white

    # Print results if not silent
    if not silent:
        print(f"Sigma_r = {sigma_r:.6f}")
        print(f"Sigma_w = {sigma_w:.6f}")
        print(f"Gamma = {gamma:.6f}")
        print(f"RMS of white component is {rms_white:.6f}")
        print(f"RMS of red component is {rms_red:.6f}")
        print(f"Ratio of red to white RMS is {alpha:.6f}")

    # Save results (original and filtered component) to a text file
    # with open('results.dat', 'w') as f:
    #     for i in range(len(x)):
    #         f.write(f"{x[i]:.6f} {redcomp[i]:.6f}\n")
    
    # Return results
    sol = [sigma_r, sigma_w]
    return redcomp, whitecomp, alpha, sol

if __name__ == "__main__":
    # Example input data
    x = np.loadtxt('vector.txt')
    
    # Run solveredwv
    redcomp, whitecomp, alpha, sol = solveredwv(x, silent=False, zeropad=True)
