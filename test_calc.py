from app import calc


def test_dti():
    assert calc.dti(28000, 85000) == 32.94
    assert calc.dti(1000, 0) == 0.0


def test_utilization():
    assert calc.utilization(240000, 300000) == 80.0
    assert calc.utilization(0, 0) == 0.0
    assert calc.utilization(500, 0) == 100.0


def test_category_bands():
    assert [calc.category(s) for s in (300, 599, 600, 699, 700, 749, 750, 900)] == \
        ["Poor", "Poor", "Fair", "Fair", "Good", "Good", "Excellent", "Excellent"]


def test_delta():
    assert calc.delta(None, 650) == 0
    assert calc.delta(650, 672) == 22
    assert calc.delta(700, 690) == -10
