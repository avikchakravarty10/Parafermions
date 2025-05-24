import pandas as pd
import itertools
k = 11
print(f"level k: {k}")
def cw(a,b): # This function defines the conformal weight
    if a >= b:
        return a-(1/k)*(a*a+b*b-a*b)
    else:
        return b-(1/k)*(a*a+b*b-a*b)

def deg(a1,a2,a3,a4,b1,b2,b3,b4): 
    # This function defines the degree for the divisor D(K(sl_3,k), \bigotimes_{j=1}^4 M^{ 0, 0 - ( a_j , b_j ) }  )
    p1,p2 = (a1+a2)%k, (b1+b2)%k
    q1,q2 = (a1+a3)%k, (b1+b3)%k
    r1,r2 = (a1+a4)%k, (b1+b4)%k
    return int(cw(a1,b1)+cw(a2,b2)+cw(a3,b3)+cw(a4,b4)-cw(p1,p2)-cw(q1,q2)-cw(r1,r2))
    
 

def check(k):
    #This  function gives a model for what we wish to compute. 
    # We gather all possible tuples of (a_1,b_1,a_2,b_2,a_3,b_3,a_4,b_4) and 
    # then execute the degree function for each of them and finally output the minimum degree.
    # We infact break this function into CASES below and use those codes instead.
    # CASE0: a_j >= b_j for all 1\leq j\leq 4. 
    # CASE1: a_1  > b_1, a_2  < b_2, a_3 = b_3, a_4  = b_4.
    # CASE2: a_1 >= b_1, a_2  > b_2, a_3 < b_3, a_4 <= b_4.
    # CASE3: a_1 >= b_1, a_2 >= b_2, a_3 > b_3, a_4  < b_4.
    # In all four cases, we assume that a_1 + a_2 + a_3 + a_4 > k and  b_1 + b_2 + b_3 + b_4 > k
    # since the a_1 + a_2 + a_3 + a_4 = k = b_1 + b_2 + b_3 + b_4 is already taken care of in the paper.
    

    # Generate all possible 8-tuples where each entry is between 0 and k-1
    all_tuples = list(itertools.product(range(k), repeat=8))
    # Create a DataFrame for easier manipulation
    df = pd.DataFrame(all_tuples, columns=["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"])
    # Calculate the sums for the first and second groups
    df["sum1"] = df["a1"] + df["a2"] + df["a3"] + df["a4"]
    df["sum2"] = df["b1"] + df["b2"] + df["b3"] + df["b4"]
 # Compute the `deg` column using row-wise operations
    df["deg"] = df.apply(
        lambda row: deg(
            row["a1"], row["a2"], row["a3"], row["a4"], 
            row["b1"], row["b2"], row["b3"], row["b4"]
        ), axis=1
    )

    # Filter tuples that satisfy the conditions
    df = df[(df["a1"]+df["b1"]>0)&(df["a2"]+df["b2"]>0)&(df["a3"]+df["b3"]>0)&(df["a4"]+df["b4"]>0)]
    # The above fiter makes sure that none of the modules are trivial. For example, if a1+b1=0, then a1=b1=0 and 
    # hence M^{0,0-(a1,b1)}= K(sl_3,k) is the trivial module. 
    df = df[((df["sum1"])%k == 0) & ((df["sum2"]%k) == 0)]
    # The above filter makes sure we do not have all four modules have the first or second idex zero, 
    # since then the comutation reduces to that for modules in K(sl_2,k).

    # The following returns the minimum degree value
    min_value = df['deg'].min()

   # Return the filtered tuples and their count
    return df, len(df),min_value


def CASE0(k):

    # Generate all possible 8-tuples where each entry is between 0 and k-1
    all_tuples = list(itertools.product(range(k), repeat=8))
    # Create a DataFrame for easier manipulation
    df = pd.DataFrame(all_tuples, columns=["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"])
    # Calculate the sums for the first and second groups
    df["sum1"] = df["a1"] + df["a2"] + df["a3"] + df["a4"]
    df["sum2"] = df["b1"] + df["b2"] + df["b3"] + df["b4"]

    # Filter tuples that satisfy the conditions
    df = df[(df["a1"]+df["b1"]>0)&(df["a2"]+df["b2"]>0)&(df["a3"]+df["b3"]>0)&(df["a4"]+df["b4"]>0)]
    df = df[((df["sum1"])%k == 0) & ((df["sum2"]%k) == 0)]
    # df = df[(df["a1"]!= df["b1"])|(df["a2"] != df["b2"])|(df["a3"]!= df["b3"])|(df["a4"] != df["b4"])]

    df = df[(df["sum1"] > k) | (df["sum2"] > k)]
    df = df[(df["a1"] >= df["b1"])&(df["a2"] >= df["b2"])&(df["a3"] >= df["b3"])&(df["a4"] >= df["b4"])]

 # Compute the `deg` column using row-wise operations
    df["deg"] = df.apply(
        lambda row: deg(
            row["a1"], row["a2"], row["a3"], row["a4"], 
            row["b1"], row["b2"], row["b3"], row["b4"]
        ), axis=1
    )
    min_value = df['deg'].min()
   # Return the filtered tuples and their count
    return df, len(df), min_value



def CASE1(k):

    # Generate all possible 8-tuples where each entry is between 0 and k-1
    all_tuples = list(itertools.product(range(k), repeat=8))
    # Create a DataFrame for easier manipulation
    df = pd.DataFrame(all_tuples, columns=["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"])
    # Calculate the sums for the first and second groups
    df["sum1"] = df["a1"] + df["a2"] + df["a3"] + df["a4"]
    df["sum2"] = df["b1"] + df["b2"] + df["b3"] + df["b4"]

    # Filter tuples that satisfy the conditions
    df = df[(df["a1"]+df["b1"]>0)&(df["a2"]+df["b2"]>0)&(df["a3"]+df["b3"]>0)&(df["a4"]+df["b4"]>0)]
    df = df[((df["sum1"])%k == 0) & ((df["sum2"]%k) == 0)]
    df = df[(df["a1"]!= df["b1"])|(df["a2"] != df["b2"])|(df["a3"]!= df["b3"])|(df["a4"] != df["b4"])]

    df = df[(df["sum1"] > k) | (df["sum2"] > k)]
    df = df[(df["a1"]>df["b1"])&(df["a2"]<df["b2"])&(df["a3"]== df["b3"])&(df["a4"] == df["b4"])]

 # Compute the `deg` column using row-wise operations
    df["deg"] = df.apply(
        lambda row: deg(
            row["a1"], row["a2"], row["a3"], row["a4"], 
            row["b1"], row["b2"], row["b3"], row["b4"]
        ), axis=1
    )
    min_value = df['deg'].min()
   # Return the filtered tuples and their count
    return df, len(df), min_value




def CASE2(k):
    # Generate all possible 8-tuples where each entry is between 0 and k-1
    all_tuples = list(itertools.product(range(k), repeat=8))
    # Create a DataFrame for easier manipulation
    df = pd.DataFrame(all_tuples, columns=["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"])
    # Calculate the sums for the first and second groups
    df["sum1"] = df["a1"] + df["a2"] + df["a3"] + df["a4"]
    df["sum2"] = df["b1"] + df["b2"] + df["b3"] + df["b4"]

    # Filter tuples that satisfy the conditions
    df = df[(df["a1"]+df["b1"]>0)&(df["a2"]+df["b2"]>0)&(df["a3"]+df["b3"]>0)&(df["a4"]+df["b4"]>0)]
    df = df[((df["sum1"])%k == 0) & ((df["sum2"]%k) == 0)]
    df = df[(df["a1"]!= df["b1"])|(df["a2"] != df["b2"])|(df["a3"]!= df["b3"])|(df["a4"] != df["b4"])]

    df = df[(df["sum1"] > k) | (df["sum2"] > k)]
    df = df[(df["a1"]>= df["b1"])&(df["a2"]>df["b2"])&(df["a3"]< df["b3"])&(df["a4"] <= df["b4"])]

 # Compute the `deg` column using row-wise operations
    df["deg"] = df.apply(
        lambda row: deg(
            row["a1"], row["a2"], row["a3"], row["a4"], 
            row["b1"], row["b2"], row["b3"], row["b4"]
        ), axis=1
    )
    min_value = df['deg'].min()
   # Return the filtered tuples and their count
    return df, len(df),min_value


def CASE3(k):
    # Generate all possible 8-tuples where each entry is between 0 and k-1
    all_tuples = list(itertools.product(range(k), repeat=8))
    # Create a DataFrame for easier manipulation
    df = pd.DataFrame(all_tuples, columns=["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"])
    # Calculate the sums for the first and second groups
    df["sum1"] = df["a1"] + df["a2"] + df["a3"] + df["a4"]
    df["sum2"] = df["b1"] + df["b2"] + df["b3"] + df["b4"]

    # Filter tuples that satisfy the conditions
    df = df[(df["a1"]+df["b1"]>0)&(df["a2"]+df["b2"]>0)&(df["a3"]+df["b3"]>0)&(df["a4"]+df["b4"]>0)]
    df = df[((df["sum1"])%k == 0) & ((df["sum2"]%k) == 0)]

    df = df[(df["sum1"] > k) | (df["sum2"] > k)]
    df = df[(df["a1"]!= df["b1"])|(df["a2"] != df["b2"])|(df["a3"]!= df["b3"])|(df["a4"] != df["b4"])]

    df = df[(df["a1"]>= df["b1"])&(df["a2"]>=df["b2"])&(df["a3"]> df["b3"])&(df["a4"] < df["b4"])]

 # Compute the `deg` column using row-wise operations
    df["deg"] = df.apply(
        lambda row: deg(
            row["a1"], row["a2"], row["a3"], row["a4"], 
            row["b1"], row["b2"], row["b3"], row["b4"]
        ), axis=1
    )
    min_value = df['deg'].min()
   # Return the filtered tuples and their count
    return df, len(df),min_value




# COMPUTATION FOR CASE0
result, count,min_val = CASE0(k)
# Display the result
print(f"Number of valid tuples satisfying CASE0: {count}")
print(f"Minimal value of degree: {min_val}")
# print("Table of the degree for all cases considered:")
# print(result)

# # COMPUTATION FOR CASE1
# result, count,min_val = CASE1(k)
# # Display the result
# print(f"Number of valid tuples satisfying CASE1: {count}")
# print(f"Minimal value of degree: {min_val}")
# # COMPUTATION FOR CASE2
# result, count,min_val = CASE2(k)
# # Display the result
# print(f"Number of valid tuples satisfying CASE2: {count}")
# print(f"Minimal value of degree: {min_val}")
# # COMPUTATION FOR CASE3
# result, count,min_val = CASE3(k)
# # Display the result
# print(f"Number of valid tuples satisfying CASE3: {count}")
# print(f"Minimal value of degree: {min_val}")