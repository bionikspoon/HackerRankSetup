![HackerRank]

#Sherlock and Queries

[HackerRank \ Algorithms \ Summations and Algebra \ Sherlock and Queries](https://www.hackerrank.com/challenges/sherlock-and-queries)

Help Sherlock in answering Queries

##Problem Statement

Watson gives Sherlock an array ![$A$] of ![$N$] elements and two arrays ![$B$] and ![$C$], of ![$M$] elements each. Then he asks Sherlock to perform the following program:

    for i = 1 to M do
        for j = 1 to N do
            if j % B[i] == 0 then
                A[j] = A[j] * C[i]
            endif
        end do
    end do

This code needs to be optimized. Can you help Sherlock and tell him the resulting array ![$A$]? You should print all the array elements modulo ![$(10^9 + 7)$].

###Input Format

The first line contains two integer, ![$N$] and ![$M$]. The next line contains ![$N$] integers, the elements of array ![$A$]. The last two lines contain ![$M$] integers each, the elements of array ![$B$] and ![$C$], respectively.

###Output Format

Print ![$N$] space-separated integers, the elements of array ![$A$] after performing the program modulo ![$(10^9 + 7)$].

###Constraints

![$1 le N, M le 10^5$]

![$1 le Bi le N$]

![$1 le Ai, Ci le 10^5$]

###Sample Input

    4 3
    1 2 3 4
    1 2 3
    13 29 71

###Sample Output

    13 754 2769 1508

[HackerRank]:https://www.hackerrank.com/assets/brand/typemark_60x200.png
[$A$]:../assets/53d147e7f3fe6e47ee05b88b166bd3f6.png
[$N$]:../assets/f9c4988898e7f532b9f826a75014ed3c.png
[$M$]:../assets/fb97d38bcc19230b0acd442e17db879c.png
[$1 le N, M le 10^5$]:../assets/404294123ec13c62c8a0b390d4e8f6ee.png
[$C$]:../assets/9b325b9e31e85137d1de765f43c0f8bc.png
[$B$]:../assets/61e84f854bc6258d4108d08d4c4a0852.png
[$1 le Ai, Ci le 10^5$]:../assets/d133006232caf463e513a0ef1f36103c.png
[$1 le Bi le N$]:../assets/ef9ba375db3112e1c88aa798dd3522c4.png
[$(10^9 + 7)$]:../assets/c4e61dbf8b36a31aa53c4e418152f3d2.png