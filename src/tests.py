from main import Image

images = [
    Image(idx='0', shape='H', tags={'sun', 'beach', 'cat'}),
    Image(idx='1', shape='V', tags={'smile', 'selfie'}),
    Image(idx='2', shape='V', tags={'selfie', 'garden'}),
    Image(idx='3', shape='H', tags={'cat', 'garden'})
]


def test_sim():
    assert images[0].sim(images[3]) == 1
    assert images[3].sim(images[0]) == 1
