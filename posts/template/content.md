Introduction
============

Inline math like $a^2+b^2=c^2$ and display math:
$$\int_0^1 x^2\,dx = \frac{1}{3}.$$

A set $S$ is *countable* if it is finite or in bijection with
$\mathbb{N}$.

There is no bijection between $\mathbb{N}$ and $(0,1)$.

Sketch the diagonalization and you're done.

A figure and a table
====================

See .

  Col 1   Col 2   Col 3
  ------- ------- -------
  a       b       c

  : A neat table.

Code
====

``` {.haskell language="Haskell" caption="Reverse a list"}
rev :: [a] -> [a]
rev = foldl (flip (:)) []
```
