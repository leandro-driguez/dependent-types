from .matrix import Matrix
from dependent_types import Attr, _

m = Matrix([[23,3,5,43],[95,23,34,45],[93,12,23,43],[55,53,43,34]])

N = Attr('amount_rows')
M = Attr('amount_cols')

def test_1():
    assert not issubclass(
        Matrix[ N, _ | (N < 100) & ( N > 50) ], 
        Matrix[ _, M | ( M > 50 ) ]
    )

def test_2():
    assert isinstance(m, 
        Matrix[ N, M | (((N > 4) | ((N < 1) | (N > 2))) | ((N == 4) & (M == 3))) ]
    )
    
def test_3(): 
    assert issubclass(
        Matrix[ N, M | ( ((N < 80)  & (M > 60)) | ((N > 101) & (M <49))) ],
        Matrix[ N, M | ( ((N < 100) & (M > 50)) | ((N > 100) & (M <50))) ]
    )

def test_4(): 
    assert not issubclass(
        Matrix[ N, M | ( ((N < 80)  & (M > 60)) | ((N > 99)  & ( M <49))) ],
        Matrix[ N, M | ( ((N < 100) & (M > 50)) | ((N > 100) & ( M <50))) ]
    )

def test_5(): 
    assert not issubclass(
        Matrix[ N, M | (((N < 80)  & (M > 60)) | (N > 100)) ],
        Matrix[ N, M | (((N < 100) & (M > 50)) | ((N > 100) & (M <50))) ]
    )

def test_6(): 
    assert issubclass(
        Matrix[ N, M | (((N < 100) & (M > 50)) | ((N < 100) & (M < 51))) ],
        Matrix[ N, M | (N < 100) ]
    )
    
def test_7(): 
    assert issubclass( 
        Matrix[ N, M | (N < 100) ],
        Matrix[ N, M | (((N < 100) & (M > 50)) | ((N < 100) & (M < 51))) ]
    )
