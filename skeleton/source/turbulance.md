---
title: Simulation numérique de la turbulance
author: FJ
eq: 1 
...

# Équations de Navier et Stokes

Considérons une particule de fluide. On commence par écrire la conservation du moment :

$$
  \rho \gamma_i = \sum_{j=1}^3 \frac{\partial \sigma_{i,j}}{\partial x_j} + f_i \qquad , i = 1 ,2 ,3
$${#eq:1}

où :

* $\gamma = ( \gamma_1 , \gamma_2 , \gamma_3  )$ : le vecteur accélération ;
* $f = (f_1,f_2,f_3)$ : les forces volumiques appliquées au fluide ;
* $\sigma = \sigma(x,t)$ : tenseur des contraintes au point $x$ à l'instant $t$ ;
* $x=(x_1,x_2,x_3)$ : la position.

Conservaltion de la masse :

$$
  \frac{\partial \rho}{\partial t} + \mathrm{div}(\rho u) = 0
$${#eq:2}

où $u(x,t)$ est la vitesse du fluide au point $x$ à l'instant $t$.

$$
  \begin{array}{r l}
    \gamma(x,t) = \frac{ \mathrm{d} u(x,t) }{\mathrm{d}t} = && \frac{\partial u}{\partial t} + \sum_{j=1}^3 \frac{\partial y}{\partial x_j}\frac{\mathrm{d} x_j}{\mathrm{d} t} \\
                                                          = && \frac{\partial u}{\partial t} + (u\cdot \nabla)u
  \end{array}
$${#eq:3}

Substituant ([-@eq:3]) dans ([-@eq:1]) le terme $\rho \gamma$ devient $\rho(u\cdot \nabla)u$.
Supposant le fluide newtonnien, $\sigma$ s'écrit :

$$
  \sigma_{i,j} = \mu \left( \frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i} \right) + (\lambda \mathrm{div}(u) - p)\delta_{ij}
$${#eq:4}

$\mu$ et $\lambda$ constants, $\mu >0$ coefficient de viscosité et $p(x,t)$ la pression.

On suppose que le fluide est incompressible et homogène d'où $\rho(x,t) = \rho_0 = cste$.

On déduit de ([-@eq:2]) que :

$$
  \mathrm{div}(u) = 0
$${#eq:5}

Il s'agit de la contrainte d'incompressibilité.

En utilisant ([-@eq:4]) et ([-@eq:5]) on déduit de ([-@eq:1]) :

$$
  \frac{\partial u}{\partial t} + (u\cdot \nabla)u - \nu \Delta u + \nabla p = f
$${#eq:6}

avec $\Delta$ l'opérateur laplacien, $\nabla$ l'opérateur gradient.

Le équations ([-@eq:6]) et ([-@eq:5]) constituent les équations de Navier-Stokes incompressibles pour les fluides visqueux.

Pour étable ([-@eq:6]) on a posé $\rho_0 = 1$ et $\nu = \mu$. Si $\rho \ne 1$ on obtient ([-@eq:6]) en posant $\nu = \frac{\mu}{\rho_0}$.

> **Remarque :** Dans les écoulements turbulents, on considère le vecteur vorticité $\omega = \vec{\mathrm{rot}}u = \nabla \wedge u$ vitesse tourbillonnnaire. En utilisant $\omega$, le terme intertiel $(u\cdot \nabla)u = \omega \wedge u + \frac{1}{2}\nabla q^2$ avec $q = |u|$ (norme euclidienne).
>
> Le terme $p + \frac{1}{2}q^2$ est appelé pression totale, le terme associé à la vitesse s'écrit : $\nu \Delta u = -\nu \nabla \wedge \omega$.


> **Remarque :** Si $\Omega \subset \mathbb{R}^2$ on considère des écoulement plans, ce sera le cas d'écoulements dans des couches très fines.

## Adimensionnalisation des équations de Navier-Stokes

On pose $x = L_{*} x'$, $t = T_{*} t'$, $L_{*}$ et $T_{*}$ sont, respectivement, une longueur et un temps caractéristique.

$p = P_* p'$, $u=U_* u'$ et $f = \frac{L_*}{T_*^2}f'$ avec $P_* = U_*^2$ et $U_* = \frac{L_*}{T_*}$.

En substituant dans ([-@eq:6]) on obtient les équations de Navier-Stokes adimentionalisées :

$$
  \frac{\partial u'}{\partial t} + (u'\cdot \nabla)u' - Re \Delta u' + \nabla p' = f'
$${#eq:7}

avec $u'$, $p'$ et $f'$ les variables réduites et $Re = \frac{L_* U_*}{\nu}$ ;e nombre de Reynolds. Les écoulements turbulents corspondent à des nombres de Reynolds grands.

On définit l'énergie cinéritque :

$$
  e(u) = \frac{1}{2} \int_{\Omega} |u(x)|^2\,\mathrm{d}x
$${#eq:8}

et l'enstrophiei ou énergie tourbillonaire :

$$
  E(u) = \int_{\Omega} |\nabla u|^2\,\mathrm{d}x = \sum_{i,j=1}^3 \int_{\Omega} \left| \frac{\partial u_i}{\partial x_j}(x) \right|^2\,\mathrm{d}x
$${#eq:9}

L'enstrophie est associée à la dissipation de l'énergie cinétique. En effet, supposons $\Omega = \mathbb{R}^3$, que $u$ et $p$ tendent rapidement vers $0$ à l'infini, on prend alors le produit scalaire de ([-@eq:6]) avec $u$ et en intégrant par partis on obtient :

$$
  \frac{\mathrm{d}}{\mathrm{d}x}e(u) = -\nu E(u) + \int_{\Omega} f\cdot u\,\mathrm{d}x
$${#eq:10}

si $f=0$ on obtient :

$$
  \frac{\mathrm{d}}{\mathrm{d}x}e(u) = -\nu E(u) < 0
$${#eq:11}

L'équation ([-@eq:11]) montre que $e(u)$ décroît quant $t$ augmente et la décroissance est dûe à $E(u)$.

## Problèmes considérés

Les équations de Navier-Stokes ([-@eq:5]) et ([-@eq:6]) sont complétés par une condition initiale et des conditions aux limites.

On considère dans ce cours deux problèmes :

Condition au limites périodiques

:  Ces conditions limites correspondent à des écoulements en domaine infini (par d'effet de bord) la turbulence associée à ce type d'écoulement c'est la turbulence homogène. $u$, $f$ et $p$ sont périodiques dans chacune des directions d'espace $x_i$ de période $L_i$. $\Omega = (0,L_1)\times(0,L_2)\times(0,L_3) \subset \mathbb{R}^3$ ou $\Omega = (0,L_1)\times(0,L_2) \subset \mathbb{R}^2$.

Écoulement dans un canal

: On considère l'écoulement dans un canal parallèle au plan $0x_1x_2$ on a $\Omega = (0,L_1)\times(-h,+h)\times(0,L_3)$, la direction de l'écoulement est $x_1$, les parois du canal sont en $x_2 \pm h$ (largeur du canal $2h$) l'écoulement est supposé périodique dans les directions $x_1$ et $x_3$ de période $L_1$ et $L_3$ respectivement.
: Finalement les conditions limites sont :

