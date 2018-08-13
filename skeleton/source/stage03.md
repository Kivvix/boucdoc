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

La variable de base dans le modèle est le temps $t$ ; à chaque pas de temps on calcule la somme des forces pour obtenir l'accélération, la vitesse puis la position s'obtiennent par intégration successive.

Ce modèle est très coûteux en temps de calcul puisqu'il possède une complexité algorithmique en $\mathcal{O}(2^n)$ où $n$ est le nombre de particules en interaction. L'utilisation de ce type de modèle est inenvisageable dès que le nombre de particules atteint la centaine de particules. Dans le cadre de l'étude des plasma, le nombre $n$ de particules en interaction est voisin du nombre d'Avogadro $\mathcal{N}_A \approx 6,02\cdot 10^{23}$.

Une approximation de ce modèle est parfois utilisé à l'aide d'une représentation arborescente de l'espace via un *quadtree*, ou *$kd$-tree* par exemple ; cela permet de négliger les interactions à plus longue distance. C'est ce qui est par exemple utilisé dans des simulations de galaxies, ou dans des moteurs de collision comme celui du jeu vidéo *Doom*.


## Modèle cinétique

Le principe du modèle cinétique est de proposer une description intermédiaire entre le modèle microscopique et macroscopique. On représente les particules dans l'espace des phases $(x,v)$, où $x \in \Omega \subset \mathbb{R}^d$ désigne la position et $v \in \mathbb{R}^d$ la vitesse, avec $d=1,2,3$ la dimension du problème.

Nous n'étudions pas chaque particule individuellement mais une valeur statistique qu'est la fonction de distribution de particules dans l'espace des phases $f$ : $f(t,x,v)\mathrm{d}x\mathrm{d}v$ représente le nombre de particules dans un volume élémentaire de l'espace des phases $\mathrm{d}x\mathrm{d}v$ au temps $t \geq 0$.

L'inconnue $f(t,x,v)$ est alors solution d'une équation de transport dans l'espace des phases à laquelle on ajoute un terme de collision\ :

$$
  \partial_t f + v\cdot\nabla_x f = Q(f,f)
$${#eq:cine}

où le transport s'effectue à vitesse $v$ dans la direction $x$. $Q(f,f)$ représente un opérateur quadratique de collision, il modélise les interactions binaires entre particules ; plusieurs expressions sont possibles comme l'opérateur de Boltzmann pour les gaz raréfiés, ou les opérateurs Landau ou BGK par exemple pour le cas des particules chargées.

Les variables de base du problème sont $t$, $x$ et $v$. Une simulation directe du problème complet impose donc de travailler en 7 dimensions : une de temps, et 6 pour l'espace des phases $(x,v)$. Travailler dans un espace de dimension aussi élevé implique des coûts importants en temps de calcul et dans l'utilisation de la mémoire. Un maillage non cartésien permet de ne raffiner que localement le domaine, mais les contraintes de gestion du maillage nous ont orientés vers une autre alternative.

L'étude théorique se fera en dimension $d$, mais pour simplifier l'étude, l'implémentation et la visualisation se feront en dimension $d=1$.

Ce modèle utilise à la manière du modèle macroscopique, une grandeur intégrale ; celle-ci vit dans l'espace des phases ce qui permet d'avoir une description plus précise puisqu'elle prend en compte la répartition des particules en vitesse. La grandeur de travail est une fonction $f$ vivant dans l'espace des phases $(x,v)$. Les variables $(t,x,v)$ vivent dans $[0,T]\times\Omega\times\mathbb{R}^d$, où $\Omega$ est un fermé borné de $\mathbb{R}^d$, la vitesse $v$ n'est *a priori* pas borné par notre modélisation. Ce grand nombre de dimensions implique un nombre important de variables à stocker lors de la simulation numérique du modèle, ainsi qu'un nombre important de boucles pour parcourir toutes les dimensions du problème, le modèle est donc coûteux en temps de calcul ainsi qu'en utilisation de la mémoire.

### Conservation de la masse

> Mettre dans la partie [Cinetique vers fluide](#cinétique-vers-fluide), car concrètement j'utilise les notations présentées là-bas

Les propriétés de l'opérateur de collision $Q(f)$ de l'équation [!eq:cine] implique la conservation de la masse, de l'impulsion et de l'énergie lors des collisions\ :

$$
  \int_{\mathbb{R}^d} m(v)Q(f)\,\mathrm{d}v = 0
$$

où $m(v) = ( 1, v , |v|^2 )$. En multipliant [!eq:cine] par $m(v)$, puis en intégrant selon les directions $x$ et $v$ on obtient\ :

$$
  \iint_{\Omega\times\mathbb{R}^d} m(v)(\partial_t f + v\cdot\nabla_x f)\,\mathrm{d}x\mathrm{d}v = \frac{1}{\varepsilon}\iint_{\Omega\times\mathbb{R}^d}m(v)Q(f)\,\mathrm{d}x\mathrm{d}v
$$

Or les moments de $Q(f)$ sont nuls, et l'intégrale sur l'esapce de la dérivée spatiale vaut zéro. On obtient finalement\ :

$$
  \frac{\mathrm{d}}{\mathrm{d}t}\iint_{\Omega\times\mathbb{R}^d} m(v)f(t,x,v)\,\mathrm{d}x\mathrm{d}v = 0
$${#eq:cine:conservation}

La grandeur $f$ représente la densité de particules chargées dans l'espace des phases, donc la grandeur $\iint f(t,x,v)\,\mathrm{d}x\mathrm{d}v$ correspond à la masse totale du système. Les composantes suivantes calculées dans [!eq:cine:conservation] représentent l'impulsion et l'énergie totale du système. Cette équation garantit la conservation de la masse, de la quantité de mouvement et de l'énergie dans le modèle.

### Équation de Poisson

Dans le contexte de la physique des plasmas, nous étudions le mouvement de particules chargées formant le plasma, c'est à dire des électrons et des ions. L'équation de Poisson est un modèle physique de l'évolution du champ électrique $E$ en fonction des particules chargées présentes\ :

$$
  \nabla_x \cdot E = \sum_s q_s \rho_s
$$

avec $q_s$ la charge électrique d'une espèce $s$ de particule, $\rho_s$ la densité de cette même espèce $s$. Dans le cadre du modèle cinétique, $f$ représente la densité d'électrons, seule espèce chargée considérée comme mouvante ; en effet les ions, beaucoup plus lourds, peuvent être considérés comment statique. En normalisant les charges électriques, l'équation de Poisson peut se réécrire\ :

$$
  \nabla_x \cdot E = \int_{\mathrm{R}^d} f\,\mathrm{d}v - 1
$${#eq:cine:poisson}

où $f$ est la distribution d'électrons et le terme $1$ représente la densité ionique. En rajoutant le terme de force induit par le champ électrique $E$, l'équation du modèle cinétique [!eq:cine] mène à l'équation de Vlasov\ :

$$
  \begin{cases}
    \partial_t f + v\cdot\nabla_x f + E\cdot\nabla_v f = Q \\
    \nabla_x\cdot E = \int f\,\mathrm{d}v -1
  \end{cases}
$${#eq:cine:vp}

Ce modèle est une équation de transport dans l'espace des phases à vitesse $v$ dans la direction $x$ et $E$ dans la direction $v$ avec un terme de collision $Q$.

## Modèle macroscopique

Les modèles macroscopiques sont très utilisés en mécanique des fluides ; le système d'équations dépend alors de peu de variables physiques pour d'écrire l'état thermodynamique. Ces variables sont condensées en un seul vecteur de variables extensives $U$\ :

$$
  U = (\rho,u,T,\dots)(t,x)
$$

où $\rho$ désigne la densité, $u$ la vitesse moyenne et $T$ la température au temps $t\geq 0$ à la position $x$ ; $U$ vérifie l’équation d’Euler ou de Navier-Stockes\ :

$$
  \partial_t U + \nabla_x\cdot \mathcal{F}(U)(t,x) = 0
$${#eq:euler}

où la fonction $\mathcal{F}$ désigne le flux.

Les variables de bases du problème sont $t$ et $x$. La simulation n'impose que 4 dimensions, une de temps et 3 d'espace ; donc dans une région se comportant globalement comme un fluide il est privilégié d'utiliser ce type de méthode, moins coûteuse en temps de calcul qu'un modèle microscopique ou cinétique.

Nous resterons ici dans le cadre des équations d'Euler, $U$ est définit par\ :

$$
  U = \begin{pmatrix}
    \rho   \\
    \rho u \\
    e
  \end{pmatrix}
$$

où $e$ est l’énergie interne. Le vecteur $U$ vit dans $\mathbb{R}^{d+2}$ car $\rho \in \mathbb{R}$, $e\in\mathbb{R}$ et $u\mathbb{R}^d$. Le flux $\mathcal{F}$ est alors défini en dimension $d$ par\ :

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

En dimension $d \ne 1$ le flux $\mathcal{F}(U)$ n'est plus un vecteur, mais puisque l'on calcule la divergence du flux : $\nabla_x\cdot\mathcal{F}(U)$, on retrouve bien un vecteur à $d+2$ dimensions. En effet la première et dernière composante sont de simples scalaires, donc leur dérivé est aussi un scalaire ; la seconde composante est une matrice carrée de taille $d$, dont la divergence donne un vecteur de taille $d$.


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

> TODO: cette dernière remarque à plus sa place dans la partie suivante puisque c'est là que l'on discute de l'équivalence entre le modèle cinétique et macroscopique (on a pas encore précisé ici que $\int f\,\mathrm{d}v = \rho$)


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

Par la suite nous choisirons l'opérateur de collision BGK dans l'équation [!eq:cine], celui-ci est définit par\ :

$$
  Q(f) = \frac{1}{\varepsilon}(M_{[f]} - f)
$$

où $\varepsilon = \frac{\ell}{L}$ est une donnée du problème physique avec $\ell$ le libre parcours moyen et $L$ la dimension du domaine ; $\mathcal{M}_{[f]}$ est la distribution de vitesse maxwellienne définit par\ :

$$
  \mathcal{M}_{[f]} = \frac{\rho}{(2\pi T)^{\frac{d}{2}}}\exp\left(-\frac{|v-u|^2}{2T}\right)
$$

Une propriété des opérateurs de collisions est de garantir la conservation de la masse, de l'impulsion et de l'énergie, cela se traduit par l'équation\ :

$$
  \int_{\mathbb{R}^d} m(v)Q(f)\,\mathrm{d}v = 0
$$

Par conséquent, avec l'opérateur de collision BGK cela signifie\ :

$$
  \int_{\mathbb{R}^d} m(v)\mathcal{M}_{[f]}\,\mathrm{d}v = \int_{\mathbb{R}^d} m(v)f(v)\,\mathrm{d}v
$$

On multiplie l'équation [!eq:cine] par $m(v)$ puis on intègre par rapport à $v$ pour obtenir\ :

$$
  \partial_t U + \nabla_x\cdot\int_{\mathbb{R}^d}vm(v)f\,\mathrm{d}v = 0
$${#eq:cineuler]

Quand $\varepsilon \to 0$ on trouve grâce à [!eq:cine] que $f \to \mathcal{M}_{[f]}$ ; on peut donc écrire $f$ comme un développement limitée en $\varepsilon$ comme\ :

$$
  f(t,x,v) = \mathcal{M}_{[f]} + \mathcal{O}(\varepsilon)
$$

Le vecteur $U$ peut donc s'écrire aussi bien via $f$ ou $\mathcal{M}$\ :

$$
  \begin{aligned}
    U(t,x) &= \int_{\mathbb{R}^d} m(v)f(t,x,v)\,\mathrm{d}v \\
           &= \int_{\mathbb{R}^d} m(v)\mathcal{M}_{[U(t,x)]}(v)\,\mathrm{d}v
  \end{aligned}
$$

Ainsi en écrivant, composante par composante l'équation [!eq:cineuler] on trouve\ :

$$
  \partial_t\begin{pmatrix}U_1 \\ U_2 \\ U_3 \end{pmatrix} + \nabla_x\cdot\begin{pmatrix}U_2\\ U_3 \\ \int v^3f\,\mathrm{d}v \end{pmatrix} = 0
$${#eq:cineulero}

où le terme $\int vm(v)f\,\mathrm{d}v$ peut s'approximer à l'aide de la maxwellienne, en effet\ :

$$
  \int_{\mathbb{R}^d} vm(v)\mathcal{M}\,\mathrm{d}v = \begin{pmatrix} \rho u \\ \rho u\otimes u + p\mathbb{I}_d \\ u(e+p) \end{pmatrix}
$$

Ainsi on peut fermer le problème [!eq:cineulero] par une approximation de $\int v^3\mathcal{M}_{[U]}(v)\,\mathrm{d}v = \rho u^3 + 3\rho Tu$. On retrouve alors les équations d'Euler.

En ajoutant un terme dans le développement limité de $f$ en $\varepsilon$ on obtient de manière similaire les équations de Navier-Stokes.

Nous obtenons donc une équivalence entre le modèle cinétique et fluide lorsque $\varepsilon$ tend vers $0$. Cette remarque permet de valider nos schéma et d'en vérifier les résultats en les comparant à un simulateur de fluide eulérien.



# Modèles hybrides fluides-cinétiques

Pour tenter d'obtenir un compromis coût numérique, précision, on se propose de suivre une approche hybride fluide, cinétique. Pour cela, on va construire un modèle *micro-macro* basé sur une décomposition de l'inconnue cinétique $f$ en une partie macroscopique (une distribution maxwellienne) ; plus une partie microscopique (l'écart par rapport à l'équilibre thermodynamique). Cette décomposition est similaire à celle décrite dans [@dimarco] ou [@crestetto].

Dans la pratique, la fonction inconnue $f$ n'est jamais éloignée de son équilibre maxwellien ; nous pouvons donc réécrire $f$ comme une somme\ :

$$
  f = \mathcal{M}_{[f]} + g
$$

où $g$ est l'écart à l'équilibre maxwellien. On peut montrer que $g$ est à moyenne nulle en $v$, or il existe une décomposition unique dans $L^2$ de $f$ en somme d'une fonction $M$ et d'une fonctionne de moyenne nulle en $v$. Puisque nous avons\ :

$$
  \int_{\mathbb{R}^d} m(v)\mathcal{M}_{[f]}\,\mathrm{d}v = \int_{\mathbb{R}^d} m(v)f\,\mathrm{d}v
$$

Nous pouvons en conclure que $\int m(v)g\,\mathrm{d}v =0$. Cette décomposition $f = \mathcal{M}+g$ correspond à une décomposition de $L^2$ selon le noyau de l'opérateur de collision\ :

$$
  L^2 = \ker Q + \text{Im} Q
$$

Cette décomposition peut s'exprimer comme une projection $\Pi$, d'où la décomposition de $f$\ :

$$
  f = \Pi_f + (I-\Pi_f)f
$$

On a donc $\mathcal{M}_{[f]} = \Pi_f$ et $(I-\Pi_f)f = g$, où le projecteur $\Pi$ est défini dans [@crestetto] par\ :

$$
  \begin{aligned}
    \Pi_{\mathcal{M}_{[f]}}(\varphi) = \frac{1}{\rho}\left[\vphantom{\frac{\Delta}{\Delta}} \langle \varphi \rangle \right. & + \frac{(v-u)\langle(v-u)\varphi\rangle}{T} \\
     & + \left. \left( \frac{|v-u|^2}{2T} - \frac{1}{2} \right)\left\langle \left(\frac{|v-u|^2}{T}-1\right)\varphi \right\rangle \right]\mathcal{M}_{[f]}
  \end{aligned}
$${eq:defPi}

La projecteur $\Pi$ va nous permettre d'écrire une équation sur les paramètres de $\mathcal{M}_{[f]}$, à savoir $U$ ou $(\rho,u,T)$, qui représentera le modèle *macro* ; et une équation sur $g$, représentant le modèle *micro*.


## Obtention du modèle *macro*

Le vecteur $U$ est lié à l'inconnue $f$ via son moment\ :

$$
  U = \int_{\mathbb{R}^d} m(v)f(v)\,\mathrm{d}v
$$

En multipliant le modèle cinétique ([!eq:cine]) par $m(v)$ puis en intégrant selon $v$ on obtient\ :

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

Équation que l'on peut réécrire sous la forme suivante\ :

$$
  \partial_t U + \nabla_x\cdot\mathcal{F}(U) +  \nabla_x\langle vm(v)g \rangle_v = -\nabla_v\cdot \langle E_fm(v)(\mathcal{M}_{[f]} + g)\rangle_v
$${#eq:mima:macro}

L'équation [!eq:mima:macro] correspond à la description macroscopique du modèle hybride *micro-macro*.

## Obtention du modèle *micro*

Pour obtenir la description microscopique, on ne s'intéresse qu'à la perturbation $g$ de $f$. En effet toute l'information sur l'équilibre maxwellien $\mathcal{M}_{[f]}$ est contenue dans la description macroscopique. Il suffit maintenant de reprendre la modèle cinétique [!eq:cine] et de la projeter sur $\text{Im}Q$, c'est-à-dire en appliquant le projecteur $I-\Pi$\ :

$$
  \partial_t g + (I-\Pi)\left[v\cdot\nabla_x(\mathcal{M}_{[f]}+g) + E_f\cdot\nabla_v(\mathcal{M}_{[f]}+g)\right ] = -\frac{1}{\varepsilon}g
$${#eq:mima:micro}

Il s'agit là de la description microscopique du modèle *micro-macro*.

On peut montrer l'équivalence entre le modèle *micro-macro* (composé des équations [!eq:mima:macro] et [!eq:mima:micro]) et le modèle cinétique original (équation [!eq:cine])\ : 

$$
  \begin{cases}
    \partial_t U + \nabla_x\cdot \mathcal{F}(U) + \nabla_x\cdot \langle vm(v)g \rangle_v = 0 \\
    \partial_t g + v\cdot\nabla_x g = -\frac{1}{\varepsilon}g - (I-\Pi)(v\cdot\nabla_x \mathcal{M}_{[f]}) + \Pi(v\cdot\nabla_x g)
  \end{cases}
$${#eq:mM}


Le modèle cinétique [!eq:cine] sur $f$. Dans l'état, le modèle *micro-macro* n'a pas d'utilité propre ; cette réécriture du modèle cinétique sert de base pour des approximations. En effet il sera plus simple dans cette description de négliger la perturbation à l'équilibre $g$ sur une partie du domaine, que l'on nommera partie fluide du domaine.

Dans le cas limite $\varepsilon \to 0$, la seconde équation de [!eq:mM] nous donne formellement $g \to 0$, on retrouve alors l'équation d'Euler dans la première équation. Un développement en puissance de $\varepsilon$ donne\ :

$$
  g = -\varepsilon(I-\Pi)v\cdot\nabla_x\mathcal{M}_{[f]}
$$

résultat que l'on peut injecter dans l'équation *macro* pour obtenir les équations de Navier-Stokes.


## Approximation du modèle micro-macro

> TODO: Introduire l'idée en parlant de [@dimarco]

Le principal intérêt du modèle *micro-macro* est qu’il est possible d’effectuer plus simplement des approximations du modèle, en particulier ce que nous allons faire ici est une approximation uniquement de la partie *micro*.

Dans les régions où le système est à l'équilibre, c'est-à-dire $f \approx \mathcal{M}_{[f]}$, nous allons faire l'approximation $g=0$ dans cette zone. Nous introduisons la fonction $h:\Omega\mapsto[0,1]$ telle que :

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

Tentons d'exploiter cette hypothèse dans le modèle *micro-macro*, reprenons le modèle *micro* que nous multiplions par $h$\ :

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
  \partial_t g_K + hv\cdot\nabla_x g_K = -\frac{1}{\varepsilon}g_K - h(I-\Pi)(v\cdot\nabla_x \mathcal{M}_{[f]}) + h\Pi(v\cdot\nabla_x g_K) + \frac{g_K}{h}\partial_t h
$$

> TODO: ajouter la gestion du champ électrique


# Présentation des schémas

Dans cette partie, nous allons présenter différents schémas numériques pour résoudre le modèle *micro-macro* [!eq:mM]. Ce modèle comporte plusieurs difficultés qui devront être surmontées :

* Nous allons chercher des schémas d'ordre élevé en $(x,v)$ pour capturer les forts gradients qui peuvent apparaître selon les conditions initiales. Ces schémas dans l'espace des phases devront aussi fonctionner en multi-dimensions.
* L'opérateur de collision apporte un terme de raideur en $\frac{1}{\varepsilon}$ dans le cas où $\varepsilon \in ]0,1]$.
* Il est bien évidemment nécessaire d'assurer la stabilité du schéma par rapport au terme de transport, les simulations de plasma se font souvent en temps long.


## Schémas en temps

Pour étudier la raideur en $\frac{1}{\varepsilon}$, on se propose d'étudier la dynamique temporelle de l'équation différentielle suivante qui permet d'étudier la difficulté de $\varepsilon$ dans un modèle simplifié par rapport au modèle *micro-macro* complet\ :

$$
  \begin{cases}
    \frac{\mathrm{d}y}{\mathrm{d}t}(t) = -\frac{1}{\varepsilon}y(t) + \mathcal{F}(y(t)) \\
    y(0) = y_0
  \end{cases}
$${#eq:edot}

avec $t$ représentant le temps, $y:\mathbb{R}_+\to\mathbb{R}$ la fonction inconnue, $\mathcal{F}:\mathbb{R}\to\mathbb{R}$ le flux, avec comme condition initiale $y_0\in\mathbb{R}$.

On peut résumer la difficulté au cas $\mathcal{F} = 0$ pour étudie la stabilité des schémas temporels, au détriment de quelques paramètres physiques\ :

$$
  \frac{\mathrm{d}y}{\mathrm{d}t} = -\frac{1}{\varepsilon}y
$${#eq:edot2}

où $\varepsilon > 0$ peut être aussi petit que l'on veut pour représenter un système fluide. L'enjeu du schéma temporel est de pouvoir choisir le pas de temps $\Delta t$ indépendamment du paramètre physique $\varepsilon$.

Une discrétisation en temps de [!eq:edot2] nous amènera à calculer une approximation $y^n \approx y(t^n)$ où $t^n = n\Delta t$ avec $\Delta t$ notre pas de temps. Ainsi la discrétisation via un schéma d'Euler explicite de [!eq:edot2] nous donne\ :

$$
  \frac{y^{n+1}-y^n}{\Delta t} = -\frac{1}{\varepsilon}y^n
$$

soit\ :

$$
  y^n = \left( 1-\frac{\Delta t}{\varepsilon}\right)^n y_0
$$

La solution $(y^n)_n$ reste bornée si et seulement si $| 1-\frac{\Delta t}{\varepsilon} |\leq 1$, *ie* $\Delta t \leq 2\varepsilon$. Or le libre parcours moyen $\varepsilon$ peut être choisi arbitrairement petit, donc cette condition CFL n'est pas avantageuse et conduit à des temps de calculs trop coûteux. Il est donc impératif d'utiliser un schéma d'Euler implicite de la forme\ :

$$
  \frac{y^{n+1}-y^n}{\Delta t} = -\frac{1}{\varepsilon}y^{n+1}
$$

soit, sous forme itérative\ :

$$
  y^n = \frac{1}{(1+\frac{\Delta t}{\varepsilon})^n}y_0
$$

ce qui est inconditionnellement stable quelque soit la valeur de $\Delta t$ et de $\varepsilon$. Par conséquent nous utiliserons un schéma d'Euler implicite en temps pour tester et valider nos différents schémas sur le terme de transport.


### Schéma Runge-Kutta d'ordre 3

Pour des raisons de stabilité, lié à l'utilisation de schémas d'ordre élevé en $x$ (que l'on détaillera plus tard), nous avons été amené à considérer le schéma de Runge-Kutta d'ordre 3.

Le schéma en temps se résout de manière indépendante du schéma d'advection, par conséquent il s'agit d'une simple équation différentielle ordinaire que nous écrirons\ :

$$
  \frac{\mathrm{d}y}{\mathrm{d}t}(t) = L(y(t),t)
$$

avec $t$ le temps, $y:\mathbb{R}_+\to\mathbb{R}$ la fonction inconnue, $L:\mathbb{R}\times\mathbb{R}_+\to\mathbb{R}$ une fonction linéaire dépendant de $y$ et du temps. Nous cherchons à calculer $y^n \approx y(t^n)$, une approximation de $y$ au temps $t^n = n\Delta t$, avec $\Delta t > 0$ le pas de temps. Il existe plusieurs formulation du schéma de Runge-Kutta d'ordre 3, l'ordre 3 nécessite au minimum 3 étapes de calculs, une version ajoutant de la stabilité en 4 étapes existes, ainsi qu'une version utilisant peu de mémoire, décrient dans [@ssp_rk3]. Nous utiliserons le schéma suivant, le plus rapide en temps de calcul\ :

> TODO: se mettre d'accord sur les notations $u^n$ ou $y^n$

$$
  \begin{aligned}
    u^{(1)} &= u^n + \Delta t L(u^n,t^n) \\
    u^{(2)} &= \frac{3}{4}u^n + \frac{1}{4}u^{(1)} + \frac{1}{4}\Delta t L(u^{(1)},t^n+\Delta t) \\
    u^{n+1} &= \frac{1}{3}u^n + \frac{2}{3}u^{(2)} + \frac{2}{3}\Delta t L(u^{(2)},t^n+\frac{1}{2}\Delta t)
  \end{aligned}
$$

Dans le cadre du modèle *micro-macro* par exemple, nous avons $y=\mathcal{M}_{[f]}+g$ dans la partie *micro* sans terme de collision.

#### Application à un modèle cinétique avec collisions

> TODO: mettre ça après les schémas d'ordre élevé en espace

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

Pour approcher le terme de transport $\partial_t g + v\cdot\nabla_x g$, il est primordial d'utiliser des schémas d'ordre élevé  pour : capturer les forts gradients en diminuant la viscosité numérique ; utiliser moins de points lors de la simulation. Pour ces raisons nous allons présenter deux schémas d'ordre élevé permettant de résoudre une part des problèmes.

Le transport de $g$ donné par\ :

$$
  \partial_t g + v\cdot\nabla_x g = 0
$$

se ramène à une équation d'advection linéaire lorsque $v$ est discrétisé $v_k = k\Delta v$, avec $\Delta v > 0$ le pas de vitesse dans l'espace des phases. Ainsi l'exemple de base que nous utiliserons pour présenter ces schémas est une équation d'advection linéaire en une dimension\ :

$$
  \begin{cases}
    \partial_t u + a \partial_x u = 0 \\
    u(t=0,x) = u_0(x)
  \end{cases}
$$

où $t$ est le temps, $x$ la dimension d'espace et $u : \mathbb{R}_+\times\mathbb{R}\to\mathbb{R}$ est la fonction inconnue. On ajoute à cette équation des conditions aux bords qui dépendront des cas tests présentés.

Nous cherchons à calculer $u^n_i \approx u(t^n,x_i)$ une approximation de $u$ au temps $t^n = n\Delta t$, avec $\Delta t>0$ le pas de temps, en $x_i = i\Delta x$, avec $\Delta x>0$ le pas d'espace.

### Schéma compact

Dans un premier temps nous présenterons uniquement le cas d'un transport à vitesse $a$ positive. Un schéma linéaire différence finies avec un *stencil* de taille $r+s+1$ peut s'écrire de manière générale comme\ :

$$
  u_i^{n+1} = \sum_{k=-r}^s \gamma_k u_{i+k}^n
$${#eq:df:compact}

où $\gamma_k$ est un coefficient dépendant du nombre CFL $\nu = a\frac{\Delta t}{\Delta x}$.

L'erreur de consistance du schéma, au sens des différences finies, est définie par\ :

$$
  R_i^n = u(t^{n+1},x_i) - \sum_{k=-r}^s \gamma_k u(t^n,x_{i+k})
$$

on y reconnait la solution exacte en $x_i$ à l'instant $t^{n+1}$ : $u(t^{n+1},x_i)$ ainsi que l'approximation que l'on en fait par le biais d'un schéma aux différences finies : $\sum_{k=-r}^s \gamma_k u(t^n,x_{i+k})$.

On peut réécrire [!eq:df:compact] comme interprétation en volumes finis\ :

$$
  u_i^{n+1} = u_i^n - \nu (u^n_{i+\frac{1}{2}} - u^n_{i-\frac{1}{2}})
$$

où $u^n_{i+\frac{1}{2}}$ sont les flux numériques. Le calcul de ces flux est présenté dans [@Boyer:2014aa], nous choisirons ceux d'ordre élevé décrits dans [@despres]. L'ordre du flux dépend du choix du couple $(r,s)$, il est ainsi possible de retrouver plusieurs flux connus\ :

* Le schéma décentré amont, ou *upwind*\ :

  $$
    u_{i+\frac{1}{2}}^n = u_i^n
  $$

* Une combinaison de *Lax-Wendroff* (LW) et de *Beam-Warming* (BW) : $(1-\alpha )LW + \alpha BW$ avec $\alpha = \frac{1+\nu}{3}$\ :

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

C'est ce dernier flux que nous utiliserons par la suite.

#### Obtention de l'ordre

La solution exacte d'un problème de transport à vitesse $a$ constante est connue. Nous allons donc partir de ce problème, le résoudre sur un premier maillage et en calculer l'erreur ; puis répéter l'opération sur un maillage plus fin. Les différentes résolutions sur différents maillages s'effectuent toutes jusqu'au même temps final.

Le problème que nous considérons est\ :

$$
  \partial_t u + a\partial_x u = 0
$$

Pour simplifier le problème nous prendrons $a=1$, sans pour autant perdre en généralité dans le calcul de l'ordre. L'équation est considérée valide sur l'ensemble $x\in[0,2\pi]$, avec des conditions aux bords périodiques ; et nous allons considérer un cosinus comme condition de départ\ :

$$
  u_i^0 = cos(x_i)
$$

avec $x_i = i\Delta x$ et le pas d'espace $\Delta x = \frac{2\pi}{N}$, où $N$ est le nombre de points du maillage. La solution exacte au temps $t^n$ est\ :

$$
  u_i^n = cos(x_i - t^n)
$$

##### Calcul à pas de temps fixe

Pour être certain de ne pas prendre en compte l'erreur en temps dans le calcul de l'erreur, il est possible de résoudre le problème sur un seul pas de temps toujours identique. Ainsi le seul paramètre modifié d'une simulation à l'autre est le raffinage du maillage et on observera que l'erreur en espace.

Un seul pas de temps suffit pour l'obtention de l'ordre :

$$
  u_i^1 = u_i^0 - \frac{\Delta t}{\Delta x}( u^0_{i+\frac{1}{2}} - u^0_{i-\frac{1}{2}}) = \cos(x_i - \Delta t) + \mathcal{O}(\Delta x^m)
$$

où $m$ est l'ordre recherché. L'erreur se calcule par la norme de la différence de la solution approchée avec la solution exacte :

$$
  e_1 = \| U^1 - \cos(X_i - \Delta t) \|_1 = \sum_i |u_i^1 - \cos(x_i - \Delta t) |\Delta x = \mathcal{O}(\Delta x^m)
$$

$$
  e_{\infty} = \| U^1 - \cos(X_i - \Delta t) \|_{\infty} =  \sup_i |u_i^1 - \cos(x_i - \Delta t) |
$$

On en déduit que $e_1 = C\Delta x^m$m donc en traçant l'erreur sur une échelle logarithmique on trouve :

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

Il est intéressant de faire une simulation sur plusieurs pas de temps pour amplifier la visibilité de l'ordre du schéma ; l’inconvénient est que l'erreur du schéma temporel, potentiellement plus élevée, empêche d'observer l'erreur dû au schéma spatial sans choisir un pas de temps arbitrairement très faible. Pour remédier en partie à ce problème nous allons travailler sur un nombre de CFL constant, c'est-à-dire\ :

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

#### Obtention de l'ordre

#### Test de viscosité

> Cas où l'on fait tourner 12 fois un pacman : [@qiu2011]

> Cas où l'on fait tourner une gaussienne, comparer entre Euler et RK3 (apparition d'une *vague de traine* dans le cas Euler)

## Couplage du l'équation de transport et du terme de raideur

Dans cette section, on applique les schémas précédent au modèle *micro-macro*, ce qui va amener à des études supplémentaires comme le calcul de la condition de CFL, ou la reformulation en exponentielle du modèle.


### Calcul de la condition CFL

Le terme raide, apporté par l'opérateur de collision BGK va induire une modification de la condition CFL habituelle lors du couplage du schéma d'Euler implicite avec un schéma en espace.

Pour calculer le nombre de CFL nous allons dans un premier temps nous intéresser au modèle cinétique [!eq:cine], la description microscopique du modèle *micro-macro* est similaire et implique la même condition. Nous utiliserons le schéma d'Euler implicite pour la discrétisation en temps, et pour simplifier les notations nous n'utiliserons qu'un schéma *upwind* en espace, encore une fois le champ électrique est négligé dans cette partie.

$$
  \frac{f_{i,k}^{n+1}-f_{i,k}^n}{\Delta t} + v\frac{f_{i+\frac{1}{2},k}^n - f_{i-\frac{1}{2},k}^n}{\Delta x} = \frac{1}{\varepsilon}((\mathcal{M}_{[f^{n+1}]})_{i,k} - f_{i,k}^{n+1})
$$

Ce qui peut se réécrire, pour une interprétation itérative\ :

$$
  f_{i,k}^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ f_{i,k}^n - v_k\frac{\Delta t}{\Delta x}(f_{i+\frac{1}{2},k}^n - f_{i-\frac{1}{2},k}^n) + \frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k} \right]
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

### Reformulation exponentielle du modèle *micro*

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



## Résolution du problème de Poisson

Pour résoudre le problème de Poisson en condition aux bords périodiques nous utiliserons une méthode de transformée de Fourrier. Le champ électrique est une fonction de la densité $\rho(t^n)$, il est donc nécessaire de résoudre le problème de Poisson à chaque pas de temps.

Notons $\rho^\prime = \rho -1$, il suffit de calculer la transformée de Fourrier de $\rho\prime$ pour résoudre le problème [!eq::poisson] dans le contexte spectral\ :

$$
  i\kappa \hat{E}_{\kappa} = \hat{\rho}^\prime_{\kappa}
$$

où $\kappa$ est l'indice du coefficient de Fourrier et $i$ le nombre complexe tel que $i^2 = -1$. Ainsi on définit pour tout $\kappa$ le coefficient de Fourrier\ :

* $\hat{E}_{\kappa} = -i\displaystyle\frac{\hat{\rho}^\prime_{\kappa}}{\kappa}$ si $\kappa \neq 0$
* $\hat{E}_0 = 0$ car $E_f$ est à moyenne nulle d'après la condition [!eq:poisson:vp]

Ainsi tous les coefficients de Fourrier de $E_f$ sont calculés, il suffit d'effectuer la transformée inverse pour trouver le résultat souhaité.




# Application aux modèles cinétiques et *micro-macro*

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
  $${#eq:eq:max:numcal}

6. On approxime $f^{n+1}_{i,k}$ via le schéma avec le terme de transport et de diffusion :
  
  $$
    f^{n+1}_{i,k} = \frac{1}{1+\frac{\Delta t}{\varepsilon}} \left[ f^n_{i,k} - \frac{\Delta t}{\Delta x}v_k (f^n_{i+\frac{1}{2},k} - f^n_{i-\frac{1}{2},k}) +\frac{\Delta t}{\varepsilon}(\mathcal{M}_{[f^{n+1}]})_{i,k}  \right]
  $$

7. On corrige l’approximation $U_i^{n+1}$ via le calcul du moment de $f^{n+1}_{i,\cdot}$ :

  $$
    U_i^{n+1} \gets \sum_k m(v_k)f_{i,k}^{n+1} \Delta v
  $$


### Propriété sur la température

Le calcul de la maxwellienne $|\mathcal{M}_{[f^{n}]}$ dans [!eq:max:numcal] nécessite l'extraction de la racine carré de la température $(T_i)_i$ à tout temps $t^n$, or celle-ci est uniquement définit par\ :

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

Nous allons étudier ce que donnent les propriétés de conservations énnoncées dans l'équation [!eq:cine:conservation] dans le domaine discret\ :

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

### Cas tests

#### Conditions aux bords périodiques

#### Conditions aux bords de Neumann

> Tube à choc de Sob

## Micro-macro

> Algorithme,tests numériques (périodique et Neumann), comparaison avec Euler et cinétique, évocation du temps de calcul (repris dans le récap)

### Écriture de la partie *macro*

La partie *macro* du modèle est une modification du modèle d’Euler classique. Le code de simulation des équations d'Euler qui servait pour les précédents tests, utilise un flux de Lax-Friedrichs avec un limiteur de pente de van Leer symétrique.

Nous obtenons alors le schéma suivant\ :

$$
  U_i^{n+1} = U_i^n - \frac{\Delta t}{\Delta x}(\mathcal{F}_{i+\frac{1}{2}}^n - \mathcal{F}_{i-\frac{1}{2}}^n) - \frac{\Delta t}{2\Delta x}(G_{i+1}^n - G_{i-1}^n)
$$

Avec le flux numérique $\mathcal{F}_{i+\frac{1}{2}}^n$ donné par\ :

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

Le flux $G_{i}^n$ fait le lien avec la partie micro et sera détaillé plus tard.


### Écriture de la partie *micro*

La partie micro ne correspond plus simplement au modèle cinétique précédemment étudié, l’impact du projecteur $\Pi$ ([!eq:defPi]) fait intervenir un nouveau terme.

$$
  g^{n+1} = \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[ g^n - \Delta t (I-\Pi)(v \partial_x g^n) - \Delta t (I-\Pi)(v\partial_x \mathcal{M}_{[U^{n+1}]}) \right]
$$


### Algorithme général

On souhaite résoudre le modèle *micro-macro* suivant ([!eq:mima])\ :

$$
  \begin{cases}
    \partial_t U + \partial_x \mathcal{F}(U) + \partial_x \langle vm(v)g \rangle = 0 \\
    \partial_t g + v\partial_x g = -\frac{1}{\varepsilon}g - (I-\Pi)(v\partial_x \mathcal{M}_{[f]}) + \Pi(v\partial_x g)
  \end{cases}
$$

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
    g_{i,k}^{n+1} \gets \frac{1}{1+\frac{\Delta t}{\varepsilon}}\left[\vphantom{\frac{\Delta}{\Delta}} g_{i,k}^n \right. & - (I-\Pi)\left(\frac{\Delta t}{\Delta x}v_k(g_{i+\frac{1}{2},k}^n - g_{i-\frac{1}{2},k}^n)\right) \\
    & \left. - (I-\Pi)\left( \frac{\Delta t}{\Delta x}v_k( (\mathcal{M}_{[U^{n+1}]})_{i+\frac{1}{2},k} - (\mathcal{M}_{[U^{n+1}]})_{i-\frac{1}{2},k})\right) \vphantom{\frac{\Delta}{\Delta}} \right]
  \end{aligned}
  $$

  Ceci peut se résumer à deux termes de transports projetés selon $(I-\Pi)$. La discrétisation en temps présenté ici utilise une méthode d'Euler implicite ; numériquement nous n'avons pas observé d'instabilité dans le cadre d'un gaz raréfié. La mécanique des plasmas étudie traditionnellement des comportement en temps long, dans ce cas une discrétisation d'ordre plus élevé en temps fut nécessaire pour accompagner l'ordre élevé en espace. 


### Cas tests

#### Conditions aux bords périodiques

#### Conditions aux bords de Neumann

#### Milieu non homogène : $\varepsilon = \varepsilon(x)$

> Cas test dans [@filbet], comparatif au code cinétique.


## Approximation $h(t,x)$

> Différents tests avec $h(x)$ (fonction porte, et trapézoïdale), puis obtention de $h(t,x)$ avec $x_s$ et $x_e$.

> Dans [@dimarco] la fonction $h(t,x)$ est calculée à partir de $\langle m(v_k)g_{i,k}^n\rangle_v$ donc obligé de calculer en tout point à tout instant. Dans [@filbet] il y a aussi un principe multi-échelle mais le critère est calculé sur chaque cellule à chaque instant, donc pas de gain non plus. Utiliser $x_s$ et $x_e$ demande une préparation en amont (avoir une idée de ce que cela va devenir) mais permet de réduire le temps de calcul.

## Comparaison

> Temps de calcul des différents modèles, et erreur par rapport au code de référence : Euler, et avantage qualitatif des différents modèles (plasma avec $\varepsilon \not\to 0$ et champ électrique : impossible avec simple approximation Euler)


# Application pour les plasma

> C'est dans cette partie qu'on a vraiment besoin des tests 2D et qu'on introduit dans un champ électrique

## Modèle cinétique

> Programme de référence, présentation un peu plus rapide avec l'ajout du terme de champ électrique. Préciser la nécessité numériquement d'introduire RK3 pour l'ordre élevé en espace, avec recalcule de l'équation de Poisson sur chaque étape du RK3.

### Cas proche de l'équilibre

> Landau

### Cas éloigné de l'équilibre

> Double faisceau


## Modèle *micro-macro*

> Modèle hybride basé sur le modèle cinétique, donc comparatif aux résultats précédents, précision de l'ajout dans la partie *micro* et *macro* du champ électrique. Pour le moment RK3 ne fonctionne pas (*a priori* la Maxwellienne ne reste pas constante sur chaque étape de RK3 donc obligé de recalculer $u$, et $T$, pas uniquement $\rho$, et même ainsi j'ai encore des instabilités).

> Introduction de $h(t,x)$


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

