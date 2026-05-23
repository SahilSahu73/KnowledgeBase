# Dynamic Programming
- Crucial to recognize if a problem can be approached using DP techniques.
This is especially relevant when the problem exhibits certain characteristics that
align with the strengths of DP.
- Common indicators of DP:
    - Problem asking for count the total number of ways.
    - Given multiple ways of performing a task, it is asked which way will yield the
    minimum or maximum output.

If either of the above 2 points are implied, then recursion can be applied to attempt solve it.
Once recursive solution is obtained, it can be converted into a dynamic programming approach.

# How to write recurrence relation
Once the problem has been identified, then:
- try to represent the problem in terms of indexes.
- try all possible choices/ways at every index according to the problem statement.
- If question states "count all the ways", then the sum of all choices/ways should be returned.
If the question asks to find "the maximum/minimum", then the choice/way with the max/min output
should be returned.

In recursion, top-down approach is followed

