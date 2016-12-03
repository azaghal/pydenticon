# Standard library imports.
import hashlib
import unittest
from io import BytesIO

# Third-party Python library imports.
import mock
import PIL
import PIL.ImageChops

# Library imports.
from pydenticon import Generator


class GeneratorTest(unittest.TestCase):
    """
    Implements tests for pydenticon.Generator class.
    """

    def test_init_entropy(self):
        """
        Tests if the constructor properly checks for entropy provided by a
        digest algorithm.
        """

        # Set-up the mock instance.
        hexdigest_method = mock.MagicMock(return_value="aabb")
        digest_instance = mock.MagicMock()
        digest_instance.hexdigest = hexdigest_method

        # Set-up digest function that will always return the same digest
        # instance.
        digest_method = mock.MagicMock(return_value=digest_instance)

        # This should require 23 bits of entropy, while the digest we defined
        # provided 2*8 bits of entropy (2 bytes).
        self.assertRaises(ValueError, Generator, 5, 5, digest=digest_method)

    def test_init_parameters(self):
        """
        Verifies that the constructor sets-up the instance properties correctly.
        """

        generator = Generator(5, 5, digest=hashlib.sha1, foreground=["#111111", "#222222"], background="#aabbcc")

        # sha1 provides 160 bits of entropy - 20 bytes.
        self.assertEqual(generator.digest_entropy, 20 * 8)
        self.assertEqual(generator.digest, hashlib.sha1)
        self.assertEqual(generator.rows, 5)
        self.assertEqual(generator.columns, 5)
        self.assertEqual(generator.foreground, ["#111111", "#222222"])
        self.assertEqual(generator.background, "#aabbcc")

    def test_get_bit(self):
        """
        Tests if the check whether bit is 1 or 0 is performed correctly.
        """

        generator = Generator(5, 5)
        hash_bytes = [0b10010001, 0b10001000, 0b00111001]

        # Check a couple of bits from the above hash bytes.
        self.assertEqual(True, generator._get_bit(0, hash_bytes))
        self.assertEqual(True, generator._get_bit(7, hash_bytes))
        self.assertEqual(False, generator._get_bit(22, hash_bytes))
        self.assertEqual(True, generator._get_bit(23, hash_bytes))

    def test_generate_matrix(self):
        """
        Verifies that the matrix is generated correctly based on passed hashed
        bytes.
        """

        # The resulting half-matrix should be as follows (first byte is for
        # ignored in matrix generation):
        #
        # 100
        # 011
        # 100
        # 001
        # 110
        hash_bytes = [0b11111111, 0b10101010, 0b01010101]

        expected_matrix = [
            [True, False, False, False, True],
            [False, True, True, True, False],
            [True, False, False, False, True],
            [False, False, True, False, False],
            [True, True, False, True, True],
            ]

        generator = Generator(5, 5)

        matrix = generator._generate_matrix(hash_bytes)

        self.assertEqual(matrix, expected_matrix)

    def test_data_to_digest_byte_list_raw(self):
        """
        Test if correct digest byte list is returned for raw (non-hex-digest)
        data passed to the method.
        """

        # Set-up some raw data, and set-up the expected result.
        data = "this is a test\n"
        expected_digest_byte_list = [225, 156, 18, 131, 201, 37, 179, 32, 102, 133, 255, 82, 42, 207, 227, 230]

        # Instantiate a generator.
        generator = Generator(5, 5, digest=hashlib.md5)

        # Call the method and get the results.
        digest_byte_list = generator._data_to_digest_byte_list(data)

        # Verify the expected and actual result are identical.
        self.assertEqual(expected_digest_byte_list, digest_byte_list)

    def test_data_to_digest_byte_list_hex(self):
        """
        Test if correct digest byte list is returned for passed hex digest
        string.
        """

        # Set-up some test hex digest (md5), and expected result.
        hex_digest = "e19c1283c925b3206685ff522acfe3e6"
        expected_digest_byte_list = [225, 156, 18, 131, 201, 37, 179, 32, 102, 133, 255, 82, 42, 207, 227, 230]

        # Instantiate a generator.
        generator = Generator(5, 5, digest=hashlib.md5)

        # Call the method and get the results.
        digest_byte_list = generator._data_to_digest_byte_list(hex_digest)

        # Verify the expected and actual result are identical.
        self.assertEqual(expected_digest_byte_list, digest_byte_list)

    def test_data_to_digest_byte_list_hex_lookalike(self):
        """
        Test if correct digest byte list is returned for passed raw data that
        has same length as hex digest string.
        """

        # Set-up some test hex digest (md5), and expected result.
        data = "qqwweerrttyyuuiiooppaassddffgghh"
        expected_digest_byte_list = [25, 182, 52, 218, 118, 220, 26, 145, 164, 222, 33, 221, 183, 140, 98, 246]

        # Instantiate a generator.
        generator = Generator(5, 5, digest=hashlib.md5)

        # Call the method and get the results.
        digest_byte_list = generator._data_to_digest_byte_list(data)

        # Verify the expected and actual result are identical.
        self.assertEqual(expected_digest_byte_list, digest_byte_list)

    def test_generate_image_basics(self):
        """
        Tests some basics about generated PNG identicon image. This includes:

        - Dimensions of generated image.
        - Format of generated image.
        - Mode of generated image.
        """

        # Set-up parameters that will be used for generating the image.
        width = 200
        height = 200
        padding = [20, 20, 20, 20]
        foreground = "#ffffff"
        background = "#000000"
        matrix = [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            ]

        # Set-up a generator.
        generator = Generator(5, 5)

        # Generate the raw image.
        raw_image = generator._generate_image(matrix, width, height, padding, foreground, background, "png")

        # Try to load the raw image.
        image_stream = BytesIO(raw_image)
        image = PIL.Image.open(image_stream)

        # Verify image size, format, and mode.
        self.assertEqual(image.size[0], 240)
        self.assertEqual(image.size[1], 240)
        self.assertEqual(image.format, "PNG")
        self.assertEqual(image.mode, "RGBA")

    def test_generate_ascii(self):
        """
        Tests the generated identicon in ASCII format.
        """

        # Set-up parameters that will be used for generating the image.
        foreground = "1"
        background = "0"
        matrix = [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            ]

        # Set-up a generator.
        generator = Generator(5, 5)

        # Generate the ASCII image.
        ascii_image = generator._generate_ascii(matrix, foreground, background)

        # Verify that the result is as expected.
        expected_result = """00100
00100
00100
01110
01110"""
        self.assertEqual(ascii_image, expected_result)

    def test_generate_format(self):
        """
        Tests if identicons are generated in requested format.
        """

        # Set-up a generator.
        generator = Generator(5, 5)

        # Set-up some test data.
        data = "some test data"

        # Verify that PNG image is returned when requested.
        raw_image = generator.generate(data, 200, 200, output_format="png")
        image_stream = BytesIO(raw_image)
        image = PIL.Image.open(image_stream)
        self.assertEqual(image.format, "PNG")

        # Verify that JPEG image is returned when requested.
        raw_image = generator.generate(data, 200, 200, output_format="jpeg")
        image_stream = BytesIO(raw_image)
        image = PIL.Image.open(image_stream)
        self.assertEqual(image.format, "JPEG")

        # Verify that GIF image is returned when requested.
        raw_image = generator.generate(data, 200, 200, output_format="gif")
        image_stream = BytesIO(raw_image)
        image = PIL.Image.open(image_stream)
        self.assertEqual(image.format, "GIF")

        # Verify that ASCII "image" is returned when requested.
        raw_image = generator.generate(data, 200, 200, output_format="ascii")
        self.assertIsInstance(raw_image, str)

    def test_generate_format_invalid(self):
        """
        Tests if an exception is raised in case an unsupported format is
        requested when generating the identicon.
        """

        # Set-up a generator.
        generator = Generator(5, 5)

        # Set-up some test data.
        data = "some test data"

        # Verify that an exception is raised in case of unsupported format.
        self.assertRaises(ValueError, generator.generate, data, 200, 200, output_format="invalid")

    @mock.patch.object(Generator, '_generate_image')
    def test_generate_inverted_png(self, generate_image_mock):
        """
        Tests if the foreground and background are properly inverted when
        generating PNG images.
        """

        # Set-up some test data.
        data = "Some test data"

        # Set-up one foreground and background colour.
        foreground = "#ffffff"
        background = "#000000"

        # Set-up the generator.
        generator = Generator(5, 5, foreground=[foreground], background=background)

        # Verify that colours are picked correctly when no inverstion is requsted.
        generator.generate(data, 200, 200, inverted=False, output_format="png")
        generate_image_mock.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, foreground, background, "png")

        # Verify that colours are picked correctly when inversion is requsted.
        generator.generate(data, 200, 200, inverted=True, output_format="png")
        generate_image_mock.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, background, foreground, "png")

    @mock.patch.object(Generator, '_generate_ascii')
    def test_generate_inverted_ascii(self, generate_ascii_mock):
        """
        Tests if the foreground and background are properly inverted when
        generating ASCII "images".
        """

        # Set-up some test data.
        data = "Some test data"

        # Set-up one foreground and background colour. These are not used for
        # ASCII itself (instead a plus/minus sign is used).
        foreground = "#ffffff"
        background = "#000000"

        # Set-up the generator.
        generator = Generator(5, 5, foreground=[foreground], background=background)

        # Verify that foreground/background is picked correctly when no
        # inverstion is requsted.
        generator.generate(data, 200, 200, inverted=False, output_format="ascii")
        generate_ascii_mock.assert_called_with(mock.ANY, "+", "-")

        # Verify that foreground/background is picked correctly when inversion
        # is requsted.
        generator.generate(data, 200, 200, inverted=True, output_format="ascii")
        generate_ascii_mock.assert_called_with(mock.ANY, "-", "+")

    @mock.patch.object(Generator, '_generate_image')
    def test_generate_foreground(self, generate_image_mock):
        """
        Tests if the foreground colour is picked correctly.
        """

        # Set-up some foreground colours and a single background colour.
        foreground = ["#000000", "#111111", "#222222", "#333333", "#444444", "#555555"]
        background = "#ffffff"

        # Set-up the generator.
        generator = Generator(5, 5, foreground=foreground, background=background)

        # The first byte of hex digest should be 121 for this data, which should
        # result in foreground colour of index '1'.
        data = "some test data"
        generator.generate(data, 200, 200)
        generate_image_mock.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, foreground[1], background, "png")

        # The first byte of hex digest should be 149 for this data, which should
        # result in foreground colour of index '5'.
        data = "some other test data"
        generator.generate(data, 200, 200)
        generate_image_mock.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, foreground[5], background, "png")

    def test_generate_image_compare(self):
        """
        Tests generated PNG identicon against a set of pre-generated samples.
        """

        # Set-up a list of foreground colours (taken from Sigil). Same as used
        # for reference images.
        foreground = ["rgb(45,79,255)",
                      "rgb(254,180,44)",
                      "rgb(226,121,234)",
                      "rgb(30,179,253)",
                      "rgb(232,77,65)",
                      "rgb(49,203,115)",
                      "rgb(141,69,170)"]

        # Set-up a background colour (taken from Sigil). Same as used for
        # reference images.
        background = "rgb(224,224,224)"

        # Set-up parameters equivalent as used for samples.
        width = 200
        height = 200
        padding = (20, 20, 20, 20)

        # Load the reference images, making sure they're in RGBA mode.
        test1_ref = PIL.Image.open("tests/samples/test1.png").convert(mode="RGBA")
        test2_ref = PIL.Image.open("tests/samples/test2.png").convert(mode="RGBA")
        test3_ref = PIL.Image.open("tests/samples/test3.png").convert(mode="RGBA")

        # Set-up the Generator.
        generator = Generator(5, 5, foreground=foreground, background=background)

        # Generate first test identicon.
        raw_image = generator.generate("test1", width, height, padding=padding)
        image_stream = BytesIO(raw_image)
        test1 = PIL.Image.open(image_stream)

        # Generate second test identicon.
        raw_image = generator.generate("test2", width, height, padding=padding)
        image_stream = BytesIO(raw_image)
        test2 = PIL.Image.open(image_stream)

        # Generate third test identicon.
        raw_image = generator.generate("test3", width, height, padding=padding)
        image_stream = BytesIO(raw_image)
        test3 = PIL.Image.open(image_stream)

        # Calculate differences between generated identicons and references.
        diff1 = PIL.ImageChops.difference(test1, test1_ref)
        diff2 = PIL.ImageChops.difference(test2, test2_ref)
        diff3 = PIL.ImageChops.difference(test3, test3_ref)

        # Verify that all the diffs are essentially black (i.e. no differences
        # between generated identicons and reference samples).
        expected_extrema = ((0, 0), (0, 0), (0, 0), (0, 0))

        self.assertEqual(diff1.getextrema(), expected_extrema)
        self.assertEqual(diff2.getextrema(), expected_extrema)
        self.assertEqual(diff3.getextrema(), expected_extrema)

if __name__ == '__main__':
    unittest.main()
