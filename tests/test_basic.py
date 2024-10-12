import embryo

def test_compare():
    a = embryo.Cell(True, 3)
    b = embryo.Cell(True, 3)

    assert a.status == b.status
    assert a.age == b.age
    assert a == b
