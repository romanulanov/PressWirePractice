import pytest
from unittest.mock import patch
from tools import get_random_number  


@patch("random.randint", return_value=5)  
def test_get_random_number(mock_randint):
    result = get_random_number()
    assert result == 5

    mock_randint.assert_called_once_with(1, 10)
