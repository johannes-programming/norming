import inspect as ins
import unittest
from typing import *

from norming.core import Norming


# Example norm function
def example_norm(cls: type, x: Any, y: Any = 0) -> tuple:
    """Normalize to tuple of (x, y)."""
    return (x * 2, y + 1)


# reconstruct normedtuple
normedtuple: Norming = Norming(tuple)

# Decorate with normedtuple
ExampleTuple: type = normedtuple(example_norm)


class TestNormedTuple(unittest.TestCase):
    def test_instance_is_tuple(self: Self) -> None:
        obj: Any = ExampleTuple(2, 3)
        self.assertIsInstance(obj, tuple)
        self.assertEqual(obj, (4, 4))

    def test_docstring_and_name(self: Self) -> None:
        self.assertEqual(ExampleTuple.__doc__, example_norm.__doc__)
        self.assertEqual(ExampleTuple.__name__, example_norm.__name__)

    def test_default_argument(self: Self) -> None:
        obj: Any = ExampleTuple(5)
        self.assertEqual(obj, (10, 1))

    def test_signature_preserved(self: Self) -> None:
        # Signature exposed on the class constructor (should exclude 'cls')
        params: list = list(ins.signature(example_norm).parameters.values())
        expected_public_sig: ins.Signature = ins.signature(example_norm)
        expected_public_sig: ins.Signature = expected_public_sig.replace(
            parameters=params[1:]
        )
        self.assertEqual(
            ins.signature(ExampleTuple).parameters, expected_public_sig.parameters
        )
        self.assertEqual(ins.signature(ExampleTuple).return_annotation, Self)
        # Signature on __new__ (should match exactly, including 'cls')
        self.assertEqual(
            ins.signature(ExampleTuple.__new__).parameters,
            ins.signature(example_norm).parameters,
        )
        self.assertEqual(ins.signature(ExampleTuple.__new__).return_annotation, Self)


if __name__ == "__main__":
    unittest.main()
