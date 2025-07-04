#!/usr/bin/env bash
set -euo pipefail

# 🚀 Récupère automatiquement un token JWT (admin/admin)
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.com","password":"admin"}' \
  | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

# 1) Lister toutes les reviews
echo "➜ Liste des reviews existantes:"
curl -s -H "Authorization: Bearer $TOKEN" \
     http://127.0.0.1:5000/api/v1/reviews/ \
  | python -m json.tool

# 2) Créer une review pour la place #1
echo "➜ Création d'une review:"
curl -s -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"place_id":"1","text":"Un moment magique avec Mr Philips"}' \
  | python -m json.tool

# 3) Récupérer l'ID de la dernière review créée
NEW_ID=$(
  curl -s -H "Authorization: Bearer $TOKEN" \
       http://127.0.0.1:5000/api/v1/reviews/ \
  | python -c 'import sys,json; data=json.load(sys.stdin); print(data[-1]["id"])'
)

echo "→ Nouvel ID = $NEW_ID"

# 4) Modifier la review (texte corrigé)
echo "➜ Modification de la review #$NEW_ID:"
curl -s -X PUT http://127.0.0.1:5000/api/v1/reviews/$NEW_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"text":"Superbe exp\u00e9rience avec Mr Philips"}' \
  | python -m json.tool

# 5) Supprimer la review
echo "➜ Suppression de la review #$NEW_ID:"
curl -s -X DELETE http://127.0.0.1:5000/api/v1/reviews/$NEW_ID \
  -H "Authorization: Bearer $TOKEN" \
  | python -m json.tool

echo "✅ Opérations terminées."