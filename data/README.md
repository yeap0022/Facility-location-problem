# Data Format:

> |N| |M|  
> s_0 cap_0 x_0 y_0  
> s_1 cap_1 x_1 y_1  
> ...  
> s_|N|-1 cap_|N|-1 x_|N|-1 y_|N|-1
> d_|N| x_|N| y_|N|  
> d_|N|+1 x_|N|+1 y_|N|+1  
> ...  
> d_|N|+|M|-1 x_|N|+|M|-1 y_|N|+|M|-1  

N = number of facilities  
M = number of customers  
s = cost of facility  
cap = capacity of facility  
d = demand of customer  
(x, y) = coordinate of facility and customer

# Example:

In problem_1.txt, the data below means that there are 3 facilities available to serve 4 customers.  
To open each facility, it costs about $100. The first two facilities have capacity of 100, whereas the third has capacity of 500.  
The four customers have demand of 50, 50, 75 and 75, respectively.  
The location of facilities and customers is indicated in the last two inputs on each row.   
> 3 4  
> 100 100 1065.0 1065.0  
> 100 100 1062.0 1062.0  
> 100 500 0.0 0.0  
> 50 1397.0 1397.0  
> 50 1398.0 1398.0  
> 75 1399.0 1399.0  
> 75 586.0 586.0  
