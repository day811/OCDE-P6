curl -X POST http://127.0.0.1:3000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "first_use_type": "Hospital",
      "second_use_type": "None",
      "multiple_use_type": 1,
      "sum_largest_GFA": 108434.0,
      "use_steam": true,
      "use_gas": false,
      "number_of_floors": 12.0,
      "number_of_buildings": 3.0,
      "city_distance": 8.5,
      "neighborhood": "DOWNTOWN",
      "year_built": 1999
    }
  }'
