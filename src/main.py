from collections import namedtuple, defaultdict


Image = namedtuple('Image', ['idx', 'shape', 'tags'])


def sim(img1, img2):
    intersect = img1.tags.intersection(img2.tags)
    if intersect == 0:
        return 0

    return min(len(img1.tags.intersection(img2.tags)),
               len(img1.tags.difference(img2.tags)),
               len(img2.tags.difference(img1.tags)))


def parse(filename):
    num_photo = int(filename.readline())
    for i in range(num_photo):
        line = filename.readline().strip().split(' ')
        shape = line[0]
        tags = set(line[2:])
        yield Image(idx=str(i), shape=shape, tags=tags)


def max_image(image, images, buckets, visited):
    curr_image = -1
    curr_max = -1
    stop = 3

    buckets = sorted([buckets[t] for t in images[image].tags], key=len)

    for buc in buckets:
        stop -= 1
        if stop == 0:
            break

        for idx in buc:
            if idx not in visited:
                alt_sim = sim(images[idx], images[image])
                if curr_max < alt_sim:
                    curr_image = idx
                    curr_max = alt_sim
    return curr_image


def merge_V(images):
    Himages = list(filter(lambda x: x.shape == 'H', images))
    Vimages = sorted(
        list(filter(lambda x: x.shape == 'V', images)),
        key=lambda x: tuple(x.tags))

    V1images = Vimages[:len(Vimages)//2]
    V2images = Vimages[len(Vimages)//2:]

    for i in Himages:
        yield i

    for i, j in zip(V1images, V2images):
        yield Image(idx='%s %s' % (i.idx, j.idx), shape='V', tags=i.tags.union(j.tags))


def index_bucket(images):
    buckets = defaultdict(set)

    for i in images:
        for t in i.tags:
            buckets[t].add(i.idx)

    return buckets


def random_image(image_set):
    i = image_set.pop()
    image_set.add(i)
    return i


def solve(images):
    '''
    Return list of tuple of images []

    '''
    images = list(merge_V(images))
    buckets = index_bucket(images)

    # print([len(b) for b in buckets.values()])

    # return

    image = images[0].idx
    images = {i.idx: i for i in images}
    image_set = set([i.idx for i in images.values()])

    i = 0

    visited = set()

    while True:
        i += 1
        if i % 1000 == 0:
            print(i, image)

        if len(image_set) > 1:
            image_set.remove(image)
            visited.add(image)
            next_image = max_image(image, images, buckets, visited)

            if next_image == -1:
                next_image = random_image(image_set)

            yield (images[next_image], )
            image = next_image
        elif len(image_set) == 1:
            break


def write(solution, filename):
    filename.write('%d\n' % len(solution))
    for i in solution:
        filename.write('%s\n' % (i[0].idx))


def uniqui_tags(images):
    all_tags = set()
    for i in images:
        for t in i.tags:
            all_tags.add(t)
    return list(all_tags)


if __name__ == "__main__":
    files = [
        # 'a_example',
        # 'b_lovely_landscapes',
        # 'c_memorable_moments',
        # 'd_pet_pictures',
        'e_shiny_selfies'
    ]

    for f in files:
        images = list(parse(open('../inputs/%s.txt' % f)))
        solution = list(solve(images))
        write(solution, open('../outputs-bucket3/%s.out' % f, 'w'))
        print(f)
