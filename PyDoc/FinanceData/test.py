import numpy as np

def matGenerate_Sort(rows=1000, cols=50, range=[0, 3]):
    output = np.random.randint(range[0], range[1], (rows, cols))
    output = output[np.lexsort((-output[:,1], output[:,0]))]
    return output

def sortbycols(data, cols, descending):
    if type(cols) != list:
        if descending:
            data = data[np.lexsort((data[:, cols], data[:, cols]))]
        else:
            data = data[np.lexsort((-data[:, cols], -data[:, cols]))]
    elif type(descending) != list:
        cols.reverse()
        if descending:
            data = data[np.lexsort(data[:, cols].T, axis=-1)]
        else:
            data = data[np.lexsort(-data[:, cols].T, axis=-1)]
    else:
        cols.reverse()
        descending.reverse()
        order = data[:, cols].T
        for col in range(len(cols)):
            if not descending[col]:
                order[col] = -order[col]
        data = data[np.lexsort(order, axis=-1)]
    return data

matone = matGenerate_Sort(10, 10)
mattwo = np.random.randint(0, 3, (10, 5))
print(sortbycols(mattwo, [0, 1, 2], [False, True, True]))