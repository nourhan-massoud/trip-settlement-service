1 - Set up the API project and connect it to the database.
      Folders:
      - app/controllers
      - app/models
      - app/requests
      - app/helpers
      - routes/
      Config:
      - .env.example in git (no real secrets)
      - .env local only (git ignores it)
      - app/helpers/config.py reads env values

2 - Create TripModel.
      - fare_amount is DECIMAL, not float.

3 - Save and read trip events in TripModel.

4 - Create a trip_events table:
      - event_id is UNIQUE (no duplicate events).
      - index on driver_id (faster driver summary).
      - fare_amount is DECIMAL.

5 - Validate the full batch before saving any events.
      - Fail-fast: if one event is invalid, reject the whole request (HTTP 400).
      - Do not save a partial batch.

6 - Save events safely and ignore duplicate event_id values.
      - Do not overwrite an event that already exists.

7 - Return the correct number of inserted and duplicate events.

8 - Add the driver summary endpoint:
      - trips_count counts all stored trips for that driver.
      - total_payout_amount sums only completed trips.

9 - Add tests for validation, duplicates, out-of-order events, summaries, and concurrent requests.

10 - Add Docker setup, simple run/test commands, API documentation, curl examples, and design notes in the README.
      - README must explain fail-fast, DECIMAL money, and the driver_id index.
