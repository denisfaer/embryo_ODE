import pytest
from epipeODE import DualCusp, HeteroclinicFlip, Fate

def test_dual_cusp():
    model = DualCusp(K1=0.15)
    fate = Fate(0.5, 0.5)

    potential = model.potential(fate)
    assert potential is not None

    dx, dy = model.gradient(fate)
    assert dx != 0
    assert dy != 0

def test_heteroclinic_flip():
    model = HeteroclinicFlip(K2=1.5, fs=1.0)
    fate = Fate(0.5, 0.5)
    population = [Fate(0.6, 0.6), Fate(0.7, 0.7)]

    feedback = model.calculate_feedback(population)
    assert feedback != 0

    dx, dy = model.gradient(fate, population)
    assert dx != 0
    assert dy != 0