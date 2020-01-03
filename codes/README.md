# Manuel d'utilisation:

## 1) Extraction du texte depuis les pdf
Utilisation du script **extractText.sh** : 
```
./extractText DOSSIER_ORIGINE/ DOSSIER_SORTIE/
```
En sortie : tous les documents du DOSSIER_ORIGINE se retrouvent dans des fichiers indépendants .txt dans le DOSSIER_SORTIE

/!\ : Peut prendre beaucoup de temps si l'OCR s'active

Problèmes avec l'OCR : 
- Crash de la transformation d'image pour documents très longs (> 30 pages)
- Certains documents ont seulement quelques pages en OCR parmi des pages avec du texte facilement extractable. Les pages nécessitants l'OCR sont alors considérées vides et le texte n'est pas récupéré.
- Certains documents pdf présentent uniquement le texte "Pour de meilleurs résultats, ouvrez ce porte document PDF dans 9, Adobe Acrobat Reader 9 ou version antérieure." lors de la lecture du texte inscrit. Il nous faut chercher une manière d'ouvrir ce genre de documents

## 2) Récupération des éléments clefs du texte 
Utilisation du code  **find_code.py**, utilisant des REGEX : 
```
python find_code.py DOCUMENT_TXT_ENTREE
```
Sortie : référence des arrêtés/articles/décrets/RAA, dates, titres des arrêtés

Des améliorations sont a prévoir pour la détection des titres.


## 3) Analyse avec word2vec.py


## 4) Mise en forme JSON
Utilisation du script **fill_json.sh**, appellant le script python **fill_json.py**, lui même dépendant de **find.py**
```
./fill_json.sh DOSSIER_CONTENANT_TXT
```
Sortie : fichier prefet_json.json contenant les métadonnées de chaque fichiers formatées pour ElasticSearch.
