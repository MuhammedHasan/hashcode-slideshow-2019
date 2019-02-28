from collections import namedtuple


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
        yield Image(idx=i, shape=shape, tags=tags)


def max_image(image, images, image_set):
    curr_image = -1
    curr_max = -1
    stop = 10

    for i in image_set:
        stop -= 1
        if stop == 0:
            break

        alt_sim = sim(images[i], images[image])
        if curr_max < alt_sim:
            curr_image = i
            curr_max = alt_sim

    return curr_image

    return max(image_set,
               key=lambda x: sim(images[image], images[x]))


def solve(images):
    '''
    Return list of tuple of images []

    '''
    images = list(filter(lambda x: x.shape == 'H', images))
    image = images[0].idx
    images = {i.idx: i for i in images}
    image_set = set([i.idx for i in images.values()])

    i = 0

    while True:
        i += 1
        print(i, image)
        if len(image_set) > 1:
            image_set.remove(image)
            next_image = max_image(image, images, image_set)
            yield (images[next_image], )
            image = next_image
        elif len(image_set) == 1:
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
        # 'b_lovely_landscapes',
        'c_memorable_moments',
        'd_pet_pictures',
        'e_shiny_selfies'
    ]

    for f in files:
        images = list(parse(open('../inputs/%s.txt' % f)))
        solution = list(solve(images))
        write(solution, open('../outputs/%s.out' % f, 'w'))
        print(f)
