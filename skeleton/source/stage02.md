---
title: Stage
author: Josselin
bibliography: source/biblio/bib.yaml
...

# Présentation des différents modèles

Il existe trois grandes familles de modèles que l'on utilise selon l'échelle à laquelle on se place.

## Modèle microscopique

Les modèles microscopiques fonctionnent sur le principe de l'étude newtonienne de particules. On ne s'intéresse qu'à la trajectoire de ces particules, et on a donc :

$$
  \begin{cases}
    \dot{x}_i (t) = v_i(t) \\
    \dot{v}_i (t) = \displaystyle\sum_{j \atop j \ne i} F_{ij}(t,x_i)
  \end{cases}
$$

Ce modèle pose problème lorsque le nombre de particules devient très grand. La complexité algorithmique est alors en $\mathcal{O}(2^n)$ (nombre de couples dont on doit calculer l'interaction), avec $n$ le nombre de particules. Il devient donc très vite inenvisageable d'effectuer ce genre de calcul sans d'importantes approximations.

La variable de base du problème est $t$, à chaque pas de temps on calcule la somme des forces, par intégration on obtient la vitesse ce qui nous permet de remonter à la position de nous pas intégration.

## Modèles cinétique

Les modèles cinétiques s'appliquent à l'échelle mésoscopique, on modélise les particules par une densité de particules, et on a en particulier $f(x,t,v)\mathrm{d}x\mathrm{d}v$ le nombre de particules (où $\mathrm{d}x\mathrm{d}v$ représente un élément de volume dans l'espace des phases).

Ces modèles s’appuient sur une équation du type :

$$
  \partial_t f + v\cdot\nabla_x f + E_f\cdot\nabla_v f = Q(f,f)
$$

où $E_f$ représente le champ électrique, et $Q(f,f)$ un opérateur quadratique de collision.

Les variables de bases du problème sont $t$, $x$ et $v$. Une simulation directe impose donc de travailler en 7 dimensions : une de temps et 6 pour l'espace des phases $(x,v)$. Dans la pratique l'étude théorique du schéma se fait classiquement en dimension $d$, mais pour simplifier l'étude, l'implémentation et la visualisation des résultats on prendra souvent $d=1$.

> Les modèles microscopiques étant inutilisables dans la pratique pour $n$ grand, les modèles cinétiques sont aussi appelé modèles microscopique, d'où la dénomination du modèle micro-macro que nous allons étudier par la suite.

## Modèle macroscopique

Les modèles macroscopiques s'apparentent à la mécanique des fluides, le système d'équations dépend alors de peu d'équations qui permettent de résoudre le problème. Ces variables sont souvent condensées en un seul vecteur de variables intensives $U$ :

$$
  U = (\rho,u,T,\dots)(t,x)
$$

où $U$ vérifie l'équation d'Euler ou de Navier-Stockes :

$$
  \partial_t U + \nabla_x \cdot \mathcal{F}(U)(t,x) = S(U)
$$

Le terme source $S(U)$ non explicité vaut $0$ dans le cadre des équations d'Euler, et un ensemble de perturbations dans le cadre des équations de Navier-Stockes.

Les variables de bases du problème sont $t$ et $x$. La simulation n'impose que 4 dimensions, une de temps et 3 d'espace, donc dans une région se comportement globalement comme un fluide il est privilégié d'utiliser ce type de méthode, moins coûteuse en temps de calcul qu'un modèle cinétique.


# Couplage des modèles

Nous nous intéresserons à un plasma dans un domaine $\Omega$ dans lequel nous considérerons une zone cinétique, où le modèle valide est un modèle cinétique (aussi appelé microscopique), une zone fluide où le modèle valide est un modèle macroscopique basé sur les équations d'Euler, ainsi qu'une zone de transition où la modélisation utilise une combinaison des deux modèles. Le modèle générale se nomme *micro-macro* car il utilise conjointement un modèle microscopique et macroscopique.

À cause de la dépendance au modèle cinétique nos variables $(t,x,v)$ vivent dans $[0,T]\times\Omega\times\mathbb{R}^d$, où $\Omega$ est un fermé borné de $\mathbb{R}^d$ périodique, la vitesse $v$ n'est a priori pas borné par notre modélisation. Dans la pratique $d = 1,2,3$.

> Idéalement $d=3$ mais pour simplifier les notations ainsi que les représentations graphiques nous prendrons $d=1$.

Lorsque les particules de notre plasma ne sont pas chargées, le terme $E_f\cdot \nabla_v f$ du modèle cinétique est nul, de plus nous utiliseront l'opérateur de collisions le plus simple, s'exprimant à partir d'un équilibre qui est une maxwellienne :

$$
  Q(f,f) = \frac{1}{\varepsilon}(\mathcal{M}_{[f]} - f)
$$

où $\varepsilon = \frac{\ell}{L}$ est le libre parcours moyen, avec $L$ la longueur du domaine et $\mathcal{M}_{[f]}$ est la maxwellienne de $f$ qui se définit comme suit :

$$
  \mathcal{M}_{[f]} = \frac{\rho}{(2\pi T)^{\frac{d}{2}}} \exp \left( -\frac{|v-u|^2}{2T} \right)
$${#eq:defM}

Le modèle cinétique se réécrit alors :

$$
  \begin{cases}
    \partial_t f + v\cdot\nabla_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]}-f) \\
    f(t=0,x,v) = f_0 (x,v)
  \end{cases}
$$

Formellement, on remarque que si $\varepsilon \rightarrow 0$ alors $f \rightarrow \mathcal{M}_{[f]}$, pour éviter la divergence du terme vers l'infini, on en déduit que la maxwellienne est bien un état d'équilibre et que la solution de notre inconnue $f$ doit être relativement proche de $\mathcal{M}_{[f]}$, on retrouve alors les équations d'Euler :

$$
  \partial_t f + v\cdot\nabla_x f = 0
$$

Donc $f$ doit se comporter comme un fluide non visqueux. Cette remarque permettra de valider nos schémas et d'en vérifier les résultats.

## Approximations et modèle micro-macro

Dans la pratique la fonction inconnue $f$ n'est jamais éloignée de son équilibre maxwellien, nous pouvons donc réécrire $f$ comme une somme :

$$
  f = \mathcal{M}_{[f]} + g
$$

où $g$ est l'écart à l'équilibre prédit par la physique. On peut montrer que $g$ est à moyenne nulle en $v$, or il existe une décomposition unique dans $L^2$ de $f$ en somme d'une fonction $M$ et d'une fonction de moyenne nulle en $v$. Cette décomposition peut s'exprimer comme une projection de projecteur $\Pi$, d'où la décomposition suivante de $f$ :

$$
  f = \Pi_f + (I-\Pi_f)f
$$

On a donc $\mathcal{M}_{[f]} = \Pi_f$ et $(I-\Pi_f)f$ = g$, où le projecteur $\Pi$ est défini par :

$$
  \Pi_{\mathcal{M}_{[f]}}(\varphi) = \frac{1}{\rho}\left[ \langle \varphi \rangle + \frac{(v-u)\langle(v-u)\varphi\rangle}{T} + \left( \frac{|v-u|^2}{2T} - \frac{1}{2} \right)\left\langle \left(\frac{|v-u|^2}{T}-1\right)\varphi \right\rangle \right]\mathcal{M}_{[f]}
$$

L'équation du modèle cinétique devient :

$$
  \partial_t(\mathcal{M}_{[f]} + g) + v\cdot\nabla_x(\mathcal{M}_{[f]}+g) = -\frac{1}{\varepsilon}g
$${#eq:cine-Mg}

### Obtention du modèle macro

Notons $U$ le moment de $f$ définit par le vecteur suivant :

$$
  U = \int_{\mathbb{R}^d} m(v) f(v)\,\mathrm{d}v = \begin{pmatrix}
        \rho_f \\
        \rho_f u_f \\
        \rho_f |u_f|^2 + \frac{d}{2}\rho_f T_f
      \end{pmatrix}
$$

où $m(v) = (1 \, v \, |v|^2)^{\mathsf{R}}$, $\rho_f$ est la densité de particules, $u_f$ la vitesse moyenne, et $T_f$ la température. Le vecteur $U$ est de dimension $d+2$, en effet la deuxième composante $\rho_f u_f$ est un vecteur de dimension $d$ qui s'obtient comme suit :

$$
  \rho_f u_f = \int_{\mathbb{R}^d} v  f(v)\,\mathrm{d}v
$$

\ù $v$ est un vecteur de dimension $d$ et $f(v)$ un scalaire.

En utilisant la décomposition de $f$ vue précédemment on peut écrire :

$$
  U(t,x) = \int_{\mathbb{R}^d} m(v) f(v)\,\mathrm{d}v = \int_{\mathbb{R}^d} m(v) \mathcal{M}\,\mathrm{d}v + \int_{\mathbb{R}^d} m(v) g\,\mathrm{d}v
$$

or $\int_{\mathbb{R}^d} m(v) g\,\mathrm{d}v = 0$ car $g$ est à moyenne nulle en $v$.

En multipliant [-@eq:cine-Mg] par $v$ et en intégrant sur cette même variable on obtient :

$$
  \partial_t U + \nabla_x \int_{\mathbb{R}^d} v\, m(v)(\mathcal{M}+g)\,\mathrm{d}v = 0
$$

Le produit $v\,m(v)$ est une opération triviale en dimension 1 mais se complexifie en dimension $d$, en effet celle-ci fait intervenir un produit tensoriel :

$$
  v\,m(v) = \begin{pmatrix}v_1 \\ v_2 \\ v_3 \end{pmatrix} \otimes \begin{pmatrix} 1 \\ v_1 \\ v_2 \\ v_3 \\ |v|^2 \end{pmatrix} = \cdots
$$

On trouve alors :

$$
  \partial_t U + \nabla_x \int_{\mathbb{R}^d}v\,m(v)\mathcal{M}_{[f]}\,\mathrm{d}v + \nabla_x\int_{mathbb{R}^d} v\,m(v)g\,\mathrm{d}v = 0
$${#eq:mm-macro}

L'équation [-@eq:mm-macro] est l'équation macro du modèle micro-macro

### Obtention du modèle micro

Pour obtenir la partie micro on ne s'intéresse qu'à la perturbation $g$ de $f$, en effet toute l'information sur l'équilibre $\mathcal{M}_{[f]}$ est contenue dans la partie macro. Pour cela on reprend le modèle cinétique ([-@eq:cine-Mg]) et on projette dans la direction $Ker(\Pi)$, *ie* avec le projecteur $I-\Pi$ :

$$
  \partial_t g + (I-\Pi)(v\cdot\nabla_x(\mathcal{M}_{[f]} + g)) = - \frac{1}{\varepsilon}g
$${#eq:mm-micro}

Il s'agit là de l'équation micro du modèle micro-macro.

On peut montrer l'équivalence entre le modèle micro-macro composé des équations [-@eq:mm-micro] et [-@eq:mm-macro] sur $u$ et $g$, et le modèle cinétique [-@eq:cine-Mg] sur $f$. Dans l'état le modèle micro-macro n'a pas d'utilité propre mais cette réécriture du modèle cinétique sert de base pour des approximations. En effet il sera plus simple dans cette écriture de négliger la perturbation à l'équilibre $g$ dans une partie du domaine, aussi appelée partie fluide.

# Résolution du modèle cinétique

## Schéma d'Euler en temps

Le modèle cinétique est de la forme :

$$
  \partial_t f = -\frac{1}{\varepsilon}(\mathcal{M}_{[f]} - f) - v\cdot\nabla_x f
$$

De manière plus générale ce modèle est de la forme :

$$
  \partial_t f = -\frac{1}{\varepsilon}f + \mathcal{F}(f)
$$

### Schéma d'Euler explicite

On cherche à résoudre un problème du type :

$$
  \begin{cases}
    \dot{y}(t) = -\frac{1}{\varepsilon}y(t) + \mathcal{F}(y(t)) \\
    y(0) = y_0
  \end{cases}
$$

Ce qui donne le schéma explicite suivant :

$$
    \frac{ y^{n+1} - y^n}{\Delta t} = -\frac{1}{\varepsilon}y^n + \mathcal{F}(y^n)
$$

Qui peut se réécrire sous une forme itérative :

$$
  \begin{cases}
    y^{n+1} = (1-\frac{\Delta t}{\varepsilon})y^n + \Delta t \mathcal{F}(y^n)\\
    y^0 = y_0
  \end{cases}
$$

Pour calculer une condition CFL, considérons le cas où $\mathcal{F} = 0$, on obtient donc une formule de récurrence explicite simple pour $y^{n}$ :

$$
  y^{n} = \left(1-\frac{\Delta t}{\varepsilon}\right)^n y^0
$$

Or cela converge si et seulement si $\left|1-\frac{\Delta t}{\varepsilon}\right| \le 1$, *ie* $\Delta t \le \varepsilon$. Or le libre parcours moyen $\varepsilon$ peut être choisi arbitrairement petit, donc cette condition CFL n'est pas avantageuse. En effet $\varepsilon \rightarrow 0$ correspond au cas fluide, et le schéma doit rester stable dans ce cas.

### Schéma d'Euler implicite

En reprenant les mêmes notations on peut écrire un schéma d'Euler implicite sous la forme :

$$
  \frac{y^{n+1} - y^n}{\Delta t} = -\frac{1}{\varepsilon} y^{n+1} + \mathcal{F}(y^n)
$$

Qui peut se réécrire sous une forme itérative :

$$
  \begin{cases}
    (1+\frac{\Delta t}{\varepsilon})y^{n+1} = y^n + \Delta t\mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$

Schéma que l'on rend facilement explicite car $1+\frac{\Delta t}{\varepsilon} \ne 0$ :

$$
  \begin{cases}
    y^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}y^n + \frac{1}{1+\frac{\Delta t}{\varepsilon}}\mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$

De même en prenant $\mathcal{F}$ nulle on trouve une formule de récurrence de la forme :

$$
  y^n = \left( \frac{1}{1+\frac{\Delta t}{\varepsilon}} \right)^n y^0
$$

ce qui est inconditionnellement stable quelque soit la valeur de $\Delta t$ et de $\varepsilon$.

## Application au modèle cinétique

En appliquant un schéma d'Euler implicite en temps sur le modèle cinétique, celui-ci devient :

$$
  f^{n+1} = f^n - \Delta t\, v\cdot\nabla_x f^n + \frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]} - f^{n+1})
$$

On réécrit ce schéma en temps sous une forme explicitée :

$$
  f^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ f^n - \Delta t\, v\cdot\nabla_x f^n + \frac{\Delta t}{\varepsilon} \mathcal{M}_{[f^{n+1}]} \right]
$$

On peut étudier les termes un à un :

* $- \Delta t\, v\cdot\nabla_x f^n$ est un terme de transport, que nous résoudrons par un schéma compact d'ordre élevé, celui-ci reste de la forme classique d'un schéma volumes finis avec un flux numérique que nous définirons plus tard :
  $$
    - \Delta t\, v\cdot\nabla_x f^n \simeq -\frac{\Delta t}{\Delta x} v\cdot(f^n_{i+\frac{1}{2}}-f^n_{i-\frac{1}{2}})
  $$
* $\frac{\Delta t}{\varepsilon} \mathcal{M}_{[f^{n+1}]}$ est une partie du terme de diffusion, et ne nécessite que l'approximation de la maxwellienne en tout point. Puisque nous utilisons un schéma implicite en temps il est nécessaire d'avoir une première approximation de $f^{n+1}$ pour calculer ce terme, dans la pratique seule les variables $(\rho^{n+1},u^{n+1},T^{n+1})$ sont nécessaires, et il est possible de les obtenir sans calculer entièrement $f^{n+1}$.

## Terme de transport

Il est possible, sur le terme de transport, de monter facilement en ordre, cela permet d'assurer une précision importe sur ce terme et nous espérons donc augmenter la précision global du schéma.

Deux méthodes sont classiquement utilisées pour monter en ordre :

* Les schémas compacts de B. Duprés.
* Le schéma WENO de Shu.

Nous utiliserons ici un schéma compact.

### Écriture générale du schéma

On part d'une équation d'advection classique :

$$
  \partial_t u + a \partial_x u = 0 \quad ,\, a>0
$$

Les schémas linéaires de différences finies peuvent s'écrire comme :

$$
  u_i^{n+1} = \sum_{r=k-p}^k \alpha_r u_{i+r}^n
$$

avec $\alpha_r = \alpha_r(\nu)$ dépendant du schéma choisi et où $\nu = a \frac{\Delta t}{\Delta x}$ est le nombre de CFL. Ce schéma général a un *stencil* de $p+1$ cellules continues, d'un décalage de $k$. Dans la pratique $p$ sera impair pour considérer un groupe de cellules centré sur la cellule courante, et $k$ sera généralement choisi par $k=\frac{p-1}{2}$ pour avoir les cellules adjacentes à la cellule courante.

Dans le cadre de la méthode des volumes finis on privilégie l'écriture :

$$
  \frac{u_i^{n+1}-u_i^n}{\Delta t} + a \frac{u_{i+\frac{1}{2}}^n - u_{i-\frac{1}{2}}^n}{\Delta x} = 0
$$

où $u_{i+\frac{1}{2}}^n$ est le flux numérique que l'on choisit en fonction de l'ordre que l'on souhaite atteindre. Pour préparer sa mise en place en informatique, on privilégiera l'écriture incrémentale, plus proche des différences finies :

$$
  u_i^{n+1} = u_i^n - \frac{\Delta t}{\Delta x}a(u_{i+\frac{1}{2}}^n - u_{i-\frac{1}{2}}^n)
$$

On rappelle que la vitesse $a$ peut être dépendante de l'espace et n'est non nécessairement positive, pour prendre en compte une vitesse négative on distingue $a$ en 2 parties :

* $a^+ = \max(a,0)$
* $a^- = \min(a,0)$

Le schéma volumes finis devient alors :

$$
  u_i^{n+1} = u_i^n -\frac{\Delta t}{\Delta x}[ a^+(u_{i+\frac{1}{2}}^n - u_{i-\frac{1}{2}}^n) + a^-(u_{i+\frac{3}{2}}^n - u_{i+\frac{1}{2}}^n) ]
$$

Cette écriture est indépendante du flux choisi

### Choix du flux

Maintenant nous allons présenter plusieurs flux qui dépendent du choix de $(p,k)$ :

* Pour $(p,k) = (1,0)$, on retrouve le schéma *upwind* :
  $$
    u_{i+\frac{1}{2}}^n = u_i^n
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

Le choix, pour l'implémentation, s'est tourné vers le schéma $(p,k)=(5,2)$.

### Obtention de l'ordre

La solution exacte d'un problème de transport à vitesse $a$ constante est connue et simple à calculer. Nous allons donc partir de ce problème, le résoudre sur un premier maillage et en calculer l'erreur, puis pour un maillage plus fin, idéalement 2 fois plus fin, résoudre ce même problème et en calculer l'erreur. Les deux résolutions s'effectuent avec un même pas de temps on étudie donc bien l'évolution de l'erreur spatiale, seul paramètre évoluant entre les deux simulations.

Le problème est :

$$
  \partial_t u + a\partial_x u = 0
$$

Pour simplifier le problème nous prendrons $a=1$, sans pour autant perdre en généralité dans le calcul de l'ordre. L'équation est considérée valide sur l'ensemble $x\in[0,2\pi]$, avec des conditions aux bords périodiques ; et nous allons considérer un cosinus comme condition de départ :

$$
  u_i^0 = cos(x_i)
$$

Un seul pas de temps suffit pour l'obtention de l'ordre :

$$
  u_i^1 = u_i^0 - \frac{\Delta t}{\Delta x}( u^0_{i+\frac{1}{2}} - u^0_{i-\frac{1}{2}}) = \cos(x_i - \Delta t) + \mathcal{O}(\Delta x^n)
$$

où $n$ est l'ordre recherché. L'erreur se calcule par la norme de la différence de la solution approchée avec la solution exacte :

$$
  e_1 = \| U^1 - \cos(X_i - \Delta t) \|_1 = \sum_i |u_i^1 - \cos(x_i - \Delta t) |\Delta x = \mathcal{O}(\Delta x^n)
$$

$$
  e_{\infty} = \| U^1 - \cos(X_i - \Delta t) \|_{\infty} =  \sup_i |u_i^1 - \cos(x_i - \Delta t) |
$$

On en déduit que $e_1 = C\Delta x^n$m donc en traçant l'erreur sur une échelle logarithmique on trouve :

$$
  \log e_1 = \log C + n \log \Delta x
$$

En effectuant cette simulation pour différentes valeurs de $\Delta x$ on peut tracer $\log e_1 = f(\log \Delta x)$, où l'on doit obtenir une droite dont la pente indique l'ordre.

Dans notre cas nous prendrons $\Delta x = \frac{2\pi}{20} , \frac{2\pi}{40} , \frac{2\pi}{60} , \frac{2\pi}{80}$. Pour assurer notre condition CFL nous choisirons $\Delta t < \frac{2\pi}{100}$ fixé.

![Représentation de $U_i = f(x_i)$](template/result.png)

On peut tracer l'erreur local faite en chaque point :

![Graphique de $U_i - \cos(x_i - \Delta t) = f(x_i)$](template/local_error.png)

On remarque que l'erreur diminue drastiquement avec l'augmentation du nombre de cellules, pour mesure un peu plus exactement l'erreur nous traçons $log(e) = f(log(\Delta x)$ :

![Graphique de $log(e_{1 | \infty}) = f(log(\Delta x))_{\,}$](template/global_error.png)

Les données exactes sont :

| $m$ | $\log(\Delta x)$    | $\log(e_1)$         | $\log(e_{\infty})$  |
|:---:|:-------------------:|:-------------------:|:-------------------:|
| 20  | -1.1578552071446455 | -11.321382952262143 | -12.796612398363203 |
| 40  | -1.8510023877045909 | -15.053093155672141 | -16.481696395438853 |
| 60  | -2.2564674958127551 | -17.496886112790701 | -18.910724909301070 |
| 80  | -2.5441495682645363 | -19.683545087249144 | -21.090157757561656 |

  : Données de l'erreur en fonction de $\Delta x = \frac{2\pi}{m}$

## Algorithme général

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


### Propriété sur la température

À plusieurs reprises on extrait la racine carré de la température $(T_i)_{i}$, or celle-ci est uniquement donnée par :

$$
  T_i^{n+1} = \frac{(U_3)_i^n}{(U_1)_i^n} - \left(\frac{(U_2)_i^n}{(U_1)_i^n}\right)^2
$$

Rien ne semble assurer la positivité de cette valeur, nécessaire pour la validité des calculs. De manière plus détaillées, en utilisant la définition du vecteur $U_i^n$, $T_i^{n+1}$ se calcule comme suit :

$$
  %T_i^n \simeq \frac{\int_{\mathbb{R}}|v|^2 f(v)\,\mathrm{d}v}{\int_{\mathbb{R}} f(v)\,\mathrm{d}v} - \left(\frac{\int_{\mathbb{R}} v f(v)\,\mathrm{d}v}{\int_{\mathbb{R}} f(v)\,\mathrm{d}v} \right)^2
  T_i^{n+1} = \frac{ \sum_k |v_k|^2f_{i,k}^n\Delta v }{ \sum_k f_{i,k}^n\Delta v } - \left(\frac{ \sum_k v_k f_{i,k}^n\Delta v}{ \sum_k f_{i,k}^n\Delta v }\right)^2
$$

Pour que la température reste positive il suffit de vérifier :

$$
  %\int_{\mathbb{R}}|v|^2 f(v)\,\mathrm{d}v\int_{\mathbb{R}} f(v)\,\mathrm{d}v - \left( \int_{\mathbb{R}} v f(v)\,\mathrm{d}v \right) ^2 > 0
  \sum_k |v_k|^2 f_{i,k}^n\Delta v \sum_k f_{i,k}^n\Delta v - \left( \sum_k v_k f_{i,k}^n\Delta v \right)^2 \geq 0
$$

Or, en appliquant l'inégalité de Cauchy-Schwarz discrète sur le premier terme avec le fonctions $v_k\sqrt{f_{i,k}^n}$ et $\sqrt{f_{i,k}^n}$ on obtient :

$$
  %\int (v\sqrt{f})^2 \int (\sqrt{f})^2 \geq \left| \int v\sqrt{f}\sqrt{f} \right|^2
  \sum_k (v_k\sqrt{f_{i,k}^n})^2\Delta v \sum_k (\sqrt{f_{i,k}^n})^2\Delta v \geq \left| \sum_k v_k \sqrt{f_{i,k}^n}\sqrt{f_{i,k}^n} \Delta v \right|^2
$$

C'est à dire que l'on a bien :

$$
  %\int |v|^2 f \int f \geq \left| \int vf \right|^2
  \sum_k |v_k|^2 f_{i,k}^n \Delta v \sum_k f_{i,k}^n \Delta v \geq \left( \sum_k v_k f_{i,k}^n \Delta v \right)^2
$$

Ce qui garantie bien la positivité de $T_i^n$ en tout point $x_i$ de l'espace et pour tout temps $t^n$.

### Propriétés de conservations

On résout le modèle suivant :

$$
  \partial_t f + v\partial_x f = \frac{1}{\varepsilon}(\mathcal{M}-f)
$$

En calculant les moments et en intégrant en $x$ on obtient :

$$
  \iint_{\Omega \times \mathbb{R}^d} m(v)(\partial_t f + v\partial_x f)\,\mathrm{d}x\mathrm{d}v = \frac{1}{\varepsilon}\iint_{\Omega \times \mathbb{R}^d} m(v)(\mathcal{M}_{[f]}-f)\,\mathrm{d}x\mathrm{d}v
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

> On constate bien une conservation de ces valeurs. La légère évolution de ces valeurs est dû à la mauvaise approximation de la maxwellienne.

### Condition de CFL

Il n'est pas possible de calculer directement la CFL du schéma en $f_{i,k}$ nous allons donc utiliser l'analyse de *von Neumann* pour résoudre ce problème. Pour cela, posons $f_{j,k}^n = e^{i\kappa j\Delta x}A^n$, l'indice d'espace est dorénavant $j$ et $i$ est le nombre imaginaire tel que $i^2 = -1$. Nous pouvons donc facilement exprimer $f_{j-1,k}^n$ directement en fonction de $f_{j,k}^n$ :

$$
  f_{j-1,k}^n = e^{i\kappa (j-1)\Delta x}A^n = f_{j,k}^n e^{-i\kappa\Delta x}
$$

Cela permet donc d'exprimer $f_{j,k}^{n+1}$ en fonction uniquement de $f_{j,k}^n$, et donc d'obtenir une formule de récurrence du type :

$$
  f_{j,k}^{n+1} = \mathcal{A} f_{j,k}^n = (\mathcal{A})^{n+1} f_{j,k}^0
$$

On remarque de suite qu'il est nécessaire pour que le schéma converge d'avoir $|\mathcal{A}| \leq 1$. Pour trouver cette formule de récurrence nous travaillerons sur une version simplifiée du schéma, en particulier nous ne considérerons qu'un schéma *upwind* pour le terme de transport au lieu d'un schéma compact d'ordre élevé, et nous négligerons l'impact de la maxwellienne.

On part du schéma simplifié sur $f$ :

$$
  f_{j,k}^{n+1} = \frac{\varepsilon}{\varepsilon + \Delta t}\left[ f_{j,k}^n - \frac{\Delta t}{\Delta x}v_k(f_{j,k}^n - f_{j,k}^ne^{-i\kappa\Delta x} )  \right]
$$

Ce que l'on peut écrire sous la forme :

$$
  f_{j,k}^{n+1} = f_{j,k}^n\frac{\varepsilon}{\varepsilon + \Delta t}\left[ 1-\frac{\Delta t}{\Delta x}v_k(1-e^{-i\kappa\Delta x}) \right]
$$

On obtient bien la forme désiré $f_{j,k}^{n+1} = \mathcal{A} f_{j,k}$, pour simplifier l'étude de $\mathcal{A}$ écrivons ce terme sous la forme :

$$
  \mathcal{A} = \frac{\varepsilon}{\varepsilon + \Delta t} \mathcal{B}
$$

Étudions $|\mathcal{B}|^2$ :

* $\mathrm{Im}(\mathcal{B}) = -\frac{\Delta t}{\Delta x}v_k\sin(\kappa \Delta x)$
* $\mathrm{Re}(\mathcal{B}) = 1-\frac{\Delta t}{\Delta x}v_k(1-\cos(\kappa \Delta x)$

D'où :

$$
  \begin{array}{rcl}
    |\mathcal{B}|^2 &=& \mathrm{Re}(\mathcal{B})^2 + \mathrm{Im}(\mathcal{B})^2 \\
                    &=& 1 + 2(1-\cos(\kappa\Delta x))\Delta t \left[ \frac{\Delta t}{\Delta x^2}v_k^2 - \frac{v_k}{\Delta x}\right] \\
  \end{array}
$$

On souhaite $|\mathcal{A}|^2 = \left(\frac{\varepsilon}{\varepsilon + \Delta t}\right)^2|\mathcal{B}|^2 \leq 1$ c'est-à-dire :

$$
  \begin{array}{rcl}
    |\mathcal{B}|^2 &\leq& \left(\frac{\varepsilon + \Delta t}{\varepsilon}\right)^2 \\
    \Delta t \left[(1-\cos(\kappa\Delta x))\frac{v^2}{\Delta x^2} - \frac{1}{2\varepsilon^2}\right] &\leq& \frac{1}{\varepsilon} + (1-\cos(\kappa\Delta x))\frac{v}{\Delta x} \\
  \end{array}
$$

Cette inégalité doit être vérifiée pour toute vitesse $v_k$ nous allons donc majorer par $v_{\textrm{max}}$, de même quelque soit le nombre d'onde $\kappa$ nous allons donc majorer $1-\cos(\kappa\Delta x)=2\sin^2(\frac{\kappa\Delta x}{2})$ par 2. Ce qui nous donne après simplification :

$$
  \Delta t (2v\varepsilon - \Delta x) \leq 2\Delta x \varepsilon
$$

Il est nécessaire d'étudier le signe de $2v\varepsilon - \Delta x$ :

* $2v\varepsilon - \Delta x < 0$ alors $\Delta t >0$ ce qui est toujours vérifier. Cette condition est vérifiée si :
  $$
    \varepsilon < \frac{\Delta x}{2v}
  $$
  Avec classiquement $\Delta x \sim 10^{-2}$ et $v\sim 18$ ce qui nous donne $\varepsilon \sim 10^{-3}$.
* $2v\varepsilon - \Delta x > 0$ alors :
  $$
    \Delta t \leq \frac{2\Delta x \varepsilon}{2v\varepsilon - \Delta x}
  $$

En étudiant la fonction :
$$
  h:\varepsilon\mapsto\frac{ \frac{\Delta x}{v} \varepsilon}{\varepsilon - \frac{1}{2}\frac{\Delta x}{v}}
$$
on trouve que cette fonction est décroissante et a pour limite $\frac{\Delta x}{v}$, nous utiliserons donc une fraction de cette limite comme base de temps. On retrouve aussi le pôle $\frac{\Delta x}{2v}$ qui correspond au changement de condition pour obtenir $\Delta t$.

## Cas tests

Ce que l'on connait est le cas $\varepsilon \rightarrow 0$ qui est le cas des équations d'Euler, par conséquent nous allons tester ce code en comparant les résultats avec une simulation de fluide eulérien.

### Conditions aux bords périodiques

Nous prenons comme condition initiale une fonction de densité dans l'espace des phases de la forme :

$$
  f_{i,k}^0 = \frac{1}{\sqrt{2\pi}}(1-\alpha \cos(kx_i)) e^{-\frac{v_k^2}{2}}
$$

Pour la condition initiale eulérienne on ne se préoccupe d'aucune variation dans la direction $v$ on retire donc l'exponentielle et le terme de normalisation.

<div>
  ![Densité    ](template/periodic_rho.png)

  ![Vitesse    ](template/periodic_u.png)

  ![Température](template/periodic_T.png)

Grandeurs intensives dans le cas de condition aux bords périodique
</div>

### Conditions aux bords de Neumann

De la même manière qu'avec des conditions périodiques, on s'arrange ici pour avoir une condition initiale qui s’interprète facilement avec les équations d'Euler, c'est-à-dire avec peu de variation en $v$, ici il s'agit des conditions initiales d'un tube à choc de Sob.

La condition initiale est donc donnée par :

$$
  \left\{ \begin{array}{ll}
    U_L = (\rho,u,T)_L = (1,0,1) & ,\,x\leq \frac{1}{2} \\
    U_R = (0.125,0,0.8)          & ,\,x\geq\frac{1}{2} \\
  \end{array}\right.
$$

Ce qui nous donne pour le code cinétique une condition initiale donnée par la maxwellienne de ces deux vecteurs de variables intensives.

<div>
![Densité    ](template/neumann_rho.png)

![Vitesse    ](template/neumann_u.png)

![Température](template/neumann_T.png)

Grandeurs intensives dans le cas de condition aux bords de Neumann
</div>


