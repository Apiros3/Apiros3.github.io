Introduction
============

The Fundamental Theorem of Calculus connects differentiation and
integration, showing that these two operations are essentially inverse
processes.

The First Fundamental Theorem
=============================

If $f$ is continuous on $[a,b]$ and $F$ is defined by:

$$F(x) = \int_a^x f(t) \, dt$$

then $F$ is differentiable on $(a,b)$ and:

$$F'(x) = f(x)$$

The Second Fundamental Theorem
==============================

If $f$ is continuous on $[a,b]$ and $F$ is any antiderivative of $f$,
then:

$$\int_a^b f(x) \, dx = F(b) - F(a)$$

Examples
========

Example 1
---------

Find the derivative of: $$g(x) = \int_0^x \sin(t^2) \, dt$$

By the First Fundamental Theorem: $$g'(x) = \sin(x^2)$$

Example 2
---------

Evaluate: $$\int_1^4 (2x + 3) \, dx$$

An antiderivative is $F(x) = x^2 + 3x$, so:
$$\int_1^4 (2x + 3) \, dx = F(4) - F(1) = (16 + 12) - (1 + 3) = 24$$

Applications
============

The Fundamental Theorem has many applications:

-   Computing definite integrals

-   Solving differential equations

-   Physics problems involving rates of change

-   Economics and optimization

Proof Sketch
============

The proof relies on the Mean Value Theorem and the definition of the
derivative. The key insight is that:

$$\frac{F(x+h) - F(x)}{h} = \frac{1}{h} \int_x^{x+h} f(t) \, dt$$

As $h \to 0$, this approaches $f(x)$ by continuity.

Conclusion
==========

The Fundamental Theorem of Calculus is one of the most important results
in mathematics, providing the foundation for much of modern analysis and
its applications.
