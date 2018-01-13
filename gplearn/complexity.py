import numpy as np

def complexity(xdata, ydata):
    print("######### start complexity measurement ###############")
    print("xdata: \n",xdata)
    print("ydata: \n", ydata)

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

    # initialize vector of complexity values (one value per dimension):
    complexityvalues = np.zeros(ndims)

    # calculate complexity values for each dimension separately:
    for d in range(0, ndims):

        xdata_d = xdata[:, d]
        #print("checking dimension ", d, "with data ", xdata_d)

        # sort the x values on each dimension (by ascending order), keeping the order index:
        index = xdata_d.argsort()
        sortedxdata = xdata_d[index]

        #print("sortedxdata: ", sortedxdata)
        #print("index: ",  index)

        # sort the y values (using the the index):
        sortedydata = ydata[index]
        #print("sortedydata", sortedydata)


        # because the same x value may have different y values (when ndims>1)
        # we use the median of the y values. to do this:

        # find the indexes with repeated x values and create unique values array:
        xfinal, indeces = np.unique(sortedxdata, return_index=True)  # indeces returns the indexes of the unique values
        #print("xfinal ", xfinal, "indeces ", indeces)
        # (when there is a repeated value, indeces contains the index of the *first*
        #  occurrence of the value

        if len(xfinal) != len(sortedxdata):  # if there are no repetitions skip this entire part
            yfinal = np.zeros(len(xfinal))
            for i in range(0,len(indeces)):

                # special case: repetition at the end of the sortedxdata
                if i == len(indeces)-1:
                    next_index = len(sortedydata)
                else:
                    next_index = indeces[i+1]

               # from x_i to x_i+1 there are repetions
                yfinal[i] = np.median(sortedydata[indeces[i]:next_index])
                #print("yfinal[",i,"]:", yfinal[i])

        else:
            yfinal = sortedydata[:, 0]

        #print("yfinal", yfinal)

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
        print("complexity in dimension", d, ": ", complexityvalues[d])


    # - Now we use whatever we want from this vector
    # - I suggest using (and comparing results with) average and maximum values


# sum elements in vector!


X_test = np.array([
    [5],
    [2],
    [9],
    [0],
    [7],
    [7],
])
y_test = np.array([
    [1],
    [5],
    [7],
    [8],
    [4],
    [0],
     ])
complexityarray = complexity(X_test, y_test)

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



X_test = np.array([
    [0],
    [1],
    [2],
    [3],
    [4],
 ])
y_test = np.array([
    [0],
    [1],
    [2],
    [1],
    [2],
 ])
complexityarray = complexity(X_test, y_test)

X_test = np.array([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 4],
 ])
y_test = np.array([
    [0],
    [1],
    [2],
    [1],
    [2],
 ])
complexityarray = complexity(X_test, y_test)


X_test = np.array([
    [0, 5, 9],
    [1, 2, 1],
    [2, 8, 0],
 ])
y_test = np.array([
    [0],
    [1],
    [2],
 ])
complexityarray = complexity(X_test, y_test)