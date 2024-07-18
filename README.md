# Digital Signal Processing (DSP) Tasks


<br>


## Introduction
- Signal processing is the task of detecting, manipulating, and extracting information from signals (physical objects vary in time), and involves manipulating real-world signals like voice, audio, images, videos, temperature, pressure, or position that have been digitized
- Signals are processed to display, analyze, or convert them into another type of signal for enabling the usage of programming instead of analog electronic circuits

<br>

## Task 1

- The ability to read samples of a signal from a txt file and display it in both continuous and discrete representations.
- The ability to generate sinusoidal or cosinusoidal signals, the user should choose whether he wants cosine or sine, the amplitude A, the phase shift theta, the analog frequency, and the sampling frequency needed. (Hint: the sampling frequency chosen should obey the sampling theorem). Your framework should include a menu named Signal Generation with two items sine wave and cosine wave

![DSP Task 1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/654b6b11-e6c4-4ad5-ad90-95baf8c568f0)




<br>




## Task 2

- Addition: add input signals (any number) and display the resulting signal.
- Subtraction: subtract input signals and display the resulting signal.
- Multiplication: multiply a signal by a constant value to amplify or reduce the signal amplitude. (If the constant equals -1, then the signal will be inverted).
- Squaring: squaring a signal and displaying the resulting signal.
- Shifting: add to the signal a (+ve) or (-ve) constant.
- Normalization: normalize the signal from -1 to 1 or 0 to 1 depending on user choice.
- Accumulation of input signal.

![DSP Task 2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/da38e4cb-a887-4b10-b7a2-35377999d0d4)




<br>




## Task 3

- The ability to quantize an input signal (its samples), the application should ask the user for the needed levels or a number of bits available (in case of a number of bits the application should compute the appropriate number of levels). Thereafter, the application should display the quantized signal and quantization error besides the encoded signal.

![DSP Task 3](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/63adeace-17b5-4c2a-8fe1-4558a829edf0)





<br>




## Task 4

- The ability to apply Fourier transform to any input signal and then display frequency versus amplitude and frequency versus phase relations after asking the user to enter the sampling frequency in HZ.
- Allow modification of the amplitude and phase of the signal components.
- Allow signal reconstruction using IDFT.
- The frequency components should be saved in txt file in polar form (amplitude and phase).
- The ability to read a txt file that contains frequency components in polar form and reconstruct the signal by IDFT.

![DSP Task 4](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/67337518-53d0-42d9-86e3-1ab0d5f3b86b)





<br>





## Task 5

- Computing DCT for a given input, display the result and the user can choose the first m coefficients to be saved in a txt file:

$$
y(k) = \sqrt{\frac{2}{N}} \sum_{n=1}^{N} x(n) \cos \left( \frac{\pi}{4N} (2n - 1)(2k - 1) \right)
$$

<!-- ![image](https://github.com/user-attachments/assets/70d2a7dd-1c3d-4505-8d2e-ac25f9d51bde)  -->
- Remove the DC component. 

![DSP Task 5](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/a33703f3-3ae2-4a0c-9a4e-77d6dd4a8292)





<br>





## Task 6

- Smoothing: Compute moving average y(n) for signal x(n) and let the user enter the number of points included in averaging.
- Sharpening: Compute and display y (n) which represents:
    - First Derivative of the input signal   ->  Y(n) = x(n)-x(n-1)
    - Second derivative of the input signal  ->  Y(n)= x(n+1)-2x(n)+x(n-1)
- Delaying or advancing a signal by k steps.
- Folding a signal.
- Delaying or advancing a folded signal.
- Remove the DC component in the frequency domain.

![DSP Task 6](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/542a1030-5412-43ca-9bbf-d36d0db5be75)





<br>




## Task 7
- The convolution of two discrete-time signals 𝑥[n] and ℎ[𝑛] is defined as:

$$
\ y[n] = (x * h)[n] = \sum_{k=-\infty}^{\infty} x[k] * h[n - k] \
$$

![DSP Task 7](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/61be4307-f146-43ce-9b5d-f9ea1723f801)





<br>





## Task 8

- Correlation: compute normalized cross-correlation of two signals.

![DSP Task 8](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/1b8bf191-228d-4b41-84f3-8dfc115f5a08)






<br>






## Task 9

- Fast convolution. 
- Fast correlation.

![DSP Task 9](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/b957a036-2a5e-4979-b532-b0612561cc54)






<br><br><br>















<!--
![task1_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/d5addbbe-9a9b-499f-a78f-13529728702e)
![task1_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/6a2602e2-880c-4ba0-b2f7-d6d055301255)
![task2_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/189714f4-2e58-48d7-bdf8-91afc3b837f6)
![task2_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/d50ce583-856f-4162-bc18-5624deff36cc)
![task3_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/4f4810c9-eed4-4895-9912-bd20ef8cf4b5)
![task3_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/c3bd2912-ac8d-4789-ae4d-585b4153baf7)
![task3_3](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/f9cc678c-5921-4418-8477-dfa58397e587)
![task4_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/a31f441b-21e3-4f0c-81be-1552d8435e62)
![task4_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/4ccbba51-8f3d-4348-84a3-9442af181f81)
![task5_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/53c29a2e-5afc-4c11-a640-d40ad0cd6d08)
![task5_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/312ad239-eb04-4a5b-bd24-b99157c3c8bc)
![task6_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/be78b960-ec53-4ee4-beae-ba83d524fb29)
![task6_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/5076d227-63d3-4cea-ba49-cffa0d5e5c0e)
![task7_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/7a1a505e-c534-470b-ac6d-1c16ec8a8d63)
![task7_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/ef834379-6c42-4a5e-ac6b-7d0b139c6c7f)
![task8_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/98ebbfca-843b-4c50-83bd-26c3c5bcff8a)
![task8_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/d08ecf5d-6b74-488c-98de-c8c69fedd00c)
![task9_1](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/1079755c-c79a-42b6-bb23-175ac3e8c294)
![task9_2](https://github.com/Hossam-H22/DSP_Tasks/assets/88390970/64bfa55c-32b8-4b00-9bb7-382921ef9be5)
-->









