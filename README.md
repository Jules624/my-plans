```
pip install annotated-types anyio click ezdxf fastapi fonttools h11 idna numpy pandas pydantic pydantic_core pyparsing python-dateutil pytz six sniffio typing-inspection typing_extensions tzdata uvicorn
```

```bash
uvicorn main:app --reload
```

```bash
curl -X POST "http://127.0.0.1:8000/generer_caisson" \
     -H "Content-Type: application/json" \
     -d '{
           "nom": "Caisson Toto",
           "largeur": 600,
           "profondeur": 550,
           "hauteur": 1200,
           "epaisseur_montant": 19,
           "epaisseur_traverse": 19,
           "epaisseur_fond": 8,
           "quantite": 1,
           "nombre_tablettes": 1
           "epaisseur_tablette": 19
         }'
```

```bash
curl -X POST "http://127.0.0.1:8000/generer_caisson" \
     -H "Content-Type: application/json" \
     -d '{
           "nom": "Caisson Toto",
           "largeur": 600,
           "profondeur": 550,
           "hauteur": 1200,
           "epaisseur_montant": 19,
           "epaisseur_traverse": 19,
           "epaisseur_fond": 8,
           "quantite": 1,
           "porte": {
               "type_porte": "simple",
               "epaisseur": 19,
               "jeu_gauche": 0,
               "jeu_droit": 0,
               "jeu_haut": 0,
               "jeu_bas": 0,
               "jeu_avant": 2
           },
           "nombre_tablettes": 1,
           "epaisseur_tablette": 10
         }'

```

```bash
Invoke-WebRequest -Uri "http://127.0.0.1:8000/generer_caisson" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"nom": "Caisson Test", "largeur": 900, "profondeur": 550, "hauteur": 2000, "epaisseur_montant": 19, "epaisseur_fond": 8, "epaisseur_traverse": 19, "quantite": 5}'
```
