from dtypes import DependentType
from matrix import Matrix
from dtypes import Attr, _

N = Attr()
M = Attr()

m = Matrix(
    [[43,23,54,22],
     [13,65,54,34],
     [84,23,54,23],
     [29,49,23,53]]
)

assert isinstance(m, Matrix[ _, M | ( M < 50 ) ])
