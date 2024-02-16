## Conditions préalables
Vous devez installer les différents linters de sécurité pour Kubernetes. Actuellement ils sont :
-  [ checkov ] ( https://github.com/bridgecrewio/checkov )
-  [ kubesec ] ( https://github.com/controlplaneio/kubesec )
-  [ kubeaudit ] ( https://github.com/Shopify/kubeaudit )

## Installer

Cette application nécessite que [ pipenv ] ( https://pipenv.pypa.io/en/latest/ ) soit disponible et installé.
Exécutez ` pipenv install` pour télécharger automatiquement toutes les dépendances nécessaires
## Courir 
Un moyen simple d'exécuter le script est :
` pipenv exécutez python main.py -f input/example.yml `
À FAIRE
- Augmenter le nombre de contrôleurs de sécurité (actuellement, il n'y a que checkov)
- Développer les règles de fuzzing
- Comment gérer plusieurs sorties pour la même entrée ?
