Definition
==========

Let $A$ be an $n \times n$ matrix. A non-zero vector $\mathbf{v}$ is an
**eigenvector** of $A$ if:

$$A\mathbf{v} = \lambda\mathbf{v}$$

for some scalar $\lambda$, called the **eigenvalue**.

Characteristic Polynomial
=========================

The eigenvalues of $A$ are the roots of the characteristic polynomial:

$$p(\lambda) = \det(A - \lambda I) = 0$$

Example: 2×2 Matrix
===================

Consider the matrix: $$A = \begin{pmatrix}
3 & 1 \\
0 & 2
\end{pmatrix}$$

The characteristic polynomial is: $$\begin{aligned}
\det(A - \lambda I) &= \det\begin{pmatrix}
3-\lambda & 1 \\
0 & 2-\lambda
\end{pmatrix} \\
&= (3-\lambda)(2-\lambda) - 0 \cdot 1 \\
&= \lambda^2 - 5\lambda + 6 \\
&= (\lambda - 2)(\lambda - 3)\end{aligned}$$

So the eigenvalues are $\lambda_1 = 2$ and $\lambda_2 = 3$.

Eigenvectors
============

For $\lambda_1 = 2$: $$(A - 2I)\mathbf{v} = \begin{pmatrix}
1 & 1 \\
0 & 0
\end{pmatrix}\mathbf{v} = \mathbf{0}$$

This gives us $\mathbf{v}_1 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$.

For $\lambda_2 = 3$: $$(A - 3I)\mathbf{v} = \begin{pmatrix}
0 & 1 \\
0 & -1
\end{pmatrix}\mathbf{v} = \mathbf{0}$$

This gives us $\mathbf{v}_2 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$.

Diagonalization
===============

If $A$ has $n$ linearly independent eigenvectors, it can be diagonalized
as:

$$A = PDP^{-1}$$

where $P$ contains the eigenvectors and $D$ is a diagonal matrix of
eigenvalues.

Applications
============

Eigenvalues and eigenvectors are fundamental in:

-   Principal Component Analysis (PCA)

-   Quantum mechanics

-   Stability analysis of dynamical systems

-   Google's PageRank algorithm

-   Image compression

Conclusion
==========

Eigenvalues and eigenvectors provide deep insights into the structure
and behavior of linear transformations.
