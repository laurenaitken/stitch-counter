import pytest
from stitch_pattern.pattern import expand_pattern


@pytest.mark.parametrize("text, expected",
                         [("k1, p1, k1, p1", ['k', 'p', 'k', 'p']), 
                          ("k5, p2", ['k', 'k', 'k', 'k', 'k', 'p', 'p']), 
                          ("k2 p2 * k1 p1 * x3", ['k', 'k', 'p', 'p', 'k', 'p', 'k', 'p', 'k', 'p']),
                          ("K3 P2", ['k', 'k', 'k', 'p', 'p']),
                          ("k1,p1", ['k', 'p']),
                          ("*k1 p1* x2", ['k', 'p', 'k', 'p'])
                          ],
                          ids=['1basic', '9counted', '10repeat', '8case', '15messycomma', '19messyasterisk']
                          )
def test_expand_pattern_returns_stitch_list(text, expected):
    assert expand_pattern(text) == expected
