import unittest

from PIL import Image
import numpy as np

from mlozaic.parser import parse
from mlozaic.renderer import render

render_or_check = "check"


class TestParsing(unittest.TestCase):
    def render_or_check(self, name, program, env={}):
        image = render(parse(program).evaluate(env), stretch=1)

        path = f"examples/{name}.png"

        if render_or_check == "render":
            image = Image.fromarray(image, "RGB")

            image.save(path)
        else:
            actual = Image.open(path)
            self.assertEqual(0, (np.array(actual) != image).sum())

    def test_in_check_mode(self):
        self.assertEqual(
            "check", render_or_check, "should be in check mode to check images"
        )

    def test_basic_circle(self):
        self.render_or_check("black-circle", "(circle black 0 0 50 50)")

    def test_color(self):
        self.render_or_check("red-circle", "(circle red 0 0 50 50)")

    def test_square(self):
        self.render_or_check(
            "circle-and-square",
            "(combine (circle green 0 0 30 30) (square blue 0 0 20 20))",
        )

    def test_line_of_circles(self):
        self.render_or_check(
            "line-of-circles",
            "(repeat $0 0 9 (circle black (- (* $0 10) 40) 0 5 5))",
        )

    def test_rotated_square(self):
        self.render_or_check(
            "rotated-squares",
            "(repeat $0 0 3 (rotate (/ $0 4) (square black 0 0 30 30)))",
        )

    def test_parabola(self):
        self.render_or_check(
            "parabola",
            "(repeat $0 -30 30 (circle black $0 (/ (* $0 $0) 30) 1 1))",
        )

    def test_star_field(self):
        self.render_or_check(
            "star-field",
            """
            (combine
                (square darkblue 0 0 100 100)
                (repeat $0 -3 4
                    (repeat $1 -3 4
                        (ife (= (% (+ $0 $1) 2) 0)
                            (circle white (* 12 $0) (* 12 $1) 5 5)
                            (square white (* 12 $0) (* 12 $1) 5 5)))))
            """,
        )
