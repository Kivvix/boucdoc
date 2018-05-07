---
title: Idées
author : josselin
...


# TVD

*Total variation diminishing*  est un ensemble de schémas numériques où l'on vise à diminuer la variations totale de la solution. Il est souvent intéressant de mesurer la variation total $TV$ :

$$
  TV = \int \left|\frac{\partial u}{\partial x}\right|\,\mathrm{d}x
$$

Ce qui peut s'écrire de manière discète par :

$$
  TV = \sum_i | u_{i+1} - u{i} |
$$

Une méthode numérique est dite *TVD* si :

$$
  TV(u^{n+1}) \leq TV(u^n)
$$

## Variation totale de l'intégrale

Or dans notre cas il n'est pas si simple de définir $\sum_i | u_{i+1} - u_{i} |$, nous allons donc définir 2 variations totales, une sur $x$ et une sur $v$. Ces variations sont des variations dans une direction de l'intégrale dans l'autre direction. Une première variation totale intégrale en $x$ :

$$
  TV_x = \sum_i \left| \sum_k f_{i+1,k} - \sum_k f_{i,k}  \right|
$$

Et une seconde variation totale de l'intégrale en $v$

$$
  TV_v = \sum_k \left| \sum_i f_{i,k+1} - \sum_i f_{i,k} \right|
$$

On s'assure de la différence entre $TV_x$ et $TV_v$ par leur écriture dans le cas continue :

$$
  TV_x \equiv \int_{\Omega} \left| \partial_x \int_{\mathbb{R}^d} f\,\mathrm{d}v \right|\,\mathrm{d}x
$$

et

$$
  TV_v \equiv \int_{\mathbb{R}^d} \left| \partial_v \int_{\Omega} f\,\mathrm{d}x  \right|\,\mathrm{d}v
$$

On peut donc tracer l'évolution de $TV_x$ et $TV_v$ au cours de la simulation.

![Évolution de $TV_x$ et $TV_v$ au cours du temps de simulation](template/tvdi.png)

|                    |                                                                                |
|:------------------:|:------------------------------------------------------------------------------:|
| $f(x,v)$           | $f(x,v) = \frac{1}{\sqrt{2\pi}}\exp(-\frac{v}{2})(1+\alpha \cos(\frac{x}{2}))$ |
| $T_{\mathrm{max}}$ | 0.67                                                                           |
| `nbx`              | 200                                                                            |
| `nbv`              | 32                                                                             |
| $\varepsilon$      | 0.0001                                                                         |

  : Paramètres de simulation

L'interprétation que j'en fais est seulement que la variation totale diminue, donc le schéma a donc une légère diffusion. Sans faire de tests avec d'autres $\Delta x$ et $\Delta v$ il est dure de se prononcer quand à la tendance générale de ce phénomène.

> ~~Le calcul effectué dans le code des grandeurs $TV_x$ et $TV_v$ est discutable dans le sens où il ne prend pas en compte la périodicité du domaine $\Omega$, donc la boucle sur `i` omet la différence entre les extrémités du domaine qui sont pourtant voisine.~~ Code corrigé et aucun changement de l'allure de la courbe.

## Variation totale

Il est aussi possible de définir des variations totaltes différemment :

$$
  TV_x = \sum_k \sum_i |f_{i+1,k} - f_{i,k}| \equiv \int_{\mathbb{R}^d}\int_{\Omega}|\partial_x f|\,\mathrm{d}x\mathrm{d}v
$$

Et de même pour la vitesse :

$$
  TV_v = \sum_i \sum_k |f_{i,k+1} - f_{i,k}| \equiv \int_{\Omega}\int_{\mathbb{R}^d}|\partial_v f|\,\mathrm{d}v\mathrm{d}x
$$

Pour ces grandeurs on obtient alors :

![Évolution de $TV_x$ et $TV_v$ au cours du temps de simulation](template/tvd.png)


# Méthode d'intégration

À plusieurs reprise, pour des calculs de flux ou de moments nous effectuons le calcul de l'intégrale :

$$
  \int_{\mathbb{R}} m(v)f(x,v)\,\mathrm{d}v
$$

Ce que nous approximons par la méthode des rectangles par :

$$
  \sum_k m(v_k)f(x,v_k)\,\Delta v
$$

Or il est connu que la méthode des rectangles n'est pas nécessairement la meilleure méthode d'intégration. Nous n'allons pas nous attarder ici pour présenter les différentes méthodes d'intégration, si cela est pleinement validé nous le détaillerons dans le rapport de stage (je dis nous... c'est surtout je).

* Méthode des ractangles : simple à mettre en place, rapide, méthode d'ordre 0.
* Méthode des trapèzes : légèrement plus compliqué, assez rapide, méthode d'ordre 1.
* Méthode de Simpson : un peu plus compliqué, un peu plus lente (pas mesuré mais le nombre d'opérations est plus élevé), nécessite un sous maillage dans sa définition classique, méthode d'ordre 2, possiblement d'ordre 4 car on considère des fonctions $\mathcal{C}^{\infty}$.

Le problème de la méthode de Simpson est des méthodes d'ordre plus élevé, est la nécessité du sous maillage, or il n'est pas possible d'effectuer une évaluation de la fonction sur les mailles intermédiaires, nous comparerons donc ces 3 méthodes avec le même maillage. Pour la méthode de Simpson nous utiliserons des mailles 2 fois plus grandes pour utiliser le point milieu, mais nous avancerons par demi-maille pour profiter pleinement du maillage complet.

Finalement sur différents tests, la méthode de Simpson sans véritable point milieu n'est pas perforante, et la méthode des trapèzes permet une meilleure approximation, mais le gain n'est pas significatif.

> Ok pour la méthode des trapèzes si le temps le permet. Éventuellement comparer les temps d'exécutions car le nombre d'intégrations est assez important. D'où avec l'approximation des trapèzes on calcule l'intégrale comme suit :
> $$
    \int_{\mathbb{R}}m(v)f(x,v)\,\mathrm{d}v \equiv \sum_k \frac{m(v_{k+1})f(x,v_{k+1}) + m(v_k)f(x,v_k)}{2}\Delta v
  $$

