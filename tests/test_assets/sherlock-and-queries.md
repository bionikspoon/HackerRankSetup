![HackerRank]
#Sherlock and Queries
[HackerRank \ Algorithms \ Implementation \ Sherlock and Queries](https://www.hackerrank.com/challenges/sherlock-and-queries)
Help Sherlock in answering Queries

##Problem Statement
Watson gives to Sherlock an array: $A_1, A_2, \cdots, A_N$. He also gives to Sherlock two other arrays: $B_1, B_2, \cdots, B_M$ and $C_1, C_2, \cdots, C_M$.
Then Watson asks Sherlock to perform the following program:

    for i = 1 to M do
        for j = 1 to N do
            if j % B[i] == 0 then
                A[j] = A[j] * C[i]
            endif
        end do
    end do

This code needs to be optimised. Can you help Sherlock and tell him the resulting array $A$? You should print all the array elements modulo $(10^9 + 7)$.

**Input Format**
The first line contains two integer numbers $N$ and $M$. The next line contains $N$ integers, the elements of array $A$. The next two lines contains $M$ integers each, the elements of array $B$ and $C$.

**Output Format**
Print $N$ integers, the elements of array $A$ after performing the program modulo $(10^9 + 7)$.

**Constraints**
$1 \le N, M \le 10^5$
$1 \le B[i] \le N$
$1 \le A[i], C[i] \le 10^5$

**Sample Input**

    4 3
    1 2 3 4
    1 2 3
    13 29 71

**Sample Output**

    13 754 2769 1508

[HackerRank]:https://www.hackerrank.com/assets/brand/typemark_60x200.png