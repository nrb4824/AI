from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt

def ConvertToBinaryG(value):
    lb = -0.524
    R = .524 * 2
    d = ((value - lb) * (2 ** 7 - 1)) / R
    d = int(d)
    binary = '{0:07b}'.format(d)
    return binary_to_gray(int(binary))
def binary_to_gray(n):
    """Convert Binary to Gray codeword and return it."""
    n = int(n, 2)  # convert to int
    n ^= (n >> 1)

    # bin(n) returns n's binary representation with a '0b' prefixed
    # the slice operation is to remove the prefix
    return bin(n)[2:]



y = [ 0.52181625, -0.02906091,  0.12968241, -0.10380712, -0.00554951,  0.03398099,
0.27489796,  0.49573379, -0.20131499, -0.01634993]
for i in range(10):
    b = binary_to_gray(y[i])
    print('Gray codeword:', b)




# x = np.arange(10)
# y = [ 0.52181625, -0.02906091,  0.12968241, -0.10380712, -0.00554951,  0.03398099,
#   0.27489796,  0.49573379, -0.20131499, -0.01634993]
# y2 = [4.5, 3.3333, -2.1, -.05, -.4, 3.2, .7, .2, 3.5, -.9]
# # use bc_type = 'natural' adds the constraints as we described above
# f = CubicSpline(x, y, bc_type='natural')
# f2 = CubicSpline(x, y2, bc_type='natural')
# x2, step2 = np.linspace(0,10,100, retstep=True)
# x_new, step= np.linspace(0, 10, 100, retstep=True)
# y_new = f(x_new)
#
# print(step)
# print(step2)
# i = 0
# total = 199
# for i in range(100):
#     if y_new[i] > .524:
#         y_new[i] = .524
#     elif y_new[i] < -.524:
#         y_new[i] = -.524
# # while i <= total:
# #     if y_new[i] > .524 or y_new[i] < -.524:
# #         #print(i)
# #         print(y_new[i])
# #         y_new = np.delete(y_new, i)
# #         print(y_new[i])
# #         total -= 1
# #         i -= 1
# #     i += 1
# plt.figure(figsize = (10,8))
# plt.plot(x_new, y_new, 'b')
# plt.plot(x, y, 'ro')
# plt.title('Cubic Spline Interpolation')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()