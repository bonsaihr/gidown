"""
Example script that downloads images for 3 actors:

* Kit Harington
* Iwan Rheon
* Peter Dinklage

and saves them to *./out*.
"""
import os

from gidown.advanced import Type, Size
from gidown import image_query

from multiprocessing import Pool, cpu_count


def save(args):
    """
    Save image to disk. Wrapper to be used with multiprocessing.Pool.
    
    :param args: tuple of (image: GoogleSearchImage, root: str, name: str)
    """
    image, root, name = args
    try:
        image.save(os.path.join(root, name), auto_ext=True)
    except:
        pass


def main():
    """
    Download images for 3 actors and save them to *./out*.
    """
    num_imgs = 20
    output_dir = "out"
    pool = Pool(cpu_count())

    actors = ["Kit Harington", "Iwan Rheon", "Peter Dinklage"]

    for actor in actors:

        images = image_query(actor, Type.FACE, Size.LARGE)

        actor_output_dir = os.path.join(output_dir, actor.replace(" ", "_"))
        if not os.path.exists(actor_output_dir):
            os.makedirs(actor_output_dir)

        pool.map(save, ((img, actor_output_dir, str(i)) for i, img in enumerate(images[:num_imgs])))


if __name__ == '__main__':
    main()
