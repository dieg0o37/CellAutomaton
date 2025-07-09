# Rules Formatting
- State = "Dead" or "Alive"
- Operator = "=", "!="
- Int = Number of alive neighbors

```
    # Conditions for a cell to live based on their current state and the number of alive neighbors
 if <State> <Operator> <Int>
 if <State> <Operator> <Int>
    ....
    # as many as you want
```
## Obs
- The rules are applied in the order they are defined.
- Leave the rules entry empty to play Conways Game of Life.
