"""
Module that implements a simple interface for accessing Google Image Search.


To download 5 images of cats and save them, these four lines are needed:

>>> import gidown
>>> images = gidown.image_query("cat")
>>> for i, image in enumerate(images[:5]):
>>>     image.save("img_{}".format(i), auto_ext=True)

File extensions are automatically determined from the image data or, if that fails, 
directly from the results of the image search, as Google wa kind enough to provide a JSON with all information
about the image (image URL, source page URL, Type, Width, Height, Thumbnail URL, ...).

All this information can be accesses as:

>>> print("{}x{}".format(image.width,image.height)
600x400
"""

from gidown.search import *
from gidown.query import QueryBuilder
