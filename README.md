# Rapport du projet de programmation

[![Repo](https://img.shields.io/badge/Projet-GitHub-blue)](https://github.com/atbrt/projet_programmation)

## 1. Introduction : Présentation du problème du Swap Puzzle

### A. Description du problème

Dans ce projet, nous nous intéressons au problème du **swap puzzle**. Imaginons une grille composée de _m_ lignes et _n_ colonnes, où chaque case contient un carreau numéroté de 1 à _mn_, initialement placé de manière aléatoire. L'objectif est de trouver la séquence la plus courte de mouvements pour réorganiser les carreaux en une configuration ordonnée.

Les seuls mouvements autorisés sont des **swaps** verticaux ou horizontaux entre carreaux adjacents. Les swaps ne sont pas autorisés sur les bords extérieurs de la grille.

### B. Applications du problème

La résolution de ce problème a des applications en **intelligence artificielle** et en **recherche opérationnelle**, notamment pour développer des algorithmes de recherche et d'optimisation. Par exemple, il est possible d'utiliser des techniques telles que la recherche en profondeur, la recherche en largeur, ou l'algorithme **A*** pour résoudre ce type de problème.

## 2. Méthodologie algorithmique

### A. Méthodes algorithmiques

Nous avons exploré différentes approches, des plus simples aux plus optimisées :

- **Méthode naïve** : On place chaque carreau à sa position correcte séquentiellement, en utilisant des swaps. Bien que non optimale, cette méthode permet de toujours trouver une solution.
- **Algorithme BFS** : Le problème est modélisé comme un graphe, avec des nœuds représentant des configurations de grilles, et les arcs correspondant à des swaps. On utilise ensuite un parcours en largeur pour trouver la solution.
- **Algorithme A\*** : Cet algorithme utilise une **heuristique** (la distance de Manhattan) pour choisir les nœuds à explorer, en optimisant ainsi le temps de résolution.

### B. Implémentation

Chaque méthode a été implémentée en Python, avec les fonctionnalités suivantes :

- **Naïve** : Fonction de swap simple.
- **BFS** : Création dynamique du graphe des grilles possibles, évitant la construction complète en mémoire.
- **A\*** : Heuristique de distance pour optimiser le parcours.

## 3. Analyse de la complexité

- **Méthode naïve** : Complexité temporelle de $O((m \times n)^2)$.
- **BFS** : Complexité en $O((m \times n)! \times (2m \times n - m - n + 1))$, coûteux en espace mémoire.
- **A\*** : Optimisation grâce à l'heuristique de Manhattan.

## 4. Résultats et évaluation

- **Méthode naïve** : Solution trouvée en 0.0114 secondes avec un chemin de 6 swaps.
- **BFS amélioré** : Solution trouvée en 0.06 secondes.
- **A\*** : Solution optimale trouvée en 0.0115 secondes, mais avec une séquence de swaps légèrement plus longue.

Pour une grille plus grande (6x6), les résultats sont les suivants :
- **Méthode naïve** : 124 swaps en 0.01 secondes.
- **A\*** : 102 swaps en 6.5 secondes.

## 5. Conclusion

L'algorithme **A\*** fournit une solution plus courte, mais la **méthode naïve** reste la plus rapide pour les petites grilles. L'algorithme **BFS**, bien qu'utile, est moins efficace en termes de temps et de mémoire pour les grandes grilles.

## 6. Sources

[Optimisation logistique et recherche opérationnelle](https://www.supplychaininfo.eu/dossier-optimisation-logistique/comment-utiliser-recherche-operationnelle-optimisation-logistique/)
