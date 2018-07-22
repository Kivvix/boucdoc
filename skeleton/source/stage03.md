---
title: Modèles hybrides fluide/cinétique pour les plasmas chauds
author: Josselin
bibliography: source/biblio/biblio.bib
...

> Introduction générale. Motivations, objectifs :
>
> * Simulation de problèmes hors équilibre
> * Approche hybride F/K
> * Schémas multi-échelles
> * Optimisation, coût numérique
>
> Modèle mM rassemble tous ces points

# Présentation des modèles

> Partie théorique, liste des modèles étudiés pendant le stage

## Modèle microscopique particulaire

Les modèles microscopiques fonctionnent sur le principe de l'étude newtonienne de particules. Le modèle cherche à déterminer la trajectoire de chaque particule par le principe fondamental de la dynamique, d'où le système\ :

$$
  \begin{cases}
    \dot{x}_i (t) = v_i(t) \\
    \dot{v}_i (t) = \displaystyle\sum_{j \atop j \ne i} F_{ij}(t,x_i)
  \end{cases}
$$

Ce modèle est lent en temps de calcul puisqu'il possède une complexité algorithmique en $\mathcal{O}(2^n)$ où $n$ est le nombre de particules en interaction. Cette complexité peut être divisée par 2 en remarquant que $F_{ij} = F_{ji}$ d'après le principe de l'action-réaction ; mais la complexité reste exponentielle. L'utilisation de ce type de modèle est inenvisageable dès que le nombre de particules atteint la centaine de particules. Dans le cadre de l'étude des plasma, le nombre $n$ de particules en interaction est voisin du nombre d'Avogadro $\mathcal{N}_A \approx 6,02\cdot 10^{23}$.

Une approximation de ce modèle est parfois utilisé à l'aide d'une représentation arborescente de l'espace via un *quadtree* par exemple ; cela permet de négliger les interactions à longue distance. C'est ce qui est par exemple utilisé dans des simulations de galaxies, ou dans des moteurs de collision comme celui du jeu vidéo Doom.

La variable de base dans le modèle est le temps $t$ ; à chaque pas de temps on calcule la somme des forces pour obtenir l'accélération, la vitesse puis la position s'obtiennent par intégration successive.

## Modèle cinétique

> Introduire en indiquant qu'il s'agit d'une meilleure description physique que le cas macroscopique (donc mettre cette partie après la partie macroscopique ?). Introduire le problème du coût de calcul/mémoire (6D).

Le principe du modèle cinétique est de proposer une description intermédiaire entre le modèle microscopique et macroscopique. On représente les particules dans l'espace des phases $(x,v)$. À la manière d'un modèle macroscopique nous n'étudions pas chaque particule individuellement mais une valeur intégrale qu'est la densité de particules dans l'espace des phases $f$. Ainsi $f(t,x,v)\mathrm{d}x\mathrm{d}v$ représente le nombre de particules dans l'élément de volume $\mathrm{d}x\mathrm{d}v$ de l'espace des phases, c'est-à-dire le nombre de particules à la position $x$ à la vitesse $v$.

Ce modèle s'appuie sur une équation de transport dans l'espace des phases à laquelle on ajoute un terme de collision\ :

$$
  \partial_t f + v\cdot\nabla_x f + E_f\cdot\nabla_v f = Q(f,f)
$${#eq:cine}

où le transport s'effectue à vitesse $v$ dans la direction $x$ et à la vitesse $E_f$ (le champ électrique) dans la direction $v$. $Q(f,f)$ représente un opérateur quadratique de collision, il modélise les interactions binaires entre particules ; plusieurs expressions sont possibles : Boltzman, Landau ou BGK par exemple.

Les variables de base du problème sont $t$, $x$ et $v$. Une simulation directe du problème complet impose donc de travailler en 7 dimensions : une de temps, et 6 pour l'espace des phases $(x,v)$. Travailler dans un espace de dimension aussi élevé implique des coûts importants en temps de calcul et dans l'utilisation de la mémoire ; un maillage non cartésien permet de ne raffiner que localement le domaine, mais les contraintes de gestion du maillage nous ont orientés vers une autre alternative.

L'étude théorique se fera en dimension $d$, mais pour simplifier l'étude, l'implémentation et la visualisation on prendre souvent $d=1$.

Ce modèle utilise à la manière du modèle macroscopique, une grandeur intégrale, mais celle-ci vit dans l'espace des phases pour avoir une description plus proche du modèle particulaire. La grandeur de travail est une fonction $f$ vivant dans l'espace des phases $(x,v)$. Les variables $(t,x,v)$ vivent dans $[0,T]\times\Omega\times\mathbb{R}^d$, où $\Omega$ est un fermé borné de $\mathbb{R}^d$, la vitesse $v$ n'est *a priori* pas borné par notre modélisation.

## Modèle macroscopique

Le modèle macroscopique est un modèle de mécanique des fluides ; le système d'équations dépend alors de peu de variables physiques pour d'écrire l'état thermodynamique. Ces variables sont condensées en un seul vecteur de variables intensives $U$\ :

$$
  U = (\rho,u,T,\dots)(t,x)
$$

où $U$ vérifie l’équation d’Euler ou de Navier-Stockes\ :

$$
  \partial_t U + \nabla_x \cdot \mathcal{F}(U)(t,x) = S(U)
$$

où les variables contenues dans le vecteur $U$, la fonction $\mathcal{F}$ et le terme source $S$ sont à définit selon le jeu d'équations choisi entre Euler et Navier-Stockes.

Les variables de bases du problème sont $t$ et $x$. La simulation n'impose que 4 dimensions, une de temps et 3 d'espace ; donc dans une région se comportant globalement comme un fluide il est privilégié d'utiliser ce type de méthode, moins coûteuse en temps de calcul qu'un modèle microscopique ou cinétique.

Nous resterons ici dans le cadre des équations d'Euler, $U$ est définit par\ :

$$
  U = \begin{pmatrix}
    \rho   \\
    \rho u \\
    e
  \end{pmatrix}
$$

où $e$ est l’énergie du système. Nous avons la fonction $\mathcal{F}$ définit par\ :

$$
  \mathcal{F}(U) = \begin{pmatrix}
    \rho u       \\
    \rho u^2 + p \\
    u(e+p)
  \end{pmatrix}
$$

où la pression $p$ est calculée via\ :

$$
  p = 2(e - \frac{1}{2}\rho u^2)
$$

Le terme source $S(U)$ est nul dans le cadre des équations d'Euler en l'absence d'un champ électrique $\vec{E}$, en présence d'un champ ce terme s'explicite sous la forme suivante\ :

$$
  S(U) = \int_{\mathbb{R}^d} m(v)\partial_v (Ef)\,\mathrm{d}v = \begin{pmatrix} 0 \\ \rho E \\ 2JE \end{pmatrix}
$$

avec $J$ l'intensité du courrant définit par $J = \rho u$.


## Cinétique vers fluide

Dans le modèle cinétique [!eq:cine], il est possible de lier la fonction de densité dans l'espace des phases au vecteur de variables extensives utilisé dans les équations d'Euler via\ :

$$
  U_{[f]} = \int_{\mathbb{R}^d} m(v)f\,\mathrm{d}v = \begin{pmatrix}\rho_f \\ \rho_f u_f \\ \rho_f|u_f|^2 + \frac{d}{2}\rho_fT_f\end{pmatrix}
$$

où $m(v) = (1 \; v \; |v|^2)^{\mathsf{T}}$, $\rho_f$ est la densité de particules, $u_f$ la vitesse moyenne, et $T_f$ la température. Le vecteur $U$ est de dimension $d+2$ ; en effet la deuxième composante $\rho_f u_f$ est un vecteur de dimension $d$ qui s’obtient comme suit\ :
$$
  \rho_f u_f = \int_{\mathbb{R}^d} v  f(v)\,\mathrm{d}v
$$
où $v$ est un vecteur de dimension $d$ et $f(v)$ un scalaire.

À partir de ce vecteur $U$ on peut retrouver les grandeurs physique intensives $(\rho,u,T)$\ :
$$
  \begin{pmatrix}
    \rho \\
    u    \\
    T
  \end{pmatrix} =
  \begin{pmatrix}
    U_1             \\
    \frac{U_2}{U_1} \\
    \frac{U_3}{U_1} - \left(\frac{U_2}{U_1}\right)^2
  \end{pmatrix}
$$

Pour valider nos modèles nous prendrons dans un premier temps un champ électrique nul : $E_f = 0$ ; le transport s'effectue alors seulement en espace et non en vitesse. De plus nous utiliserons l'opérateur de collision le plus simple, s'exprimant à partir d'un équilibre qu'est la loi de distribution maxwellienne\ :

$$
  Q(f,f) = \frac{1}{\varepsilon}(\mathcal{M}_{[f]} - f)
$$

où $\varepsilon = \frac{\ell}{L}$ est une donnée du problème physique avec $\ell$ le libre parcours moyen et $L$ la dimension du domaine ; $\mathcal{M}_{[f]}$ est la distribution maxwellienne définit par\ :

$$
  \mathcal{M}_{[f]} = \frac{\rho}{(2\pi T)^{\frac{d}{2}}}\exp\left(-\frac{|v-u|^2}{2T}\right)
$$

Le modèle que nous résoudrons par la suite s'écrit donc\ :

$$
  \begin{cases}
    \partial_t f + v\cdot\nabla_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]} - f) \\
    f(t=0,x,v) = f_0(x,v)
  \end{cases}
$$

Formellement, on remarque que si $\varepsilon \to 0$ alors $f\to\mathcal{M}_{[f]}$, pour éviter la divergence du terme vers l'infini ; on en déduit que la maxwellienne est bien un état d'équilibre et que la solution $f$ doit être relativement proche de $\mathcal{M}_{[f]}$. Ce cas permet aussi de retrouver les équations d'Euler\ :

$$
  \partial_t f + v\cdot\nabla_x f = 0
$$

Donc $f$ doit se comporter comme un fluide non visqueux. Cette remarque permettra de valider nos schémas et d’en vérifier les résultats en les comparant à un simulateur de fluide eulérien.



## Couplage des modèles

> Obtention du modèle micro-macro

> Introduire la motivation de ce couplage. Le projecteur $\Pi$ est définit dans [@crestetto] donc peut-être en parler.

Dans la pratique, la fonction inconnue $f$ n'est jamais éloignée de son équilibre maxwellien ; nous pouvons donc réécrire $f$ comme une somme\ :

$$
  f = \mathcal{M}_{[f]} + g
$$

où $g$ est l'écart à l'équilibre maxwellien. On peut montrer que $g$ est à moyenne nulle en $v$, or il existe une décomposition unique dans $L^2$ de $f$ en somme d'une fonction $M$ et d'une fonctionne de moyenne nulle en $v$. Cette décomposition peut s'exprimer comme une projection $\Pi$, d'où la décomposition de $f$\ :

$$
  f = \Pi_f + (I-\Pi_f)f
$$

On a donc $\mathcal{M}_{[f]} = \Pi_f$ et $(I-\Pi_f)f = g$, où le projecteur $\Pi$ est défini par\ :

$$
  \Pi_{\mathcal{M}_{[f]}}(\varphi) = \frac{1}{\rho}\left[ \langle \varphi \rangle + \frac{(v-u)\langle(v-u)\varphi\rangle}{T} + \left( \frac{|v-u|^2}{2T} - \frac{1}{2} \right)\left\langle \left(\frac{|v-u|^2}{T}-1\right)\varphi \right\rangle \right]\mathcal{M}_{[f]}
$$

Il est donc possible de réécrire le modèle cinétique en $\mathcal{M}_{[f]}$ et $g$\ :

$$
  \partial_t(\mathcal{M}_{[f]} + g) + v\cdot\nabla_x(\mathcal{M}_{[f]}+g) = -\frac{1}{\varepsilon}g
$$

### Obtention du modèle *macro*

Le vecteur $U$ est lié à l'inconnue $f$ via son moment\ :

$$
  U = \int_{\mathbb{R}^d} m(v)f(v)\,\mathrm{d}v
$$

En utilisant la décomposition de $f$ vue précédemment on peut réécrire $U$ comme\ :

$$
  U(t,x) = \int_{\mathbb{R}^d}m(v)\mathcal{M}_{[f]}\,\mathrm{d}v + \int_{\mathbb{R}^d}m(v)g\,\mathrm{d}v
$$

or $\int_{\mathbb{R}^d}m(v)f\,\mathrm{d}v = 0$ car $g$ est à moyenne nulle en $v$.

Ainsi en multipliant le modèle cinétique ([!eq:cine]) par $m(v)$ puis en intégrant selon $v$ on obtient\ :

$$
  \partial_t U + \nabla_x \int_{\mathbb{R}^d}vm(v)(\mathcal{M}_{[f]}+g)\,\mathrm{d}v = 0
$$

Le produit $vm(v)$ est une opération triviale en dimension 1 mais se complexifie en dimension $d$ ; celui-ci cache un produit tensoriel\ :

$$
  v\,m(v) = \begin{pmatrix}v_1 \\ v_2 \\ v_3 \end{pmatrix} \otimes \begin{pmatrix} 1 \\ v_1 \\ v_2 \\ v_3 \\ |v|^2 \end{pmatrix} = \cdots
$$

Finalement, en notant $\langle \cdot \rangle_v = \int_{\mathbb{R}^d}\cdot\,\mathrm{d}v$ on peut récrire ce modèle\ :

$$
  \partial_t U + \nabla_x \langle vm(v)\mathcal{M}_{[f]}\rangle_v + \nabla_v \langle E_fm(v)(\mathcal{M}_{[f]} + g)\rangle_v = - \nabla_x\langle vm(v)g \rangle_v
$$

Équation que l'on peut réécrire sous une forme plus proche des équations d'Euler par :

$$
  \partial_t U + \nabla_x\cdot\mathcal{F}(U) +  \nabla_x\langle vm(v)g \rangle_v = -\nabla_v \langle E_fm(v)(\mathcal{M}_{[f]} + g)\rangle_v
$${#eq:mima:macro}

L'équation [!eq:mima:macro] correspond à la description macroscopique du modèle hybride *micro-macro*.

### Obtention du modèle *micro*

Pour obtenir la description microscopique, on ne s'intéresse qu'à la perturbation $g$ de $f$. En effet toute l'information sur l'équilibre maxwellien $\mathcal{M}_{[f]}$ est contenue dans la description macroscopique. Il suffit maintenant de reprendre la modèle cinétique [!eq:cine] et de la projeter dans la direction $\ker (\Pi)$, c'est-à-dire en appliquant le projecteur $I-\Pi$\ :

$$
  \partial_t g + (I-\Pi)(v\cdot\nabla_x(\mathcal{M}_{[f]}+g) + E_f\cdot\nabla_v(\mathcal{M}_{[f]}+g)) = -\frac{1}{\varepsilon}g
$${#eq:mima:micro}

Il s'agit là de la description microscopique du modèle *micro-macro*.

On peut montrer l'équivalence entre le modèle *micro-macro* composé des équations [!eq:mima:micro] et [!eq:mima:macro] su $U$ et $g$, et le modèle cinétique [!eq:cine] sur $f$. Dans l'état, le modèle *micro-macro* n'a pas d'utilité propre ; cette réécriture du modèle cinétique sert de base pour des approximations. En effet il sera plus simple dans cette description de négliger la perturbation à l'équilibre $g$ sur une partie du domaine, que l'on nommera partie fluide du domaine.


## Approximation du modèle micro-macro

> Introduction de la fonction $h(t,x)$ et approximation $g_F = 0$

> Introduire l'idée en parlant de [@dimarco]

Le principal intérêt du modèle *micro-macro* est qu’il est possible d’effectuer plus simplement des approximations du modèle, en particulier ce que nous allons faire ici est une approximation uniquement de la partie *micro*.

Dans les régions où le système est à l'équilibre, c'est-à-dire $f \approx \mathcal{M}_{[f]}$, nous allons faire l'approximation $g=0$ dans cette zone. Nous introduisons la fonction $h:\Omega\mapsto[0,1]$ telle que :

* $h = 0$ dans la zone proche de l'équilibre, zone que nous nommerons fluide.
* $h=1$ dans la zone hors équilibre, zone que l'on nommera cinétique.

> TODO: tracer un truc ressemblant à $h(x)$

Utiliser une fonction indicatrice $h$ continument dérivable permet d’éviter une rupture de modèle ; nous obtenons donc une zone de transition des modèles où la solution calculée est une superposition des deux solutions, pondérée par la valeur de $h$. Nous allons pouvoir définir\ :

$$
  g = hg + (1-h)g
$$

Ce que l'on notera aussi\ :

$$
  g = g_K + g_F
$$

où $g_K=hg$ correspond à la perturbation par rapport à l'équilibre maxwellien dans un modèle cinétique, et $g_F = (1-h)g$ correspond à celle dans un modèle fluide. Un modèle fluide est macroscopique et ne propose donc pas de perturbation par rapport à l'équilibre, par conséquent la grandeur $g_F$ pourra être négligée.

Reprenons le modèle *micro* que nous multiplions par $h$\ :

$$
  \underbrace{h\partial_t g}_{(1)} + \underbrace{h(I-\Pi)(v\cdot\nabla_x\mathcal{M}_{[f]})}_{(2)} + \underbrace{h(I-\Pi)(v\cdot\nabla_x(g_K+g_F))}_{(3)} = -\frac{h}{\varepsilon}g
$$

1. Or $\partial_t g_k = \partial_t(hg) = h\partial_t g - g\partial_t h$ ; donc $h\partial_t g = \partial_t g_K - g\partial_t h$ ;
2. Le second terme ne dépend par de $g$, on le passe donc dans le membre de droite.
3. On distingue ce terme en deux parties, entre le projecteur identité et le projecteur $\Pi$, ce second terme ira dans le membre de droite.

D’où\ :

$$
  \partial_t g_K + hv\cdot\nabla_x g_K + hv\cdot\nabla_x g_F = -\frac{1}{\varepsilon}g_K + \frac{g_K}{h}\partial_t h - h(I-\Pi)(v\cdot\nabla_x\mathcal{M}) + h\Pi(v\cdot\nabla_x(g_K+g_F))
$$

Nous effectuons une approximation par rapport à $g$, en effet la fonction indicatrice $h$ permet de subdiviser le domaine. Nous négligerons $g_F$ par la suite\ :

$$
  g_F = 0
$$

La partie *micro* du modèle *micro-macro*, après cette approximation devient\ :

$$
  \partial_t g_K + hv\partial_x g_K = -\frac{1}{\varepsilon}g_K - h(I-\Pi)(v\partial_x \mathcal{M}_{[f]}) + h\Pi(v\partial_x g_K) + \frac{g_K}{h}\partial_t h
$$


## Problème de Poisson

Ce que nous modélisons dans le modèle cinétique ou *micro-macro* est une densité de particules dans un espace des phases. Les particules que nous considérons en particulier dans le plasma sont les électrons, c'est à dire des particules chargées. Les ions, au vu du rapport de masse entre le noyau atomique et les électrons, fait que l'on peut considérer ces particules statiques.

Le problème de Poisson est un modèle physique de l'évolution du champ électrique en fonction des particules chargées présentes\ :

$$
  \partial_x E = \sum_s q_s \rho_s
$$

avec $q_s$ la charge électrique d'un type espèce $s$ de particule, $\rho_s$ la densité de cette même espèce $s$. La somme s'effectue sur tous les types d'espèces chargées présentes dans le plasma, ici des électrons et des ions. Au vu du rapport de masse entre les électrons et les ions, nous pouvons considérer ces derniers comme statique. Ainsi la densité de particules que nous modélisons dans la variable $f$ est la densité d'électrons dans l'espace des phases. En normalisant les charges nous pouvons réécrire le problème de Poisson comme suit\ :

$$
  \partial_x E_f = \rho - 1
$${#eq:poisson}

où $1$ traduit la dynamique nulle des ions que l'on normalise, et $\rho$ est la densité de particules liées à la variable $f$.

Le champ électrique est définit à une constante près, c'est une variable de jauge, il manque donc une condition initiale pour compléter notre problème, nous choisirons\ :

$$
  \int_{\Omega} E_f\,\mathrm{d}x = 0
$${#eq:poisson:condi}


# Présentation des schémas

> Présentation des schémas utilisés (il ne me semble pas nécessaire de s'attarder sur les schémas en temps), on s'attarde surtout sur les schémas d'ordre élevé pour le terme d'advection présent dans les modèles cinétique et micro.

## Schémas en temps

La dynamique temporelle du modèle cinétique [!eq:cine] peut se résumer par une EDO du type\ :

$$
  \begin{cases}
    \dot{y}(t) = -\frac{1}{\varepsilon}y(t) + \mathcal{F}(y(t)) \\
    y(0) = y_0
  \end{cases}
$${#eq:edot}

On peut résumer la difficulté au cas $\mathcal{F} = 0$ pour étudie la stabilité des schémas temporels, au détriment de quelques petits paramètres physiques\ :

$$
  \dot{y} = -\frac{1}{\varepsilon}y
$$

où $\varepsilon$ peut être aussi petit que l'on veut pour représenter un système fluide. L'enjeu du schéma temporel est de pouvoir choisir le pas de temps $\Delta t$ indépendamment du paramètre physique $\varepsilon$.

$$
  \Delta t \not\sim \varepsilon
$$


### Schéma d'Euler implicite


Un schéma d'Euler explicite sur [!eq:edot] nous donne\ :

$$
  \frac{ y^{n+1} - y^n}{\Delta t} = -\frac{1}{\varepsilon}y^n + \mathcal{F}(y^n)
$$

Qui peut se réécrire sous une forme itérative\ :

$$
  \begin{cases}
    y^{n+1} = (1-\frac{\Delta t}{\varepsilon})y^n + \Delta t \mathcal{F}(y^n)\\
    y^0 = y_0
  \end{cases}
$$

Pour calculer une condition CFL, considérons le cas où $\mathcal{F} = 0$, on obtient donc une formule de récurrence explicite simple pour $y^{n}$\ :

$$
  y^{n} = \left(1-\frac{\Delta t}{\varepsilon}\right)^n y^0
$$

Or cela converge si et seulement si $\left|1-\frac{\Delta t}{\varepsilon}\right| \le 1$, ie $\Delta t \le 2\varepsilon$. Or le libre parcours moyen $\varepsilon$ peut être choisi arbitrairement petit, donc cette condition CFL n’est pas avantageuse. En effet $\varepsilon \to 0$ correspond au cas fluide, et le schéma doit rester stable dans ce cas.

Il est donc impératif d'utiliser un schéma d'Euler implicite de la forme\ :

$$
  \frac{y^{n+1} - y^n}{\Delta t} = -\frac{1}{\varepsilon} y^{n+1} + \mathcal{F}(y^n)
$$

Qui peut se réécrire sous une forme itérative\ :

$$
  \begin{cases}
    (1+\frac{\Delta t}{\varepsilon})y^{n+1} = y^n + \Delta t\mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$

Schéma que l’on rend facilement explicite car $1+\frac{\Delta t}{\varepsilon} \ne 0$\ :

$$
  \begin{cases}
    y^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}y^n + \frac{1}{1+\frac{\Delta t}{\varepsilon}}\mathcal{F}(y^n) \\
    y^0 = y_0
  \end{cases}
$$

De même en prenant $\mathcal{F}$ nulle on trouve une formule de récurrence de la forme\ :

$$
  y^n = \left( \frac{1}{1+\frac{\Delta t}{\varepsilon}} \right)^n y^0
$$

ce qui est inconditionnellement stable quelque soit la valeur de $\Delta t$ et de $\varepsilon$. Par conséquent nous utiliserons un schéma d'Euler implicite en temps dans un premier temps pour tester et valider nos différents schémas sur le terme de transport.

### Schéma Runge-Kutta d'ordre 3

> Obligé d'utiliser du RK3 avec du WENO à cause de [@weno_time]

Le schéma en temps se résout de manière indépendante du schéma d'advection, par conséquent il s'agit d'une simple équation différentielle ordinaire que nous écrirons\ :

$$
  \frac{\mathrm{d}u}{\mathrm{d}t}(t) = L(u(t),t)
$$

> RK3... on a les équations suivante dans [@ssp_rk3]

$$
  \begin{aligned}
    u^{(1)} &= u^n + \Delta t L(u^n,t^n) \\
    u^{(2)} &= \frac{3}{4}u^n + \frac{1}{4}u^{(1)} + \frac{1}{4}\Delta t L(u^{(1)},t^n+\Delta t) \\
    u^{n+1} &= \frac{1}{3}u^n + \frac{2}{3}u^{(2)} + \frac{2}{3}\Delta t L(u^{(2)},t^n+\frac{1}{2}\Delta t)
  \end{aligned}
$$

Dans le cadre du modèle *micro-macro* par exemple, on aura $u=\mathcal{M}_{[f]}+g$ dans la partie *micro* sans terme de collision.

#### Application à un modèle cinétique avec collisions

Au sein du modèle *micro-macro*, la partie *micro* fait intervenir un terme de collision : $\frac{1}{\varepsilon}g$, ce terme empêche d'utiliser directement une autre discrétisation en temps que le schéma Euler implicite ou explicite. Or en proposant de l'ordre élevé en espace il devient intéressant, voir indispensable, de monter l'ordre en temps, plus d'information dans [@weno_time]. Il est nécessaire de modifier la formulation du modèle *micro* pour faire intervenir ce type de discrétisation.

Nous rappelons le modèle *micro* :

$$
  \partial_t g + (I-\Pi)(v\partial_x(\mathcal{M}_{[f]}+g) + E\partial_v(\mathcal{M}_{[f]}+g)) = -\frac{1}{\varepsilon}g
$${#eq:rk3:micro0}

En remarquant que :

$$
  \partial_t g+\frac{1}{\varepsilon} = e^{-\frac{t}{\varepsilon}}\partial_t\left(e^{\frac{t}{\varepsilon}}g\right)
$$

On pose donc $\zeta = e^{\frac{t}{\varepsilon}}g$, l'équation [!eq:rk3:micro0] devient donc :

$$
  \partial_t \zeta +(I-\Pi)(v\partial_x(\zeta+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]})+E\partial_v(\zeta+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]})) = 0
$$

Il devient donc possible d'appliquer une discrétisation type Runge-Kutta d'ordre 3, avec :

$$
  L(u,t) = -(I-\Pi)(v\partial_x(u+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]})+E\partial_v(u+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]}))
$$

## Schémas d'advection d'ordre élevé

Il est primordial d'utiliser des schémas d'ordre élevé pour le terme de transport pour : capturer les forts gradients en diminuant la viscosité numérique ; utiliser moins de points lors de la simulation. Pour ces raisons nous allons présenter deux schémas d'ordre élevé permettant de résoudre une part des problèmes.

### Schéma compact

> Présentation du schéma, mesure de l'ordre (explication de la méthode d'obtention de l'ordre), et différents cas tests

> Dire à un moment que ça vient de [@despres], ou [@Boyer:2014aa]

On présente ici la résolution d'une équation d'advection linéaire\ :

$$
  \partial_t u + a \partial_x u = 0
$$

Dans un premier temps nous présenterons uniquement le cas d'un transport à vitesse $a$ positive. Un schéma linéaire différence finies avec un *stencil* de taille $r+s+1$ peut s'écrire de manière générale comme\ :

$$
  u_i^{n+1} = \sum_{k=-r}^s \gamma_k u_{i+k}^n
$$

où $\gamma_k$ est un coefficient dépendant du nombre CFL $\nu = a\frac{\Delta t}{\Delta x}$.

L'erreur de consistance du schéma, au sens des différences finies, est définie par\ :

$$
  R_i^n = u(t^{n+1},x_i) - \sum_{k=-r}^s \gamma_k u(t^n,x_{i+k})
$$

on y reconnait la solution exacte en $x_i$ à l'instant $t^{n+1}$ : $u(t^{n+1},x_i)$ ainsi que l'approximation que l'on en fait par le biais d'un schéma aux différences finies : $\sum_{k=-r}^s \gamma_k u(t^n,x_{i+k})$.


> Dans le contexte des volumes finis on peut aussi écrire un schéma de la même forme. Le lien depuis les différences finies se fait en considérant le flux des différences finies comme une approximation du flux sur les bords du volumes de contrôle, auquel on ajoute un limiteur de flux. Cette étape laisse place à de nombreux choix quand au limiteur de pente : centré, décentrée amont ou aval, *minmod*, *superbee*, etc. Le flux ainsi présenté dans le formalisme des volumes finis sera directement celui calculé dans [@despres].

#### Choix du flux

Avec cette écriture nous pouvons généraliser plusieurs flux selon le choix du couple $(r,s)$\ :

* Le schéma décentré amont, ou *upwind*\ :

  $$
    u_{i+\frac{1}{2}}^n = u_i^n
  $$

* Une combinaison de *Lax-Wendroff* et de *Beam-Warming* $(1-\alpha )LW + \alpha BW$ avec $\alpha = \frac{1+\nu}{3}$\ :

  $$
    u_{i+\frac{1}{2}}^n = u_i^n + \frac{2-\nu}{6}(1-\nu)(u_{i+1}^n-u_{i}^n) + \frac{1+\nu}{6}(1-\nu)(u_i^n-u_{i-1}^n)
  $$

* On peut aussi trouver un schéma à 6 points d'ordre 5, qui est celui que nous allons utiliser\ :

  $$
    \begin{aligned}
      u_{i+\frac{1}{2}}^n = & \ u_{i+2}^n + \frac{\nu+3}{2}(u_{i+1}^n-u_{i+2}^n) + \frac{(2+\nu)(1+\nu)}{6}(u_i^n - 2u_{i+1}^n + u_{i+2}^n) \\
                          & + \frac{(2+\nu)(1+\nu)(\nu-1)}{24}(u_{i-1}^n - 3u_{i}^n + 3u_{i+1}^n - u_{i+2}^n) \\
                          & + \frac{(2+\nu)(1+\nu)(\nu-1)(\nu-2)}{120}(u_{i-2}^n - 4u_{i-1}^n + 6u_{i}^n - 4u_{i+1}^n + u_{i+2}^n)
    \end{aligned}
  $$

#### Obtention de l'ordre
 
La solution exacte d'un problème de transport à vitesse $a$ constante est connue. Nous allons donc partir de ce problème, le résoudre sur un premier maillage et en calculer l'erreur ; puis répéter l'opération sur un maillage plus fin.

##### Calcul à pas de temps fixe

Pour être certain de ne pas prendre en compte l'erreur en temps dans le calcul de l'erreur, il est possible de résoudre le problème sur un seul pas de temps toujours identique. Ainsi le seul paramètre modifié d'une simulation à l'autre est le raffinage du maillage et on observera que l'erreur en espace.

![Mesure de l'ordre sur un seul pas de temps](img/ordre.png)

|   m | $\log(\Delta x)$ | $log(\Delta e_1)$ | $log(\Delta e_{\infty})$ | Ordre partiel |
|-----|------------------|-------------------|--------------------------|---------------|
|  20 |                  |                   |                          |               |
|  40 |                  |                   |                          |               |
|  60 |                  |                   |                          |               |
|  80 |                  |                   |                          |               |
| 100 |                  |                   |                          |               |

  : Erreur et ordre sur un seul pas de temps $\Delta t = \frac{2\pi}{100}$

##### Calcul à nombre de CFL constant

Il est intéressant de faire une simulation sur plusieurs pas de temps pour amplifier la visibilité de l'ordre du schéma ; l’inconvénient est que l'erreur du schéma temporel, potentiellement plus élevée, empêche d'observer l'erreur dû au schéma spatial sans choisir un pas de temps arbitrairement très faible.

![Mesure de l'ordre sur plusieurs itérations](img/ordre.png)

|   m | $\log(\Delta x)$ | $log(\Delta e_1)$ | $log(\Delta e_{\infty})$ | Nombre d'itérations | Ordre partiel |
|-----|------------------|-------------------|--------------------------|---------------------|---------------|
|  20 |                  |                   |                          |                     |               |
|  40 |                  |                   |                          |                     |               |
|  60 |                  |                   |                          |                     |               |
|  80 |                  |                   |                          |                     |               |
| 100 |                  |                   |                          |                     |               |
  
  : Erreur et ordre au temps $t_1 = 0.1$

|   m | $\log(\Delta x)$ | $log(\Delta e_1)$ | $log(\Delta e_{\infty})$ | Nombre d'itérations | Ordre partiel |
|-----|------------------|-------------------|--------------------------|---------------------|---------------|
|  20 |                  |                   |                          |                     |               |
|  40 |                  |                   |                          |                     |               |
|  60 |                  |                   |                          |                     |               |
|  80 |                  |                   |                          |                     |               |
| 100 |                  |                   |                          |                     |               |
   
  : Erreur et ordre au temps $t_2 = 1$

### Schéma WENO

> Présentation du schéma, mesure de l'ordre (explication de la méthode d'obtention de l'ordre), et différents cas tests

> Introduire WENO en citant [@weno] ou [@icase], dire qu'une autre interpolation est possible pour des problèmes particulier comme Vlasov-Poisson : [@banks]

WENO pour *weighted essentially non-oscillatory* est une famille de schémas numériques qui se généralise facilement à l'ordre élevé sans pour autant provoquer d'oscillations. L'idée des schémas WENO est d'effectuer plusieurs interpolations polynomiales lagrangiennes sur des *stencils* incluant le point à évaluer, pondérées pour limiter les oscillations. La méthode que nous allons présenter ici est un schéma WENO d'ordre 5.

> Faire un schéma où on remonte une courbe caractéristique et dire que le problème se "limite" à un problème d'interpolation, et que pour limiter les oscillations d'une interpolation polynomiale d'ordre élevé on en fait 3 d'ordre moins élevé, que l'on pondère pour réduire encore plus le risque oscillant.

Pour présenter le schéma nous nous intéressons uniquement au terme de transport selon $x$, les résultats seront simplement à transposer dans la direction $v$ pour le second terme d'advection. De plus pour alléger les notations, nous nous placerons à un temps $t^n$. Nous souhaitons approximer $\partial_x(vf)_{|x=x_i}$, dans un premier temps uniquement pour $v_k >0$ :

$$
  \partial(vf)_{|x=x_i,v=v_k} \approx \frac{1}{\Delta x}(\hat{f}_{i+\frac{1}{2},k} - \hat{f}_{i-\frac{1}{2},k})
$$

où $\hat{f}_{i,k}$ est une approximation de $(vf)_{i,k}$ et $\hat{f}_{i+\frac{1}{2},k}$ est le flux numérique. Dans un premier temps nous allons distinguer les cas $v_k >0$ et $v_k <0$ en écrivant $\hat{f}$ comme :

$$
  \hat{f}_{i,k} = \hat{f}_{i,k}^+ + \hat{f}_{i,k}^-
$$

où :

* $\hat{f}_{i,k}^+ = v_k^+f_{i,k} = \max(v_k,0)f_{i,k}$
* $\hat{f}_{i,k}^- = v_k^-f_{i,k} = \min(v_k,0)f_{i,k}$

Chaque flux numérique est donnée par la somme pondérée de 3 approximations sur 3 *stencils* différents :

$$
  \begin{aligned}
    \hat{f}_{i+\frac{1}{2},k}^+ =\,&w_0^+\left(\frac{2}{6}f_{i-2,k}^+ - \frac{7}{6}f_{i-1,k}^+ + \frac{11}{6}f_{i,k}^+\right)
                        +   w_1^+\left(-\frac{1}{6}f_{i-1,k}^+ + \frac{5}{6}f_{i,k}^+   +  \frac{2}{6}f_{i+1,k}^+\right) \\
                        +\,&w_2^+\left( \frac{2}{6}f_{i,k}^+   + \frac{5}{6}f_{i+1,k}^+ -  \frac{1}{6}f_{i+2,k}^+\right)
  \end{aligned}
$$

et

$$
  \begin{aligned}
  \hat{f}_{i+\frac{1}{2},k}^- =\,&w_2^-\left(-\frac{1}{6}f_{i-1,k}^- + \frac{5}{6}f_{i,k}^-   + \frac{2}{6}f_{i+1,k}^-\right)
                        +   w_1^-\left( \frac{2}{6}f_{i,k}^-   + \frac{5}{6}f_{i+1,k}^- - \frac{1}{6}f_{i+2,k}^-\right) \\
                        +\,&w_0^-\left(\frac{11}{6}f_{i+1,k}^- - \frac{7}{6}f_{i+2,k}^- + \frac{2}{6}f_{i+3,k}^-\right)
  \end{aligned}
$$

Les poids non linéaires $w_{n}^{\pm}$ sont des fractions rationnelles données par :

$$
  w_{n}^{\pm} = \frac{\tilde{w}_{n}^{\pm}}{\sum_{m=0}^2 \tilde{w}_{m}^{\pm} } \,, \quad \tilde{w}_{n}^{\pm} = \frac{\gamma_n}{(\epsilon + \beta_{n}^{\pm})^2}
$$

avec les poids linéaires $\gamma_{n}$ donnés par :

$$
  \gamma_{0} = \frac{1}{10} \,, \quad \gamma_{1} = \frac{3}{5}\,,\quad \gamma_{2} = \frac{3}{10}
$$

et les indicateurs de continuités $\beta_n^{\pm}$ donnés par :

$$
 \begin{aligned}
   \beta_0^+ &= \frac{13}{12}(f^+_{i-2,k} -2f^+_{i-1,k} + f^+_{i  ,k})^2 + \frac{1}{4}(f^+_{i-2,k} - 4f^+_{i-1,k} + 3f^+_{i,k})^2 \\
   \beta_1^+ &= \frac{13}{12}(f^+_{i-1,k} -2f^+_{i  ,k} + f^+_{i+1,k})^2 + \frac{1}{4}(f^+_{i-1,k} - f^+_{i+1,k})^2 \\
   \beta_2^+ &= \frac{13}{12}(f^+_{i  ,k} -2f^+_{i+1,k} + f^+_{i+2,k})^2 + \frac{1}{4}(3f^+_{i,k} - 4f^+_{i+1,k} + f^+_{i+2,k} )^2 
 \end{aligned}
$$

et

$$
 \begin{aligned}
   \beta_0^- &= \frac{13}{12}(f^-_{i+1,k} -2f^-_{i+2,k} + f^-_{i+3,k})^2 + \frac{1}{4}(3f^-_{i+1,k} - 4f^-_{i+2,k} + f^-_{i+3,k})^2 \\
   \beta_1^- &= \frac{13}{12}(f^-_{i  ,k} -2f^-_{i+1,k} + f^-_{i+2,k})^2 + \frac{1}{4}(f^-_{i,k} - f^-_{i+2,k})^2 \\
   \beta_2^- &= \frac{13}{12}(f^-_{i-1,k} -2f^-_{i  ,k} + f^-_{i+1,k})^2 + \frac{1}{4}(f^-_{i,k} - 4f^-_{i,k} + 3f^-_{i+1,k})^2
 \end{aligned}
$$


et enfin, $\epsilon$ est un paramètre pour prévenir que le dénominateur soit égal à $0$ ; il est généralement pris à $\epsilon = 10^{-6}$ (dans [@weno]) ou $\epsilon = 10^{-5}\times\max_{i,k} v^0_k f^0_{i,k}$ (dans [@qiu]).

On a ainsi définit l'approximation du terme de transport à l'aide d'un schéma WENO pour toute vitesse $v_k$ :

$$
  \partial_x (vf)_{|x=x_i,v=v_k} \approx \frac{1}{\Delta x}\left[ (\hat{f}^+_{i+\frac{1}{2},k} - \hat{f}^+_{i-\frac{1}{2},k}) + (\hat{f}^-_{i+\frac{1}{2},k} - \hat{f}^-_{i-\frac{1}{2},k}) \right] 
$$

### Obtention de l'ordre

### Test de viscosité

> Cas où l'on fait tourner 12 fois un pacman : [@qiu2011]

> Cas où l'on fait tourner une gaussienne, comparer entre Euler et RK3 (apparition d'une *vague de traine* dans le cas Euler)


## Condition CFL

Pour calculer le nombre de CFL nous allons dans un premier temps nous intéresser au modèle cinétique [!eq:cine], la description microscopique du modèle *micro-macro* est similaire et implique la même condition. Nous utiliserons le schéma d'Euler implicite pour la discrétisation en temps, et pour simplifier les notations nous n'utiliserons qu'un schéma *upwind* en espace, encore une fois le champ électrique est négligé dans cette partie.

$$
  \frac{f_{i,k}^{n+1}-f_{i,k}^n}{\Delta t} + v\frac{f_{i+\frac{1}{2},k}^n - f_{i-\frac{1}{2}}}{\Delta x} = \frac{1}{\varepsilon}(\mathcal{M}_{[f^{n+1}]} - f_{i,k}^{n+1})
$$

Ce qui peut se réécrire, pour une interprétation itérative\ :

$$
  f_{i,k}^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ f_{i,k}^n - \frac{\Delta t}{\Delta x}(f_{i+\frac{1}{2},k}^n - f_{i-\frac{1}{2},k}^n) + \frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k} \right]
$$


Il n’est pas possible de calculer directement la CFL du schéma en $f_{i,k}$ nous allons donc utiliser l’analyse de von Neumann pour résoudre ce problème. Pour cela, posons $f_{j,k}^n = e^{i\kappa j\Delta x}A^n$, l’indice d’espace est dorénavant $j$ et $i$ est le nombre imaginaire tel que $i^2 = -1$. Nous pouvons donc facilement exprimer $f_{j-1,k}^n$ directement en fonction de $f_{j,k}^n$\ :

$$
  f_{j-1,k}^n = e^{i\kappa (j-1)\Delta x}A^n = f_{j,k}^n e^{-i\kappa\Delta x}
$$

Cela permet donc d’exprimer $f_{j,k}^{n+1}$ en fonction uniquement de $f_{j,k}^n$, et donc d’obtenir une formule de récurrence du type\ :

$$
  f_{j,k}^{n+1} = \mathcal{A} f_{j,k}^n = (\mathcal{A})^{n+1} f_{j,k}^0
$$

On remarque de suite qu’il est nécessaire pour que le schéma converge d’avoir $|\mathcal{A}| \leq 1$. Pour trouver cette formule de récurrence nous travaillerons sur une version simplifiée du schéma, en particulier nous ne considérerons qu’un schéma upwind pour le terme de transport au lieu d’un schéma compact d’ordre élevé, et nous négligerons l’impact de la maxwellienne.

On part du schéma simplifié sur $f$\ :

$$
  f_{j,k}^{n+1} = \frac{\varepsilon}{\varepsilon + \Delta t}\left[ f_{j,k}^n - \frac{\Delta t}{\Delta x}v_k(f_{j,k}^n - f_{j,k}^ne^{-i\kappa\Delta x} )  \right]
$$

Ce que l’on peut écrire sous la forme\ :

$$
  f_{j,k}^{n+1} = f_{j,k}^n\frac{\varepsilon}{\varepsilon + \Delta t}\left[ 1-\frac{\Delta t}{\Delta x}v_k(1-e^{-i\kappa\Delta x}) \right]
$$

On obtient bien la forme désirée $f_{j,k}^{n+1} = \mathcal{A} f_{j,k}$, pour simplifier l’étude de $\mathcal{A}$ écrivons ce terme sous la forme\ :

$$
  \mathcal{A} = \frac{\varepsilon}{\varepsilon + \Delta t} \mathcal{B}
$$

Étudions $|\mathcal{B}|^2$\ :

* $\mathrm{Im}(\mathcal{B}) = -\frac{\Delta t}{\Delta x}v_k\sin(\kappa \Delta x)$
* $\mathrm{Re}(\mathcal{B}) = 1-\frac{\Delta t}{\Delta x}v_k(1-\cos(\kappa \Delta x)$

D’où\ :

$$
  \begin{aligned}
    |\mathcal{B}|^2 &= \mathrm{Re}(\mathcal{B})^2 + \mathrm{Im}(\mathcal{B})^2 \\
                    &= 1 + 2(1-\cos(\kappa\Delta x))\Delta t \left[ \frac{\Delta t}{\Delta x^2}v_k^2 - \frac{v_k}{\Delta x}\right] \\
  \end{aligned}
$$

On souhaite $|\mathcal{A}|^2 = \left(\frac{\varepsilon}{\varepsilon + \Delta t}\right)^2|\mathcal{B}|^2 \leq 1$ c’est-à-dire\ :

$$
  |\mathcal{B}|^2 \leq \left(\frac{\varepsilon + \Delta t}{\varepsilon}\right)^2
$$

Ce que l’on peut reformuler comme suit, pour majorer $\Delta t$\ :

$$
    \Delta t \left[(1-\cos(\kappa\Delta x))\frac{v^2}{\Delta x^2} - \frac{1}{2\varepsilon^2}\right] \leq \frac{1}{\varepsilon} + (1-\cos(\kappa\Delta x))\frac{v}{\Delta x}
$$

Cette inégalité doit être vérifiée pour toute vitesse $v_k$ nous allons donc majorer par $v_{\textrm{max}}$, de même quelque soit le nombre d’onde $\kappa$ nous allons donc majorer $1-\cos(\kappa\Delta x)=2\sin^2(\frac{\kappa\Delta x}{2})$ par 2. Ce qui nous donne après simplification\ :

$$
  \Delta t (2v\varepsilon - \Delta x) \leq 2\Delta x \varepsilon
$$

Il est nécessaire d’étudier le signe de $2v\varepsilon - \Delta x$\ :

* $2v\varepsilon - \Delta x < 0$ alors $\Delta t >0$ ce qui est toujours vérifié. Cette condition est vérifiée si\ :
  
  $$
    \varepsilon < \frac{\Delta x}{2v}
  $$

  Avec classiquement $\Delta x \sim 10^{-2}$ et $v\sim 18$ ce qui nous donne $\varepsilon \sim 10^{-3}$.
* $2v\varepsilon - \Delta x > 0$ alors\ :

  $$
    \Delta t \leq \frac{2\Delta x \varepsilon}{2v\varepsilon - \Delta x}
  $$

En étudiant la fonction\ :

$$
  \mathscr{C}:\varepsilon\mapsto\frac{ \frac{\Delta x}{v} \varepsilon}{\varepsilon - \frac{1}{2}\frac{\Delta x}{v}}
$$

> TODO: tracer cette fonction

on trouve que cette fonction est décroissante et a pour limite $\frac{\Delta x}{v}$, nous utiliserons donc une fraction de cette limite comme base de temps. On retrouve aussi le pôle $\frac{\Delta x}{2v}$ qui correspond au changement de condition pour obtenir $\Delta t$.


## Résolution du problème de Poisson

Pour résoudre le problème de Poisson en condition aux bords périodiques nous utiliserons une méthode de transformée de Fourrier. Le champ électrique est une fonction de la densité $\rho(t^n)$, il est donc nécessaire de résoudre le problème de Poisson à chaque pas de temps.

Notons $\rho^\prime = \rho -1$, il suffit de calculer la transformée de Fourrier de $\rho\prime$ pour résoudre le problème [!eq:poisson] dans le contexte spectral\ :

$$
  i\kappa \hat{E}_{\kappa} = \hat{\rho}^\prime_{\kappa}
$$

où $\kappa$ est l'indice du coefficient de Fourrier et $i$ le nombre complexe tel que $i^2 = -1$. Ainsi on définit pour tout $\kappa$ le coefficient de Fourrier\ :

* $\hat{E}_{\kappa} = -i\displaystyle\frac{\hat{\rho}^\prime_{\kappa}}{\kappa}$ si $\kappa \neq 0$
* $\hat{E}_0 = 0$ car $E_f$ est à moyenne nulle d'après la condition [!eq:poisson:condi]

Ainsi tous les coefficients de Fourrier de $E_f$ sont calculés, il suffit d'effectuer la transformée inverse pour trouver le résultat souhaité.




# Application pour les gaz rares

> Partie numérique, on présente l'application de la partie 2 sur les modèles de la partie 1. Pas de section pour le modèle Euler car supposé provenant du code de référence. Conclusion de la partie sur un comparatif des performances (temps et erreur) des différents schémas et modèles.


## Cinétique

> Algorithme, propriété de la température et conservation des variables intensives, calcul de CFL, tests numériques (périodique et Neumann) comparaison avec Euler

Dans un premier temps, pour pouvoir comparer les résultats avec un code de simulation des équations d'Euler, on étudie le modèle sans champ électrique $E$, c'est-à-dire le modèle suivant\ :

$$
  \partial_t f + v\partial_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]}-f)
$$

La résolution nécessite une grille en espace et en vitesse, c'est-à-dire un maille de l'espace des phases. On note $f_{i,k}^n$ l'approximation $f(t^n,x_i,v_k)$. On suppose $f_{i,k}^n$ donnée par l'itération précédente, le calcul de la nouvelle itération s'effectue schématiquement comme suit\ :

1. On calcule le flux numérique $f_{i+\frac{1}{2},k}^n$ du schéma en espace souhaité (*upwind*, schéma compact ou WENO)\ :

  $$
    f_{i+\frac{1}{2},k}^n \gets ((f_{j,k}^n)_{j\in[i-2;i+2]},v_k)
  $$

2. On calcule le flux numérique $F_{i+\frac{1}{2}}^n$ pour le schéma sur $U$ à partir du flux $f_{i+\frac{1}{2},k}^n$\ :
  
  $$
    F_{i+\frac{1}{2}}^n \gets \sum_k v_km(v_k)f_{i+\frac{1}{2},k}^n\Delta v
  $$

3. On appelle le schéma sur $U$\ :
  
  $$
    U_i^{n+1} \gets U_i^n - \frac{\Delta t}{\Delta x}(F_{i+\frac{1}{2}}^n - F_{i-\frac{1}{2}}^n)
  $$

4. On calcule les variables intensives $(\rho_i^{n+1},u_i^{n+1},T_i^{n+1})$\ :

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

5. On calcule la maxwellienne $(\mathcal{M}_{[f^{n+1}]})_{i,k}$ en tout point $(i,k)$ de l’espace des phases\ :

  $$
    (\mathcal{M}_{[f^{n+1}]})_{i,k} = \frac{\rho_i^{n+1}}{\sqrt{2\pi T^{n+1}_i}}\exp\left(-\frac{1}{2}\frac{|v_k - u_i^{n+1} |^2}{T^{n+1}_i} \right)
  $$

6. On approxime $f^{n+1}_{i,k}$ via le schéma avec le terme de transport et de diffusion :
  
  $$
    f^{n+1}_{i,k} = \frac{1}{1+\frac{\Delta t}{\varepsilon}} \left[ f^n_{i,k} - \frac{\Delta t}{\Delta x}v_k (f^n_{i+\frac{1}{2},k} - f^n_{i-\frac{1}{2},k}) +\frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k}  \right]
  $$

7. On corrige l’approximation $U_i^{n+1}$ via le calcul du moment de $f^{n+1}_{i,\cdot}$ :

  $$
    U_i^{n+1} \gets \sum_k m(v_k)f_{i,k}^{n+1} \Delta v
  $$


### Propriété sur la température

Le calcul de la maxwellienne $|\mathcal{M}_{[f^{n}]}$ nécessite l'extraction de la racine carré de la température $(T_i)_i$ à tout temps $t^n$, or celle-ci est uniquement définit par\ :

$$
  T_i^n = \frac{(U_3)_i^n}{(U_1)_i^n} - \left(\frac{(U_2)_i^n}{(U_1)_i^n}\right)^2
$$

Rien ne semble assurer la positivité de cette valeur, condition nécessaire pour assurer la validité des calculs. En utilisant la définition du vecteur $U_i^n$ on peut reformuler $T_i^n$ comme\ :

$$
  T_i^n = \frac{ \sum_k |v_k|^2f_{i,k}^n\Delta v }{ \sum_k f_{i,k}^n\Delta v } - \left(\frac{ \sum_k v_k f_{i,k}^n\Delta v}{ \sum_k f_{i,k}^n\Delta v }\right)^2
$$

Pour que la température reste positive il suffit de vérifier\ :

$$
  \sum_k |v_k|^2 f_{i,k}^n\Delta v \sum_k f_{i,k}^n\Delta v - \left( \sum_k v_k f_{i,k}^n\Delta v \right)^2 \geq 0
$$

Or, en appliquant l’inégalité de Cauchy-Schwarz discrète sur le premier terme avec les fonctions $v_k\sqrt{f_{i,k}^n}$ et $\sqrt{f_{i,k}^n}$ on obtient\ :

$$
  \sum_k (v_k\sqrt{f_{i,k}^n})^2\Delta v \sum_k (\sqrt{f_{i,k}^n})^2\Delta v \geq \left| \sum_k v_k \sqrt{f_{i,k}^n}\sqrt{f_{i,k}^n} \Delta v \right|^2
$$

C’est à dire que l’on a bien\ :

$$
  \sum_k |v_k|^2 f_{i,k}^n \Delta v \sum_k f_{i,k}^n \Delta v \geq \left( \sum_k v_k f_{i,k}^n \Delta v \right)^2
$$

Ce qui garantit bien la positivité de $T_i^n$ en tout point $x_i$ de l’espace et pour tout temps $t^n$.

### Propriétés de conservations

On résout le modèle suivant\ :

$$
  \partial_t f + v\partial_x f = \frac{1}{\varepsilon}(\mathcal{M}-f)
$$

En calculant les moments et en intégrant en $x$ on obtient\ :

$$
  \iint_{\Omega \times \mathbb{R}^d} m(v)(\partial_t f + v\partial_x f)\,\mathrm{d}x\mathrm{d}v = \frac{1}{\varepsilon}\iint_{\Omega \times \mathbb{R}^d} m(v)(\mathcal{M}_{[f]}-f)\,\mathrm{d}x\mathrm{d}v
$$

Or les moments de $\mathcal{M}$ et de $f$ sont égaux. De plus le second terme du premier membre vaut zéro car par échange de la dérivée sous le signe somme on dérive en $x$ une intégrale sur $x$ et $v$ qui ne dépend donc plus de $x$, on obtient finalement\ :

$$
  \frac{\mathrm{d}}{\mathrm{d}t}\int_{\Omega} U(t,x)\,\mathrm{d}x = 0
$$

Écrit de façon discrète cela équivaut à\ :

$$
  \sum_i U^n_i \Delta x = c
$$

où $c$ est une constante indépendante de $t$. On peut aussi comparer ce résultat à\ :

$$
  \sum_{i,k} m(v_k)f^n_{i,k} \Delta x \Delta v
$$

On constate bien une conservation de ces valeurs. La légère évolution de ces valeurs est due à la mauvaise approximation de la maxwellienne.

> TODO: insérer ici un graph prouvant ces dires

### Cas tests

#### Conditions aux bords périodiques

#### Conditions aux bords de Neumann

> Tube à choc de Sob

## Micro-macro

> Algorithme,tests numériques (périodique et Neumann), comparaison avec Euler et cinétique, évocation du temps de calcul (repris dans le récap)

### Cas tests

#### Conditions aux bords périodiques

#### Conditions aux bords de Neumann

#### Milieu non homogène : $\varepsilon = \varepsilon(x)$

> Cas test dans [@filbet]


## Approximation $h(t,x)$

> Différents tests avec $h(x)$ (fonction porte, et trapézoïdale), puis obtention de $h(t,x)$ avec $x_s$ et $x_e$.

> Dans [@dimarco] la fonction $h(t,x)$ est calculée à partir de $\langle m(v_k)g_{i,k}^n\rangle_v$ donc obligé de calculer en tout point à tout instant. Dans [@filbet] il y a aussi un principe multi-échelle mais le critère est calculé sur chaque cellule à chaque instant, donc pas de gain non plus. Utiliser $x_s$ et $x_e$ demande une préparation en amont (avoir une idée de ce que cela va devenir) mais permet de réduire le temps de calcul.

## Comparaison

> Temps de calcul des différents modèles, et erreur par rapport au code de référence : Euler, et avantage qualitatif des différents modèles (plasma avec $\varepsilon \not\to 0$ et champ électrique : impossible avec simple approximation Euler)


# Application pour les plasma

> C'est dans cette partie qu'on a vraiment besoin des tests 2D et qu'on introduit dans un champ électrique

## Modèle cinétique

> Programme de référence

### Cas proche de l'équilibre

> Landau

### Cas éloigné de l'équilibre

> Double faisceau


## Modèle *micro-macro*

> Modèle hybride basé sur le modèle cinétique, donc comparatif aux résultats précédents

> Introduction de $h(t,x)$


# Liste des figures à refaire

Pour chaque simulation consever les paramètres de simulation : entrée, $\varepsilon$, $\Delta x$, $\Delta v$, $\Delta t$, $nx$, $nv$, $T_f$ 

* Ordre en 1D et 2D :
  - WENO
  - Schéma compact
* Simulation cinétique et micro-macro des cas tests usuels sans champ électrique, comparatif entre les schémas du terme de transport :
  - périodique
  - Neumann (tube de Sob)
* Simulation cinétique et micro-macro avec $\varepsilon(x_i)$
* Simulation cas Neumann avec $h(t,x)$
  - Pour justifier le $h(t,x)$ tracer des coupes du cas Neumann : $f(t_f,x=\{2,7,10\},v)$ et voir une maxwellienne dans le cas fluide et une maxwellienne plus une perturbation dans le cas cinétique (proche du choc)
* Évolution de la masse au cours du temps sur un cas simple (pour prouver que cela a été vérifié)
* tester WENO en temps long sur la rotation d'une gaussienne avec Euler et RK3 (apparition d'une trainée)
* Cas tests de viscosité (rotation d'un pacman)
* $log||E||_2 = f(t)$ sur plusieurs cas tests

