# K-d Tree for 2-dimensional data
class KdNode():
    '''
    Create the KdNode class for K-d Tree
    '''

    def __init__(self, point=None, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right


class KdTree():
    '''
    Create the KdTree class
    '''

    def __init__(self, data):
        k = len(data[0])

        def CreateKdTree(d, depth=0):
            '''
            Create the KdTree
            '''
            if not d:
                return None
            axis = depth % k
            # sort data according to the axis
            d.sort(key=lambda x: x[axis])
            mid = len(d) // 2
            # Use median as pivot element
            return KdNode(point=d[mid],
                          left=CreateKdTree(d[:mid], depth + 1),
                          right=CreateKdTree(d[mid + 1:], depth + 1))

        self.root = CreateKdTree(data)

    def query(self, point, k=1):
        '''
        Nearest Neighbor Query for KdTree
        '''

        def nearest_neighbor_query(node, point, depth=0, best=None):
            '''
            Search the nearest neighbor node
            '''
            if node is None:
                return best
            axis = depth % len(point)
            # Search the left subtree
            if best is None or node.point[axis] >= point[axis]:
                best = nearest_neighbor_query(node.left, point, depth + 1, best)
            # Search the right subtree
            if best is None or node.point[axis] < point[axis]:
                best = nearest_neighbor_query(node.right, point, depth + 1, best)
            # Update the best point
            if best is None or self.distance(node.point, point) < self.distance(best, point):
                best = node.point
            return best

        best = nearest_neighbor_query(self.root, point)
        return best

    def range(self, low, high):
        '''
        Range Query for KdTree
        '''

        def range_query(node, low, high, depth=0):
            '''
            Search all points in range
            '''
            if node is None:
                return []
            axis = depth % len(low)
            # Search the left subtree
            if low[axis] <= node.point[axis]:
                left_points = range_query(node.left, low, high, depth + 1)
            # Search the right subtree
            if high[axis] >= node.point[axis]:
                right_points = range_query(node.right, low, high, depth + 1)
            # If this node's point is in the range
            if self.in_range(node.point, low, high):
                mid_point = [node.point]
            else:
                mid_point = []
            return left_points + mid_point + right_points

        points = range_query(self.root, low, high)
        return points

    def insert(self, point):
        '''
        Insert a point in KdTree
        '''

        def insert_point(node, point, depth=0):
            '''
            Insert a point in KdTree
            '''
            if node is None:
                return KdNode(point=point)
            axis = depth % len(point)
            if point[axis] < node.point[axis]:
                node.left = insert_point(node.left, point, depth + 1)
            else:
                node.right = insert_point(node.right, point, depth + 1)
            return node

        self.root = insert_point(self.root, point)
        return

    # Compute the Euclidean distance between two points
    def distance(self, a, b):
        '''
        Compute the Euclidean distance between two points
        '''
        if len(a) != len(b):
            raise ValueError('The points have different dimensions.')
        dist = 0
        for i in range(len(a)):
            dist += (a[i] - b[i]) ** 2
        dist = dist ** 0.5
        return dist

    # Check if the point is in the given range
    def in_range(self, point, low, high):
        '''
        Check if the point is in the given range
        '''
        if len(point) != len(low) or len(point) != len(high):
            raise ValueError('The points have different dimensions.')
        for i in range(len(point)):
            if point[i] < low[i] or point[i] > high[i]:
                return False
        return True