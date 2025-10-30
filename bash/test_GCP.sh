
curl -X POST https://building-energy-prediction-190096654611.europe-west1.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "first_use_type": "Hotel",
      "second_largest_property_use_type": null,
      "multiple_use_type": 1,
      "sum_largest_GFA": 88434.0,
      "use_steam": true,
      "use_electricity": true,
      "use_gas": false,
      "number_of_floors": 12.0,
      "number_of_buildings": 1.0,
      "city_distance": 8.5,
      "neighborhood": "DOWNTOWN",
      "year_built": 1999
    }
  }'