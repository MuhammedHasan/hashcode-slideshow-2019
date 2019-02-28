import pytest
from main import Image, sim

img1 = Image(idx=3, shape='H', tags={'garden', 'selfie', 'smile'})
img2 = Image(idx=1, shape='V', tags={'cat', 'garden'})


def test_sim():
    assert sim(img1, img2) == 1
