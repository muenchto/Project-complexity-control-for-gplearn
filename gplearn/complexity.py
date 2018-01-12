import numpy as np

def complexity(xdata, ydata):
    print("######### start complexity measurement ###############")
    print("xdata: \n",xdata)
    print("ydata", ydata)

    #error checking
    nrowsx = xdata.shape[0]
    nrowsy = ydata.shape[0]
    if nrowsx != nrowsy:
        raise ValueError("COMPLEXITY: The number of rows must be the same in both matrices.")
    else:
        if nrowsx<2:
            raise ValueError("COMPLEXITY: The number of rows in each matrix must be at least 2.")

    # number of dimensions of input data:
    ndims = xdata.shape[1]
    #print("ndims", ndims)
    # number of points in each dimension:
    npoints = nrowsx

    # initialize vector of complexity values (one value per dimension):
    complexityvalues = np.zeros(ndims)

    # sort the x values on each dimension (by ascending order):
    index = xdata[:, 0].argsort()
    sortedxdata = xdata[index]

    #print("sortedxdata: ", sortedxdata)
    #print("index: ",  index)
    # sort the y values (using the ndims different orders):
    ydata = np.kron(np.ones((1, ndims)), ydata)
    sortedydata = ydata[index]
    print("sortedydata", sortedydata)

    # calculate complexity values for each dimension separately:
    for d in range(0, ndims):
        # because the same x value may have different y values (when ndims>1)
        # we use the median of the y values. to do this:

        # find the indexes with repeated x values:
        x = sortedxdata[:, d]
        print("checking dimension ",d, "with data ",x)
        ux, i = np.unique(x, return_index=True)  # i returns the indexes of the unique values
        print("ux ", ux, "i ", i)
        ri = np.setdiff1d(range(0, npoints), i)  # ri returns the indexes of the repetitions
        # (when there is a repeated value, i contains the index of the *first*
        #  occurrence of the value, while ri contains the indexes of the n
        #  first occurrences of the value (n>=1)
        print("ri", ri)
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
            yfinal = np.zeros(len(y))
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
        xfinal1 = xfinal[0:len(xfinal) - 1]
        xfinal2 = xfinal[1:len(xfinal)]
        yfinal1 = yfinal[0:len(yfinal) - 1]
        yfinal2 = yfinal[1:len(yfinal)]
        xfinal0 = xfinal2 - xfinal1  # differences between consecutive x points
        #print("xfinal0 ",xfinal0)
        yfinal0 = yfinal2 - yfinal1  # differences between consecutive y points
        #print("yfinal0 ",yfinal0)
        slopes = yfinal0 / xfinal0
        #print("slopes", slopes)


        # absolute differences between consecutive slopes:
        slopes1 = slopes[0:len(slopes) - 1]
        slopes2 = slopes[1:len(slopes)]
        slopes0 = abs(slopes2 - slopes1)
        #print("slopes0", slopes0)

        # complexity of this dimension is the sum of the differences:
        cvalue = sum(slopes0)
        complexityvalues[d] = cvalue
        print("complexity in dimension", d, ": ", complexityvalues)


    # - Now we use whatever we want from this vector
    # - I suggest using (and comparing results with) average and maximum values


# sum elements in vector!


#X_test = np.array([
#    [5],
#    [2],
#    [9],
#    [0],
#    [7],
#    [7],
#])
#y_test = np.array([
#    [1],
#    [5],
#    [7],
#    [8],
#    [4],
#    [0],
#     ])
#complexityarray = complexity(X_test, y_test)

X_test = np.array([
[0],
    [0],
    [1],
    [2],
[2],
])
y_test = np.array([
[0],
    [0],
    [1],
    [0],
[0]
])
complexityarray = complexity(X_test, y_test)



# X_test = np.array([
#     [0],
#     [1],
#     [2],
# [3],
# [4],
# ])
# y_test = np.array([
#     [0],
#     [1],
#     [2],
#     [1],
#     [2],
# ])
# complexityarray = complexity(X_test, y_test)