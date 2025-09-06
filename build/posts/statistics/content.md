Bayes' Theorem
==============

The foundation of Bayesian statistics is Bayes' theorem:

$$P(A|B) = \frac{P(B|A)P(A)}{P(B)}$$

In the context of machine learning, this becomes:

$$P(\theta|D) = \frac{P(D|\theta)P(\theta)}{P(D)}$$

where $\theta$ represents model parameters and $D$ represents data.

Prior, Likelihood, and Posterior
================================

-   **Prior** $P(\theta)$: Our beliefs about parameters before seeing
    data

-   **Likelihood** $P(D|\theta)$: Probability of data given parameters

-   **Posterior** $P(\theta|D)$: Updated beliefs after seeing data

Conjugate Priors
================

A prior is **conjugate** to a likelihood if the posterior belongs to the
same family as the prior.

Beta-Binomial Example
---------------------

For a binomial likelihood with Beta prior:

$$\begin{aligned}
\text{Likelihood: } &P(x|n,p) = \binom{n}{x} p^x (1-p)^{n-x} \\
\text{Prior: } &P(p) = \text{Beta}(\alpha, \beta) \\
\text{Posterior: } &P(p|x) = \text{Beta}(\alpha + x, \beta + n - x)\end{aligned}$$

Maximum A Posteriori (MAP)
==========================

The MAP estimate maximizes the posterior:

$$\hat{\theta}_{MAP} = \arg\max_{\theta} P(\theta|D) = \arg\max_{\theta} P(D|\theta)P(\theta)$$

Regularization
==============

Bayesian methods naturally provide regularization. For linear regression
with Gaussian priors:

$$P(\mathbf{w}|D) \propto \exp\left(-\frac{1}{2\sigma^2}\|y - X\mathbf{w}\|^2 - \frac{\lambda}{2}\|\mathbf{w}\|^2\right)$$

This is equivalent to L2 regularization (Ridge regression).

Markov Chain Monte Carlo
========================

For complex posteriors, we use MCMC methods like the Metropolis-Hastings
algorithm:

1.  Sample $\theta'$ from proposal distribution
    $q(\theta'|\theta^{(t)})$

2.  Accept with probability
    $\min\left(1, \frac{P(\theta'|D)q(\theta^{(t)}|\theta')}{P(\theta^{(t)}|D)q(\theta'|\theta^{(t)})}\right)$

3.  If accepted, set $\theta^{(t+1)} = \theta'$; otherwise,
    $\theta^{(t+1)} = \theta^{(t)}$

Applications in ML
==================

Bayesian methods are used in:

-   Gaussian Process regression

-   Bayesian neural networks

-   Latent Dirichlet Allocation (LDA)

-   Variational inference

-   Uncertainty quantification

Conclusion
==========

Bayesian statistics provides a principled framework for incorporating
uncertainty and prior knowledge into machine learning models.
