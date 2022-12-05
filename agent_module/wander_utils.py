def add_lists(list1, list2):
    """Add the contents of two lists together, element-wise.

    Parameters
    ----------
    list1 : List
        The first list to be added.
    list2 : List
        The second list to be added.
        
    Returns
    -------
    List
        A list containing the element-wise addition of the two lists.
        An error will occur if the two lists are of types that cannot be added together.
    """
    
    output = []
    for num1, num2 in zip(list1, list2):
        output.append(num1 + num2)
    return output


def check_bounds(position, size):
    """Check if a position is within bounds of length size.

    Parameters
    ----------
    position : List of int or float
        The coordinates of the position to be evaluated.
    size : int or float
        The size of each dimension of the bounds to check.
        
    Returns
    -------
    Bool
        True if position is within bounds, False otherwise
    """
    
    for item in position:
        if item < 0 or item >= size:
            return False
    return True