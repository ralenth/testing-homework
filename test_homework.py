from homework import calculate, take_from_list
import json
import os
import pytest
import unittest.mock


class TestTakeFromList:
    """Tests for take_from_list function."""

    ELEMENTS = 10

    def test_empty_list(self):
        assert take_from_list([], []) == []

    def test_empty_indices(self):
        assert take_from_list([1, 2, 3], []) == []

    @pytest.mark.parametrize('indices', [
        "foo",
        ["foo"],
        (1, 2, 3),
        [1, 2, "3"],
        [1, 2, 3.0],
    ])
    def test_invalid_indices(self, indices):
        with pytest.raises(ValueError):
            take_from_list(list(range(self.ELEMENTS)), indices)

    @pytest.mark.parametrize('indices', [
        10,
        [11],
        [1, 2, 12],
    ])
    def test_too_big_indices(self, indices):
        with pytest.raises(IndexError):
            take_from_list(list(range(self.ELEMENTS)), indices)

    def test_singleton_list(self):
        elem = "foo"
        li = [elem]

        assert take_from_list(li, 0) == li
        assert take_from_list(li, -1) == li
        assert take_from_list(li, [0, 0]) == [elem, elem]


class TestCalculate:
    """Tests for calculate function."""

    IN_FILE = "in.json"
    OUT_FILE = "out.json"

    def test_no_in_file(self, tmpdir):
        in_file, out_file = tmpdir / self.IN_FILE, tmpdir / self.OUT_FILE
        with pytest.raises(FileNotFoundError):
            calculate(in_file, out_file)

    def test_invalid_in_file(self, tmpdir):
        in_file, out_file = tmpdir / self.IN_FILE, tmpdir / self.OUT_FILE
        with open(in_file, 'w') as f_p:
            f_p.write('foo')

        with pytest.raises(json.JSONDecodeError):
            calculate(in_file, out_file)

    @pytest.mark.parametrize('content', [
        '{}',
        '{"list": []}',
        '{"indices": []}'
    ])
    def test_incomplete_in_file(self, tmpdir, content):
        in_file, out_file = tmpdir / self.IN_FILE, tmpdir / self.OUT_FILE
        with open(in_file, 'w') as f_p:
            f_p.write(content)

        with pytest.raises(KeyError):
            calculate(in_file, out_file)

    @unittest.mock.patch('homework.take_from_list')
    def test_save(self, take_from_list_mock, tmpdir):
        in_file, out_file = tmpdir / self.IN_FILE, tmpdir / self.OUT_FILE
        with open(in_file, 'w') as f_p:
            f_p.write('{"list": [], "indices": []}')

        mocked_return_value = ['foo', 'bar']
        take_from_list_mock.return_value = mocked_return_value

        calculate(in_file, out_file)
        assert take_from_list_mock.call_args == (([], []),)

        with open(out_file, 'r') as f_p:
            assert json.load(f_p) == mocked_return_value


class TestE2E:
    """End-to-end tests for both calculate and take_from_list functionalities."""

    def test_example_input(self, tmpdir):
        in_file, out_file = os.path.join(os.path.dirname(__file__), "input.json"), tmpdir / "out.json"

        calculate(in_file, out_file)
        with open(out_file, 'r') as f_p:
            assert json.load(f_p) == [81, 62, 78, 67, 89, 33, 106, 126, 112, 20, 56, 128, 106, 3, 107]
