```
pip install annotated-types anyio click ezdxf fastapi fonttools h11 idna numpy pandas pydantic pydantic_core pyparsing python-dateutil pytz six sniffio typing-inspection typing_extensions tzdata uvicorn
```

```bash
uvicorn main:app --reload
```

```bash
curl -X POST "http://127.0.0.1:8000/generer_caisson" \
     -H "Content-Type: application/json" \
     -d '{"nom": "Caisson Test", "largeur": 900, "profondeur": 550, "hauteur": 1000, "epaisseur_montant": 19, "epaisseur_fond": 8, "epaisseur_traverse": 19, "quantite": 1}'
```


```bash
Invoke-WebRequest -Uri "http://127.0.0.1:8000/generer_caisson" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"nom": "Caisson Test", "largeur": 900, "profondeur": 550, "hauteur": 2000, "epaisseur_montant": 19, "epaisseur_fond": 8, "epaisseur_traverse": 19, "quantite": 5}'
```
