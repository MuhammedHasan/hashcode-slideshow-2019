import pytest
from main import Image
from bit_trick import BitEncoder

images = [
    Image(idx='0', shape='H', tags={'sun', 'beach', 'cat'}),
    Image(idx='1', shape='V', tags={'smile', 'selfie'}),
    Image(idx='2', shape='V', tags={'selfie', 'garden'}),
    Image(idx='3', shape='H', tags={'cat', 'garden'})
]


def test_sim():
    assert images[0].sim(images[3]) == 1
    assert images[3].sim(images[0]) == 1


@pytest.fixture
def bit_encoder():
    return BitEncoder()


def test_bit_encoder_fit(bit_encoder):
    bit_encoder.fit(images)
    expected = sorted(['garden', 'selfie', 'cat', 'sun', 'beach', 'smile'])
    assert sorted(bit_encoder._tags) == expected


def test_bit_encoder_transform(bit_encoder):
    bit_encoder.fit(images)
    bit_encoder.transform(images[0]).count() == 3
    bit_encoder.transform(images[3]).count() == 2


def test_sim_bitwise(bit_encoder):
    bit_encoder.fit(images)

    images[0].bit_tags = bit_encoder.transform(images[0])
    images[3].bit_tags = bit_encoder.transform(images[3])

    assert images[0].sim_bitwise(images[3]) == 1
    assert images[3].sim_bitwise(images[0]) == 1
