I didn't write any code for this. I just copied the numbers into Google Sheets on my smartphone and it gave me an autosum.

But I guess I could have done something like this:
```shell
awk '{sum += $0} END {print sum}' puzzle_input
```
