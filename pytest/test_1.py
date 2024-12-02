import pytest
import sys


# Написать параметризованный автотест (pytest.mark.parametrize)


@pytest.mark.parametrize("test_input,expected", [("2**3", 8), ("5%2", 1), ("6/2", 2)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


# Написать автотест, проверяющий что в нужный момент всплывает исключение с правильным текстом сообщения об ошибке (pytest.raises)


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0


# Написать автотест, проверяющий содержимое вывода в консоль


def print_error():
    print("Ошибка!", file=sys.stderr)


def test_console_output(capsys):
    print_error()

    captured = capsys.readouterr()
    assert captured.err == "Ошибка!\n"
