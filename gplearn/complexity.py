import numpy as np

def complexity(xdata, ydata):
    #error checking
    nrowsx = xdata.size
    nrowsy = ydata.size
    if nrowsx != nrowsy:
        raise ValueError("COMPLEXITY: The number of rows must be the same in both matrices.")
    else:
        if nrowsx<2:
            raise ValueError("COMPLEXITY: The number of rows in each matrix must be at least 2.")

    # number of dimensions of input data:
    ndims = xdata.shape[1]
    # number of points in each dimension:
    npoints = nrowsx

    # initialize vector of complexity values (one value per dimension):
    complexityvalues = np.zeros(ndims)

    # sort the x values on each dimension (by ascending order):
    print(xdata)
    sortedxdata, index = xdata.argsort(axis=0)
    # sort the y values (using the ndims different orders):
    ydata = np.kron(np.ones((1, ndims)), ydata)
    print(index)
    print(ydata)
    sortedydata = ydata[index]

    # calculate complexity values for each dimension separately:
    for d in range(0, ndims-1):
        # because the same x value may have different y values (when ndims>1)
        # we use the median of the y values. to do this:

        # find the indexes with repeated x values:
        x = sortedxdata[:, d]
        ux, i = np.unique(x)  # i returns the indexes of the unique values
        ri = np.setdiff1d(range(0, npoints-1), i)  # ri returns the indexes of the repetitions
        # (when there is a repeated value, i contains the index of the *last*
        #  occurrence of the value, while ri contains the indexes of the n
        #  first occurrences of the value (n>=1)

        if ri:  # if there are no repetitions skip this entire part

            # count occurrences, to help identify the "groups" of repetitions:
            from collections import Counter
            c = [Counter(x).values()]
            # ans, c = countfind(x,ux)  # how many times each value appears
            # c = c(c != 1)  # we are only interested if it appears more than once
            c = [c[j] for j in range(len(c)) if c[j] != 1]
            # (c now contains the number of occurrences of each repeated value)
            # (c and ri can now be used to transform the y vector to replace
            #  repetitions with median values)

            # build final y vector with medians where necessary:
            y = sortedydata[:, d]
            yfinal = []
            endlastrep = 0  # index on the y vector, end of last repetition
            endthisrep = 0
            for i in range(0, len(c)-1):
                beginthisrep = ri[sum(c[1:i - 1])-(i - 1) + 1]
                yfinal = [[yfinal],[y[endlastrep + 1: beginthisrep - 1]]]
                # (appends to yfinal everything until this repetition)
                endthisrep = beginthisrep + c[i] - 1
                # (take note where this repitition ends)
                yfinal[len(yfinal) + 1 , 1] = np.median(y[beginthisrep:endthisrep])
                # (appends to yfinal the median value)
                # (do NOT remove the ,1 or you may get a row instead of column)
                endlastrep = endthisrep

            yfinal = [[yfinal],[y[endthisrep + 1: len(y)]]]
            # (appends to yfinal everything after the final repetition)

            # also build final x vector:
            xfinal = ux  # no secret here, just take the unique values
        else:
            yfinal = sortedydata[:, d]
            xfinal = x

        # if ~isempty(ri)

        # finally, calculate slopes using xfinal and yfinal:
        xfinal1 = xfinal[1:len(xfinal) - 1]
        xfinal2 = xfinal[2:len(xfinal)]
        yfinal1 = yfinal[1:len(xfinal) - 1]
        yfinal2 = yfinal[2:len(xfinal)]
        xfinal0 = xfinal2 - xfinal1  # differences between consecutive x points
        yfinal0 = yfinal2 - yfinal1  # differences between consecutive y points
        slopes = yfinal0 / xfinal0

        # absolute differences between consecutive slopes:
        slopes1 = slopes[1:len(slopes) - 1]
        slopes2 = slopes[2:len(slopes)]
        slopes0 = abs(slopes2 - slopes1)

        # complexity of this dimension is the sum of the differences:
        cvalue = sum(slopes0)
        complexityvalues[d] = cvalue


    # - Now we use whatever we want from this vector
    # - I suggest using (and comparing results with) average and maximum values



X_test = np.array([[0], [1]])
y_test = np.array([1, 2])
complexityarray = complexity(X_test, y_test)