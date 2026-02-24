import pytest
from app.calculations import add


@pytest.mark.parametrize("num1,num2,expected",[
    (3,2,5),
    (12,3,15),
    (2,5,7)
    ])
def test_add(num1,num2,expected):
    print("testing add functions")
    assert add(num1,num2) == expected


