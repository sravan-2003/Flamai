# Parametric Curve Parameter Estimation


The objective is to determine the unknown parameters θ, M, and X in the given parametric curve:

x = (t ∗ cos(θ) − eM∣t∣ ⋅ sin(0.3t)sin(θ) + X)

y = (42 + t ∗ sin(θ) + e ⋅ sin(0.3t) cos(θ) M∣t∣ )

The parameter ranges are:

0 deg < θ < 50 deg
−0.05 < M < 0.05 
0 < X < 100 
6 < t < 60 
6 < t < 60

The provided `xy_data.csv` contains 1500 points belonging to the curve.

## Approach

The problem was and is treated as a nonlinear parameter estimation problem.

The three unknown parameters given are:

- (theta): rotation/orientation of the curve
- (M): exponential amplitude parameter
- (X): horizontal translation

Since (t>6), we can have:

|t|=t


The equations can be interpreted as  rotated and translated version of:

u=t


v=e^{Mt}\sin(0.3t)


For a candidate (theta) and (X), the observed points were transformed back using:


u=(x-X)cos(theta)+(y-42)sin(theta)



v=-(x-X)sin(theta)+(y-42)cos(theta)


For the correct parameters:


v=e^{Mu}sin(0.3u)


The optimization objective was therefore defined using the mean L1 error:


L1=frac{1}{N}sum_i
left|v_i-e^{Mu_i}sin(0.3u_i)right|


## Optimization

Differential Evolution was used as the global optimization algorithm.

The parameter bounds were:


0^circ < theta < 50^circ

-0.05 < M < 0.05

0 < X < 100


**The optimization produced:

Theta = 29.99997300146329°
M     = 0.02999997098189272
X     = 54.99999833985623**

The optimization objective value was approximately:

2.56×10^-6

Final Parametric Equation
x(t)=tcos(30)-e^{0.03|t|}sin(0.3t)sin(30^)+55 
y(t)=42+tsin(30)+e^{0.03|t|}sin(0.3t)cos(30) 

where:

6<t<60
