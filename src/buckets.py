from tqdm import tqdm
from collections import defaultdict
from datasketch import MinHash, MinHashLSH


def index_bucket(images):
    buckets = defaultdict(set)

    # print('\t- Indexing buckets...')

    for i in images:
        for t in i.tags:
            buckets[t].add(i)

    return buckets


class LocalSensitiveHashing:

    def index(self, images, threshold=0.25):
        self.lsh = MinHashLSH(threshold=threshold, num_perm=128)
        self.indexes = dict()

        print('\t- Indexing minhash...')

        for i in tqdm(images):
            mh = MinHash(num_perm=128)

            for t in i.tags:
                mh.update(t.encode('utf8'))

            self.indexes[i] = mh
            self.lsh.insert(i, mh)

    def query(self, image):
        return self.lsh.query(self.indexes[image])


def index_balanced_bucket(images):
    buckets = defaultdict(set)

    print('\t- Indexing balanced buckets...')

    for i in images:
        bucket = min((buckets[t] for t in i.tags), key=lambda x: len(x))
        bucket.add(i)

    return buckets


def index_sub_buckets(images, threshold=1000, parents=None):
    parents = parents or set()
    buckets = index_bucket(images)
    i = 0

    for k, buc in buckets.items():

        if len(parents) == 0:
            print(i)
            i += 1

        if len(buc) > threshold:
            if k not in parents:
                buc_parents = parents or set()
                buc_parents.add(k)
                yield from index_sub_buckets(buc, threshold, buc_parents)
        else:
            yield buc
