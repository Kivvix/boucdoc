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


# Introduction


# Présentation des modèles

Dans cette partie, nous présenterons différents modèles mathématiques utilisés dans la littérature pour décrire un système de particules, potentiellement chargées. Ces modèles vont de la description particulaire, qui est la plus précise, jusqu'à la description hydrodynamique, en passant par la description cinétique. 

## Modèle microscopique particulaire

Les modèles microscopiques fonctionnent sur le principe de l'étude newtonienne de particules. Un tel modèle cherche à déterminer la trajectoire de chaque particule par le principe fondamental de la dynamique, d'où le système\ :

$$
  \begin{cases}
    \dot{x}_i (t) = v_i(t) \\
    \dot{v}_i (t) = \displaystyle\sum_{j \atop j \ne i} F_{ji}(t,x_i(t))
  \end{cases}
$$

où $x_i(t)$ et $v_i(t)$ représentent respectivement la position et la vitesse au temps $t \geq 0$ de la $i$-ème particule avec $i=1,\dots,n$ où $n$ est le nombre de particules. $F_{ji}$ représente la force exercée par la particule $j$ sur $i$, cela permet d'expliquer la contrainte de sommation $j \ne i$. La force considérée dans ce modèle peut être l'interaction coulombienne pour représenter l'interaction électrostatique entre particules, ou la force gravitationnelle pour représenter l'interaction à grande distance entre masses.

La variable de base dans le modèle est le temps $t$ ; à chaque pas de temps on calcule la somme des forces pour obtenir l'accélération. La vitesse puis la position s'obtiennent par intégration successive.

Ce modèle est très coûteux en temps de calcul puisqu'il possède une complexité algorithmique en $\mathcal{O}(2^n)$. L'utilisation de ce type de modèle est inenvisageable dès que le nombre de particules $n$ atteint la centaine. Dans le cadre de l'étude des plasmas, le nombre $n$ de particules en interaction est voisin du nombre d'Avogadro $\mathcal{N}_A \approx 6,02\cdot 10^{23}$.

Une approximation de ce modèle est parfois utilisé à l'aide d'une représentation arborescente de l'espace via un *quadtree*, ou *$kd$-tree* par exemple ; cela permet de négliger les interactions à plus longue distance. C'est ce qui est par exemple utilisé dans des simulations de galaxies, ou dans des moteurs de collision comme celui du jeu vidéo *Doom*.


## Modèle cinétique

Le principe du modèle cinétique est de proposer une description intermédiaire entre le modèle microscopique et macroscopique. On représente les particules dans l'espace des phases $(x,v)$, où $x \in \Omega \subset \mathbb{R}^d$ désigne la position et $v \in \mathbb{R}^d$ la vitesse, avec $d=1,2,3$ la dimension du problème.

Nous n'étudions pas chaque particule individuellement mais une valeur statistique qu'est la fonction de distribution de particules dans l'espace des phases notée $f$. La grandeur $f(t,x,v)\mathrm{d}x\mathrm{d}v$ représente la densité de particules dans un volume élémentaire de l'espace des phases $\mathrm{d}x\mathrm{d}v$ centré en $(x,v)$ au temps $t \geq 0$.

L'inconnue $f(t,x,v)$ est alors solution d'une équation de transport dans l'espace des phases à laquelle on ajoute un terme de collision\ :

$$
  \partial_t f + v\cdot\nabla_x f = Q(f)
$${#eq:cine}

où le transport s'effectue à vitesse $v$ dans la direction $x$. $Q(f)$ représente un opérateur quadratique de collision, il modélise les interactions binaires entre particules ; plusieurs expressions sont possibles comme l'opérateur de Boltzmann pour les gaz raréfiés, ou les opérateurs Landau ou BGK par exemple pour le cas des particules chargées.

Les variables de base du problème sont $t$, $x$ et $v$. Une simulation directe du problème complet impose donc de travailler en 7 dimensions : une de temps, et 6 pour l'espace des phases $(x,v)$. Travailler dans un espace de dimension aussi élevée implique des coûts importants en temps de calcul et dans l'utilisation de la mémoire, cela est cependant moins coûteux qu'un modèle microscopique. De plus il est possible de développer des schémas numériques adaptés au problème considéré et réduire le temps de calcul, par exemple via des techniques de décomposition de domaine. En effet un maillage non cartésien permet de ne raffiner que localement le domaine et ainsi réduire le temps de calcul sur certaines régions de l'espace. Mais les contraintes de gestion du maillage nous ont orientés vers une autre alternative.

L'étude théorique se fera en dimension $d /geq 1$ quelconque, mais pour simplifier l'étude, l'implémentation et la visualisation se feront en dimension $d=1$.

> TODO: revoir le paragraphe suivant, redondant avec le reste, mais ajoute quelques détails.

Ce modèle utilise à la manière du modèle macroscopique, une grandeur intégrale ; celle-ci vit dans l'espace des phases ce qui permet d'avoir une description plus précise puisqu'elle prend en compte la répartition des particules en vitesse. La grandeur de travail est une fonction $f$ vivant dans l'espace des phases $(x,v)$. Les variables $(t,x,v)$ vivent dans $[0,T]\times\Omega\times\mathbb{R}^d$, où $\Omega$ est un fermé borné de $\mathbb{R}^d$, la vitesse $v$ n'est *a priori* pas borné par notre modélisation. Ce grand nombre de dimensions implique un nombre important de variables à stocker lors de la simulation numérique du modèle, ainsi qu'un nombre important de boucles pour parcourir toutes les dimensions du problème, le modèle est donc coûteux en temps de calcul ainsi qu'en utilisation de la mémoire.

### Conservation de la masse, de l'impulsion et de l'énergie

> TODO: Revoir ce paragrphe sous forme de théorème + preuve

Les propriétés de l'opérateur de collision $Q(f)$ de l'équation [!eq:cine] impliquent la conservation de la masse, de l'impulsion et de l'énergie lors des collisions\ :

$$
  \int_{\mathbb{R}^d} m(v)Q(f)\,\mathrm{d}v = 0
$$

où $m(v) = ( 1, v , |v|^2 )$. En multipliant [!eq:cine] par $m(v)$, puis en intégrant selon les directions $x$ et $v$ on obtient\ :

$$
  \iint_{\Omega\times\mathbb{R}^d} m(v)(\partial_t f + v\cdot\nabla_x f)\,\mathrm{d}x\mathrm{d}v = \iint_{\Omega\times\mathbb{R}^d}m(v)Q(f)\,\mathrm{d}x\mathrm{d}v
$$

Or les moments de $Q(f)$ sont nuls, et l'intégrale sur tout l'espace de la dérivée en $x$ vaut zéro. On obtient finalement\ :

$$
  \frac{\mathrm{d}}{\mathrm{d}t}\iint_{\Omega\times\mathbb{R}^d} m(v)f(t,x,v)\,\mathrm{d}x\mathrm{d}v = 0
$${#eq:cine:conservation}

La grandeur $f$ représente la densité de particules chargées dans l'espace des phases, donc la grandeur $\iint f(t,x,v)\,\mathrm{d}x\mathrm{d}v$ correspond à la masse totale du système. Les composantes suivantes, calculées dans [!eq:cine:conservation], représentent l'impulsion et l'énergie totale du système. Cette équation garantit la conservation de la masse, de la quantité de mouvement et de l'énergie dans le modèle.

### Équation de Poisson

Dans le contexte de la physique des plasmas, nous étudions le mouvement de particules chargées formant le plasma, c'est-à-dire des électrons et des ions. L'équation de Poisson est un modèle physique de l'évolution du champ électrique $E$ en fonction des particules chargées présentes\ :

$$
  \nabla_x \cdot E = \sum_s q_s \rho_s
$$

avec $q_s$ la charge électrique d'une espèce $s$ de particule, $\rho_s$ la densité de cette même espèce $s$. Dans le cadre du modèle cinétique, $f$ représente la densité d'électrons, seule espèce chargée considérée comme mouvante ; en effet les ions, beaucoup plus lourds, peuvent être considérés comme statique. Le rapport de masse entre la masse du proton et celle de l'électron est d'environ $\mu = \frac{m_p}{m_e} \approx 1\,836$, or les ions considérés ne sont pas nécessairement des ions hydrogènes, composés d'un unique proton. En normalisant les charges électriques, l'équation de Poisson peut se réécrire\ :

$$
  \nabla_x \cdot E = \int_{\mathrm{R}^d} f\,\mathrm{d}v - 1
$${#eq:cine:poisson}

où $f$ est la distribution d'électrons et le terme $1$ représente la densité ionique. En rajoutant le terme de force induit par le champ électrique $E$, l'équation du modèle cinétique [!eq:cine] mène à l'équation de Vlasov\ :

$$
  \begin{cases}
    \partial_t f + v\cdot\nabla_x f + E\cdot\nabla_v f = Q(f) \\
    \nabla_x\cdot E = \int f\,\mathrm{d}v -1
  \end{cases}
$${#eq:cine:vp}

Ce modèle est une équation de transport dans l'espace des phases à vitesse $v$ dans la direction $x$ et $E$ dans la direction $v$ avec un terme de collision $Q(f)$.

## Modèle macroscopique

Les modèles macroscopiques sont très utilisés en mécanique des fluides ; le système d'équations dépend alors de peu de variables physiques pour d'écrire l'état thermodynamique. Ces variables sont condensées en un seul vecteur de variables extensives $U$, mettant en jeu des variables thermodynamiques comme\ :

$$
  (\rho,u,T,\dots)(t,x)
$$

où $\rho$ désigne la densité, $u$ la vitesse moyenne et $T$ la température au temps $t\geq 0$ à la position $x$ ; $U$ vérifie les équations d’Euler\ :

$$
  \partial_t U + \nabla_x\cdot \mathcal{F}(U) = 0
$${#eq:euler}

où la fonction $\mathcal{F}$ désigne le flux.

Les variables de bases du problème sont $t$ et $x$. La simulation n'impose que 4 dimensions, une de temps et 3 d'espace ; donc dans une région se comportant globalement comme un fluide il est privilégié d'utiliser ce type de méthode, moins coûteuse en temps de calcul qu'un modèle microscopique ou cinétique.

Dans le cadre des équations d'Euler, $U$ est défini par\ :

$$
  U = \begin{pmatrix}
    \rho   \\
    \rho u \\
    e
  \end{pmatrix}
$$

où $e$ est l’énergie interne. Le vecteur $U$ vit dans $\mathbb{R}^{d+2}$ car $\rho \in \mathbb{R}$, $e\in\mathbb{R}$ et $u\in\mathbb{R}^d$. Le flux $\mathcal{F}$ est alors défini en dimension $d$ par\ :

$$
  \mathcal{F}(U) = \begin{pmatrix}
    \rho u       \\
    \rho u\otimes u + p \mathbb{I}_d \\
    u(e+p)
  \end{pmatrix}
$$

où $u\otimes u$ désigne le produit tensoriel de $u$ avec lui-même, *i.e.* un simple produit lorsque $d=1$ ou la matrice $(u\otimes u)_{ij} = u_iu_j$ sinon ; $\mathbb{I}_d$ est la matrice identité et la pression $p$ est calculée en fonction des inconnues par la relation\ :

$$
  p = 2(e - \frac{1}{2}\rho |u|^2)
$$

En dimension $d \ne 1$ le flux $\mathcal{F}(U)$ n'est plus un vecteur, mais puisque l'on calcule la divergence du flux : $\nabla_x\cdot\mathcal{F}(U)$, on retrouve bien un vecteur à $d+2$ dimensions. En effet la première et dernière composante sont de simples scalaires, donc leur dérivée est aussi un scalaire ; la seconde composante est une matrice carrée de taille $d$, dont la divergence donne bien un vecteur de taille $d$.


### Ajout du champ électrique

De manière analogue au modèle cinétique, le contexte de l'étude des plasmas nécessite l'ajout d'un second membre à [!eq:euler] :

$$
  \partial_t U + \nabla_x\cdot\mathcal{F}(U) = S(U)
$$

Le terme source $S(U)$ est nul dans le cadre des équations d'Euler en l'absence d'un champ électrique $E$, en présence de celui-ci le terme s'explicite sous la forme suivante\ :

$$
  S(U) = \begin{pmatrix} 0 \\ \rho E \\ 2\rho uE \end{pmatrix}
$$

Le champ électrique $E$ est calculé avec l'équation de Poisson\ :

$$
  \nabla_x \cdot E = \rho -1
$${#eq:macro:poisson}

où $\rho$ représente la densité d'électron, et $1$ la densité ionique. On retrouve bien une définition équivalente à [!eq:cine:poisson] puisque : $\int f(t,x,v)\,\mathrm{d}v = \rho(t,x)$.


## Cinétique vers fluide

Il est possible d'interpréter la description fluide à partir de la description cinétique. Cela permet d'assurer une continuité des modèles entre la description macroscopique et cinétique.

Dans le modèle cinétique [!eq:cine], il est possible de lier la fonction de densité dans l'espace des phases au vecteur de variables extensives $U$ utilisé dans les équations d'Euler via\ :

$$
  U = \int_{\mathbb{R}^d} m(v)f\,\mathrm{d}v = \begin{pmatrix}\rho \\ \rho u \\ \rho|u|^2 + \frac{d}{2}\rho T\end{pmatrix}
$$

où $m(v) = (1 \; v \; |v|^2)^{\mathsf{T}}$, $\rho$ est la densité de particules, $u$ la vitesse moyenne, et $T$ la température. Le vecteur $U$ est de dimension $d+2$ ; en effet la deuxième composante $\rho u$ est un vecteur de dimension $d$ qui s’obtient comme suit\ :

$$
  \rho u = \int_{\mathbb{R}^d} v  f(v)\,\mathrm{d}v
$$

Par la suite nous choisirons l'opérateur de collision BGK dans l'équation [!eq:cine], celui-ci est défini par\ :

$$
  Q(f) = \frac{1}{\varepsilon}(M_{[f]} - f)
$$

où $\varepsilon = \frac{\ell}{L}$ est une donnée du problème physique avec $\ell$ le libre parcours moyen des particules et $L$ la taille du domaine ; $\mathcal{M}_{[f]}$ est la distribution de vitesse maxwellienne définie par\ :

$$
  \mathcal{M}_{[f]} = \frac{\rho}{(2\pi T)^{\frac{d}{2}}}\exp\left(-\frac{|v-u|^2}{2T}\right)
$${#eq:DefM}

Une propriété des opérateurs de collisions est de garantir la conservation de la masse, de l'impulsion et de l'énergie, cela se traduit par l'équation\ :

$$
  \int_{\mathbb{R}^d} m(v)Q(f)\,\mathrm{d}v = 0
$$

Par conséquent, avec l'opérateur de collision BGK cela signifie\ :

$$
  \int_{\mathbb{R}^d} m(v)\mathcal{M}_{[f]}\,\mathrm{d}v = \int_{\mathbb{R}^d} m(v)f(v)\,\mathrm{d}v = U(t.x)
$$

On multiplie l'équation [!eq:cine] par $m(v)$ puis on intègre par rapport à $v$ pour obtenir\ :

$$
  \partial_t U + \nabla_x\cdot\int_{\mathbb{R}^d}vm(v)f\,\mathrm{d}v = 0
$${#eq:cineuler}

Composante par composante l'équation [!eq:cineuler] s'écrit\ :

$$
  \partial_t\begin{pmatrix}U_1 \\ U_2 \\ U_3 \end{pmatrix} + \nabla_x\cdot\begin{pmatrix}U_2\\ U_3 \\ \int v^3f\,\mathrm{d}v \end{pmatrix} = 0
$${#eq:cineulero}

Or quand $\varepsilon \to 0$ on trouve grâce à [!eq:cine] que $f \to \mathcal{M}_{[f]}$ ; on peut donc écrire $f$ comme un développement limité en $\varepsilon$ comme\ :

$$
  f(t,x,v) = \mathcal{M}_{[f]} + \mathcal{O}(\varepsilon)
$$

Ainsi on peut fermer le problème [!eq:cineulero] par une approximation de $\int v^3f\,\mathrm{d}v$ par $\int v^3\mathcal{M}_{[U]}(v)\,\mathrm{d}v = \rho u^3 + 3\rho Tu$. On retrouve alors les équations d'Euler.

En ajoutant un terme dans le développement limité de $f$ en $\varepsilon$ on obtient de manière similaire les équations de Navier-Stokes.

Nous obtenons donc une équivalence entre le modèle cinétique et fluide à la limite $\varepsilon \to 0$. Cette remarque permet de valider nos schémas et d'en vérifier les résultats en les comparant à un simulateur de fluide eulérien.



# Modèles hybrides fluides-cinétiques

Les modèles macroscopiques se déteriorent dans des régions localisées du domaine de calcul ; pour certains problèmes, comme dans les zones de chocs ou les problèmes de couches limites, cette description n'est pas suffisante pour un flux hors d'état d'équilibre. Il n'est pour autant pas nécessaire de résoudre un modèle cinétique sur tout le domaine d'étude, qui est bien plus coûteux en temps de calcul.

Pour tenter d'obtenir un compromis coût numérique, précision, on se propose de suivre une approche hybride fluide-cinétique. Pour cela, nous allons construire un modèle *micro-macro*, décrit dans [@dimarco],  basé sur une décomposition de l'inconnue cinétique $f$ en une partie macroscopique (une distribution maxwellienne) , plus une partie microscopique (l'écart par rapport à l'équilibre thermodynamique). Cette décomposition est similaire à celle décrite dans [@dimarco] ou [@crestetto].

Dans de nombreux cas pratiques, la fonction inconnue $f$ n'est pas trop éloignée de son équilibre maxwellien ; nous pouvons donc décrire $f$ comme une somme\ :

$$
  f = \mathcal{M}_{[f]} + g
$$

avec $\mathcal{M}_{[f]}$ est définie par [!eq:DefM], et où $g$ est l'écart à l'équilibre maxwellien. Or nous avons\ :

$$
  \int_{\mathbb{R}^d} m(v)\mathcal{M}_{[f]}\,\mathrm{d}v = \int_{\mathbb{R}^d} m(v)f\,\mathrm{d}v
$$

nous pouvons en conclure que $\int m(v)g\,\mathrm{d}v =0$. Cette décomposition $f = \mathcal{M}_{[f]}+g$ correspond à une décomposition de $L^2$ selon le noyau de l'opérateur de collision\ :

$$
  L^2 = \ker Q + \text{Im} Q
$$

Cette décomposition peut s'exprimer comme une projection orthogonale $\Pi_f$, d'où la décomposition de $f$\ :

$$
  f = \Pi_f(f) + (I-\Pi_f)(f)
$$

On a donc $\mathcal{M}_{[f]} = \Pi_f(f)$ et $(I-\Pi_f)(f) = g$, où le projecteur $\Pi_f$ est défini dans [@BENNOUNE20083781] par\ :

$$
  \begin{aligned}
    \Pi_f(\varphi) = \frac{1}{\rho}\left[\vphantom{\frac{\Delta}{\Delta}} \langle \varphi \rangle \right. & + \frac{(v-u)\cdot\langle(v-u)\varphi\rangle}{T} \\
     & + \left. \left( \frac{|v-u|^2}{2T} - \frac{d}{2} \right)\frac{2}{d}\left\langle \left(\frac{|v-u|^2}{2T}-\frac{d}{2}\right)\varphi \right\rangle \right]\mathcal{M}_{[f]}
  \end{aligned}
$${#eq:defPi}

La projecteur $\Pi_f$ va nous permettre d'écrire une équation sur les paramètres de $\mathcal{M}_{[f]}$, à savoir $U$ ou $(\rho,u,T)$, qui représentera le modèle *macro* ; et une équation sur $g$, représentant le modèle *micro*.


## Obtention du modèle *macro*

Le vecteur $U$ est lié à l'inconnue $f$ via son moment\ :

$$
  U = \int_{\mathbb{R}^d} m(v)f(v)\,\mathrm{d}v
$$

En introduisant la décomposition $f=\mathcal{M}_{[f]}+g$ et en multipliant le modèle cinétique ([!eq:cine:vp]) par $m(v)$ puis en intégrant selon $v$ on obtient\ :

$$
  \partial_t U + \nabla_x\cdot\int_{\mathbb{R}^d}vm(v)(\mathcal{M}_{[f]}+g)\,\mathrm{d}v + \int_{\mathbb{R}^d}E\cdot\nabla_v (\mathcal{M}_{[f]}+g)m(v)\,\mathrm{d}v = 0
$$

Le produit $vm(v)$ est une opération triviale en dimension 1 mais se complexifie en dimension $d$ ; celui-ci cache un produit tensoriel\ :

$$
  v\,m(v) = \begin{pmatrix}v \\ v\otimes v \\ v|v|^2 \end{pmatrix} 
$$

où la composante $(i,j)$ du produit tensoriel $(v\otimes v)$ est donnée par\ :

$$
  (v\otimes v)_{i,j} = v_i v_k \quad i,j=1,\dots , d
$$

Finalement, en notant $\langle \cdot \rangle_v = \int_{\mathbb{R}^d}\cdot\,\mathrm{d}v$ on peut récrire ce modèle\ :

$$
  \partial_t U + \nabla_x \cdot \langle vm(v)\mathcal{M}_{[f]}\rangle_v + \nabla_v \langle E_fm(v)(\mathcal{M}_{[f]} + g)\rangle_v = - \nabla_x\cdot\langle vm(v)g \rangle_v
$$

Équation que l'on peut réécrire sous la forme suivante, en utilisant les calculs d'approximation effectués dans la section [2.4](#cinétique-vers-fluide)\ :

$$
  \partial_t U + \nabla_x\cdot\mathcal{F}(U) +  \nabla_x\langle vm(v)g \rangle_v = -\nabla_v\cdot \langle E_fm(v)(\mathcal{M}_{[f]} + g)\rangle_v
$${#eq:mima:macro}

L'équation [!eq:mima:macro] correspond à la partie macroscopique du modèle hybride *micro-macro*.

## Obtention du modèle *micro*

Pour obtenir la description microscopique, on ne s'intéresse qu'à la perturbation $g$ de $f$. En effet toute l'information sur l'équilibre maxwellien $\mathcal{M}_{[f]}$ est contenue dans la description macroscopique. Il suffit maintenant de reprendre le modèle cinétique [!eq:cine:vp] et de le projeter sur $\text{Im}Q$, c'est-à-dire en appliquant le projecteur $I-\Pi_f$\ :

$$
  \partial_t g + (I-\Pi_f)\left[v\cdot\nabla_x(\mathcal{M}_{[f]}+g) + E_f\cdot\nabla_v(\mathcal{M}_{[f]}+g)\right ] = -\frac{1}{\varepsilon}g
$${#eq:mima:micro}

Il s'agit là de la partie microscopique du modèle *micro-macro*. Pour alléger les notations de la partie *micro*, nous introduisons l'opérateur de transport $\mathcal{T}_{v,E}$ suivant\ :

$$
  \mathcal{T}_{v,E} = v\cdot\nabla_x + E\cdot\nabla_v
$$

Ainsi nous pouvons écrire le modèle *micro-macro* complet sous la forme\ :

$$
  \begin{cases}
    \partial_t U + \nabla_x\cdot\mathcal{F}(U) + \nabla_x\cdot\langle vm(v)g \rangle_v = \begin{pmatrix}0 \\ \rho E \\ \rho uE \end{pmatrix} \\
    \partial_t g + (I-\Pi_f)[\mathcal{T}_{v,E}(\mathcal{M}_{[f]}+g)] = -\frac{1}{\varepsilon}
  \end{cases}
$${#eq:mM}

où le champ électrique $E$ est calculé de manière similaire à [!eq:cine:poisson]\ :

$$
  \nabla_x\cdot E = \int_{\mathbb{R}^d} (\mathcal{M}_{[f]}+g)\,\mathrm{d}v -1
$$


M. Bennoune, M. Lemou et L. Mieussens montrent l'équivalence entre le modèle *micro-macro* ([!eq:mM]) et le modèle cinétique original ([!eq:cine]) dans [@BENNOUNE20083781].

Dans l'état, le modèle *micro-macro* n'a pas d'utilité propre ; cette réécriture du modèle cinétique sert de base pour des approximations. En effet il sera plus simple dans cette description de négliger la perturbation à l'équilibre $g$ sur une partie du domaine, que l'on nommera partie fluide du domaine.

Dans le cas limite $\varepsilon \to 0$, la seconde équation de [!eq:mM] nous donne formellement $g \to 0$, on retrouve alors l'équation d'Euler dans la première équation. Un développement en puissance de $\varepsilon$ donne\ :

$$
  g = -\varepsilon(I-\Pi_f)v\cdot\nabla_x\mathcal{M}_{[f]}
$$

résultat que l'on peut injecter dans l'équation *macro* pour obtenir les équations de Navier-Stokes.


## Approximation du modèle micro-macro

Le principal intérêt du modèle *micro-macro* est qu’il permet de développer des modèles pertinents et des schémas numériques performants dans des cas où l'écart entre $f$ et son équilibre $\mathcal{M}_{[f]}$ varie fortement, en espace ou en temps. Dans cette étude, nous nous intéressons à des cas où $f$ est très proche de $\mathcal{M}_{[f]}$ dans certaines régions du domaine, et s'en éloigne dans les autres régions.

L'idée introduite par P. Degond, G. Dimarco et L. Mieussens dans [@dimarco], est de coupler le modèle *micro* (basé sur un modèle cinétique) et le modèle *macro* (basé sur les équations d'Euler) à l'aide d'une décompostion de domaine adaptative. Cette décomposition permet d'approximer la partie *micro* lorsque le fluide est proche de son état d'équilibre thermodynamique.

Dans les régions où le système est à l'équilibre, c'est-à-dire $f \approx \mathcal{M}_{[f]}$, nous allons faire l'approximation $g=0$ dans cette zone. Nous introduisons la fonction $h:\Omega\mapsto[0,1]$ telle que\ :

* $h = 0$ dans la zone proche de l'équilibre aussi appelée zone fluide, notée $\Omega_F$.
* $h=1$ dans la zone hors équilibre aussi appelée zone cinétique, notée $\Omega_K$.

$$
  \Omega = \Omega_F \cup \Omega_K
$$

> TODO: tracer un truc ressemblant à $h(x)$

Utiliser une fonction indicatrice $h$ continument dérivable permet d’éviter une rupture de modèle ; comme les approches de décomposition de domaine classiques qui nécessitent des conditions aux bords pour connecter les différents modèles, ainsi qu'une gestion difficile entre l’interface fluide et cinétique en plusieurs dimensions. Nous obtenons donc une zone de transition des modèles où la solution calculée est une superposition des deux solutions, pondérée par la valeur de $h$. Nous allons pouvoir définir\ :

$$
  g = hg + (1-h)g = g_K + g_F
$$

où $g_K=hg$ correspond à la perturbation par rapport à l'équilibre maxwellien dans $\Omega_K$, et $g_F = (1-h)g$ dans $\Omega_F$. Dans $\Omega_F$ on suppose que le système est proche de l'équilibre $f \approx \mathcal{M}_{[f]}$, par conséquent la grandeur $g_F$ pourra être négligée.

Tentons d'exploiter cette hypothèse dans le modèle *micro-macro* [!eq:mM], reprenons le modèle *micro* que nous multiplions par $h$\ :

$$
  \underbrace{h\partial_t g}_{(1)} + \underbrace{h(I-\Pi_f)(\mathcal{T}_{v,E}\mathcal{M}_{[f]})}_{(2)} + \underbrace{h(I-\Pi_f)(\mathcal{T}_{v,E}(g_K+g_F))}_{(3)} = -\frac{h}{\varepsilon}g
$$

1. Or $\partial_t g_k = \partial_t(hg) = h\partial_t g - g\partial_t h$ ; donc $h\partial_t g = \partial_t g_K - g\partial_t h$ ;
2. Le second terme ne dépend par de $g$, on le passe donc dans le membre de droite.
3. On distingue ce terme en deux parties, entre l'opérateur identité et le projecteur $\Pi_f$, ce second terme ira dans le membre de droite.

D’où\ :

$$
  \begin{aligned}
    \partial_t g_K + h\mathcal{T}_{v,E}(g_K) + h\mathcal{T}_{v,E}(g_F) &= \\
     -\frac{1}{\varepsilon}g_K + \frac{g_K}{h}\partial_t h - h(I-\Pi_f)&(\mathcal{T}_{v,E}\mathcal{M}_{[f]}) + h\Pi_f(\mathcal{T}_{v,E}(g_K+g_F))
  \end{aligned}
$${#eq:mMh:gF}

P. Degond, G. Dimarco et L. Mieussens proposent dans [@dimarco] une simplification du terme $- h(I-\Pi_f)(\mathcal{T}_{v,E}\mathcal{M}_{[f]}) + h\Pi_f(\mathcal{T}_{v,E}(g_K+g_F))$ pour ne l'exprimer qu'en fonction de la distribution maxwellienne $\mathcal{M}_{[f]}$. Pour cela il est nécessaire de reprendre le modèle *macro* ([!eq:mima:macro]), qui en décomposant $f=\mathcal{M}_{[f]} + g$ permet d'exprimer $\partial_t\mathcal{M}_{[f]}$\ :

$$
  \partial_t\mathcal{M}_{[f]} = - \partial_t g - \frac{1}{\varepsilon}g - \mathcal{T}_{v,E}(\mathcal{M}_{[f]}+g)
$$

Le modèle *micro* ([!eq:mima:micro]) quant à lui nous donne une expression pour $\partial_t g$\ :

$$
  -\partial_t g = \frac{1}{\varepsilon}g +(I-\Pi_f)(\mathcal{T}_{v,E}(\mathcal{M}_{[f]}+g))
$$

Ainsi $\partial_t\mathcal{M}_{[f]}$ peut s'exprimer comme suit\ :

$$
  \partial_t\mathcal{M}_{[f]} = -\Pi_f(\mathcal{T}_{v,E}(\mathcal{M}_{[f]}+g_K+g_F))
$$

Il devient alors possible de simplifier le dernier terme de [!eq:mMh:gF], ce qui mène à la réécriture suivante\ :

$$ 
  \partial_t g_K + h\mathcal{T}_{v,E}(g_K) + h\mathcal{T}_{v,E}(g_F) = -\frac{1}{\varepsilon}g_K + \frac{g_K}{h}\partial_t h - h(\partial_t+\mathcal{T}_{v,E})\mathcal{M}_{[f]}
$$

Cette formulation permet de ne conserver aucune projection de $g_F$ ou $g_K$. Il devient donc plus aisé de travailler sur ces grandeurs que nous souhaitons approximer, mais implique numériquement le calcul de l'approximation de $\partial_t \mathcal{M}_{[f]}$ qui est une opération potentiellement coûteuse aussi bien en temps de calcul qu'en utilisation mémoire, ainsi dans la partie numérique la formulation conservant les projections de $g_K$ sera préférée.

Nous effectuons une approximation par rapport à $g$, en effet la fonction indicatrice $h$ permet de subdiviser le domaine. Nous négligerons $g_F$ par la suite\ :

$$
  g_F = 0
$$

La partie *micro* du modèle *micro-macro*, après cette approximation devient\ :

$$
  \partial_t g_K + h\mathcal{T}_{v,E}(g_K) = -\frac{1}{\varepsilon}g_K - h(I-\Pi_f)(\mathcal{T}_{v,E} \mathcal{M}_{[f]}) + h\Pi_f(\mathcal{T}_{v,E}(g_K)) + \frac{g_K}{h}\partial_t h
$${#eq:mM:h}

# Présentation des schémas

Dans cette partie, nous allons présenter différents schémas numériques pour résoudre le modèle *micro-macro* [!eq:mM]. Ce modèle comporte plusieurs difficultés qui devront être surmontées :

* Nous allons chercher des schémas d'ordre élevé en $(x,v)$ pour capturer les forts gradients qui peuvent apparaître selon les conditions initiales. Ces schémas dans l'espace des phases devront aussi fonctionner en multi-dimensions.
* L'opérateur de collision apporte un terme de raideur en $\frac{1}{\varepsilon}$ quand $\varepsilon \to 0$.
* Il est bien évidemment nécessaire d'assurer la stabilité du schéma par rapport au terme de transport, les simulations de plasma se faisant souvent en temps long.


## Schémas en temps

Pour étudier la raideur en $\frac{1}{\varepsilon}$, on se propose d'étudier la dynamique temporelle de l'équation différentielle suivante qui contient les mêmes difficultées mais est simplifiée par rapport au modèle *micro-macro* complet\ :

$$
  \begin{cases}
    \frac{\mathrm{d}u}{\mathrm{d}t}(t) = -\frac{1}{\varepsilon}u(t) + \mathcal{F}(u(t)) \\
    u(0) = u_0
  \end{cases}
$${#eq:edot}

avec $t$ représentant le temps, $u:\mathbb{R}_+\!\to\mathbb{R}$ la fonction inconnue, $\mathcal{F}:\mathbb{R}\to\mathbb{R}$ le flux, avec comme condition initiale $u_0\in\mathbb{R}$.

On peut résumer la difficulté au cas $\mathcal{F} = 0$ pour étudier la stabilité des schémas temporels, au détriment de quelques paramètres physiques\ :

$$
  \frac{\mathrm{d}u}{\mathrm{d}t} = -\frac{1}{\varepsilon}u
$${#eq:edot2}

où $\varepsilon > 0$ peut être aussi petit que l'on veut pour représenter un système fluide. L'enjeu du schéma temporel est de pouvoir choisir le pas de temps $\Delta t$ indépendamment du paramètre physique $\varepsilon$.

Une discrétisation en temps de [!eq:edot2] nous amènera à calculer une approximation $u^n \approx u(t^n)$ où $t^n = n\Delta t$ avec $\Delta t$ notre pas de temps. Ainsi la discrétisation via un schéma d'Euler explicite de [!eq:edot2] nous donne\ :

$$
  \frac{u^{n+1}-u^n}{\Delta t} = -\frac{1}{\varepsilon}u^n
$$

soit\ :

$$
  u^n = \left( 1-\frac{\Delta t}{\varepsilon}\right)^n u_0
$$

La solution $(u^n)_n$ reste bornée si et seulement si $| 1-\frac{\Delta t}{\varepsilon} |\leq 1$, *ie* $\Delta t \leq 2\varepsilon$. Or le paramètre $\varepsilon$ peut être choisi arbitrairement petit, donc cette condition CFL est très contraignante et conduit à des temps de calculs trop coûteux. Il est donc impératif d'utiliser un schéma d'Euler implicite de la forme\ :

$$
  \frac{u^{n+1}-u^n}{\Delta t} = -\frac{1}{\varepsilon}u^{n+1}
$$

soit, sous forme itérative\ :

$$
  u^n = \frac{1}{(1+\frac{\Delta t}{\varepsilon})^n}u_0
$$

ce qui est inconditionnellement stable quelle que soit la valeur de $\Delta t$ et de $\varepsilon$. Par conséquent nous utiliserons un schéma d'Euler implicite en temps pour tester et valider nos différents schémas sur le terme de transport.


### Schéma Runge-Kutta d'ordre 3

> TODO: mettre le numéro de la section dans *"que l'on détaillera plus tard"*

Pour des raisons de stabilité, liées à l'utilisation de schémas d'ordre élevé en $x$ (que l'on détaillera plus tard), nous avons été amené à considérer le schéma de Runge-Kutta d'ordre 3 (RK3).

Le schéma en temps se résout de manière indépendante du schéma d'advection, par conséquent il s'agit d'une simple équation différentielle ordinaire que nous écrirons\ :

$$
  \frac{\mathrm{d}u}{\mathrm{d}t}(t) = L(u(t),t)
$${#eq:rk3:base}

avec $t$ le temps, $u:\mathbb{R}_+\to\mathbb{R}$ la fonction inconnue, $L:\mathbb{R}\times\mathbb{R}_+\to\mathbb{R}$ une fonction linéaire dépendant de $u$ et du temps. Nous cherchons à calculer $u^n \approx u(t^n)$, une approximation de $u$ au temps $t^n = n\Delta t$, avec $\Delta t > 0$ le pas de temps. Il existe plusieurs formulations du schéma de Runge-Kutta d'ordre 3. L'ordre 3 nécessite au minimum 3 étapes de calculs, une version ajoutant de la stabilité en 4 étapes existe, ainsi qu'une version utilisant peu de mémoire, décrie dans [@ssp_rk3]. Nous utiliserons le schéma suivant, le plus rapide en temps de calcul\ :

$$
  \begin{aligned}
    u^{(1)} &= u^n + \Delta t L(u^n,t^n) \\
    u^{(2)} &= \frac{3}{4}u^n + \frac{1}{4}u^{(1)} + \frac{1}{4}\Delta t L(u^{(1)},t^n+\Delta t) \\
    u^{n+1} &= \frac{1}{3}u^n + \frac{2}{3}u^{(2)} + \frac{2}{3}\Delta t L(u^{(2)},t^n+\frac{1}{2}\Delta t)
  \end{aligned}
$$

Dans le cadre du modèle *micro-macro* par exemple, nous avons $u=\mathcal{M}_{[f]}+g$ dans la partie *micro* sans terme de collision.

Si la simulation se concentre sur un plasma peu dense, c'est-à-dire $\varepsilon\to\infty$, le terme raide dans la partie *micro* du modèle *micro-macro* ([!eq:mM]) peut s'approximer par\ :

$$
  \partial_t g + (I-\Pi_f)[\mathcal{T}_{v,E}(\mathcal{M}_{[f]}+g)] = 0
$$

Dans ce cas, nous utilisons [!eq:rk3:base] avec $u = g$ et $L(u) = -(I-\Pi_f)[\mathcal{T}_{v,E}(\mathcal{M}_{[f]}+g]$. Pour les autres valeurs de $\varepsilon$ il est nécessaire d'effectuer une reformulation de la partie *micro* pour exploiter ce schéma temporel.

## Schémas d'advection d'ordre élevé

Pour approcher le terme de transport $\partial_t g + \mathcal{T}_{v,E}(g)$ de ([!eq:mima:micro]), il est primordial d'utiliser des schémas d'ordre élevé  pour :

* Capturer les forts gradients en diminuant la viscosité numérique ;
* Utiliser moins de points lors de la simulation.

Pour ces raisons nous allons présenter deux schémas d'ordre élevé permettant de résoudre une part de ces problèmes. 

Nous étudirons ces schémas tout d'abord en l'absence de champ électrique $E$. Le transport selon $x$ et $v$ étant indépendant ils peuvent être étudié séparément. Nous nous ramenons donc à des cas de transport 1D selon $x$. Le transport de $g$ donné par\ :

$$
  \partial_t g + v\cdot\nabla_x g = 0
$$

se ramène à une équation d'advection linéaire lorsque $v$ est discrétisé par $v_k = k\Delta v$, avec $\Delta v > 0$ le pas de vitesse dans l'espace des phases. Ainsi l'exemple de base que nous utiliserons pour présenter ces schémas est une équation d'advection linéaire en une dimension\ :

$$
  \begin{cases}
    \partial_t u + a \partial_x u = 0 \\
    u(t=0,x) = u^0(x)
  \end{cases}
$${#eq:trp:base}

où $t$ est le temps, $x$ la dimension d'espace et $u : \mathbb{R}_+\times\mathbb{R}\to\mathbb{R}$ est la fonction inconnue. On ajoute à cette équation des conditions aux bords qui dépendront des cas tests présentés.

Nous cherchons à calculer $u^n_i \approx u(t^n,x_i)$ une approximation de $u$ au temps $t^n = n\Delta t$, avec $\Delta t>0$ le pas de temps, en $x_i = i\Delta x$, avec $\Delta x>0$ le pas d'espace.

### Schéma compact

Dans un premier temps nous présenterons uniquement le cas d'un transport à vitesse $a$ constante positive. Un schéma linéaire différences finies avec un *stencil* de taille $r+s+1$ peut s'écrire de manière générale comme\ :

$$
  u_i^{n+1} = \sum_{k=-r}^s \gamma_k u_{i+k}^n
$${#eq:df:compact}

où $\gamma_k$ est un coefficient dépendant du nombre CFL $\nu = a\frac{\Delta t}{\Delta x}$.

On peut réécrire [!eq:df:compact] comme interprétation en volumes finis\ :

$$
  u_i^{n+1} = u_i^n - \nu (u^n_{i+\frac{1}{2}} - u^n_{i-\frac{1}{2}})
$$

où $u^n_{i+\frac{1}{2}}$ sont les flux numériques. Le calcul de ces flux est présenté dans [@Boyer:2014aa] pour différents ordres. Nous choisirons ceux d'ordre élevé décrits dans [@despres]. L'ordre du flux dépend du choix du couple $(r,s)$, il est ainsi possible de retrouver plusieurs flux connus\ :

* Le schéma décentré amont, ou *upwind*\ :

  $$
    u_{i+\frac{1}{2}}^n = u_i^n
  $$

* Une combinaison de *Lax-Wendroff* (LW) et de *Beam-Warming* (BW) : $(1-\alpha )LW + \alpha BW$ avec $\alpha = \frac{1+\nu}{3}$\ :

  $$
    u_{i+\frac{1}{2}}^n = u_i^n + \frac{2-\nu}{6}(1-\nu)(u_{i+1}^n-u_{i}^n) + \frac{1+\nu}{6}(1-\nu)(u_i^n-u_{i-1}^n)
  $$

* Dans [@despres], B. Després propose le schéma à 6 points d'ordre 5 suivant\ :

  $$
    \begin{aligned}
      u_{i+\frac{1}{2}}^n = & \ u_{i+2}^n + \frac{\nu+3}{2}(u_{i+1}^n-u_{i+2}^n) + \frac{(2+\nu)(1+\nu)}{6}(u_i^n - 2u_{i+1}^n + u_{i+2}^n) \\
                          & + \frac{(2+\nu)(1+\nu)(\nu-1)}{24}(u_{i-1}^n - 3u_{i}^n + 3u_{i+1}^n - u_{i+2}^n) \\
                          & + \frac{(2+\nu)(1+\nu)(\nu-1)(\nu-2)}{120}(u_{i-2}^n - 4u_{i-1}^n + 6u_{i}^n - 4u_{i+1}^n + u_{i+2}^n)
    \end{aligned}
  $$

C'est ce dernier flux que nous utiliserons par la suite.

#### Obtention de l'ordre en espace

La solution exacte d'un problème de transport à vitesse $a$ constante est connue. Nous allons donc partir de ce problème, le résoudre sur un premier maillage et en calculer l'erreur ; puis répéter l'opération sur un maillage plus fin. Les différentes résolutions sur différents maillages s'effectuent toutes jusqu'au même temps final.

Le problème que nous considérons est [!eq:trp:base] avec $a=1$\ :

$$
  \partial_t u + \partial_x u = 0
$$

L'équation est considérée valide sur l'ensemble $x\in[0,2\pi]$, avec des conditions aux bords périodiques ; et nous allons considérer un cosinus comme condition initiale\ :

$$
  u_i^0 = \cos(x_i)
$$

avec $x_i = i\Delta x$ et le pas d'espace $\Delta x = \frac{2\pi}{N}$, où $N$ est le nombre de points du maillage. La solution exacte au temps $t^n$ est\ :

$$
  u(t^n,x_i) = \cos(x_i - t^n)
$$

##### Calcul à pas de temps fixe

Pour être certain de ne pas prendre en compte l'erreur en temps dans le calcul de l'erreur en espace, il est possible de résoudre le problème sur un seul pas de temps toujours identique. Ainsi le seul paramètre modifié d'une simulation à l'autre est le raffinage du maillage et on observera uniquement l'erreur en espace.

Un seul pas de temps suffit pour l'obtention de l'ordre :

$$
  u_i^1 = u_i^0 - \frac{\Delta t}{\Delta x}( u^0_{i+\frac{1}{2}} - u^0_{i-\frac{1}{2}}) = \cos(x_i - \Delta t) + \mathcal{O}(\Delta x^m)
$$

où $m$ est l'ordre recherché. L'erreur se calcule par la norme de la différence de la solution approchée avec la solution exacte. Plus précisement, elle est définie par\ :

$$
  e_1 = \| U^1 - \cos(X_i - \Delta t) \|_1 = \sum_i |u_i^1 - \cos(x_i - \Delta t) |\Delta x
$$

en norme $L^1$, ou

$$
  e_{\infty} = \| U^1 - \cos(X_i - \Delta t) \|_{\infty} =  \sup_i |u_i^1 - \cos(x_i - \Delta t) |
$$

en norme infinie.

Par définition, un schéma d'ordre $m$ est tel que $e_1 = C\Delta x^m$ ou $e_{\infty} = \tilde{C}\Delta x^m$, donc en traçant l'erreur sur une échelle logarithmique on trouve :

$$
  \log e_1 = \log C + m \log \Delta x
$$

En effectuant cette simulation pour différentes valeurs de $\Delta x$ on peut tracer $\log e_1 = f(\log \Delta x)$, où l'on doit obtenir une droite dont la pente indique l'ordre.

Dans notre cas nous prendrons $\Delta x = \frac{2\pi}{20} , \frac{2\pi}{40} , \frac{2\pi}{60} , \frac{2\pi}{80}$. Pour assurer notre condition CFL nous choisirons $\Delta t < \frac{2\pi}{100}$ fixé.


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

Il est intéressant de faire une simulation sur plusieurs pas de temps pour amplifier la visibilité de l'ordre du schéma ; l’inconvénient est que l'erreur du schéma temporel, potentiellement plus élevée, empêche d'observer l'erreur dûe au schéma spatial sans choisir un pas de temps arbitrairement très faible. Pour remédier en partie à ce problème nous allons travailler sur un nombre de CFL constant, c'est-à-dire\ :

$$
  \frac{\Delta t}{\Delta x} = c
$$

Ainsi à chaque raffinement de maillage, le pas de temps est aussi raffiné, l'erreur en temps diminue donc de manière similaire.

> TODO: Je pensais rajouter un graphique où l'on voit la saturation de l'ordre dû à l'erreur en temps

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

> TODO: Introduire WENO en citant [@weno] ou [@icase], dire qu'une autre interpolation est possible pour des problèmes particulier comme Vlasov-Poisson : [@banks]

WENO pour *weighted essentially non-oscillatory* est une famille de schémas numériques qui se généralise facilement à l'ordre élevé sans pour autant provoquer d'oscillations. L'idée des schémas WENO est d'effectuer plusieurs interpolations polynomiales lagrangiennes sur des *stencils* incluant le point à évaluer, pondérées pour limiter les oscillations. La méthode que nous allons présenter ici est un schéma WENO d'ordre 5.

> TODO: Faire un schéma où on remonte une courbe caractéristique et dire que le problème se "limite" à un problème d'interpolation, et que pour limiter les oscillations d'une interpolation polynomiale d'ordre élevé on en fait 3 d'ordre moins élevé, que l'on pondère pour réduire encore plus le risque oscillant.

Nous présenterons ce schéma toujours à partir de l'équation [!eq:trp:base]. Le schéma WENO de base s'écrit à partir d'une vitesse $a$ pouvant dépendre de $x$, l'équation de transport s'écrit alors\ :

$$
  \partial_t u + \partial_x(a u) = 0
$$

Dans notre cas, la discrétisation de la vitesse $a$ dépend du paramètre $k$ (discrétisation de l'espace des phases), nous noterons par conséquent cette discrétisation $a_k$. Cette notation permettra d'écrire directement le schéma en espace de la partie *micro* en substituant $a_k$ par $v_k$ et $u_{i,k}$ par $g_{i,k}$. Pour alléger les notations, nous nous placerons au temps $t^n$. Nous souhaitons approximer $\partial_x(au)_{|x=x_i,y=y_k}$\ :

$$
  \partial(au)_{|x=x_i,y=y_k} \approx \frac{1}{\Delta x}(\hat{u}_{i+\frac{1}{2},k} - \hat{u}_{i-\frac{1}{2},k})
$$

où $\hat{u}_{i,k}$ est une approximation de $(au)_{i,k}$ et $\hat{u}_{i+\frac{1}{2},k}$ est le flux numérique. Nous allons distinguer les cas $a_k >0$ et $a_k <0$ en écrivant $\hat{u}$ comme :

$$
  \hat{u}_{i,k} = \hat{u}_{i,k}^+ + \hat{u}_{i,k}^-
$$

où :

* $\hat{u}_{i.k}^+ = a^+u_{i,k} = \max(a_k,0)u_{i,k}$
* $\hat{u}_{i.k}^- = a^-u_{i,k} = \min(a_k,0)u_{i,k}$

Chaque flux numérique est donnée par la somme pondérée de 3 approximations sur 3 *stencils* différents :

$$
  \begin{aligned}
    \hat{u}_{i+\frac{1}{2},k}^+ =\,&w_0^+\left(\frac{2}{6}u_{i-2,k}^+ - \frac{7}{6}u_{i-1,k}^+ + \frac{11}{6}u_{i,k}^+\right)
                        +   w_1^+\left(-\frac{1}{6}u_{i-1,k}^+ + \frac{5}{6}u_{i,k}^+   +  \frac{2}{6}u_{i+1,k}^+\right) \\
                        +\,&w_2^+\left( \frac{2}{6}u_{i,k}^+   + \frac{5}{6}u_{i+1,k}^+ -  \frac{1}{6}u_{i+2,k}^+\right)
  \end{aligned}
$$

et

$$
  \begin{aligned}
  \hat{u}_{i+\frac{1}{2},k}^- =\,&w_2^-\left(-\frac{1}{6}u_{i-1,k}^- + \frac{5}{6}u_{i,k}^-   + \frac{2}{6}u_{i+1,k}^-\right)
                        +   w_1^-\left( \frac{2}{6}u_{i,k}^-   + \frac{5}{6}u_{i+1,k}^- - \frac{1}{6}u_{i+2,k}^-\right) \\
                        +\,&w_0^-\left(\frac{11}{6}u_{i+1,k}^- - \frac{7}{6}u_{i+2,k}^- + \frac{2}{6}u_{i+3,k}^-\right)
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
   \beta_0^+ &= \frac{13}{12}(u^+_{i-2,k} -2u^+_{i-1,k} + u^+_{i  ,k})^2 + \frac{1}{4}( u^+_{i-2,k} - 4u^+_{i-1,k} + 3u^+_{i,k})^2 \\
   \beta_1^+ &= \frac{13}{12}(u^+_{i-1,k} -2u^+_{i  ,k} + u^+_{i+1,k})^2 + \frac{1}{4}( u^+_{i-1,k} -  u^+_{i+1,k})^2 \\
   \beta_2^+ &= \frac{13}{12}(u^+_{i  ,k} -2u^+_{i+1,k} + u^+_{i+2,k})^2 + \frac{1}{4}(3u^+_{i  ,k} - 4u^+_{i+1,k} + u^+_{i+2,k} )^2 
 \end{aligned}
$$

et

$$
 \begin{aligned}
   \beta_0^- &= \frac{13}{12}(u^-_{i+1,k} -2u^-_{i+2,k} + u^-_{i+3,k})^2 + \frac{1}{4}(3u^-_{i+1,k} - 4u^-_{i+2,k} + u^-_{i+3,k})^2 \\
   \beta_1^- &= \frac{13}{12}(u^-_{i  ,k} -2u^-_{i+1,k} + u^-_{i+2,k})^2 + \frac{1}{4}(u^-_{i,k} - u^-_{i+2,k})^2 \\
   \beta_2^- &= \frac{13}{12}(u^-_{i-1,k} -2u^-_{i  ,k} + u^-_{i+1,k})^2 + \frac{1}{4}(u^-_{i,k} - 4u^-_{i,k} + 3u^-_{i+1,k})^2
 \end{aligned}
$$


et enfin, $\epsilon$ est un paramètre pour prévenir que le dénominateur soit égal à $0$ ; il est généralement pris à $\epsilon = 10^{-6}$ (dans [@weno]) ou $\epsilon = 10^{-5}\times\max_{i,k}( v^0_k f^0_{i,k})$ (dans [@qiu]) ; ce dernier cas présente l'avantage de s'adapter à l'amplitude de la fonction à considérer.

On a ainsi définit l'approximation du terme de transport à l'aide d'un schéma WENO pour toute vitesse $a_k$ :

$$
  \partial_x (au)_{|x=x_i,y=y_k} \approx \frac{1}{\Delta x}\left[ (\hat{u}^+_{i+\frac{1}{2},k} - \hat{u}^+_{i-\frac{1}{2},k}) + (\hat{u}^-_{i+\frac{1}{2},k} - \hat{u}^-_{i-\frac{1}{2},k}) \right] 
$$

#### Obtention de l'ordre en espace

Comme précédemment nous allons calculer l'ordre à l'aide du transport à vitesse constante $a$, en utilisant une fonction cosinus comme condition initiale. Nous allons résoudre successivement ce problème de transport sur un maillage de plus en plus fin.

Le problème que nous considérons est ([!eq:trp:base]) avec $a=1$\ :

$$
  \partial_t u + \partial_x u = 0
$$

Un test similaire a été effectué à vitesse négative au vu du changement de formulation pour ce cas. L'équation est considérée valide sur l'ensemble $x\in[0,2\pi]$ avec des conditions aux bords périodiques ; et nous allons considérer un cosinus comme condition initiale\ :

$$
  u_i^0 = \cos(x_i)
$$

avec $x_i = i\Delta x$ et le pas d'espace $\Delta x = \frac{2\pi}{N}$ où $N$ est le nombre de points du maillage. La solution exacte au temps $t^n$ est\ :

$$
  u_i^n = \cos(x_i - t^n)
$$

Nous avons constater numériquement que l'erreur en espace de ce schéma est beaucoup plus faible que l'erreur en temps du schéma Euler implicite utilisé ici. La méthode d'obtention de l'ordre en espace sur un seul pas de temps demande alors un pas de temps trop petit pour que l'erreur du schéma soit systématiquement distingable de l'erreur machine. Pour ce schéma nous utiliserons uniquement la mesure de l'ordre avec un nombre de CFL constant, ce qui permet de réduire l'erreur en temps à mesure que le maillage se raffine.

Les différentes simulations sont effectuées avec un nombre de CFL constant, c'est-à-dire\ :

$$
  \frac{\Delta t}{\Delta x} = c
$$

donc $\Delta t = c\frac{2\pi}{N}$ change à chaque raffinement de maillage.


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

La littérature actuelle préconise l'usage de schéma de la famille WENO lors de la résolution par différences finies à l'ordre élevé d'équations aux dérivées partielles. Cela s'explique par une propriété intéressante de ces schémas qu'est l'empilement de dérivées. Le passage aux dimensions supérieures à $1$ s'effectue par addition des différentes approximations des dérivées dans chaque direction. Cette technique est parfois utilisée avec d'autres schémas, ce qui revient à supposer que les différentes dimensions du problème sont indépendantes.

Il est donc intéressant d'étudier des cas de transports en 2 dimensions\ :

$$
  \partial_t u + a \partial_x u + b \partial_y u = 0
$$

où $x$ et $y$ sont les deux directions de l'espace, dans lequel nous effectuons un transport à vitesse $a$ dans la direction $x$ et $b$ selon $y$. La solution exacte est connue pour plusieurs cas tests tels que la translation en 2 dimensions (avec $a$ et $b$ des constantes), ou pour le cas d'une rotations (avec $a=y$ et $b=-x$).



#### Test de viscosité

À partir du cas test de la rotation avec des conditions aux bords périodiques\ :

$$
  \partial_t u + y\partial_x u -x\partial_y u = 0
$$

il est possible de mettre à l'épreuve la viscosité numérique du schéma. C'est ce qui est effectué dans [@qiu2011], avec 12 rotations d'une condition initiale discontinue.

> Cas où l'on fait tourner 12 fois un pacman : [@qiu2011]

#### Problème d'instabilité

R. Wang et R. Spiteri démontrent dans [@weno_time] que l'utilisation conjointe du schéma WENO d'ordre 5 avec un schéma temporel de type d'Euler implicite est instable. Nous confirmons ce résultat numériquement avec la rotation d'une gaussienne en temps long. On remarque qu'une discrétisation en temps de Runge-Kutta d'ordre 3 stabilise le schéma.

> TODO: cas où l'on fait tourner une gaussienne, comparer entre Euler et RK3 (apparition d'une *vague de traine* dans le cas Euler)

> TODO: mettre cette même rotation de gaussienne avec *upwind* et schéma compact ? *upwind* est très visqueux et on ne voit plus rien en temps long


## Couplage de l'équation de transport et du terme de raideur

Dans cette section, on applique les schémas précédents au modèle *micro-macro*, ce qui va amener à des études supplémentaires comme le calcul de la condition de CFL, ou la reformulation exponentielle du modèle.


### Calcul de la condition CFL

Le terme raide, apporté par l'opérateur de collision BGK va induire une modification de la condition CFL habituelle lors du couplage du schéma d'Euler implicite avec un schéma en espace.

Pour calculer le nombre de CFL nous allons dans un premier temps nous intéresser au modèle cinétique [!eq:cine] avec $Q(f) = \frac{1}{\varepsilon}(\mathcal{M}_{[f]}-f)$, la description microscopique du modèle *micro-macro* est similaire et implique la même condition. Nous utiliserons le schéma d'Euler implicite pour la discrétisation en temps, et pour simplifier les notations nous n'utiliserons qu'un schéma *upwind* en espace, encore une fois le champ électrique est négligé dans cette partie.

$$
  \frac{f_{i,k}^{n+1}-f_{i,k}^n}{\Delta t} + v\frac{f_{i+\frac{1}{2},k}^n - f_{i-\frac{1}{2},k}^n}{\Delta x} = \frac{1}{\varepsilon}((\mathcal{M}_{[f^{n+1}]})_{i,k} - f_{i,k}^{n+1})
$$

Ce qui peut se réécrire, pour une interprétation itérative\ :

$$
  f_{i,k}^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ f_{i,k}^n - v_k\frac{\Delta t}{\Delta x}(f_{i+\frac{1}{2},k}^n - f_{i-\frac{1}{2},k}^n) + \frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k} \right]
$$

> TODO: revoir la notation $A^n$ car ça dépend de $k$, on ne sait pas exactement comment (peut-être juste ajouter en indice $k$)

Il n’est pas possible de calculer directement la CFL du schéma en $f_{i,k}$ nous allons donc utiliser l’analyse de von Neumann pour résoudre ce problème. Pour cela, posons $f_{j,k}^n = e^{i\kappa j\Delta x}A^n$, l’indice d’espace est dorénavant $j$ et $i$ est le nombre imaginaire tel que $i^2 = -1$. Nous pouvons donc facilement exprimer $f_{j-1,k}^n$ directement en fonction de $f_{j,k}^n$\ :

$$
  f_{j-1,k}^n = e^{i\kappa (j-1)\Delta x}A^n = f_{j,k}^n e^{-i\kappa\Delta x}
$$

Cela permet donc d’exprimer $f_{j,k}^{n+1}$ en fonction uniquement de $f_{j,k}^n$, et donc d’obtenir une formule de récurrence du type\ :

$$
  f_{j,k}^{n+1} = \mathcal{A} f_{j,k}^n = (\mathcal{A})^{n+1} f_{j,k}^0
$$

On remarque de suite qu’il est nécessaire pour que le schéma converge d’avoir $|\mathcal{A}| \leq 1$. Pour trouver cette formule de récurrence nous travaillerons sur une version simplifiée du schéma en négiligeant l’impact de la maxwellienne.

On part ainsi du schéma simplifié sur $f$\ :

$$
  f_{j,k}^{n+1} = \frac{\varepsilon}{\varepsilon + \Delta t}\left[ f_{j,k}^n - \frac{\Delta t}{\Delta x}v_k(f_{j,k}^n - f_{j,k}^ne^{-i\kappa\Delta x} )  \right]
$$

Ce que l’on peut écrire sous la forme\ :

$$
  f_{j,k}^{n+1} = f_{j,k}^n\frac{\varepsilon}{\varepsilon + \Delta t}\left[ 1-\frac{\Delta t}{\Delta x}v_k(1-e^{-i\kappa\Delta x}) \right]
$$

On obtient bien la forme désirée $f_{j,k}^{n+1} = \mathcal{A} f_{j,k}$. Pour simplifier l’étude de $\mathcal{A}$ écrivons ce terme sous la forme\ :

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

### Reformulation exponentielle du modèle *micro*

Au sein du modèle *micro-macro* ([!eq:mM]), la partie *micro* fait intervenir un terme de collision : $\frac{1}{\varepsilon}g$, ce terme empêche d'utiliser directement une autre discrétisation en temps que le schéma Euler implicite ou explicite. Or en proposant de l'ordre élevé en espace il devient intéressant, voir indispensable, de monter l'ordre en temps. En effet R. Wang et R. Spiteri démontrent dans [@weno_time] qu'il est impossible de satisfaire la condition CFL d'un schéma composé d'une partie spatiale résolue par un schéma WENO d'ordre 5, et d'une partie temporelle résolue par un schéma d'Euler implicite. Le terme raide en $\frac{1}{\varepsilon}$ ne permet pas de revenir à un cas stable. Il est nécessaire de modifier la formulation du modèle *micro* pour faire intervenir une discrétisation du schéma de Runge-Kutta d'ordre au moins 3 (RK3).

Nous rappelons le modèle *micro* :

$$
  \partial_t g + (I-\Pi_f)(v\partial_x(\mathcal{M}_{[f]}+g) + E\partial_v(\mathcal{M}_{[f]}+g)) = -\frac{1}{\varepsilon}g
$${#eq:rk3:micro0}

En remarquant que :

$$
  \partial_t g+\frac{1}{\varepsilon} = e^{-\frac{t}{\varepsilon}}\partial_t\left(e^{\frac{t}{\varepsilon}}g\right)
$$

On pose donc $\zeta = e^{\frac{t}{\varepsilon}}g$, l'équation [!eq:rk3:micro0] devient donc :

$$
  \partial_t \zeta +(I-\Pi_f)(v\partial_x(\zeta+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]})+E\partial_v(\zeta+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]})) = 0
$$

Il devient donc possible d'appliquer une discrétisation type Runge-Kutta d'ordre 3, avec :

$$
  L(u,t) = -(I-\Pi_f)(v\partial_x(u+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]})+E\partial_v(u+e^{\frac{t}{\varepsilon}}\mathcal{M}_{[f]}))
$$



## Résolution du problème de Poisson

Pour résoudre le problème de Poisson en condition aux bords périodiques nous utiliserons une méthode de transformée de Fourier. Le champ électrique est une fonction de la densité $\rho(t^n)$, il est donc nécessaire de résoudre le problème de Poisson à chaque pas de temps, et à chaque sous-étape dans le cas du schéma RK3.

Notons $\varrho = \rho -1$, il suffit de calculer la transformée de Fourier de $\varrho$ pour résoudre le problème [!eq:cine:poisson] dans le contexte spectral\ :

$$
  i\kappa \hat{E}_{\kappa} = \hat{\varrho}_{\kappa}
$$

où $\kappa$ est l'indice du coefficient de Fourier et $i$ le nombre complexe tel que $i^2 = -1$. Ainsi on définit pour tout $\kappa$ le coefficient de Fourier\ :

* $\hat{E}_{\kappa} = -i\displaystyle\frac{\hat{\varrho}_{\kappa}}{\kappa}$ si $\kappa \neq 0$
* $\hat{E}_0 = 0$ car $E_f$ est à moyenne nulle d'après la condition [!eq:cine:vp]

Ainsi tous les coefficients de Fourrier de $E_f$ sont calculés, il suffit d'effectuer la transformée inverse pour trouver le résultat souhaité.


# Application aux modèles cinétiques et *micro-macro*

Nous avons appliqué les schémas précédents à différents modèles :

* Un modèle cinétique sur $f$ ([!eq:cine]) qui permettra de tester nos schémas cinétiques sans couplage avec des équations de type Euler.
* Le modèle *micro-macro* ([!eq:mM]) qui couple la discrétisation de la parrtie cinétique *micro* à la partie fluide de type Euler.
* Le modèle *micro-macro* avec une fonction $h$ qui perrmettra de tester cette nouvelle modélisation.

## Discrétisation du modèle cinétique

> Algorithme, propriété de la température et conservation des variables intensives, calcul de CFL, tests numériques (périodique et Neumann) comparaison avec Euler

Dans un premier temps, pour pouvoir comparer les résultats avec un code de simulation des équations d'Euler, on étudie le modèle sans champ électrique $E$, c'est-à-dire le modèle suivant\ :

$$
  \partial_t f + v\partial_x f = \frac{1}{\varepsilon}(\mathcal{M}_{[f]}-f)
$$

La résolution nécessite une grille en espace et en vitesse, c'est-à-dire un maillage de l'espace des phases. On note $f_{i,k}^n$ l'approximation de $f(t^n,x_i,v_k)$. On suppose $f_{i,k}^n$ donnée par l'itération précédente, le calcul de la nouvelle itération s'effectue schématiquement comme suit\ :

1. On calcule le flux numérique $f_{i+\frac{1}{2},k}^n$ du schéma en espace souhaité (*upwind*, schéma compact ou WENO)\ :

  $$
    f_{i+\frac{1}{2},k}^n \gets ((f_{j,k}^n)_{j\in[i-2;i+2]},v_k)
  $$

2. On calcule le flux numérique $F_{i+\frac{1}{2}}^n$ pour le schéma macro sur $U$ à partir du flux $f_{i+\frac{1}{2},k}^n$\ :
  
  $$
    F_{i+\frac{1}{2}}^n \gets \sum_k v_km(v_k)f_{i+\frac{1}{2},k}^n\Delta v
  $$

3. On résout le schéma sur $U$\ :
  
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
  $${#eq:max:numcal}

6. On approxime $f^{n+1}_{i,k}$ via le schéma avec le terme de transport et de diffusion :
  
  $$
    f^{n+1}_{i,k} = \frac{1}{1+\frac{\Delta t}{\varepsilon}} \left[ f^n_{i,k} - \frac{\Delta t}{\Delta x}v_k (f^n_{i+\frac{1}{2},k} - f^n_{i-\frac{1}{2},k}) +\frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k}  \right]
  $$

7. On corrige l’approximation $U_i^{n+1}$ via le calcul du moment de $f^{n+1}_{i,\cdot}$ :

  $$
    U_i^{n+1} \gets \sum_k m(v_k)f_{i,k}^{n+1} \Delta v
  $$


### Propriété sur la température

Le calcul de la maxwellienne $\mathcal{M}_{[f^{n}]}$ dans [!eq:max:numcal] nécessite l'extraction de la racine carré de la température $(T_i^n)_i$ à tout temps $t^n$, or celle-ci est uniquement définie par\ :

$$
  T_i^n = \frac{(U_3)_i^n}{(U_1)_i^n} - \left(\frac{(U_2)_i^n}{(U_1)_i^n}\right)^2
$$

> TODO: écrire ceci sous forme de proposition + preuve

La proposition suivante assure la positivité de cette valeur, condition nécessaire pour assurer la validité des calculs. En utilisant la définition du vecteur $U_i^n$ on peut reformuler $T_i^n$ comme\ :

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

C’est-à-dire que l’on a bien\ :

$$
  \sum_k |v_k|^2 f_{i,k}^n \Delta v \sum_k f_{i,k}^n \Delta v \geq \left( \sum_k v_k f_{i,k}^n \Delta v \right)^2
$$

Ce qui garantit bien la positivité de $T_i^n$ en tout point $x_i$ de l’espace et pour tout temps $t^n$.

### Propriétés de conservations

Nous allons étudier ce que donnent les propriétés de conservations énoncées dans l'équation [!eq:cine:conservation] dans le domaine discret\ :

$$
  \sum_i U^n_i \Delta x = \sum_i U^0_i \Delta x
$$

La première composante de cette somme est la masse du système, la seconde la quantité de mouvement et la troisième l'énergie, trois grandeurs conservatives d'un point de vue physique. Il est donc important de tracer ces valeurs pour vérifier leur conservation par le schéma numérique.

On peut aussi comparer ce résultat à\ :

$$
  \sum_{i,k} m(v_k)f^n_{i,k} \Delta x \Delta v
$$

qui doit être indépendant de $n$ à erreur sur $\sum_k \mathcal{M}_[f]$ près. En effet dans le contexte fluide nous avons\ :

$$
  \sum_{i,k} m(v_k)f^n_{i,k}\Delta x \Delta v \approx \sum_{i,k} m(v_k)(\mathcal{M}_[f^n])_{i,k}\Delta x \Delta v = \sum_i U^n_i
$$

Il est nécessaire d'approximer correctement l'intégrale sur $v \in\mathbb{R}^d$, numériquement cela se traduit par un $v_{\text{max}}$ suffisamment grand.

On constate bien une conservation de ces valeurs. La légère évolution de ces valeurs est due à la mauvaise approximation de la maxwellienne.

> TODO: insérer ici un graph prouvant ces dires


## Discrétisation du modèle micro-macro

Nous voulons discrétiser le modèle *micro-macro* [!eq:mM] en considérant le couple de variables $(U_i^n,g_{i,k}^n)$ une approximation de $U(t^n,x_i)$ et $g(t^n,x_i,v_k)$ au temps $t^n = n\Delta t$ avec $\Delta t >0$ le pas de temps, à la position $x_i = i\Delta x$ avec $\Delta x$ le pas d'espace, à la vitesse $v_k = k\Delta v$ avec $\Delta v$ le pas de vitesse.

### Écriture de la partie *macro*

La partie *macro* du modèle est une modification du modèle d’Euler classique [!eq:euler]. Nous avons adapté un code de simulation des équations d'Euler, utilisant un flux de Lax-Friedrichs avec un limiteur de pente de van Leer symétrique, comme le schéma de la partie *macro* de [@dimarco]. Nous utiliserons donc le schéma suivant\ :

$$
  U_i^{n+1} = U_i^n - \frac{\Delta t}{\Delta x}(\mathcal{F}_{i+\frac{1}{2}}^n - \mathcal{F}_{i-\frac{1}{2}}^n) - \frac{\Delta t}{2\Delta x}(G_{i+1}^n - G_{i-1}^n)
$$

où la grandeur calculée $U_i^n$ est une approximation de $U(t^n,x_i)$ au temps $t^n = n\Delta t$ en $x_i = i\Delta x$. Le flux $G_{i}^n$ fait le lien avec la partie *micro*\ :

$$
  G_i^n = \sum_k v_k m(v_k) g_{i,k}^n \Delta v
$$

Le flux numérique $\mathcal{F}_{i+\frac{1}{2}}^n$ donné par\ :

$$
  \mathcal{F}_{i+\frac{1}{2}}^n = \frac{1}{2}(\mathcal{F}(U^n_{i}) + \mathcal{F}(U^n_{i+1})) -\frac{1}{2}\lambda(U_{i+1}^n - U_i^n)) + \frac{1}{4}(\sigma_i^{n,+} - \sigma_{i+1}^{n,-})
$$

où\ :

* $\mathcal{F}$ est la fonction du modèle d’Euler donné par\ :

  $$
    \mathcal{F}:U=\begin{pmatrix}\rho \\ \rho u \\ e\end{pmatrix} \mapsto \mathcal{F}(U) = \begin{pmatrix} \rho u \\ \rho u^2 + p \\ eu + pu \end{pmatrix}
  $$

  où $p=2e-\rho u^2$ est la pression.
* $\sigma_i^{n,\pm}$ est un terme correcteur de second ordre, notons $\eta_i^{n,\pm} = \mathcal{F}(U_i^n)\pm\lambda U_i^n$\ :

  $$
    \sigma_i^{n,\pm} = ( \eta_i^{n,\pm} - \eta_{i-1}^{n,\pm} )\phi(\chi_i^{n,\pm})
  $$

  avec $\phi$ la fonction de limiteur de pente de van Leer symétrique donnée par :

  $$
    \phi:x\mapsto \frac{|x|+x}{1+|x|}
  $$

  fonction que l’on applique à $\chi_i^{n,\pm}$ donné par :
  $$
    \chi_i^{n,\pm} = \frac{\eta_i^{n,\pm} - \eta_{i-1}^{n,\pm}}{\eta_{i+1}^{n,\pm} - \eta_i^{n,\pm}}
  $$

* $\lambda$ est la plus grande valeur propre du système d’Euler.

### Écriture de la partie *micro*

La partie *micro* ([!eq:mima:micro]) ne correspond plus simplement au modèle cinétique précédemment étudié. Le projecteur $\Pi$ ([!eq:defPi]) fait intervenir de nouveaux termes.

$$
  g^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ g^n - \Delta t (I\underbrace{-\Pi}_{\text{(a)}})(v\cdot\nabla_x g^n) - \Delta t (I\underbrace{-\Pi}_{\text{(b)}})(v\cdot\nabla_x \mathcal{M}_{[U^{n+1}]}) \right]
$$

Ces nouveaux termes $\text{(a)}$ et $\text{(b)}$ nécessitent l'appel du même projecteur $\Pi$, il est intéressant de les regrouper pour minimiser le temps de calcul\ :

$$
  g^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ g^n -\Delta t (I-\Pi)(v\cdot\nabla_x(g^n+\mathcal{M}_{[U^{n+1}]}) \right]
$$

Ne résulte de cette réécriture qu'une seule dérviée en espace à approximer via les flux numériques d'ordre élevé précédemment présentés.

$$
  g^{n+1}_{i,k} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ g^n_{i,k} - (I-\Pi)\left(\frac{\Delta t}{\Delta x}v_k(\tilde{f}^n_{i+\frac{1}{2},k} - \tilde{f}^n_{i-\frac{1}{2},k})\right)  \right]
$$

où $\tilde{f}^n_{i+\frac{1}{2},k}$ est le flux numérique de $\tilde{f}^n_{i,k} = g^n_{i,k} + (\mathcal{M}_{[U^{n+1}]})_{i,k}$.


### Algorithme général

On suppose donné un maillage de l'espace des phases, on suppose $g_{i,k}^n$ et $U_i^n$ donnés par l'itération précédente, le calcul de la nouvelle itération s'effectue schématiquement comme suit\ :

1. On calcule le flux $G_i^n$ de $g_{i,k}^n$\ :

  $$
    G_i^n \gets \sum_k v_k m(v_k) g_{i,k}^n \Delta v
  $$

Ceci permettra d'effectuer une approximation de $\partial_x \langle vm(v)g \rangle$ par $\frac{G_{i+1}^n - G_{i-1}^n}{2\Delta x}$.

2. Résolution de la partie *macro* : $\partial_t U + \partial_x \mathcal{F}(U) + \partial_x\langle vm(v)g \rangle = 0$ avec un schéma de *Lax-Friedrichs*, nous obtenons ainsi $U^{n+1}_i\,\forall i$.

  $$
    U_i^{n+1} \gets U_i^n - \frac{\Delta t}{\Delta x}(\mathcal{F}(U^n)_{i+\frac{1}{2}} - \mathcal{F}(U^n)_{i-\frac{1}{2}}) - \frac{\Delta t}{2\Delta x}(G_{i+1}^n - G_{i-1}^n)
  $$

3. On calcule la maxwellienne via l'incrémentation du vecteur $U^{n+1}$\ :

  $$
    (\mathcal{M}_{[U^{n+1}]})_{i,k} = \frac{\rho^{n+1}_i}{\sqrt{2\pi T^{n+1}_i}} \exp\left(-\frac{1}{2}\frac{ | u^{n+1}_i - v_k |^2 }{T^{n+1}_i}\right)
  $$

4. On calcule les flux numériques d'ordre élevé de $g_{i+\frac{1}{2},k}^n$ et $(\mathcal{M}_{[U^{n+1}]})_{i+\frac{1}{2},k}$, ceci permettra d'approximer les dérivées partielles en espace sur ces termes.

  $$
    g_{i+\frac{1}{2},k}^n \gets \left( (g_{j,k}^n)_{j\in [\![ i-2;i+2 ]\!] } , v_k \right)
  $$
  $$
    (\mathcal{M}_{[U^{n+1}]})_{i+\frac{1}{2},k} \gets \left( ((\mathcal{M}_{[U^{n+1}]})_{j,k})_{j\in [\![ i-2;i+2 ]\!] } , v_k \right)
  $$

5. On incrémente $g_{i,k}^n$ via la partie *micro*\ :

  $$
  \begin{aligned}
    g_{i,k}^{n+1} \gets \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[\vphantom{\frac{\Delta}{\Delta}} g_{i,k}^n \right. & - (I-\Pi_f)\left(\frac{\Delta t}{\Delta x}v_k(g_{i+\frac{1}{2},k}^n - g_{i-\frac{1}{2},k}^n)\right) \\
    & \left. - (I-\Pi_f)\left( \frac{\Delta t}{\Delta x}v_k( (\mathcal{M}_{[U^{n+1}]})_{i+\frac{1}{2},k} - (\mathcal{M}_{[U^{n+1}]})_{i-\frac{1}{2},k})\right) \vphantom{\frac{\Delta}{\Delta}} \right]
  \end{aligned}
  $$

  Ceci peut se résumer à deux termes de transports projetés selon $(I-\Pi_f)$. La discrétisation en temps présenté ici utilise une méthode d'Euler implicite ; numériquement nous n'avons pas observé d'instabilité dans le cadre d'un gaz raréfié. La mécanique des plasmas étudie traditionnellement des comportement en temps long, dans ce cas une discrétisation d'ordre plus élevé en temps fut nécessaire pour accompagner l'ordre élevé en espace. 

### Propriétés du schéma

Dans le modèle continue, la propriété $\Pi_f(g) = 0$ est assuré par construction de $g$, à tout instant $t$. Dans le schéma numérique il faut s'assurer que cette propriété est conserver si $\Pi_f(g^0) = 0$. Pour cela nous allons étudier $\Pi_f(g^{n+1})$ en supposant $\Pi_f(g^n) = 0$. Le schéma nous donne\ :

$$
  \Pi_f(g^{n+1}) = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ \Pi g^n - \Pi (I-\Pi)\left( \frac{\Delta t}{\Delta x}v\partial_x \tilde{f}^n  \right)  \right]
$$

Or $(I-\Pi_f)(v\partial_x \tilde{f}^n)$ appartient au noyau de $\Pi_f$, par propriété du l'opérateur de projection nous obtenons donc\ :

$$
  \Pi_f(g^{n+1}) = 0
$$

D'où la propriété suivante\ :

$$
  \Pi_f(g^n) = 0 \Rightarrow \Pi_f(g^{n+1}) = 0
$$

La variable d'entrée de simulation $g^0_{i,k}$ doit donc être initialisée de telle sorte à garantir cette propriété. Dans nos cas tests nous connaissons systématiquement la fonction $f^0_{i,k}$, il suffit alors d'initialiser $g^0_{i,k}$ à\ :

$$
  g^0_{i,k} = f^0_{i,k} - (\mathcal{M}_{[f^0]})_{i,k}
$$



## Approximation du modèle *micro-macro* avec $h(t,x)$

Dans cette partie, nous fixons la dimension du problème à $d=1$, en effet l'approche que nous avons pu avoir par la suite sur la fonction $h(t,x)$ ne se généralise pas directement au cas $d=2,3$.

La discrétisation directe du modèle *micro* avec l'approximation approtée par la fonction $h$ décrit en [!eq:mM:h] s'écrit comme\ :

$$
  \begin{aligned}
    g_{i,k}^{n+1} \gets \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[\vphantom{\frac{\Delta}{\Delta}} g_{i,k}^n \right. & - h_i^n(I-\Pi_f)\left(\frac{\Delta t}{\Delta x}v_k(g_{i+\frac{1}{2},k}^n - g_{i-\frac{1}{2},k}^n)\right) \\
    & \left. - h_i^n(I-\Pi_f)\left( \frac{\Delta t}{\Delta x}v_k( (\mathcal{M}_{[U^{n+1}]})_{i+\frac{1}{2},k} - (\mathcal{M}_{[U^{n+1}]})_{i-\frac{1}{2},k})\right) \right. \\
    & \left. \vphantom{\frac{\Delta}{\Delta}} + \frac{g_{i,k}^n}{h_i^n}\partial_t h_i^n \right]
  \end{aligned}
$${#eq:num:mM:h}

où $h_i^n$ est une approximation de $h(t^n,x_i)$

L'approche proposée dans [@dimarco] est de calculer la fonction $h(t,x)$ à partir du moment de la fonction $g$, c'est-à-dire à partir de $\langle m(v_k)g_{i,k}^n\rangle_v$. Cette méthode de calcul de la fonction $h$ nécessite le parcours de l'ensemble du domaine à l'itération $t^n$ ; une approche similaire est utilisée dans [@filbet] avec le calcul des cellules du milieu hydrodynamique ou cinétique en fonction d'un critère évalué à chaque itération. Cette méthode fonctionne très bien en théorie mais ne permet pas de réduire le temps de calcul en ne parcourant, à l'itération $t^n$, que le support de $h(t^n,\cdot)$. Nous avons opté ici pour une technique nécessitant une connaissance en amont des zones de chocs et du parcours de l'onde de choc, c'est-à-dire une connaissance *a priori* de $\Omega_K(t)$.

Dans un premier temps, pour étudier la dynamique et les conséquences d'une fonction indicatrice nous nous sommes restreints à une fonction $h$ constante au cours du temps, et avons testé différent profils : fonction porte ou trapézoïdale. Cela a permis de mettre au point la résolution de la partie *micro* uniquement sur le sous-domaine $\Omega_K$. Algorithmiquement cela se traduit par l'introduction de deux variables $x_s$ et $x_e$ ($s$ pour *start* et $e$ pour *end*) telles que\ :

$$
  \Omega_K \subset [x_s,x_e]
$$

Nous définissons 2 indices $i_s$ et $i_e$ tels que $x_s = i_s\Delta x$ et $x_e = i_e \Delta x$. Le schéma sur $g$ se définit comme\ :

$$
  g_{i,k}^n \gets \begin{cases}
    \hat{g}_{i,k}^n  & \text{si } i\in [\![ i_s , i_e  ]\!] \\
    0                & \text{sinon}
  \end{cases}
$$

où $\hat{g}_{i,k}^n$ est la grandeur calculée par [!eq:num:mM:h]. Une fois cette technique mise au point il a suffit de trouver, de manière empirique, deux fonctions $x_s:t\mapsto x_s(t)$ et $x_e:t\mapsto x_e(t)$ s'adaptant correctement aux conditions initiales simulées.

### $h$ une fonction porte

> TODO: revoir les parties de tests avec $h$

Dans un premier temps nous allons considérer une fonction $h$ continument dérivable mais dont les variations s'effectuent sur un intervalle de longueur inférieure à $\Delta x$, $h$ se résume donc à une fonction porte :

$$
  h_i = \begin{cases}
    0 &  \textrm{, si}\ x_i < x_s \\
    1 &  \textrm{, si}\ x_s \leq x_i \leq x_e \\
    0 &  \textrm{, si}\ x_i > x_e \\
    \end{cases}
$$

> TODO: mettre 2 cas tests, 1 avec $h$ trop petit (apparition d'oscillations parasites à la fonction du domaine), et un autre où tout se passe bien (domaine plus large)

Le risque de la mauvaise anticipation du domaine $\Omega_K$ est que celui-ci déborde du support de $h$. Numériquement ce risque se traduit par l'apparition d'oscillations dues à une discontinuité de $g$ aux bords du support de $h$.


### $h$ une fonction trapèze

Considérons maintenant une fonction $h$ définie comme suit :

$$
  h_i = \begin{cases}
    0                                               & \textrm{, si\ }           x_i < x_s     \\
     \frac{1}{x_s^*-x_s} x - \frac{x_s}{x_s^*-x_s}  & \textrm{, si\ } x_s     < x_i < x_s^{*} \\ 
    1                                               & \textrm{, si\ } x_s^{*} < x_i < x_e^{*} \\
    -\frac{1}{x_e-x_e^*} x + \frac{x_e}{x_e-x_e^* } & \textrm{, si\ } x_e^{*} < x_i < x_e     \\
    0                                               & \textrm{, si\ } x_e     < x_i           \\
  \end{cases}
$$

Pour les différents tests sur une telle fonction on conservera toujours les valeurs de $x_s$ et $x_e$ identiques au cas test de la fonction porte, nous allons donc jouer sur les valeurs de $x_s^*$ et $x_e^*$. On choisit généralement $x_s^*$ et $x_e^*$ de façon symétrique c'est-à-dire :

$$
  x_s^* = x_s + \delta x \qquad x_e^* = x_e - \delta x
$$

On obtient ainsi dans les cas extrêmes une fonction porte pour $\delta x = 0$ ou une fonction chapeau pour $\delta x = \frac{x_e-x_s}{2}$.

> TODO: cas d'une fonction chapeau et une ou deux fonctions trapézoïdales

### $h(t,x)$ une fonction dépendant du temps

Maintenant essayons de faire évoluer $h$ en fonction du temps. Comme nous l'avons écrit précédemment il est possible d'utiliser la troisième composante du flux cinétique de $g$, comme dans [@dimarco]. Ceci implique de calculer $g$ en tout point de l'espace, ce que l'introduction de la fonction $h$ nous permet en principe d'éviter. En effet, l'introduction de la fonction $h$ permet, dans la partie *micro*, plus coûteuse en temps de calcul que la partie *macro*, de ne parcourir l'espace qu'entre les valeurs $x_s$ et $x_e$.

Une autre méthode utilisée dans [@filbet], est de déterminer dans chaque cellule, à chaque itération, le modèle prédominant entre fluide et cinétique. Cela demande de l'évaluation systématique d'un critère, potentiellement coûteux en temps de calcul, pour éventuellement échanger le modèle prédominant dans chaque cellule. L'inconvénient de ce type d'approche est le calcul de dérivées à la jonction entre deux modèles. Le nombre restreint de cellules où le modèle cinétique est effectivement évaluée permet en principe de réduire globalement le temps de simulation.

Á l'inverse des approches présentées dans [@dimarco] et [@filbet], nous avons besoin d'une connaissance amont du problème. Pour ce faire nous allons étudier la troisème composante du flux cinétique de $g$ dans sa globalitéi, sans fonction $h$, seule composante non nulle du flux cinétique en théorie par la définition de $g$ comme étant à moyenne nulle en $v$. Ce flux (respectivement le logarithme de ce flux) est représenté en figure TODO (respectivement en figure TODO).

<div>
  ![Flux numérique de $g$](img/mimas_test/h_t/fluxg.png)
  
  ![Logarithme du flux numérique de $g$](img/mimas_test/h_t/fluxg_log.png)

Visualisation de la troisième composante du flux cinétique de $g$ en fin de simulation
</div>

Contrairement à ce qui était attendue le flux ne diminue pas suffisamment pour le contraindre dans une région. Le seuil que nous allons utilisé est $10^{-15}$, ce qui peut correspondre à la sortie du bruit numérique de la précision du zéro machine ; un seuil plus petit, au alentour de $10^{-17}$ est facilement envisageable et sans doute plus juste, mais cela se fait au détriment du temps de calcul.

![Évolution de $x_s$ et $x_e$ au cours du temps](img/mimas_test/h_t/xsxe.png)

Sur cette courbe, $x_s$ correspond au premier dépassement du seuil, et $x_e$ au dernier ; sont aussi représentés les grandeurs de $x_s$ et $x_e$ précédemment choisis dans le cas d'une fonction porte.

Nous souhaitons que $h(t,x)$ enveloppe la zone où $\langle v_km(v_k)g_{i,k}^n\rangle_3 > 10^{-15}$, pour cela nous considérons deux fonctions $x_s^n$ et $x_e^n$ donnant au cours du temps le domaine cinétique. Cette démarche ne fonctionne pas pour un système périodique c'est pour cela que nous sommes restés avec des conditions aux bords de Neumann. L'approche dans [@filbet] ne permet pas de diminuer la taille du domaine à parcourir au cours du temps ; en revanche elle propose, dans le cas d'une solution régulière, d'avoir un libre parcours moyen dépendant de $x$, cela permet d'effectuer une transition plus douce entre un modèle cinétique et fluide.



## Tests numériques dans le cas de gaz raréfiés

> Temps de calcul des différents modèles, et erreur par rapport au code de référence : Euler, et avantage qualitatif des différents modèles (plasma avec $\varepsilon \not\to 0$ et champ électrique : impossible avec simple approximation Euler)

### Conditions aux bords périodiques

Condition initiale\ :

$$
  f(t=0,x,v) = (1+\alpha\cos(k_x x))\text{e}^{-\frac{|v|^2}{2}}
$$

ou un truc du genre

### Condition aux bords de Neumann

> Tube à choc de Sob

### Milieu non homogène : $\varepsilon = \varepsilon(x)$

> Cas test dans [@filbet], comparatif au code cinétique.

### Fonction indicatrice

> TODO: mettre ici un cas où $h$ provoque des oscillations (trop petit), et des cas où ça marche bien


# Application pour les plasma

> C'est dans cette partie qu'on a vraiment besoin des tests 2D et qu'on introduit un champ électrique

## Modèle cinétique

> Programme de référence, présentation un peu plus rapide avec l'ajout du terme de champ électrique. Préciser la nécessité numériquement d'introduire RK3 pour l'ordre élevé en espace, avec recalcule de l'équation de Poisson sur chaque étape du RK3.


## Modèle *micro-macro*

> Modèle hybride basé sur le modèle cinétique, donc comparatif aux résultats précédents, précision de l'ajout dans la partie *micro* et *macro* du champ électrique. Pour le moment RK3 ne fonctionne pas (*a priori* la Maxwellienne ne reste pas constante sur chaque étape de RK3 donc obligé de recalculer $u$, et $T$, pas uniquement $\rho$, et même ainsi j'ai encore des instabilités).

> Introduction de $h(t,x)$

## Tests numériques dans le cas de plasmas

### Double beam

### Landau

# Liste des figures à refaire

Pour chaque simulation conserver les paramètres de simulation : entrée, $\varepsilon$, $\Delta x$, $\Delta v$, $\Delta t$, $nx$, $nv$, $T_f$ 

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
* Cas tests de viscosité (rotation d'un *pacman*)
* $log||E||_2 = f(t)$ sur plusieurs cas tests

