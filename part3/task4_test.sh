#!/bin/bash

# Base API URL
BASE_URL="http://127.0.0.1:5000/api/v1"

# Replace with your real JWT tokens
ADMIN_TOKEN="ey...admin..."
USER_TOKEN="ey...user..."

echo "1. Admin creates a new user"
curl -s -X POST $BASE_URL/users/ \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "newuser@example.com", "password": "pass", "first_name": "New", "last_name": "User"}'
echo -e "\n"

echo "2. Admin updates another user's information"
curl -s -X PUT $BASE_URL/users/2 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "ModifiedByAdmin", "email": "adminchange@example.com"}'
echo -e "\n"

echo "3. Regular user attempts to update another user (should be denied)"
curl -s -X PUT $BASE_URL/users/1 \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "UnauthorizedChange"}'
echo -e "\n"

echo "4. Admin updates a review without being its author"
curl -s -X PUT $BASE_URL/reviews/1 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Admin edit"}'
echo -e "\n"

echo "5. Admin creates a new amenity"
curl -s -X POST $BASE_URL/amenities/ \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Premium WiFi"}'
echo
