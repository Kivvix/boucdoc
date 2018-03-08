---
title: Modélisation pour la bio-santé 1
author: Josselin Massot
...

# Étude de la solution exacte

Nous allons étuider le problème suivant :

$$
  \left \{ \begin{array}{r c l}
    \mathrm{d}X_t &=& ((AX_t + r(t))\,\mathrm{d}t + \Sigma\,\mathrm{d}W_t \quad ,\, t\in [0,T] \\
    X_0 &=& (0,0)^{\mathsf{T}}
  \end{array} \right .
$$

## Existence et unicité de la solution

Il y a quelque chose qui s'appelle la flemme de regarder son cours pour justifier proprement cela, on va donc juste considérer que puisqu'on nous demande d'étuider ce problème celui doit avoir une solution et qui est de préférence unique.

## Solution particulière

Soit $Y$ le processus définit par :

$$
  Y_t = \int_0^t e^{-As} r(s)\,\mathrm{d}s + \int_0^t e^{-As} \Sigma\,\mathrm{d}W_s\quad,\, t\in [0,T]
$$

Soit $X_t = e^{At}Y_t$. Notons $u:(t,x)\mapsto e^{At}x$, on a alors $X_t = u(t,Y_t)$, la formule d'Itō donne alors :

$$
  \mathrm{d}X_t = \frac{\partial u}{\partial t}(t,Y_t)\mathrm{d}t + \frac{\partial u}{\partial x}(t,Y_t)\mathrm{d}Y_t + \frac{1}{2}\frac{\partial^2 u}{\partial x^2}(t,Y_t)(\mathrm{d}Y_t)^2
$$

Avec :

* $\frac{\partial u}{\partial t}(t,Y_t) = Ae^{At}Y_t$
* $\frac{\partial u}{\partial x}(t,Y_t) = e^{At}$
* $\frac{\partial^2 u}{\partial x^2}(t,Y_t) = 0$

d'où :

$$
  \mathrm{d}X_t = Ae^{At}Y_t\mathrm{d}t + e^{At}\mathrm{d}Y_t + 0
$$

or $\mathrm{d}Y_t = e^{-At}r(t)\mathrm{d}t + e^{-At}\Sigma \mathrm{d}W_t$

Donc :

$$
  \begin{array}{r c l}
    \mathrm{d}X_t &=& AX_t\mathrm{d}t + e^{At}\left( e^{-At}r(t)\mathrm{d}t + e^{-At}\Sigma \mathrm{d}W_t \right)\\
                  &=& AX_t \mathrm{d}t + r(t)\mathrm{d}t + \Sigma\mathrm{d}W_t\\
                  &=& \left( AX_t + r(t)\right)\mathrm{d}t + \Sigma\mathrm{d}W_t
  \end{array}
$$

Donc $X_t$ est bien solution du problème.

## Étude de la loi de la solution

### Calcul de l'espérance

On peut réécrire $X_t$ de la façon suivante :

$$
  X_t = \int_0^t e^{A(t-s)}r(s)\,\mathrm{d}s + \int_0^t e^{A(t-s)}\Sigma\,\mathrm{d}W_s
$$

Calculons l'espérance. La linéarité de l'espérance nous donne :

$$
  \mathbb{E}(X_t) = \mathbb{E}(\int_0^t e^{A(t-s)}r(s)\,\mathrm{d}s) + \mathbb{E}(\int_0^t e^{A(t-s)}\Sigma\,\mathrm{d}W_s)
$$

Le premier terme est purement déterministe est est donc une simple intégrale sur $[0,t]$. Dans le second terme, on peut faire *rentrer l'intégrale* grâce au théorème de Fubini, puis sortir toute la partie déterministe de l'espérance. Ceci nous donne :

$$
  \mathbb{E}(X_t) = \int_0^t e^{A(t-s)}r(s)\,\mathrm{d}s + \int_0^t e^{A(t-s)}\Sigma \mathbb{E}(\mathrm{d}W_s)
$$

Or l'espérance des accroissements du mouvement brownien standard $\mathrm{d}W_s$ est nulle d'où :

$$
  \mathbb{E}(X_t) = \int_0^t e^{A(t-s)}r(s)\,\mathrm{d}s 
$$

## Convergence en loi

Soit $G:s\mapsto G(s)=e^{A(t-s)}\Sigma$. D'après le théroème de Paul Lévy on a :

$$
  \left\{ \forall t\in \mathbb{R}, \int_0^t G_n(s)\,\mathrm{d}s \rightarrow \int_0^t G(s)\,\mathrm{d}s \right\} \Leftrightarrow \left \{ \int_0^t G_n(s)\,\mathrm{d}W_s \rightarrow \int_0^t G(s)\,\mathrm{d}W_s  \right \}
$$

D'où le résultat.

## Étude de la loi de $\int_0^t G_n(s)\,\mathrm{d}W_s$

Reformulons $\int_0^t G_n(s)\,\mathrm{d}W_s$ à l'aide du maillage :

$$
    \int_0^t G_n(s)\,\mathrm{d}W_s = \sum_{i=0}^{N-1} G_n(t_i)(W_{t_{i+1}} - W_{t_i})
$$

Pour connaître sa loi calculons son espérance et sa variance.

$$
  \begin{array}{r c l}
    \mathbb{E}\left ( \int_0^t G_n(s)\,\mathrm{d}W_s  \right ) &=& \mathbb{E}\left (\sum_{i=0}^{N-1} G_n(t_i)(W_{t_{i+1}} - W_{t_i}) \right )\\
      &=& \sum_{i=0}^{N-1} G_n(t_i) \mathbb{E}(W_{t_{i+1}} - W_{t_i}) \\
      &=& 0
  \end{array}
$$

En effet $\mathbb{E}(W_{t_{i+1}} - W_{t_i}) = 0$ car il s'agit d'une loi normale centré, car il s'agit des accroissement d'un mouvement brownien standard.

Calculons maintenant sa variance :

$$
  V\left( \int_0^t G_n(s)\,\mathrm{d}W_s \right) = \mathbb{E}(\left|\int_0^t G_n(s)\,\mathrm{d}W_s \right|^2 )
$$

L'isométrie de Itō nous donne :

$$
  V\left( \int_0^t G_n(s)\,\mathrm{d}W_s \right) = \int_0^t \mathbb{E}(|G_n(s)G_n(s)^T|)\,\mathrm{d}s 
$$

Puisque $G_n$ est une fonction déterministem on se retrouve avec une simple intégrale :

$$
  V\left( \int_0^t G_n(s)\,\mathrm{d}W_s \right) = \int_0^t G_n(s)G_n(s)^T\,\mathrm{d}s
$$

On obtient donc le résultat suivant :

$$
  \int_0^t G_n(s)\,\mathrm{d}W_s \sim \mathcal{N}\left(0,\int_0^t G_n(s)G_n(s)^T\,\mathrm{d}s\right)
$$

## Convergence en loi de la limite

Par définition de la norme de Frobénius on a :

$$
  ||A||^2_F = \sum_i\sum_j |a_{ij}|^2
$$

Donc la norme de Frobénius est invariante par passage à la transposée, opération de transposition qui est distributive avec l'addition on a donc bien :

$$
  ||G_n - G||_F = ||G_n^{\mathsf{T}} -G^{\mathsf{T}}||_F
$$ 

# Simulation numérique

$$
  \operatorname{div}u = 0
$$

