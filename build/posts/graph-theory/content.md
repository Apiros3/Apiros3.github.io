Basic Definitions
=================

A **graph** $G = (V, E)$ consists of a set of vertices $V$ and a set of
edges $E$. If the edges are ordered pairs, the graph is *directed*;
otherwise, it's *undirected*.

Graph Properties
================

Degree
------

The **degree** of a vertex $v$ in an undirected graph is the number of
edges incident to $v$:

$$\deg(v) = |\{e \in E : v \in e\}|$$

Connectivity
------------

A graph is **connected** if there exists a path between any two
vertices. The **connectivity** $\kappa(G)$ is the minimum number of
vertices whose removal disconnects the graph.

Important Theorems
==================

Handshaking Lemma
-----------------

For any graph $G = (V, E)$:

$$\sum_{v \in V} \deg(v) = 2|E|$$

This implies that the sum of all vertex degrees equals twice the number
of edges.

Euler's Formula
---------------

For a connected planar graph with $V$ vertices, $E$ edges, and $F$
faces:

$$V - E + F = 2$$

Applications
============

Graph theory has numerous applications:

-   Social network analysis

-   Computer network topology

-   Transportation systems

-   Molecular structure analysis

-   Web page ranking algorithms

Algorithmic Considerations
==========================

Many graph problems are computationally challenging. For example:

-   **Hamiltonian Path**: NP-complete

-   **Graph Coloring**: NP-complete for $k \geq 3$

-   **Shortest Path**: Polynomial time (Dijkstra's algorithm)

Conclusion
==========

Graph theory provides powerful tools for modeling and analyzing complex
systems with discrete structures.
