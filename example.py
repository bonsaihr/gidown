import os

from gis.advanced import Type, Size
from gis import Request

from multiprocessing import Pool, cpu_count
import tqdm


def save(args):
    image, root, name = args
    image.save(os.path.join(root, name), auto_extension=True)


def main():
    num_img = 20
    output_dir = "out"
    pool = Pool(cpu_count())

    actors = [
        "Kit Harington",
        "Iwan Rheon",
        "Peter Dinklage",

    ]
    with tqdm.tqdm(total=len(actors)) as pbar:

        for actor in actors:
            pbar.desc = "{:20s}".format(actor)
            images = Request().image_query(actor, Type.FACE, Size.LARGE)

            actor_output_dir = os.path.join(output_dir, actor.replace(" ", "_"))
            if not os.path.exists(actor_output_dir):
                os.makedirs(actor_output_dir)

            pool.map(save, ((img, actor_output_dir, str(i)) for i, img in enumerate(images[:num_img])))
            pbar.update(1)


if __name__ == '__main__':
    main()