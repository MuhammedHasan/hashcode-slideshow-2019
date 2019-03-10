from tqdm import tqdm
from image import Image
from graph import kruskal_path, bucket_to_graph
from buckets import index_bucket, index_balanced_bucket, \
    index_sub_buckets, LocalSensitiveHashing


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

    def _merge_vertical(self, images, sample_size=None):

        print('\t- Merging photos...')

        def _sort_key(x):
            return sorted(x.tags)

        Himages = sorted(filter(lambda x: x.shape == 'H', images),
                         key=_sort_key)
        Vimages = sorted(list(filter(lambda x: x.shape == 'V', images)),
                         key=_sort_key)

        V1images = Vimages[:len(Vimages)//2]
        V2images = list(reversed(Vimages[len(Vimages)//2:]))

        for i in Himages:
            yield i

        if not sample_size:
            sample_size = len(V1images)

        V2images = V2images + V2images

        visited = set()

        for idx, i in tqdm(enumerate(V1images)):

            other = max(
                V2images[idx: idx+sample_size],
                key=lambda x: (len(i.tags.difference(x.tags)),
                               abs(len(i.tags) - len(x.tags)))
                if x not in visited else (-1, -1)
            )

            if other not in visited:
                yield i.merge(other)

            visited.add(other)

    def _solve_naive(self, images):
        for i, image_i in tqdm(enumerate(images)):
            for j in range(i + 1, len(images)):
                image_j = images[j]
                yield (image_i, image_j, image_i.sim(image_j))

    def _solve_buckets(self, images):
        buckets = index_bucket(images)

        print('\t- Calculating pair of images...')

        for i, image_i in tqdm(enumerate(images)):
            for buc in map(lambda x: buckets[x], images[i].tags):
                for image_j in buc:
                    if image_j != image_i:
                        yield (image_i, image_j, image_i.sim(image_j))

    def _solve_balanced_buckets(self, images):
        buckets = index_balanced_bucket(images)

        print('\t- Calculating pair of images...')

        for i, buc in enumerate(buckets.values()):

            print(i, len(buc))

            for image_i in buc:
                for image_j in buc:
                    yield (image_i, image_j, image_i.sim(image_j))

    def _solve_graph(self, images):
        buckets = list(index_sub_buckets(images))
        graph = bucket_to_graph(buckets)

    def _solve_sample(self, images, sample_size=1000):

        cycled_images = images + images[:sample_size + 1]

        print('\t- Calculating pair of images...')

        for i, image_i in tqdm(enumerate(images)):

            if i % 1000 == 0:
                print(i)

            for image_j in cycled_images[i + 1: i + sample_size]:
                sim = image_i.sim(image_j)
                if sim:
                    yield (image_i, image_j, sim)

    def _solve_lsh(self, images, threshold=0.25):

        lsh = LocalSensitiveHashing()
        lsh.index(images, threshold=threshold)

        print('\t- Calculating pair of images...')

        for image_i in tqdm(images):
            for image_j in lsh.query(image_i):
                sim = image_i.sim(image_j)
                if sim:
                    yield (image_i, image_j, sim)

    def solve(self, algorithm='naive', sample_size=1000, threshold=0.25):
        images = list(self.parse())

        if algorithm == 'naive':
            images = list(self._merge_vertical(images))
            image_pairs = self._solve_naive(images)
        elif algorithm == 'buckets':
            images = list(self._merge_vertical(images))
            image_pairs = self._solve_buckets(images)
        elif algorithm == 'balanced_buckets':
            images = list(self._merge_vertical(images))
            image_pairs = self._solve_balanced_buckets(images)
        elif algorithm == 'graph':
            images = list(self._merge_vertical(images))
            image_pairs = self._solve_graph(images)
        elif algorithm == 'lsh':
            images = list(self._merge_vertical(images, sample_size=1000))
            image_pairs = self._solve_lsh(images, threshold=threshold)
        elif algorithm == 'sample':
            images = list(self._merge_vertical(images, sample_size=1000))
            image_pairs = self._solve_sample(images, sample_size=sample_size)

        solution = kruskal_path(image_pairs, images)
        self.write(solution)

    def write(self, solution):
        with open('../outputs/%s.out' % self.filename, 'w') as f:
            f.write('%d\n' % len(solution))
            for i in solution:
                f.write('%s\n' % i.idx)


if __name__ == "__main__":
    # Dataset('a_example').solve('naive')
    # print('a_example done!')

    # print('b_lovely_landscapes started...')
    # Dataset('b_lovely_landscapes').solve('buckets')
    # print('b_lovely_landscapes done!')

    # Dataset('c_memorable_moments').solve('naive')
    # print('c_memorable_moments done!')

    # print('d_pet_pictures started')
    # Dataset('d_pet_pictures').solve('lsh', threshold=0.35)
    # print('d_pet_pictures ended!')

    print('e_shiny_selfies! started')
    Dataset('e_shiny_selfies').solve('lsh', threshold=0.2)
    print('e_shiny_selfies ended!')

    # print('d_pet_pictures started')
    # Dataset('d_pet_pictures').solve('sample', sample_size=1000)
    # print('d_pet_pictures ended!')

    # print('e_shiny_selfies! started')
    # Dataset('e_shiny_selfies').solve('sample', sample_size=1000)
    # print('e_shiny_selfies ended!')
