from bitarray import bitarray
from collections import defaultdict
from itertools import cycle


class QuickUnion:
    def __init__(self, size):
        self.connections = list(range(size))
        self.size_of_root = [1] * size

    def is_connected(self, i, j):
        return self.root(i - 1) == self.root(j - 1)

    def connect(self, i, j):
        root_i = self.root(i - 1)
        root_j = self.root(j - 1)
        if self.size_of_root[root_i] > self.size_of_root[root_j]:
            self.connections[root_i] = root_j
            self.size_of_root[root_j] += root_i
        else:
            self.connections[root_j] = root_i
            self.size_of_root[root_i] += root_j

    def root(self, i):
        i = i - 1
        while self.connections[i] != i:
            self.connections[i] = self.connections[self.connections[i]]
            i = self.connections[i]
        return i


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


class Dataset:

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open('../inputs/%s.txt' % self.filename) as f:
            num_photo = int(f.readline())
            for i in range(num_photo):
                line = f.readline().strip().split(' ')
                shape = line[0]
                tags = set(line[2:])
                yield Image(idx=str(i), shape=shape, tags=tags)

    def _merge_vertical(self, images):
        Himages = list(filter(lambda x: x.shape == 'H', images))
        Vimages = sorted(
            list(filter(lambda x: x.shape == 'V', images)),
            key=lambda x: tuple(x.tags))

        V1images = Vimages[:len(Vimages)//2]
        V2images = Vimages[len(Vimages)//2:]

        for i in Himages:
            yield i

        for i, j in zip(V1images, V2images):
            yield i.merge(j)

    def _minimum_spanning_path(self, image_pairs, nodes):
        '''
        Kruskal like algorithm for creating path

        Args:
          image_pairs: list of (image1, image2, score)
        '''

        edges = defaultdict(list)
        stop = len(nodes) - 1

        # prevents self loops
        qu = QuickUnion(len(nodes))
        qu_idx = {v: i for i, v in enumerate(nodes)}

        sorted_image_pairs = sorted(image_pairs,
                                    key=lambda x: x[2], reverse=True)

        print('\t- Calculating minimum spanning path...')

        for i, j, score in sorted_image_pairs:
            # number of node constrained with two
            if len(edges[i]) < 2 and len(edges[j]) < 2 \
               and (not qu.is_connected(qu_idx[i], qu_idx[j])):
                edges[i].append(j)
                edges[j].append(i)
                qu.connect(qu_idx[i], qu_idx[j])

                # Early stop we have N-1 edge after all
                stop -= 1
                if stop == 0:
                    break

        return list(self._reconstruct_path(edges))

    def _reconstruct_path(self, edges):
        visited = set()
        start_nodes = (k for k, v in edges.items() if len(v) == 1)

        for start in start_nodes:
            if start not in visited:
                yield from (self._reconstruct_path_step(edges, start, visited))

    def _reconstruct_path_step(self, edges, start, visited):
        curr = start
        while True:
            yield curr
            visited.add(curr)

            if len(edges[curr]) == 0:
                break

            for nn in edges[curr]:
                edges[nn].remove(curr)
            curr = nn

    def _solve_naive(self, images):
        for i in range(len(images)):
            image_i = images[i]

            if i % 100 == 0:
                print(i)

            for j in range(i + 1, len(images)):
                image_j = images[j]

                yield (image_i, image_j, image_i.sim(image_j))

    def _index_bucket(self, images):
        buckets = defaultdict(set)

        print('\t- Indexing buckets...')

        for i in images:
            for t in i.tags:
                buckets[t].add(i)

        return buckets

    def _index_balanced_bucket(self, images):
        buckets = defaultdict(set)

        print('\t- Indexing balanced buckets...')

        for i in images:
            bucket = min((buckets[t] for t in i.tags), key=lambda x: len(x))
            bucket.add(i)

        return buckets

    def _solve_buckets(self, images):
        buckets = self._index_bucket(images)

        print('\t- Calculating pair of images...')

        for i in range(len(images)):
            image_i = images[i]

            for buc in map(lambda x: buckets[x], images[i].tags):
                for image_j in buc:
                    if image_j != image_i:
                        yield (image_i, image_j, image_i.sim(image_j))

    def _index_tags_as_bit(self, images):
        print('\t- Indexing bitwise...')

        bit_encoder = BitEncoder()
        bit_encoder.fit(images)

        for i in images:
            i.bit_tags = bit_encoder.transform(i)

    def _solve_balanced_buckets(self, images):
        buckets = self._index_balanced_bucket(images)

        print('\t- Calculating pair of images...')

        for i, buc in enumerate(buckets.values()):

            print(i, len(buc))

            for image_i in buc:
                for image_j in buc:
                    yield (image_i, image_j, image_i.sim(image_j))

    def _solve_sample(self, images, sample_size=1000):

        cycled_images = cycle(images)

        for i, image_i in enumerate(images):

            if i % 1000 == 0:
                print(i)

            for _ in range(sample_size):
                image_j = next(cycled_images)
                sim = image_i.sim(image_j)
                if sim:
                    yield (image_i, image_j, sim)

    def solve(self, algorithm='naive', sample_size=1000):
        images = list(self.parse())
        images = list(self._merge_vertical(images))

        if algorithm == 'naive':
            image_pairs = self._solve_naive(images)
        elif algorithm == 'buckets':
            image_pairs = self._solve_buckets(images)
        elif algorithm == 'sample':
            image_pairs = self._solve_sample(images, sample_size=sample_size)

        solution = self._minimum_spanning_path(image_pairs, images)
        self.write(solution)

    def write(self, solution):
        with open('../outputs/%s.out' % self.filename, 'w') as f:
            f.write('%d\n' % len(solution))
            for i in solution:
                f.write('%s\n' % i.idx)


if __name__ == "__main__":
    # files = [
    #     'a_example',
        # 'b_lovely_landscapes',
        # 'c_memorable_moments',
        # 'd_pet_pictures',
        # 'e_shiny_selfies'
    # ]

    # Dataset('a_example').solve('naive')
    # print('a_example done!')

    # print('b_lovely_landscapes started...')
    # Dataset('b_lovely_landscapes').solve('buckets')
    # print('b_lovely_landscapes done!')

    # Dataset('c_memorable_moments').solve('naive')
    # print('c_memorable_moments done!')

    print('d_pet_pictures started')
    Dataset('d_pet_pictures').solve('sample', sample_size=4000)
    print('d_pet_pictures ended!')

    print('e_shiny_selfies! started')
    Dataset('e_shiny_selfies').solve('sample', sample_size=5000)
    print('e_shiny_selfies ended!')
