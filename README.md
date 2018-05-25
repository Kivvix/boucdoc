# boucdoc

*Boucdoc* est à la fois un ensemble de filtres pour *Pandoc* ainsi qu'un cadre pour écrire facilement des documents *Markdown* et les convertir dans un autre format (essentiellement HTML, mais un support améliorer de LaTeX est prévu, entre autre pour la rédaction d'un rapport de stage).

## Les filtres

Différents filtres ont été développés, et ils sont prévu pour

----

Ce projet est juste un utilitaire supplémentaire pour `pandoc` similaire à ce que peut proposer *Sphinx* (utilitaire de documentation pour le projet Python). Il s'agit de convertir des fichiers *Markdown* (car simple à rédiger) en des fichiers HTML (car simple d'échanger, à l'aide en plus d'un petit serveur statique, non sécurisé), ou en PDF (avec LaTeX) pour un export plus traditionnel (il est recommandé de retravailler le fichier LaTeX de sortie, en particulier en cas de gros fichiers, il est sans doute nécessaire de revoir la structure).

En plus de cela le projet propose un filtre pour convertir des blocs de code GraphViz en diagramme (`.png` par défaut, `.pdf` par défaut en LaTeX).

## `panviz`

Ce filtre permet de convetir un bloc de code de classe `dot` en diagramme au moment de la compilation. Il est possible de préciser un `renderer` (`dot` par défaut, mais je trouve que `neato` donne de meilleurs résultats dans la majorité des cas), ainsi qu'un `format` privilégié de sortie.

Puisque l'extension `implicit_figures` est activé, le rendu sera une figure (balise `<figure>` en HTML, ou l'environnement `figure` en LaTeX), le titre de la figure (*figcaption*) sera la première ligne de code.

> TODO: changer la façon d'obtenir le titre, peut-être avec un attribut dans la liste d'attributs. À voir...

Exemple :

```
	```{ .dot renderer=neato format=gif }
	# titre de la figure

	digraph network_ring {
		node [shape = circle];
		n0 -> n1
		n1 -> n2
		n2 -> n3
		n3 -> n4
		n4 -> n0
	}
	```
```

Seul la classe `.dot` est obligatoire pour faire appel à ce filtre.

## HTML

L'export en HTML est celui qui est pour le moment le plus travaillé. Le CSS est basé sur [Skeleton](http://getskeleton.com/) légèrement customisé. Un script JavaScript ajoute automatiquement des liens sur chaque titre et bloc de code pour pouvoir faire référence à une partie particulière de la page (un peu comme la documentation de Python).

> Entre l'inspiration de Sphinx pour la structure du projet (et l'idée) et les liens vers les titres inspirés de la documentation de Python (donc de Sphinx) on peut se demander pourquoi je n'utilise pas tout simplement Sphinx. Je trouve l'utilisation de Sphinx parfois trop lourde pour de simple petites pages, je n'ai pas compris (ni cherché à comprendre) comment personnaliser le rendu, et Sphinx gère mal les types template en C++ (ok pour le moment il n'y a pas de gestion de documentation de C++ mais j'y pense). Puis j'avais envie de faire un peu de Python (j'en ai assez de coder en Fortran pour les cours), découvrir JavaScript (`anchor.js` est mon premier script JS !). Et qui êtes-vous pour me poser ce genre de question, je fais ce que je veux après tout, et si ça vous plaît pas il existe Doxygen, Sphinx, ou utilisez directement Pandoc !




