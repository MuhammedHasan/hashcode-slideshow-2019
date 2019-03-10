class Image:

    def __init__(self, idx, shape, tags):
        self.idx = idx
        self.shape = shape
        self.tags = set(tags)

    def sim(self, other):
        intersect = len(self.tags.intersection(other.tags))
        return min(
            len(self.tags) - intersect,
            len(other.tags) - intersect,
            intersect
        )

    def sim_bitwise(self, other):
        if not (self.bit_tags and other.bit_tags):
            raise ValueError('Image need to bitwise indexed!')
        intersect = (self.bit_tags & other.bit_tags).count()
        return min(
            len(self.tags) - intersect,
            len(other.tags) - intersect,
            intersect
        )

    def merge(self, other):
        if self.shape != 'V' or other.shape != 'V':
            raise ValueError('Only V shape are mergable!')
        return Image(idx='%s %s' % (self.idx, other.idx),
                     shape='H',
                     tags=self.tags.union(other.tags))

    def __hash__(self):
        return hash(self.idx)

    def __eq__(self, other):
        return self.idx == other.idx

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Image(idx='%s', shape='%s', tags=%s)" % (
            self.idx, self.shape, str(self.tags))
