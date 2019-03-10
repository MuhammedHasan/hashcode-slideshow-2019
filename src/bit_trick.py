from bitarray import bitarray


class BitEncoder:

    def fit(self, images):
        all_tags = set()
        for i in images:
            for t in i.tags:
                all_tags.add(t)
        self._tags = list(all_tags)
        return self

    def transform(self, image):
        return bitarray([
            t in image.tags for t in self._tags
        ])


def index_tags_as_bit(images):
    print('\t- Indexing bitwise...')

    bit_encoder = BitEncoder()
    bit_encoder.fit(images)

    for i in images:
        i.bit_tags = bit_encoder.transform(i)
