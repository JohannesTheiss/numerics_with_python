# Numerics with Python
numerics with python i guess xD

### cool Graph
![cool-figure](https://raw.githubusercontent.com/JohannesTheiss/numerics_with_python/main/screenshots/Figure_2.png)
---
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
Interval: [(-2, -1), (-1, 1), (1, 3)]
Si:
s1 = a1 + b1*(x + 2) + c1*(x + 2)**2 + d1*(x + 2)**3
s2 = a2 + b2*(x + 1) + c2*(x + 1)**2 + d2*(x + 1)**3
s3 = a3 + b3*(x - 1) + c3*(x - 1)**2 + d3*(x - 1)**3

derivative:
s1'= b1 + c1*(2*x + 4) + 3*d1*(x + 2)**2                 s1'' = 2*c1 + 3*d1*(2*x + 4)
s2'= b2 + c2*(2*x + 2) + 3*d2*(x + 1)**2                 s2'' = 2*c2 + 3*d2*(2*x + 2)
s3'= b3 + c3*(2*x - 2) + 3*d3*(x - 1)**2                 s3'' = 2*c3 + 3*d3*(2*x - 2)

conditions:
b₁ + 2⋅c₁ + 3⋅d₁ = b₂
2⋅c₁ + 6⋅d₁ = 2⋅c₂
b₂ + 4⋅c₂ + 12⋅d₂ = b₃
2⋅c₂ + 12⋅d₂ = 2⋅c₃
a₁ = 8
a₁ + b₁ + c₁ + d₁ = 0
a₂ = 0
a₂ + 2⋅b₂ + 4⋅c₂ + 8⋅d₂ = 2
a₃ = 2
a₃ + 2⋅b₃ + 4⋅c₃ + 8⋅d₃ = -12

natural spline
2⋅c₁ = 0
2⋅c₃ + 12⋅d₃ = 0

RESULTS:
LGS:
b₁ + 2⋅c₁ + 3⋅d₁ = b₂
2⋅c₁ + 6⋅d₁ = 2⋅c₂
b₂ + 4⋅c₂ + 12⋅d₂ = b₃
2⋅c₂ + 12⋅d₂ = 2⋅c₃
a₁ = 8
a₁ + b₁ + c₁ + d₁ = 0
a₂ = 0
a₂ + 2⋅b₂ + 4⋅c₂ + 8⋅d₂ = 2
a₃ = 2
a₃ + 2⋅b₃ + 4⋅c₃ + 8⋅d₃ = -12
2⋅c₁ = 0
2⋅c₃ + 12⋅d₃ = 0

solved LGS:
{a₁: 8, a₂: 0, a₃: 2, b₁: -10, b₂: -4, b₃: -1, c₁: 0, c₂: 6, c₃: -9/2, d₁: 2, d₂: -7/4, d₃: 3/4}

S1: interval: (-2, -1)
                 3
-10⋅x + 2⋅(x + 2)  - 12

S2: interval: (-1, 1)
     3      2
  7⋅x    3⋅x    11⋅x   1
- ──── + ──── + ──── + ─
   4      4      4     4

S3: interval: (1, 3)
   3       2
3⋅x    27⋅x    41⋅x   9
──── - ───── + ──── - ─
 4       4      4     4
```
