---
title: Stage
author: Josselin
bibliography: source/biblio/bib.yaml
nocite: |
    @*
...

# Présentation des différents types de modèles

## Les modèles microscopiques

Les modèles microscopiques fonctionnent sur le principe de l'étude newtonienne de particules. On ne s'intéresse qu'à la trajectoire de ces particules, et on a donc :

$$
  \begin{cases}
    \dot{x}_i (t) = v_i(t) \\
    \dot{v}_i (t) = \displaystyle\sum_{j \atop j \ne i} F_{ij}(t,x_i)
  \end{cases}
$$

Ce modèle pose problème lorsque le nombre de particules devient très grand. La complexité algorithmique est alors en $\mathcal{O}(2^n)$ (nombre de couples dont on doit calculer l'interaction), avec $n$ le nombre de particules. Il devient donc très vite inenvisageable d'effectuer ce genre de calcul sans d'importantes approximations.

La variable de base du problème est $t$.

## Les modèles cinétiques

Les modèles cinétiques s'appliquent à l'échelle mésoscopique, on modélise les particules par une densité de particules, et on a en particulier $f(x,t,v)\mathrm{d}x\mathrm{d}v$ le nombre de particules (où $\mathrm{d}x\mathrm{d}v$ représente un élément de volume dans l'espace des phases).

Ces modèles s'appuyent sur une équation du type :

$$
  \partial_t f + v\cdot\nabla_x f + E_f\cdot\nabla_v f = Q(f,f)
$$

où $E_f$ représente le champ électrique, et $Q(f,f)$ un opérateur quadratique de collision.

Les variables de bases du problème sont $t$, $x$ et $v$. Une simulation directe impose donc de travailler en 7 dimensions : une de temps et 6 pour l'espace des phases $(x,v)$.

> Les modèles microscopiques étant inutilisables dans la pratique pour $n$ grand, les modèles cinétiques sont aussi appelé modèles microscopique, d'où le modèle micro-macro que nous allons étudier par la suite.

## Les modèles macroscopiques

Les modèles macroscopiques s'apparentent à de la mécanique des fluides, le système d'équations dépend alors de peu d'équations qui permettent de résoudre le problème, ces variables sont souvent condensé en un seul vecteur $U$, pour des raisons de notations nous l'appellerons $\tilde{U}$

$$
  \tilde{U} = (\rho,u,T,\dots)(t,x)
$$

où $\tilde{U}$ vérifie l'équation d'Euler ou de Navier-Stockes :

$$
  \partial_t\tilde{U} + \nabla_x \cdot \mathcal{F}(\tilde{U})(t,x) = \cdots
$$

Le terme source de droite non explicité vaut $0$ dans le cadre des équations d'Euler, et un ensemble de perturbations dans le cadre des équations de Navier-Stockes.

Les variables de bases du problème sont $t$ et $x$. La simulation n'impose que 4 dimensions, une de temps et 3 d'espace, donc dans une région se comportement globalement comme un fluide il est privilégié d'utiliser ce genre de méthode, moins coûteuse en temps qu'un modèle cinétique.

# Détails du modèle micro-macro

Dans cette partie nos variables $(t,x,v)$ vivent dans $[0,T]\times \Omega \times \mathbb{R}^d$ où $\Omega$ est un fermé borné de $\mathbb{R}^d$ (périodique ?), dans la pratique $d = 1,2,3$, la vitesse n'est a priori par bornée (autrement que par une limite suffisamment grande que l'on pourrait noter $c$).

> Idéalement $d=3$ mais pour simplifier les notations ainsi que les représentations graphiques nous prendrons $d=1$.

Lorsque les particules en question ne sont pas chargées, le terme $E_f\cdot\nabla_v f$ du modèle cinétique est nul. Nous utiliserons ici uniquement l'opérateur de collisions le plus simple, s'exprimant à partir d'un équilibre qui est une maxwellienne :

$$
  Q(f,f) =\frac{1}{\varepsilon}(\mathcal{M}_{[f]} - f)
$$

où $\varepsilon = \frac{\ell}{L}$ est le libre parcours moyen, avec $L$ la longueur du domaine, et $\mathcal{M}_{[f]}$ est la maxwellienne de $f$, c'est à dire la condition d'équilibre liée à $f$. Elle est définie comme suit :

$$
  \mathcal{M}_{[f]} = \frac{\rho}{(2\pi T)^{\frac{d}{2}}}\exp \left(-\frac{|v-u|^2}{2T}\right)
$${#eq:defM}

Le système cinétique se réécrit alors :

$$
  \begin{cases}
    \partial_t f + v\cdot\nabla_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]}-f) \\
    f(t=0,x,v) = f_0 (x,v)
  \end{cases}
$$

Formellement, on remarque que si $\varepsilon \rightarrow 0$ alors $f \rightarrow \mathcal{M}_{[f]}$, pour éviter la divergence du terme vers l'infini, on en déduit que la maxwellienne est bien un état d'équilibre et que la solution de notre inconnue $f$ doit être relativement proche de $\mathcal{M}_{[f]}$. On réécrit donc $f$ sous la forme :

$$
  f = \mathcal{M}_{[f]} + g
$$

où $g$ est l'écart à l'équilibre prédit par la physique. On peut montrer que $g$ est à moyenne nulle en $v$, or il existe une décomposition unique dans $L^2$ de $f$ en une somme d'une fonction $M$ et d'une de moyenne nulle en $v$. Cette décomposition peut s'exprimer comme une projection avec comme projecteur $\Pi$, d'où la décomposition suivante de $f$ :

$$
  f = \Pi_f + (I-\Pi_f)f
$$

On a donc trivialement que $\mathcal{M}_{[f]} = \Pi_f$ et $(I-\Pi_f)f = g$. Avec la projection $\Pi$ définit par :

$$
  \Pi_{\mathcal{M}_{[f]}}(\varphi) = \frac{1}{\rho}\left[ \langle \varphi \rangle + \frac{(v-u)\langle(v-u)\varphi\rangle}{T} + \left( \frac{|v-u|^2}{2T} - \frac{1}{2} \right)\left\langle \left(\frac{|v-u|^2}{T}-1\right)\varphi \right\rangle \right]\mathcal{M}_{[f]}
$$

> Par la suite, pour alléger les notations nous noterons simplement la maxwellienne $\mathcal{M}$ et le projecteur $\Pi$.

L'équation du modèle cinétique devient :

$$
  \partial_t (\mathcal{M}+g) + v\cdot\nabla_x(\mathcal{M}+g) = -\frac{1}{\varepsilon}g
$${#eq:micro-mg}

Notons $U$ le moment définit par le vecteur suivant :

$$
  U = \int_{\mathbb{R}^d} \begin{pmatrix}
        1 \\
        v \\
        |v|^2
      \end{pmatrix} f(v)\,\mathrm{d}v = \begin{pmatrix}
        \rho_f \\
        \rho_f u_f \\
        \rho_f |u_f|^2 + \frac{d}{2}\rho_f T_f
      \end{pmatrix}
$${#eq:defU}

où $\rho_f$ est la densité de particules lié à la fonction d'état $f$, $u_f$ la vitesse moyenne, et $T_f$ la température.

> Les composantes de ce vecteur peuvent être vue comme la densité de particules, la quantité de mouvement, et l'énergie du système.
> 
> **Attention :** le vecteur $U$ est de dimension $d+2$, en effet la deuxième composante est potentiellement constituée de $d$ composantes.


En utilisant la décomposition de $f$ vu précédemment on peut écrire :

$$
  U(t,x) = \int_{\mathbb{R}^d} \begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix} f(v)\,\mathrm{d}v = \int_{\mathbb{R}^d} \begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix} (\mathcal{M}+g)\,\mathrm{d}v = U(t,x) + \underbrace{\int_{\mathbb{R}^d} \begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix} g\,\mathrm{d}v}_{\text{$= 0 $ car $g$ de moyenne nulle en $v$}}
$$

> On a :
> $$
    \partial_v(vg) = g + v\partial_v g
  $$
> En effet $\partial_v v = 1$. Par intégration sur $v$ on obtient l'égalité suivante :
> $$
    \int vg\,\mathrm{d}v = \int g\,\mathrm{d}v + v\int g\,\mathrm{d}v
  $$
> or $\int g\,\mathrm{d}v = 0$ par définition. On effectue un raisonnement similaire avec $\partial_v(v^2g)$ pour obtenir le même résultat. D'où :
> $$
    \int_{\mathbb{R}^d} \begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix} g\,\mathrm{d}v = 0
  $$

En multipliant [-@eq:micro-mg] par $v$ et en intégrant sur cette même variable on obtient :

$$
  \partial_t U + \nabla_x \int v\begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix}(\mathcal{M}+g)\,\mathrm{d}v = 0
$${#eq:vcine}

Le second terme est une intégrale en $v$ de $vg$ qui, comme montré précédemment, est nulle. On décompose le produit dans l'intégrale et on obtient finalement :

$$
  \partial_t U + \nabla_x \int v\begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix}\mathcal{M}\,\mathrm{d}v + \nabla_x \int v\begin{pmatrix} 1 \\ v \\ |v|^2 \end{pmatrix}g\,\mathrm{d}v = 0
$${#eq:macro}

Il s'agit ici de l'équation macro de notre modèle micro-macro.

Pour l'équation micro repartons de l'équation cinétique :

$$
  \partial_t f + v\nabla_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]}-f)
$$

Au lieu de projeter dans la *direction* de $\mathcal{M}$ avec $\Pi_f$, ce qui ferait perdre toute information sur $g$ par définition du projecteur, projetons dans la *direction* de $g$ avec $I-\Pi$ :

$$
  \partial_t g + (I-\Pi)(v\cdot\nabla_x(\mathcal{M}+g)) = - \frac{1}{\varepsilon}g
$${#eq:micro}

Il s'agit ici de l'équation micro de notre modèle micro-macro.

On peut montrer l'équivalence entre le modèle micro-macro composé des équations [-@eq:macro] et [-@eq:micro] sur $U$ et $g$, et le modèle cinétique sur $f$. Dans l'état le modèle micro-macro n'a pas d'utilité propre, cette réécriture du modèle sert de base pour des approximations, il sera plus simple dans cette écriture d'approximer sur une partie du domaine $f$ à son équilibre en négligeant la perturbation $g$ par exemple.

## Approximation

Soit $h$ une fonction indicatrice continument dérivable définit dans $\Omega$, elle définit l'espace où le modèle cinétique est le plus probant, et donc le modèle fluide où elle est nulle. Utiliser une fonction indicatrice continument dérivable permet d'éviter une rupture de modèle, nous obtenons donc une zone de transition des modèles où la solution calculée est une superposition des deux solutions, pondérée par la valeur de $h$. Nous allons pouvoir définir :

$$
  g = hg + (1-h)g
$$

Ce que l'on pourra aussi noter :

$$
  g = g_K + g_F
$$

où $g_K = hg$ correspond à la perturbation par rapport à l'équilibre maxwellien dans un modèle cinétique, et $g_F = (1-h)g$ correspond à la perturbation par rapport à l'équilibre dans un modèle fluide, or ce genre de modèle ne propose pas de perturbation par rapport à l'équilibre donc la grandeur $g_F$ pourra être négligée.

Reprenons le modèle micro donné par l'équation [-@eq:micro], que nous multiplions par $h$ :

$$
  \underbrace{h\partial_t g}_{\text{(1)}} + \underbrace{h(I-\Pi)(v\cdot\nabla_x\mathcal{M})}_{\text{(2)}} + \underbrace{h(I-\Pi)(v\cdot\nabla_x(g_K + g_F))}_{\text{(3)}} = -\frac{h}{\varepsilon}g
$$

1. Or $\partial_t g = \partial_t g_K - g\partial_t h$ donc $h\partial_t g = \partial_t g_K - g\partial_t h$, car $h=0$ sur le support de $g_F$.
2. Le second terme ne dépend par de $g$ donc on le passe dans le membre de droite.
3. On divise ce terme entre le projecteur identité et le projecteur $\Pi$, ce second terme ira dans le membre de droite.

D'où :

$$
  \partial_t g_K + hv\cdot\nabla_x g_K + hv\cdot\nabla_x g_F = -\frac{1}{\varepsilon}g_K + \frac{g_K}{h}\partial_t h - h(I-\Pi)(v\cdot\nabla_x\mathcal{M}) + h\Pi(v\cdot\nabla_x(g_K+g_F))
$$

> **Pour simplifier le dernier terme :** $- h(I-\Pi)(v\cdot\nabla_x\mathcal{M}) + h\Pi(v\cdot\nabla_x(g_K+g_F))$
> 
> D'après la publication *A multiscale kinetic-fluid solver with dynamic localization of kinetic effects* de P. Degond, G. Dimarco et L. Mieussens on a :
> $$
    - h(I-\Pi)(v\cdot\nabla_x\mathcal{M}) + h\Pi(v\cdot\nabla_x(g_K+g_F)) = -h(\partial_t + v\cdot\nabla_x)\mathcal{M}
  $$
> Pour retrouver ce résultat je suis parti de $-h(\partial_t + v\cdot\nabla_x)\mathcal{M}$ :
> $$
    -h(\partial_t + v\cdot\nabla_x)\mathcal{M} = -h\partial_t\mathcal{M} - hv\cdot\nabla_x\mathcal{M}
  $$
> Or le modèle macro ([-@eq:macro]) nous donne :
> $$
    \partial_t(\mathcal{M}+g) + v\cdot\nabla_x(\mathcal{M}+g) = -\frac{1}{\varepsilon}g
  $$
> On peut donc exprimer $\partial_t\mathcal{M}$ de la façon suivante :
> $$
    \partial_t\mathcal{M} = -\partial_tg - \frac{1}{\varepsilon} - v\cdot\nabla_x(\mathcal{M}+g)
  $$
> Le modèle micro ([-@eq:micro]) nous donne une équation sur $\partial_tg$ :
> $$
    -\partial_t g = \frac{1}{\varepsilon}g + (I-\Pi)(v\cdot\nabla_x(\mathcal{M}+g))
  $$
> D'où l'expression de $\partial_t\mathcal{M}$ :
> $$
    \partial_t\mathcal{M} = \frac{1}{\varepsilon}g + (I-\Pi)(v\cdot\nabla_x(\mathcal{M}+g)) - \frac{1}{\varepsilon} - v\cdot\nabla_x(\mathcal{M}+g)
  $$
> Après simplification on obtient :
> $$
    \partial_t\mathcal{M} = -\Pi(v\cdot\nabla_x(\mathcal{M}+g))
  $$
> D'où en réinjectant ce résultat dans l'équation précédente on a :
> $$
    -h(\partial_t + v\cdot\nabla_x)\mathcal{M} = h\Pi(v\cdot\nabla_x(\mathcal{M}+g)) - hv\cdot\nabla_x\mathcal{M}
  $$
> On retrouve bien $- h(I-\Pi)(v\cdot\nabla_x\mathcal{M}) + h\Pi(v\cdot\nabla_x(g_K+g_F))$, en effet en développant ce terme on trouve :
> $$
    - h(I-\Pi)(v\cdot\nabla_x\mathcal{M}) + h\Pi(v\cdot\nabla_x(g_K+g_F)) = -hv\cdot\nabla_x\mathcal{M} + h\Pi(v\cdot\nabla_x(\mathcal{M}+g))
  $$
> En effet, pour une projection $p$, on a le résultat $p(u)+p(v) = p(u+v)$.

D'où l'équation sur $g_K$ :

$$
  \partial_t g_K + hv\cdot\nabla_x g_K + hv\cdot\nabla_x g_F = -\frac{1}{\varepsilon}g_K + \frac{g_K}{h}\partial_t h - h(\partial_t + v\cdot\nabla_x)\mathcal{M}
$$

On peut effectuer la même démarche pour obtenir une équation similaire sur $g_F$ en multipliant l'équation du modèle micro [-@eq:micro] par $(1-h)$, mais nous négligerons $g_F$ par la suite :

$$
  g_F = 0
$$

> Pour information cette équation est :
> $$
    \partial_t g_F +(1-h)v\cdot\nabla_x g_K + (1-h)v\cdot\nabla_x g_F = -\frac{1}{\varepsilon}g_F - \frac{g_F}{1-h}\partial_t h - (1-h)(\partial_t +v\cdot\nabla_x)\mathcal{M}
  $$

# Schéma numérique

Le modèle micro est de la forme :

$$
  \partial_t g = - \frac{1}{\varepsilon}g - (I-\Pi)(v\cdot\nabla_x(\mathcal{M}+g)) 
$$

De manière plus global ce modèle est de la forme : 

$$
  \partial_t g = - \frac{1}{\varepsilon}g + \mathcal{F}(g)
$$

## Schéma d'Euler explicite

On a un problème du type :

$$
  \begin{cases}
    \dot{y}(t) = -\frac{1}{\varepsilon}y(t) + \mathcal{F}(y(t)) \\
    y(0) = y_0
  \end{cases}
$$

Ce qui peut se réécrire avec un schéma d'Euler explicite comme :

$$
  \begin{cases}
    y^{n+1} = (1-\frac{\Delta t}{\varepsilon})y^n + \mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$

Pour calculer une condition CFL, considérons le cas où $\mathcal{F} = 0$, on obtient donc une formule de récurrence explicite simple pour $y^{n}$ :

$$
  y^{n} = \left(1-\frac{\Delta t}{\varepsilon}\right)^n y^0
$$

Or cela converge si et seulement si $\left|1-\frac{\Delta t}{\varepsilon}\right| \le 1$, *ie* $\Delta t \le \varepsilon$. Or le libre parcours moyen $\varepsilon$ peut être choisi arbitrairement petit, donc cette condition CFL n'est pas avantageuse.

## Schéma d'Euler implicite

En reprenant les même notation on peut écrire un schéma d'Euler implicite sous la forme :

$$
  \begin{cases}
    (1+\frac{\Delta t}{\varepsilon}) y^{n+1} = y^n + \mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$

Or $(1-\frac{\Delta t}{\varepsilon}) \neq 0$ on peut donc exprimer explicitement $y^{n+1}$ :

$$
  \begin{cases}
    y^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}y^n + \frac{1}{1+\frac{\Delta t}{\varepsilon}}\mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$


## Application à l'équation micro

En réutilisant le schéma d'Euler implicite en temps avec :

* $y^n \rightarrow g^n$
* $\mathcal{F}(y) \rightarrow (I-\Pi)(v\cdot\nabla_x(\mathcal{M}+g^n))$

l'équation micro devient :

$$
  g^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}g^n - \frac{\Delta t}{1+\frac{\Delta t}{\varepsilon}}(I-\Pi)(v\cdot\nabla_x\mathcal{M}) - \frac{\Delta t}{1+\frac{\Delta t}{\varepsilon}} v\cdot\nabla_x g^n + \frac{\Delta t}{1+\frac{\Delta t}{\varepsilon}} \Pi(v\cdot\nabla_x g^n)
$$

On peut étudier les termes un à un :

* $\frac{1}{1+\frac{\Delta t}{\varepsilon}}g^n$ : ce terme ne pose pas le moindre problème
* $\frac{\Delta t}{1+\frac{\Delta t}{\varepsilon}}(I-\Pi)(v\cdot\nabla_x\mathcal{M})$ : ce terme est un peu plus complexe car il fait entre autre intervenir $\Pi$, ce terme dépendant de $U$ il est nécessaire de le réévaluer à chaque itération en temps.
* $- \frac{\Delta t}{1+\frac{\Delta t}{\varepsilon}} v\cdot\nabla_x g^n$ : il s'agit là d'un terme de transport, que nous résoudrons par un schéma *upwind* avec :
  $$
    v\cdot\nabla_x g^n = -\Delta t \left[ v^+ \frac{g^n_i - g^n_{i-1}}{\Delta x} + v^- \frac{g^n_{i+1} - g^n_{i}}{\Delta x} \right]
  $$
  où $v^+ = \max(v,0)$ et $v^-= \min(v,0)$.
* $\frac{\Delta t}{1+\frac{\Delta t}{\varepsilon}} \Pi(v\cdot\nabla_x g^n)$ : il s'agit d'un terme similaire au précédent auquel on a appliqué la projection $\Pi$, il me semble donc logique d'appliquer $\Pi$ au schéma *upwind* utilisé sur le terme précédent.


### Augmentation de l'ordre sur le terme de transport

Il est possible sur le terme de transport de monté en ordre. La méthode *upwind* est une méthode d'ordre 1 simple à mettre en place. Deux méthodes sont proposées pour monter en ordre là dessus :

* Méthode de schéma compact de B. Duprés.
* Méthode WENO de Shu

#### Schéma compact

On se base sur l'équation d'advection classique :

$$
  \partial_t u + a\partial_x u = 0 \quad , a >0
$$

Les schémas linéaire de différences finies peuvent s'écrire comme :

$$
  u_{j}^{n+1} = \sum_{r = k-p}^k \alpha_r u_{j+r}^n
$$

avec $\alpha_r = \alpha_r(\nu)$ dépendant du schéma choisi et où $\nu = a\frac{\Delta t}{\Delta x}$ est le nombre de la CFL. Ce schéma général a un stencil de $p+1$ cellules continues, d'un décalage de $k$. Dans la pratique $p$ sera impair pour considérer un groupe de cellules centré sur la cellule courante et $k$ sera généralement égale à $^{(p-1)}/_2$ pour considérer les cellules adjacentes à la cellule courante.

Dans le cadre de la méthode des volumes finis ont privilégie l'écriture :

$$
  \frac{u_j^{n+1}-u_j^{n}}{\Delta t} + a\frac{u_{j+\frac{1}{2}}^{n}-u_{j-\frac{1}{2}}^{n}}{\Delta x} = 0
$$

où $u_{j+\frac{1}{2}}^n$ est le flux qu'il va falloir choisir. Ce flux est directement lié au choix de $(p,k)$, voici quelques exemples :

* Pour $(p,k)=(1,0)$, on retrouve le schéma *upwind* :
  $$
    u_{j+\frac{1}{2}} = u_j
  $$
* Pour $(p,k)=(3,1)$, il s'agit d'une combinaison convexe des schémas de Lax-Wendroff et de Beam-Warming $(1-\alpha)LW+\alpha BW$ avec $\alpha = \frac{1+\nu}{3}$ :
  $$
    u_{j+\frac{1}{2}} = u_j + \frac{2-\nu}{6}(1-\nu)(u_{j+1}-u_{j}) + \frac{1+\nu}{6}(1-\nu)(u_j-u_{j-1})
  $$
* Pour $(p,k)=(5,2)$, on passe à un schéma à 5 points :
  $$
    \begin{array}{rl}
      u_{j+\frac{1}{2}} = & u_{j+2} + \frac{\nu+3}{2}(u_{j+1}-u_{j+2}) + \frac{(2+\nu)(1+\nu)}{6}(u_j - 2u_{j+1} + u_{j+2}) \\
                          & + \frac{(2+\nu)(1+\nu)(\nu-1)}{24}(u_{j-1} - 3u_{j} + 3u_{j+1} - u_{j+2}) \\
                          & + \frac{(2+\nu)(1+\nu)(\nu-1)(\nu-2)}{120}(u_{j-2} - 4u_{j-1} + 6u_{j} - 4u_{j+1} + u_{j+2})
    \end{array}
  $$

> Pour obtenir le schéma différences finis pour un couple $(p,k)$ il faut calculer les coefficients $\alpha_{k,p}$ donnés par :
> 
> $$
    \alpha_{p,k} = \frac{\prod_{q=0}^p (k+\nu-q)}{p!}
  $$


Le schéma volumes finis peut se réécrire :

$$
  u_j^{n+1} = u_j^n + \nu( u_{j+\frac{1}{2}}^n - u_{j-\frac{1}{2}}^n )
$${#eq:iter}

on rappelle que $\nu = a\frac{\Delta t}{\Delta x}$ est le nombre de CFL. De là on peut déduire un algorithme pour le calcul d'une itération :

```{ .f90 .numberLines .lineAnchors }
function Un1 ( Un , nu )
    ! calcul d'une nouvelle itération à partir de $U^n$ et de $\nu$
    real(rp),dimension(0:)           :: Un
    real(rp)                         :: nu ! CFL number
    real(rp),dimension(0:size(Un)-1) :: Un1

    real(rp) :: a,b,c,d
    real(rp),dimension(5) :: weights,slice1,slice2
    integer :: j
    integer :: n; n = size(Un)

    ! calcul des poids pour chaque indice pris en considération
    a = (nu+3)*0.5_rp    ; b = (2+nu)*(1+nu)/6.0_rp
    c = b*(nu-1)*0.25_rp ; d = c*(nu-2)*0.2_rp
    weights(1) = d
    weights(2) = c - 4.0_rp*d
    weights(3) = b - 3.0_rp*c + 6.0_rp*d
    weights(4) = a - 2.0_rp*b + 3.0_rp*c - 4.0_rp*d;
    weights(5) = 1.0_rp - a + b - c + d

    ! gestion des bords
    do j=0,2
      slice1 = [ Un(mod(j-2+n,n)) , Un(mod(j-1+n,n)) , Un(j)            , Un(j+1) , Un(j+2) ]
      slice2 = [ Un(mod(j-3+n,n)) , Un(mod(j-2+n,n)) , Un(mod(j-1+n,n)) , Un(j)   , Un(j+1) ]
      Un1(j) = Un(j) + nu*( u_j12( slice1 , weights ) - u_j12( slice2 , weights ) )
    end do
    do j=n-2,n-1
      slice1 = [ Un(j-2) , Un(j-1) , Un(j)   , Un(mod(j+1,n)) , Un(mod(j+2,n)) ]
      slice2 = [ Un(j-3) , Un(j-2) , Un(j-1) , Un(j)          , Un(mod(j+1,n)) ]
      Un1(j) = Un(j) + nu*( u_j12( slice1 , weights ) - u_j12( slice2 , weights ) )
    end do

    ! boucle principale
    do j=3,n-3
        ! $u^{n+1}_j = u_j^n + \nu(u_{j+1/2}^n - u{j-1/2}^n)$
        Un1(j) = Un(j) + nu*( u_j12( Un(j-2:j+2) , weights ) - u_j12( Un(j-3:j+1) , weights ) )
    end do

    ! internal function
    contains
      ! flux $u_{i+\frac{1}{2}}$
      function u_j12(U,weights) result(y)
        ! simple fonction de calcul du flux qui peut s'apparenter à un produit
        ! scalaire entre les éléments du spencil et les poids
        real(rp),dimension(:) :: U,weights
        real(rp)              :: y
        y = dot_product(U,weights)
      end function u_j12

end function
```

Pour obtenir ce code, en particulier la fonction `u_j12` qui calcule $u_{j+\frac{1}{2}}$ on réécrit le flux de la façon suivante :

$$
  \begin{array}{rl}
    u_{j+\frac{1}{2}}^n = & \delta u_{j-2}^n + (\gamma - 4 \delta)u_{j-1}^n + (\beta-3\gamma+6\delta)u_j^n \\
                          & + (\alpha-2\beta+3\gamma-4\delta) u_{j+1}^n + (1-\alpha+\beta-\gamma+\delta)u_{j+2}^n
  \end{array}
$$

où les lettres grecques $\alpha$, $\beta$, $\gamma$ et $\delta$ définissent les coefficients du flux $u_{j+\frac{1}{2}}$ :

* $\alpha = \frac{\nu+3}{2}$
* $\beta = \frac{(2+\nu)(1+\nu)}{6}$
* $\gamma = \frac{(2+\nu)(1+\nu)(\nu-1)}{24} = \beta \times \frac{(\nu-1)}{4}$
* $\delta = \frac{(2+\nu)(1+\nu)(\nu-1)(\nu-2)}{120} = \gamma \times \frac{(\nu-2)}{5} = \beta \times \frac{(\nu-1)}{4} \times \frac{(\nu-2)}{5}$

On peut donc réécrire $u_{j+\frac{1}{2}}$ sous la forme d'un produit scalaire :

$$
  u_{j+\frac{1}{2}} = \begin{pmatrix} \delta \\ \gamma-4\delta \\ \beta-3\gamma+6\delta \\ \alpha - 2\beta + 3\gamma - 4\delta \\ 1-\alpha+\beta-\gamma+\delta\end{pmatrix} \cdot \begin{pmatrix} u^n_{j-2} \\ u^n_{j-1} \\ u^n_{j} \\ u^n_{j+1} \\ u^n_{j+2} \end{pmatrix}
$$

Ensuite le code consiste à calculer le nouveau vecteur à partir de l'équation [-@eq:iter] avec des conditions aux bords periodiques. Pour d'autres conditions aux bords il suffit de modifier les stableaux `slices1` et `slices2` dans les cas limites.

Comme indiqué dans la publication *Uniform asymptotic stability of Stang's explicit compact schemes for linear advection* de B. Després, on remarque une forte oscilation de ce schéma en cas de solution discontinue, mais dans notre cas la solution est en théorie suffisamment régulière pour ne pas poser trop problème.

### Couplage des équations

On souhaite résoudre le modèle :

$$
  \partial_t f + v \partial_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]} - f)
$$

La résolution nécessite une grille en espace et en vitesse (maillage de l'espace des phases), on suppose $f_{i,k}^n$ donnée par l'itération précédente, le calcul de la nouvelle itération s'effectue schématiquement comme suit :

1. On calcule le flux numérique $f_{i+\frac{1}{2},k}^n$ du schéma compact $(p,k) = (5,2)$ :
  $$
    f_{i+\frac{1}{2},k}^n \gets ( (f_{j,k}^n)_{j\in [\![ i-2;i+2 ]\!] } , v_k )
  $$
  On rappelle que les conditions aux bords sont périodiques.
2. On calcule le flux numérique $F_{i+\frac{1}{2}}^n$ pour le schéma sur $U$ à partir du flux de $f_{i+\frac{1}{2},\cdot}^n$ :
  $$
    F_{i+\frac{1}{2}}^n \gets \sum_k v_k m(v_k) f_{i+\frac{1}{2},k}^n \Delta v
  $$
3. On appelle le schéma sur $U$ :
  $$
    U_i^{n+1} \gets U_i^n - \frac{\Delta t}{\Delta x}( F_{i+\frac{1}{2}}^n - F_{i-\frac{1}{2}}^n)
  $$
4. On calcule les variable intensives $(\rho_i^{n+1},u_i^{n+1},T_i^{n+1})$ :
  $$
    \begin{pmatrix}
      \rho^{n+1}_i \\
      u^{n+1}_i \\
      T^{n+1}_i
    \end{pmatrix}
    =
    \begin{pmatrix}
      U_1             \\
      \frac{U_2}{U_1} \\
      \frac{U_3}{U_1} - \left(\frac{U_2}{U_1}\right)^2
    \end{pmatrix}
  $$
5. On calcule la maxwellienne $(\mathcal{M}_{[f^{n+1}]})_{i,k}$ en tout point $(i,k)$ de l'espace des phases, via sa définition (voir équation [-@eq:defM])
  $$
    (\mathcal{M}_{[f^{n+1}]})_{i,k} = \frac{\rho_i^{n+1}}{\sqrt{2\pi T^{n+1}_i}}\exp\left(-\frac{1}{2}\frac{|v_k - u_i^{n+1} |^2}{T^{n+1}_i} \right)
  $$
6. On approxime $f^{n+1}_{i,k}$ via le schéma avec le terme de transport et de diffusion :
  $$
    f^{n+1}_{i,k} = \frac{1}{1+\frac{\Delta t}{\varepsilon}} \left[ f^n_{i,k} - \frac{\Delta t}{\Delta x}v_k (f^n_{i+\frac{1}{2},k} - f^n_{i-\frac{1}{2},k}) +\frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k}  \right]
  $$
7. On corrige l'approximation $U_i^{n+1}$ via le calcul du moment de $f^{n+1}_{i,\cdot}$ :
  $$
    U_i^{n+1} \gets \sum_k m(v_k)f_{i,k}^{n+1} \Delta v
  $$

Cet algorithme résoud l'équation :

$$
  \partial_t f + v\partial_x f = \frac{1}{\varepsilon}(\mathcal{M}-f)
$$

En calculant les moments et en intégrant en $x$ on obtient :

$$
  \iint m(v)(\partial_t f + v\partial_x f)\,\mathrm{d}x\mathrm{d}v = \frac{1}{\varepsilon}\iint m(v)(\mathcal{M}-f)\,\mathrm{d}x\mathrm{d}v
$$

Or les moments de $\mathcal{M}$ et de $f$ sont égaux. De plus le second terme du premier membre vaut zéro car par échange de la dérivée sous le signe somme on dérive en $x$ une intégrale sur $x$ et $v$  qui ne dépend donc plus de $x$, on obtient finalement :

$$
  \frac{\mathrm{d}}{\mathrm{d}x}\int U(t,x)\,\mathrm{d}x = 0
$$

Écrit de façon discrète cela équivaut à :

$$
  \sum_i U^n_i \Delta x = c
$$

où $c$ est une constante indépendante de $t$. On peut aussi comparer ce résultat à :

$$
  \sum_{i,k} m(v_k)f^n_{i,k} \Delta x \Delta v
$$

