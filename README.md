# numerics_with_python
numerics with python i guess xD


### like
![cool-figure](https://raw.githubusercontent.com/JohannesTheiss/numerics_with_python/main/screenshots/Figure_1.png)


## Interpolation
#### Input data
| i  | xi | fi  |
| -- | -- | --  |
| 0  | -2 | 8   |
| 1  | -1 | 0   |
| 2  | 1  | 2   |
| 3  | 3  | -12 |


#### Lagrange
```
p(x):
    3     2
-1 x + 1 x + 2 x + 2.22e-16
coef: [-1.  1.  2.  0.]
p(2)    : -0.0
```

#### Neville
```
P 0,1 = (2 - -2)* 0     - (2 - -1)* 8   / (-1 - -2)      = -24.0
P 1,2 = (2 - -1)* 2     - (2 - 1)* 0    / (1 - -1)       = 3.0
P 2,3 = (2 - 1)* -12    - (2 - 3)* 2    / (3 - 1)        = -5.0
P 0,2 = (2 - -2)* 3     - (2 - 1)* -24  / (1 - -2)       = 12.0
P 1,3 = (2 - -1)* -5    - (2 - 3)* 3    / (3 - -1)       = -3.0
P 0,3 = (2 - -2)* -3    - (2 - 3)* 12   / (3 - -2)       = 0.0
P 0,3 = p(2) = 0
```

#### Newton
```
P 0,1 =  0 - 8          / (-1 - -2)      = -8.0
P 1,2 =  2 - 0          / (1 - -1)       = 1.0
P 2,3 =  -12 - 2        / (3 - 1)        = -7.0
P 0,2 =  1 - -8         / (1 - -2)       = 3.0
P 1,3 =  -7 - 1         / (3 - -1)       = -2.0
P 0,3 =  -2 - 3         / (3 - -2)       = -1.0
coefs: [8, -8, 3, -1]
p(2) = 0
newton poly:
(x + 2)⋅((4 - x)⋅(x + 1) - 8) + 8
```

#### Cubic spline
```
p(x):
    3     2
-1 x + 1 x + 2 x + 2.22e-16
coef: [-1.  1.  2.  0.]
p(2)    : -0.0
```