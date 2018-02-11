---
title: Notes de cours de parallélisation
author: Josselin Massot (<josselin.massot@etu.univ-nantes.fr>)
...

> Tout ce cours utilise les commandes Linux, voici un petit [aide-mémoire](http://www.epons.org/commandes-base-linux.php). Toutes les commandes seront rappelé en temps voulu.

# Première connexion au CCIPL

Le travail au CCIPL s'effectue uniquement via *SSH* et donc un terminal. Pour cela il faut d'abord rentrer la commande suivante :

```{.term .sh}
ssh -X login@jaws.ccipl.univ-nantes.fr
```

L'option `-X` permet de lancer des applications graphiques à travers la connexion *SSH* (à part pour l'utilisation d'*emacs* cela me semble assez peu utile dans le cadre de nos TP).

Le mot `login` est a remplacer par le *login* `form_NN` où `NN` est le numéro dans l'ordre alphabétique.

Si la connexion réussi, l'invite de commandes demande un mot de passe (celui-ci du bout de papier), et normalement on est connecté sur la machine distante. La première chose que nous allons faire est de modifier ce mot de passe (il a été généré automatiquement, il est difficle à retenir et finalement pas si fiable, en plus il est écrit sur un bout de papier donc en cas de perte ou vol de ce papier la sécurité est réduite à néant), pour cela on va taper la commande :

```{.term .sh}
passwd
```

L'invite de commandes demande une nouvelle fois le mot de passe (c'est la dernière fois que l'on tape le mot de passe du bout de papier), puis on indique le nouveau mot de passe (plus facile à retenir), deux fois pour être sûr qu'on s'est pas planté en tapant n'importe quoi.

## Transférer de fichiers

Il est possible d'envoyer des fichiers via *SSH*, cela se fait à l'aide de la commande `scp` qui est similaire à la commande `cp` mais permet d'avoir la destination ou la source sur une autre machine (connectée en *SSH*).

Puisqu'il est difficile de connaître l'adresse exacte d'une machine de l'université, ces commandes sont à effectuer en local (*i.e.* dans un autre terminal que celui avec la connection *SSH*).

**Pour envoyer un fichier au CCIPL :**

```{.term .sh}
scp mon_fichier.f90 login@jaws.ccipl.univ-nantes.fr:
```

Il est possible d'indiquer avec les `:` un dossier particulier, par défaut celui-ci apparaîtra dans le *home* de l'utilisateur.

**Pour récupérer un fichier du CCIPL :**

```{.term .sh}
scp login@jaws.ccipl.univ-nantes.fr:mon_fichier.f90 dossier/tp/mon_fic.f90
```

Les deux commandes fonctionnent de la même manière, `scp source destination` ce qui change par rapport à la commande `cp` c'est que la destination ou la source peuve être distant, et il y a donc une syntaxe particulière à respecter.


## Se construire un environnement de travail

Dans ces TP il faudra coder, donc il faut un éditeur de texte, soit on se met ou on est déjà à l'aise avec *vim* ou *emacs* soit on préfère utiliser un éditeur un peu plus graphique comme *Geany* ou *Plum*. Pour ces derniers il faudra transférer son code, et à chaque bug renvoyer le code, cela est vite fastudieux (donc plein de `scp` d'affilé, avec à chaque fois saisie du mot de passe).

Il est donc posser de monter un dossier distant via *SSH*, à la manière de *Dropbox*, et donc naviguer à travers ses fichiers avec son explorateur de fichiers, utiliser les outils graphiques disponibles en local, etc.

Toutes les commandes suivantes sont à effectuer en local. Tout d'abord il faut créer un dossier qui servira de *point de montage* :

```{.term .sh}
mkdir jaws
```

Ce dossier doit rester vide, il se remplira automatiquement, et... ça sera magique tout fonctionnera comme il faut ^^. Maintenant on va monter un dossier distant dans ce dossier `jaws` grâce à la commande `sshfs` (pour *SSH file system* donc l'arboresence de fichiers par *SSH*).

```{.term .sh}
sshfs login@jaws.ccipl.univ-nantes.fr: jaws/
```

L'invite de commandes demande le mot de passe, puis on vérifie que tout à bien fonctionné :

```{.term .sh}
cd jaws && ls
```

Et là on doit voir tous nos fichiers présents au CCIPL. Toutes créations de fichiers, modifications sera automatiquement synchronisées avec le CCIPL. Il est donc possible d'utiliser *Geany* ou autre chose sans faire de `scp` toutes les 30 secondes.

> **Attention :** le CCIPL propose des outils de compilations qui ne sont pas disponibles en local, par conséquent il est toujours nécesaire d'avoir un terminal avec une connexion *SSH* classique pour compiler et exécuter nos programmes.


## Utilisation des modules

Pour permettre l'utilisation de plusieurs compilateurs, le CCIPL fonctionne par modules qu'il faut *loader* (flemme d'utiliser le terme français charger). Il est possible de lister les modules :

```{.term .sh}
module avail
```

Ce qui donne une liste beaucoup trop longue. Il est aussi possible d'utiliser la méthode un peu plus bourrine :

```{.term .sh}
module load
```

Et avant d'appuyer sur entrer *spamer* la touche `Tab` pour avoir la liste des modules apparaître (demande d'appuyer sur `y` pour s'assurer que l'on veut voir la liste des plus de 200 modules, puis appuyer sur `espace` pour avancer dans la liste, et appuyer sur `q` pour la quitter prématurément). Puis on peut copier-coller le nom de module et compléter la commande :

```{.term .sh}
module load openmpi/psm2/2.0.1
```

> **Astuce :** pour copier-coller sous Linux il est possible juste avec la souris de sélectionner le texte avec la souris puis de cliquer avec la molette à l'emplacement où l'on veut coller, ceci permet de faire simplement des copier-coller vers ou depuis la console (en temps normal le raccourcis est `ctrl`+`shift`+`c`/`v` ou lieu d'un simple `ctrl`+`c`/`v`).

Maintenant on va lister les modules utiles (pour le moment) en TP :

* `openmpi/psm2/2.0.1` pour les TP de *MPI* et charger le compilateur `mpif90` et l'exécuteur `mpirun`.
* `gcc/7.3.0` pour les TP d'OpenMP pour charger un bon compilateur.
* `intel/2018.1.163` pour charger le compilateur `ifort` (surtout en cours d'OpenMP).

# TP d'*MPI*

## Utiliser *MPI*

Tout d'abord il est nécessaire de charger le module pour *MPI*.

```{.term .sh}
module load openmpi/psm2/2.0.1
```

Pour compiler un code *MPI* il faudra utiliser le compilateur `mpif90` (pour du Fortran90) :

```{.term .sh}
mpif90 tp1.f90 -o tp1
```

> **Nota bene :** Si le code est en C le compilateur sera `mpicc`, si il s'agit de C++ le compilateur sera `mpicxx` ou `mpic++`, la commande reste similaire.

L'argument `-o` permet d'indiquer le fichier de sortie (*output*) donc le nom de l'exécutable, celui-ci est facultatif, par défaut le nom de l'exécutable sera `a.out` (ce qui est un beau nom), et sera écrasé à chaque nouvelle compilation (même d'un autre programme).

Pour exécuter un programme il faut exécuter son programme dans un environnement particulier pour utiliser plusieurs processeurs, ceci est géré par `mpirun` auquel on précise le nombre de processus que l'on voudra utiliser avec l'argument `-np` :

```{.term .sh}
mpirun -np 7 ./tp1
```

## Premier code *MPI*

Maintenant un premier exemple de code. La partie de code parallélisé est entre les instructions `call MPI_INIT(code)` et `call MPI_FINALIZE(code)` :

```{ .f90 .lineAnchors .numberLines #tp1 }
program tp1
implicit none
include "mpif.h" ! insertion de la librairie mpi pour fortran

integer :: nb_proc , rang , code
integer :: i,s

call MPI_INIT(code)
call MPI_COMM_SIZE(MPI_COMM_WORLD,nb_proc,code)
call MPI_COMM_RANK(MPI_COMM_WORLD,rang,code)

print *, 'je suis processus ',rang,' sur ',nb_proc

call MPI_FINALIZE(code)

end program tp1

```

Après compilation on l'exécute, on test au début avec seulement 7 processeurs :

```{.term .sh}
mpirun -np 7 ./tp1
```

Les exécutions de chaque *kernel* (partie parallélisée) se font simultanément et potentiellement les retours ne se font pas dans l'ordre, donc testons avec 70 processeurs (ne pas faire ça avec un gros code, ici le code est très rapide donc pas de problème, ce test sera purement pédagogique, ne pas répéter ceci avec d'autres codes sans savoir ce qu'on fait).

```{.term .sh}
mpirun -np 70 ./tp1
```

Ici on remarque plus facilement que l'ordre n'est pas toujours le bon, ni le même.

### Que fait ce code ?

Nous allons présenter ici les différentes procédures d'*MPI* ; toutes les procédures d'*MPI* commencent par `MPI_` en Fortran.

#### `MPI_COMM_SIZE`

Cette procédure donne le nombre de processeurs utilisés par le programme (pour être plus précis par le communicateur `MPI_COMM_WORLD` qui est le communicateur par défaut et le seul que l'on utilisera dans tous les TP, il est possible d'avoir plusieurs communicateurs qui peuvent potentiellement communiquer entre eux).

> Un communicateur est un ensemble de processeurs, dans nos TP on en utilisera toujours qu'un seul et ce sera `MPI_COMM_WORLD`.

Les arguments :

* `MPI_COMM_WORLD` : le communicateur dont on veut connaître le nombre de processeurs.
* `nb_proc` : variable de sortie indiquant le nombre de processeurs dans le communicateur.
* `code` : variable de sortie qui contient un potentiel code d'erreur, on ne teste jamais si ça ne marche pas mais en théorie il faudrait.

#### `MPI_COMM_RANK`

Cette procédure donne le numéro du processus courant (le numéro du processeur sur lequel le code actuel tourne). Attention la numérotation commence à 0.

Les arguments :

* `MPI_COMM_WORLD` : le communicateur dans lequel on travaille.
* `rang` : variable de sortie qui contiendra le numéro du processus.
* `code` : comme précédemment, c'est là juste parce qu'il faut le mettre.

## L'envoie de message entre processus

Un processus a souvent besoin d'un résultat envoyé par un autre, il est donc possible d'envoyer des résultats entre processus, pour cela on va utiliser les procédures `MPI_SEND`  pour envoyer et `MPI_RECV` pour recevoir un message, voici un exemple de code qui le fait :

```{ .f90 .lineAnchors .numberLines #a2 }
program a2
implicit none
include "mpif.h"

integer, dimension(MPI_STATUS_SIZE) :: statut
integer, parameter :: tag=100
integer :: rang , valeur , code
integer :: nb_proc

call MPI_INIT(code)

call MPI_COMM_SIZE(MPI_COMM_WORLD,nb_proc,code)
call MPI_COMM_RANK(MPI_COMM_WORLD,rang,code)
nb_proc = nb_proc -1
if ( rang == 2 ) then ! s'il s'agit du processus 2
        valeur = 1000
	! envoie de la valeur au processus `nb_proc`
        call MPI_SEND(valeur,1,MPI_INTEGER,nb_proc,tag,MPI_COMM_WORLD,code)
elseif ( rang == nb_proc ) then ! s'il s'agit du dernier processus
	! attente de la réception d'un message provenant du processus 2
        call MPI_RECV(valeur,1,MPI_INTEGER,2,tag,MPI_COMM_WORLD,statut,code)
        print *, "proc ",rang," j'ai reçu ",valeur,"du proc 2"
end if

call MPI_FINALIZE(code) 

end program a2
```

### Que fait ce code ?

Le processus 2 envoie un message au dernier processus.

#### `MPI_SEND`

Cette procédure envoie un message à un autre processus (processeur).

Les arguments :

* `valeur` : référence vers le début des données, en bref le nom de la variable que l'on souhaite envoyer.
* `1` : taille des données (ici un simple scalaire, sinon la taille du tableau).
* `MPI_INTEGER` : le type des données, l'envoie de données structurée est plus complexe, ici on ne fera qu'avec les types de bases, donc `MPI_INTEGER` ou `MPI_REAL`.
* `np_proc` : numéro du processeur destinataire du message, ici le dernier processeur. Rappel, la numérotation des processeurs se fait à partir de 0 ; de plus la numérotation des processeurs est locale au communicateur, c'est pour cela que celui-ci est toujours précisé.
* `tag` : une étiquette pour préciser un type de message (par exemple on pourrait envoyer un message d'erreur ou envoyer un message des données).
* `MPI-COMM-WORLD` : nom du communicateur sur lequel on envoie le message.
* `code` : comme précédemment, test en cas d'erreur.

#### `MPI_RECV`

Cette procédure indique que le processus attend la réception d'un message d'un autre processus.

Les arguments :

* `valeur` : variable dans laquelle on va stocker les données envoyées.
* `1` : taille de ces données.
* `MPI_INTEGER` : type de ces données.
* `2` : numéro du processus envoyeur, le processus courant est donc en attente d'un message provenant uniquement du processus 2, la réception d'un autre message sera ignoré.
* `tag` : comme précédemment.
* `MPI_COMM_WORLD` : comme précédemment.
* `statut` : informations supplémentaire sur l'état du message, il est possible de mettre le processus en attente d'un message de n'importe quel `tag` et de n'importe quel processus, dans ce cas là il peut être intéressant de savoir de qui provient le message pour savoir comment le traiter (quelle ligne de la matrice a été calculée par exemple).
* `code` : comme précédemment.


## Exercice 1

Écrire un code qui calcul la somme :

$$
	\sum_{i=0}^n e^{\frac{i}{n}}
$$

Pour cela l'intervalle $[0,n]$ sera divisé en 2 parties égales, chaque partie étant calculé sur un processus différent. On pourra mettre fin prématurément au calcul si le nombre de processeurs n'est pas 2.

### Solution

```{ .f90 .lineAnchors .numberLines #a3 }
program a3
implicit none
include "mpif.h"

integer :: nb_proc , rang , code
integer , dimension(MPI_STATUS_SIZE) :: statut
integer , parameter :: n=1000

intger :: i , n1 , n2
real :: s1,s2

call MPI_INIT(code)
call MPI_COMM_SIZE(MPI_COMM_WORLD,nb_proc,code)
if ( nb_proc /= 2 ) call MPI_ABORT(MPI_COMM_WORLD,1,code) ! on met fin au programme si le nombre de processeurs n'est pas 2

call MPI_COMM_RANK(MPI_COMM_WORLD,rang,code)

! initialisation des variables
! partie commune à tous les processus, ici s1 où on stocke la somme partielle
s1 = 0.0
! partie propre à chaque processus, les bornes de la somme
if ( rang == 0 ) then
	n1 = 1
	n2 = n/2
else
	n1 = n/2 +1
	n2 = n
end if

do i=n1,n2
	s1 = s1 + exp(real(i)/n)
end do

if ( rang == 1 ) then
	! le processus 1 envoie son résultat au processus 0
	call MPI_SEND(s1,1,MPI_REAL,0,42,MPI_COMM_WORLD,code)
else
	! réception du message dans le processus 0 dans la variable s2, puis calcul de la somme totale
	call MPI_RECV(s2,1,MPI_REAL,1,42,MPI_COMM_WORLD,statut,code)
	s1 = s1+s2
	print *, "result : ",s1
end if

call MPI_FINALIZE(code)

end program a3
```

> L'algorithme exécuté par chaque processus est identique, ce qui diffère sont les bornes, pour cela on spécifie pour chaque processus ses bornes (ses variables internes, privées), tout ce qui est écrit en dehors d'un `if` sur le rang du processus est commun à tous les processus, et sera exécuté par chacun d'entre eux.

Et on peut tester que le programme quitte bien prématurément selon le nombre de processus :

```{.term .sh}
mpirun -np 3 ./a3
```

```{.term .sh}
mpirun -np 2 ./a3
```


## Exercice 2

Le problème de ce premier exercice est que l'on n'utilise que 2 processeurs, maintenant effectuons la même chose avec $n$ processus. Il est donc nécessaire de calculer de bornes pour chaque processus dépendant du nombre total de processus, donnée décidé par l'utilisateur au moment de l'exécution.

De plus, on utilisera des nombres à virgule flottante à double précision ; pour cela il ne faut pas envoyé des données avec le type `MPI_REAL` qui sont des réel à simple précision, mais `MPI_DOUBLE_PRECISION` qui sont des réels à double précision.

Un problème est le calcul des bornes, la manière naïve de faire ce calcul est d'effectuer une division euclidienne classique et de traiter les données restantes par le dernier processus. L’inconvénient de cette méthode est le mauvais partage des données et donc du travail à effectuer, le dernier processus se retrouvera à devoir traiter le reste en plus de sa tâche de travail, il a donc plus de travail à gérer et les autres processus devront l'attendre.

Un façon simple de palier ce problème est d'effectuer une division entre réels et de convertir ce résultat en entier. Cela permet un meilleur partage que la division euclidienne entre entiers.

Le problème suivant sera la réception des données, il ne faut pas attendre la réception d'un processus d'un numéro particulier au risque de laisser attendre les autres processus. On utilisera donc comme expéditeur du message `MPI_ANY_SOURCE`.

```{ .f90 .lineAnchors .numberLines #a4 }
program a4
implicit none
include "mpif.h"

integer :: nb_proc , rang , code
integer ::,dimension(mpi_status_size) :: statut
integer,parameter :: n=1000

integer :: n1,n2 ! bornes de chaque processus
integer :: i
real :: s , tmp_s

call mpi_init(code)
call mpi_comm_size(MPI_COMM_WORLD,nb_proc,code)
call mpi_comm_rank(MPI_COMM_WORLD,rang,code)

s = 0.0 ! initialisation de la valeur de calcul
! bornes de calcul
n1 = nint((rang)*real(n)/nb_proc)
n1 = nint((rang+1)*real(n)/nb_proc)-1

if ( rang == nb_proc-1 ) n2 = n ! pour se prémunir d'erreurs d'approximation

!print *, "rang:",rang,"n1:",n1, "n2:",n2," diff:",n2-n1

! calcul
do i=n1,n2
	s = s + exp(real(i)/n)
end do

! les données sont envoyés au processus 0 (et donc reçu par lui)
if ( rang /= 0) then
	call mpi_send(s,1,MPI_DOUBLE_PRECISION, 0 ,42,MPI_COMM_WORLD,code)
else
	! proc:0 -> boucle de réception
	do i=1,nb_proc-1
		call mpi_recv(tmp_s,1,MPI_DOUBLE_PRECISION,MPI_ANY_SOURCE,42,MPI_COMM_WORLD,statut,code)
		!print *, "send from:",statut(1), " data:",tmp_s
		s = s + tmp_s
	end do
	print *, "result: ",s
end if

call mpi_finalize(code)

end program a4
```

> Le Fortran n'était pas sensible à la casse j'ai décidé d'écrire une partie en minuscule, mais ça ne change strictement rien.

Pour récupérer tous les résultats il est nécessaire d'avoir une boucle, et on attend pas nécessaire le message du processus $i$ à l'itération `i` de la boucle, en effet si un processus $j$ a déjà fini, il peut envoyé son message avant un processus $k$ avec $k < j$, ce message sera donc directement reçu. On peut aussi s'arranger pour que le processus 0 ait moins de travail que les autres pour être prêt à recevoir dès qu'un autre processus ait fini.


## La communauté de l'anneau

L'exemple précédent propose un réseau dit étoilé, le processus 0 s'occupe de tout recevoir et agglomérer les résultats. Si pour une raison ou une autre ce processus crash (à cause d'une erreur du système par exemple), les autres processus restent en attente et risquent de devenir ce qu'on appelle des processus zombies.

<div>

```{ .dot renderer=neato format=gif }
# Exemple de réseau étoilé
digraph network_star {
	node [shape = circle];
	n1 -> n0
	n2 -> n0
	n3 -> n0
	n4 -> n0
}
```

```{ .dot renderer=neato }
# Exemple de réseau en anneau 
digraph network_ring {
	size ="4,4";
	node [shape = circle];
	n0 -> n1
	n1 -> n2
	n2 -> n3
	n3 -> n4
	n4 -> n0
}
```

Exemple de topologies de réseaux
</div>

Créons donc notre premier réseau en anneau (qui prévient de certaines erreurs présentées précédemment). Chaque processus au lieu d'envoyer un message au processus 0 enverra un message au processus suivant et recevra un message du processus précédent. Il est nécessaire de définir le suivant et le précédent, cela s'effectue simplement en utilisant le rang du processus $\pm1$ modulo le nombre de processus.

```{ .f90 .lineAnchors .numberLines #a5 }
program a5
implicit none
include "mpif.h"

integer :: nb_proc , rang , code
integer ::,dimension(mpi_status_size) :: statut
integer :: proc_next , proc_prev
integer :: value

call mpi_init(code)
call mpi_comm_size(MPI_COMM_WORLD,nb_proc,code)
call mpi_comm_rank(MPI_COMM_WORLD,rang,code)

proc_next = mod(rang+1,nb_proc)
proc_prev = mod(rang-1,nb_proc)

if ( rang == 0 ) then
	! le processus 0 va initier le mouvement en envoyant et attendant un message
	value = rang
	call mpi_send(value,1,MPI_INTEGER,proc_next,42,MPI_COMM_WORLD,code)
	call mpi_recv(value,1,MPI_INTEGER,proc_prev,42,MPI_COMM_WORLD,statut,code)
else
	call mpi_recv(value,1,MPI_INTEGER,proc_prev,42,MPI_COMM_WORLD,statut,code)
	print *, "proc:",rang," get:",value," from:",statut(1)," sendto:",proc_next
	value = value + rang
	call mpi_send(value,1,MPI_INTEGER,proc_next,42,MPI_COMM_WORLD,code)
end if

call mpi_finalize(code)

end program a5
```



# TP d'*OpenMP*

## Utiliser *OpenMP*

*OpenMP* fonctionne uniquement avec des directives données au compilateur, ces directives sont considérées comme des commentaires si le compilateur ne gère pas *OpenMP* ou que l'option n'a pas été indiquée. Donc un simple compilateur moderne fera l'affaire : `gfortran` par exemple. Pour avoir la dernière version on va charger le module :

```{.term .sh}
module load gcc/7.3.0
```

Et pour compiler un code avec *OpenMP* il suffira de le compiler classiquement, en ajoutant l'option `-fopenmp` :

```{.term .sh}
gfortran -fopenmp tp1.f90 -o tp1
```

## Premier code *OpenMP*

Maintenant un premier exemple de code. La partie de code parallélisé est entre les directives `!$OMP parallel` et `!$OMP END parallel` (qui commençant par un `!` seront considéré comme des commentaires en temps normal) :

```{ .f90 .lineAnchors .numberLines #b1 }
program b1
!$ use OMP_LIB

implicit none

integer :: nthds , tid ! nombre de thread et l'id du thread

tid = 0 ; nthds = 1

! cree une équipe de threads
!$OMP parallel private(tid)
	!$ tid = omp_get_thread_num()
	write (6,*) 'Hello World thread ' , tid

	! seul le thread maitre effectue la suite
	if ( tid == 0 ) then
		!$ nthds = omp_get_num_threads()
		write (6,*) 'nombre de threads = ',nthds
	end if

! fin de la région parallele
!$OMP END parallel

end program b1
```

> On remarque que toutes les instruction d'*OpenMP* commence par `!$` et il s'agit de commentaire qui seront interprétés par le compilateur. Cela est beaucoup moins contraignant à écrire que de la parallélisation avec *MPI* et donc s'adapte beaucoup plus simplement à un code existant, la majorité des TP suivant consisteront à paralléliser un code déjà existant.

Le nombre de *threads* est limité via une variable globale (`OMP_NUM_THREADS`), il est donc possible de la modifier pour changer le nombre de *threads* qui s'exécuteront : 

```{.term .sh}
export OMP_NUM_THREADS=4
```

Limitera le nombre de *threads* à 4. Une limite à 4 ou 8 est très raisonnable et permet de ne pas surcharger le CCIPL avec nos âneries.

## Parallélisation d'une boucle

L'exemple suivant consiste à paralléliser une boucle, en effet ce que l'on souhaite c'est que simultanément plusieurs itérations d'une boucle se déroulent en parallèle.

```{#omp-last .f90 .lineAnchors .numberLines #b2 }
program b2
!$ use OMP_LIB
implicit none

integer , parameter :: n=1025
real,dimension(n,n) :: A,B
integer :: i,j

call random_number(A) ! rempli la matrice A de nombres pseudo-aléatoires

!début de la région parallèle conditionnelle
!$OMP parallel if(n>514) &
!$OMP default(none) &
!$OMP shared(A,B) private(i,j)
!$OMP do
do j = 2,n-1
	do i=1,n
		B(i,j) = A(i,j+1) - A(i,j-1)
	end do
end do
!$OMP END do
!$OMP END parallel

stop
end program b2
```

### Explication du code

Tout d'abord les directives d'*OpenMP* peuvent être longues, il est donc possible de revenir à la ligne avec une esperluette `&` et de continuer sur une nouvelle ligne avec toujours le mot clé `!$OMP` (pour que cela reste un commentaire si *OpenMP* n'est pas activé).

*OpenMP* fonctionne avec une mémoire partagée, il est donc nécessaire d'indiquer la visibilité des variables (`default(none)` indique que l'on force l'indication et que l'on ne souhaite pas que le compilateur prenne de potentiel mauvaise décision).

* `shared(A,B)` : les matrices `A` et `B` étant utilisées par tous les *threads* il est nécessaire qu'elles soient partagées, avec le risque que plusieurs *threads* écrivent au même endroit.
* `private(i,j)` : on ne veut pas que les indices de parcours de boucles soient partagés entre les *threads* (chaque *thread* écrirait chacun son tour dans ces variables faisant... n'importe quoi), ces variables seront donc privées.

La directive `OMP do` permet d'indiquer au compilateur de paralléliser la boucle `do` suivante (que la suivante, pas toutes les suivantes).

### Exécution


Compilation :

```{.term .sh}
gfortran -fopenmp b1.f90 -o b1
```

Exécution :

```{.term .sh}
./b1
```

Et là normalement ça ne fonctionne pas. La mémoire partagée est limitée est l'on souhaite y faire rentrer 2 matrices de taille 1025x1025. Il est possible de faire sauter cette limite avec la commande suivante :

```{.term .sh}
ulimit -s unlimited
```

Pour voir les différentes limites s'appliquant sur l'utilisateur il est possible d'effectuer la commande :

```{.term .sh}
ulimit -a
```

La limite nous concernant est celle nommée `stack size`.

## Les différents TP

Les TP suivants utilisent des codes déjà pré-existant qu'il va falloir paralléliser, pour cela on remarque une archive (`TP_ennonce_2017_2018.tar`) dans notre *home* :

```{.term .sh}
cd && ls
```

Soit on l'ouvre avec des outils graphiques grâce à `sshfs` soit on utilise la ligne de commandes :

```{.term .sh}
tar xvf TP_ennonce_2017_2018.tar
```

Puis on navigue dedans et on remarque la présence de plusieurs TP :

```{.term .sh}
ls -R
```

Pour le moment on a uniquement fait le TP_02, 3 dossiers y sont présents :

* `sequentiel` qui contient le code séquentiel à paralléliser (donc on le copie le code dans le dossier `parallele`).
* `parallele` qui contient un `Makefile`, il code à paralléliser est celui contenu dans le dossier `sequentiel`.
* `multi_fichiers` qui contient le même principe mais en plusieurs fichiers pour voir la porter des directives d'*OpenMP*.





