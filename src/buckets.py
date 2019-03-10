from tqdm import tqdm
from collections import defaultdict
from datasketch import MinHash, MinHashLSH


def index_bucket(images):
    buckets = defaultdict(set)

    print('\t- Indexing buckets...')

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
