import numpy as np
from numpy.testing import *
 
import scikits.image.graph.mcp as mcp

a = np.ones((8,8), dtype=np.float32)
a[1:-1, 1] = 0
a[1, 1:-1] = 0
 
## array([[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
##        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.],
##        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
##        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
##        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
##        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
##        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
##        [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.]], dtype=float32)
 
def test_basic():
    m = mcp.MCP(a, fully_connected=True)
    costs, traceback = m.find_costs([(1,6)])
    return_path = m.traceback((7, 2))
    assert_array_equal(costs,
                       [[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
                        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.],
                        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
                        [ 1.,  0.,  1.,  2.,  2.,  2.,  2.,  2.],
                        [ 1.,  0.,  1.,  2.,  3.,  3.,  3.,  3.],
                        [ 1.,  0.,  1.,  2.,  3.,  4.,  4.,  4.],
                        [ 1.,  0.,  1.,  2.,  3.,  4.,  5.,  5.],
                        [ 1.,  1.,  1.,  2.,  3.,  4.,  5.,  6.]])
 
    assert_array_equal(return_path,
                       [(1, 6),
                        (1, 5),
                        (1, 4),
                        (1, 3),
                        (1, 2),
                        (2, 1),
                        (3, 1),
                        (4, 1),
                        (5, 1),
                        (6, 1),
                        (7, 2)])

def test_route():
    return_path, cost = mcp.route_through_array(a, (1,6), (7,2), geometric=True)
    assert_almost_equal(cost, np.sqrt(2)/2)
    assert_array_equal(return_path,
                       [(1, 6),
                        (1, 5),
                        (1, 4),
                        (1, 3),
                        (1, 2),
                        (2, 1),
                        (3, 1),
                        (4, 1),
                        (5, 1),
                        (6, 1),
                        (7, 2)])
 
def test_no_diagonal():
    m = mcp.MCP(a, fully_connected=False)
    costs, traceback = m.find_costs([(1,6)])
    return_path = m.traceback((7, 2))
    assert_array_equal(costs,
                       [[ 2.,  1.,  1.,  1.,  1.,  1.,  1.,  2.],
                        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.],
                        [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  2.],
                        [ 1.,  0.,  1.,  2.,  2.,  2.,  2.,  3.],
                        [ 1.,  0.,  1.,  2.,  3.,  3.,  3.,  4.],
                        [ 1.,  0.,  1.,  2.,  3.,  4.,  4.,  5.],
                        [ 1.,  0.,  1.,  2.,  3.,  4.,  5.,  6.],
                        [ 2.,  1.,  2.,  3.,  4.,  5.,  6.,  7.]])
    assert_array_equal(return_path,
                       [(1, 6),
                        (1, 5),
                        (1, 4),
                        (1, 3),
                        (1, 2),
                        (1, 1),
                        (2, 1),
                        (3, 1),
                        (4, 1),
                        (5, 1),
                        (6, 1),
                        (7, 1),
                        (7, 2)])
 

def test_crashing():
    _test_random((1000,1000))
    _test_random((10,20,30,40))

def _test_random(shape):
    # Just tests for crashing -- not for correctness.
    np.random.seed(0)
    a = np.random.random(shape).astype(np.float32)
    starts = [[0]*len(shape), [-1]*len(shape), (np.random.random(len(shape))*shape).astype(int)]
    ends = [(np.random.random(len(shape))*shape).astype(int) for i in range(4)]
    m = mcp.MCP(a, fully_connected=True)
    costs, offsets = m.find_costs(starts)
    for point in [(np.random.random(len(shape))*shape).astype(int) for i in range(4)]:
        m.traceback(point)
    m.reset()
    m.find_costs(starts, ends)
    for end in ends:
        m.traceback(end)
    return a, costs, offsets


if __name__ == "__main__":
    run_module_suite()