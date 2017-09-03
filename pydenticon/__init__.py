# For digest operations.
import hashlib

# For saving the images from Pillow.
from io import BytesIO

# Pillow for Image processing.
from PIL import Image, ImageDraw

# For decoding hex values (works both for Python 2.7.x and Python 3.x).
import binascii


class Generator(object):
    """
    Factory class that can be used for generating the identicons
    deterministically based on hash of the passed data.

    Resulting identicons are images of requested size with optional padding. The
    identicon (without padding) consists out of M x N blocks, laid out in a
    rectangle, where M is the number of blocks in each column, while N is number
    of blocks in each row.

    Each block is a smallself rectangle on its own, filled using the foreground or
    background colour.

    The foreground is picked randomly, based on the passed data, from the list
    of foreground colours set during initialisation of the generator.

    The blocks are always laid-out in such a way that the identicon will be
    symterical by the Y axis. The center of symetry will be the central column
    of blocks.

    Simply put, the generated identicons are small symmetric mosaics with
    optional padding.
    """

    def __init__(self, rows, columns, digest=hashlib.md5, foreground=["#000000"], background="#ffffff"):
        """
        Initialises an instance of identicon generator. The instance can be used
        for creating identicons with differing image formats, sizes, and with
        different padding.

        Arguments:

          rows - Number of block rows in an identicon.

          columns - Number of block columns in an identicon.

          digest - Digest class that should be used for the user's data. The
          class should support accepting a single constructor argument for
          passing the data on which the digest will be run. Instances of the
          class should also support a single hexdigest() method that should
          return a digest of passed data as a hex string. Default is
          hashlib.md5. Selection of the digest will limit the maximum values
          that can be set for rows and columns. Digest needs to be able to
          generate (columns / 2 + columns % 2) * rows + 8 bits of entropy.

          foreground - List of colours which should be used for drawing the
          identicon. Each element should be a string of format supported by the
          PIL.ImageColor module. Default is ["#000000"] (only black).

          background - Colour (single) which should be used for background and
          padding, represented as a string of format supported by the
          PIL.ImageColor module. Default is "#ffffff" (white).
        """

        # Check if the digest produces sufficient entropy for identicon
        # generation.
        entropy_provided = len(digest(b"test").hexdigest()) // 2 * 8
        entropy_required = (columns // 2 + columns % 2) * rows + 8

        if entropy_provided < entropy_required:
            raise ValueError("Passed digest '%s' is not capable of providing %d bits of entropy" % (str(digest), entropy_required))

        # Set the expected digest size. This is used later on to detect if
        # passed data is a digest already or not.
        self.digest_entropy = entropy_provided

        self.rows = rows
        self.columns = columns

        self.foreground = foreground
        self.background = background

        self.digest = digest

    def _get_bit(self, n, hash_bytes):
        """
        Determines if the n-th bit of passed bytes is 1 or 0.

        Arguments:

          hash_bytes - List of hash byte values for which the n-th bit value
          should be checked. Each element of the list should be an integer from
          0 to 255.

        Returns:

          True if the bit is 1. False if the bit is 0.
        """

        if hash_bytes[n // 8] >> int(8 - ((n % 8) + 1)) & 1 == 1:
            return True

        return False

    def _generate_matrix(self, hash_bytes):
        """
        Generates matrix that describes which blocks should be coloured.

        Arguments:
          hash_bytes - List of hash byte values for which the identicon is being
          generated. Each element of the list should be an integer from 0 to
          255.

        Returns:
          List of rows, where each element in a row is boolean. True means the
          foreground colour should be used, False means a background colour
          should be used.
        """

        # Since the identicon needs to be symmetric, we'll need to work on half
        # the columns (rounded-up), and reflect where necessary.
        half_columns = self.columns // 2 + self.columns % 2
        cells = self.rows * half_columns

        # Initialise the matrix (list of rows) that will be returned.
        matrix = [[False] * self.columns for _ in range(self.rows)]

        # Process the cells one by one.
        for cell in range(cells):

            # If the bit from hash correpsonding to this cell is 1, mark the
            # cell as foreground one. Do not use first byte (since that one is
            # used for determining the foreground colour.
            if self._get_bit(cell, hash_bytes[1:]):

                # Determine the cell coordinates in matrix.
                column = cell // self.columns
                row = cell % self.rows

                # Mark the cell and its reflection. Central column may get
                # marked twice, but we don't care.
                matrix[row][column] = True
                matrix[row][self.columns - column - 1] = True

        return matrix

    def _data_to_digest_byte_list(self, data):
        """
        Creates digest of data, returning it as a list where every element is a
        single byte of digest (an integer between 0 and 255).

        No digest will be calculated on the data if the passed data is already a
        valid hex string representation of digest, and the passed value will be
        used as digest in hex string format instead.

        Arguments:

          data - Raw data or hex string representation of existing digest for
          which a list of one-byte digest values should be returned.

        Returns:

          List of integers where each element is between 0 and 255, and
          repesents a single byte of a data digest.
        """

        # If data seems to provide identical amount of entropy as digest, it
        # could be a hex digest already.
        if len(data) // 2 == self.digest_entropy // 8:
            try:
                binascii.unhexlify(data.encode('utf-8'))
                digest = data.encode('utf-8')
            # Handle Python 2.x exception.
            except (TypeError):
                digest = self.digest(data.encode('utf-8')).hexdigest()
            # Handle Python 3.x exception.
            except (binascii.Error):
                digest = self.digest(data.encode('utf-8')).hexdigest()
        else:
            digest = self.digest(data.encode('utf-8')).hexdigest()

        return [int(digest[i * 2:i * 2 + 2], 16) for i in range(16)]

    def _generate_image(self, matrix, width, height, padding, foreground, background, image_format):
        """
        Generates an identicon image in requested image format out of the passed
        block matrix, with the requested width, height, padding, foreground
        colour, background colour, and image format.

        Arguments:

          matrix - Matrix describing which blocks in the identicon should be
          painted with foreground (background if inverted) colour.

          width - Width of resulting identicon image in pixels.

          height - Height of resulting identicon image in pixels.

          padding - Tuple describing padding around the generated identicon. The
          tuple should consist out of four values, where each value is the
          number of pixels to use for padding. The order in tuple is: top,
          bottom, left, right.

          foreground - Colour which should be used for foreground (filled
          blocks), represented as a string of format supported by the
          PIL.ImageColor module.

          background - Colour which should be used for background and padding,
          represented as a string of format supported by the PIL.ImageColor
          module.

          image_format - Format to use for the image. Format needs to be
          supported by the Pillow library.

        Returns:

          Identicon image in requested format, returned as a byte list.
        """

        # Set-up a new image object, setting the background to provided value.
        image = Image.new("RGBA", (width + padding[2] + padding[3], height + padding[0] + padding[1]), background)

        # Set-up a draw image (for drawing the blocks).
        draw = ImageDraw.Draw(image)

        # Calculate the block widht and height.
        block_width = width // self.columns
        block_height = height // self.rows

        # Go through all the elements of a matrix, and draw the rectangles.
        for row, row_columns in enumerate(matrix):
            for column, cell in enumerate(row_columns):
                if cell:
                    # Set-up the coordinates for a block.
                    x1 = padding[2] + column * block_width
                    y1 = padding[0] + row * block_height
                    x2 = padding[2] + (column + 1) * block_width - 1
                    y2 = padding[0] + (row + 1) * block_height - 1

                    # Draw the rectangle.
                    draw.rectangle((x1, y1, x2, y2), fill=foreground)

        # Set-up a stream where image will be saved.
        stream = BytesIO()

        if image_format.upper() == "JPEG":
            image = image.convert(mode="RGB")

        # Save the image to stream.
        try:
            image.save(stream, format=image_format, optimize=True)
        except KeyError:
            raise ValueError("Pillow does not support requested image format: %s" % image_format)
        image_raw = stream.getvalue()
        stream.close()

        # Return the resulting image.
        return image_raw

    def _generate_ascii(self, matrix, foreground, background):
        """
        Generates an identicon "image" in the ASCII format. The image will just
        output the matrix used to generate the identicon.

        Arguments:

          matrix - Matrix describing which blocks in the identicon should be
          painted with foreground (background if inverted) colour.

          foreground - Character which should be used for representing
          foreground.

          background - Character which should be used for representing
          background.

        Returns:

          ASCII representation of an identicon image, where one block is one
          character.
        """

        return "\n".join(["".join([foreground if cell else background for cell in row]) for row in matrix])

    def generate(self, data, width, height, padding=(0, 0, 0, 0), output_format="png", inverted=False):
        """
        Generates an identicon image with requested width, height, padding, and
        output format, optionally inverting the colours in the indeticon
        (swapping background and foreground colours) if requested.

        Arguments:

          data - Hashed or raw data that will be used for generating the
          identicon.

          width - Width of resulting identicon image in pixels.

          height - Height of resulting identicon image in pixels.

          padding - Tuple describing padding around the generated identicon. The
          tuple should consist out of four values, where each value is the
          number of pixels to use for padding. The order in tuple is: top,
          bottom, left, right.

          output_format - Output format of resulting identicon image. Supported
          formats are anything that is supported by Pillow, plus a special
          "ascii" mode.

          inverted - Specifies whether the block colours should be inverted or
          not. Default is False.

        Returns:

          Byte representation of an identicon image.
        """

        # Calculate the digest, and get byte list.
        digest_byte_list = self._data_to_digest_byte_list(data)

        # Create the matrix describing which block should be filled-in.
        matrix = self._generate_matrix(digest_byte_list)

        # Determine the background and foreground colours.
        if output_format == "ascii":
            foreground = "+"
            background = "-"
        else:
            background = self.background
            foreground = self.foreground[digest_byte_list[0] % len(self.foreground)]

        # Swtich the colours if inverted image was requested.
        if inverted:
            foreground, background = background, foreground

        # Generate the identicon in requested format.
        if output_format == "ascii":
            return self._generate_ascii(matrix, foreground, background)
        else:
            return self._generate_image(matrix, width, height, padding, foreground, background, output_format)
