from collections import namedtuple


Image = namedtuple('Image', ['idx', 'shape', 'tags'])


def sim(img1, img2):
    return min(len(img1.tags.intersection(img2.tags)),
               len(img1.tags.difference(img2.tags)),
               len(img2.tags.difference(img1.tags)))


def parse(filename):
    num_photo = int(filename.readline())
    for i in range(num_photo):
        line = filename.readline().strip().split(' ')
        shape = line[0]
        tags = set(line[2:])
        yield Image(idx=i, shape=shape, tags=tags)


def solve(images):
    images = list(filter(lambda x: x.shape == 'H', images))

    image_set = set([i.idx for i in images])
    image = 0

    while True:
        if len(image_set) > 1:
            image_set.remove(image)
            next_image = max(image_set,
                             key=lambda x: sim(images[image], images[x]))
            yield images[next_image]
            image = next_image
        elif len(image_set) == 1:
            yield images[next_image]
            break
        else:
            break


def write(solution, filename):
    filename.write('%d\n' % len(solution))
    for i in solution:
        if len(i) == 1:
            filename.write('%d\n' % (i[0].idx))
        if len(i) == 2:
            filename.write('%d %d\n' % (i[0].idx, i[1].idx))
        if len(i) > 2:
            raise ValueError('i cannot bigger than 2')


if __name__ == "__main__":
    files = [
        'a_example',
        'b_lovely_landscapes',
        'c_memorable_moments',
        'd_pet_pictures',
        'e_shiny_selfies'
    ]

    for f in files:
        images = list(parse(open('../inputs/%s.txt' % f)))
        solution = list(solve(images))
        write(solution, open('../outputs/%s.out' % f, 'w'))
