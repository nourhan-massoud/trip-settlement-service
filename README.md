# trip-settlement-service

This API receives trip events and shows a payout summary per driver.

Stack: Python, Flask, MySQL.

## Folders

Same names as our other Flask apps. No broker (no queue in this task).

```
database/        SQL table (trip_events)
routes/          URL list (same idea as 121)
app/
  controllers/   what each URL does
  models/        TripEvent, save events, driver summary
  requests/      check the JSON before save
  helpers/       small shared code (DB, dates)
```

## Config

Copy the example file, then set your values:

```bash
cp .env.example .env
```

`.env` is not in git. Only `.env.example` is.

Do not put real passwords in the repo.

## Rules we chose

**Fail-fast**

We check the whole batch first.

If one event is invalid, we reject the full request (`400`).

We do not save some events and skip others.

**Money**

`fare_amount` is stored as `DECIMAL`, not float.

Float can change money values. Decimal keeps the exact number.

**Index**

`event_id` is unique, so the same event is not saved twice.

`driver_id` has an index, so the summary query is faster.

## API

### POST /trips

Send a list of events.

Invalid and duplicate are not the same thing.

- Invalid = bad data (missing field, negative fare, bad date). Then we return `400` and save nothing.
- Duplicate = the event is valid, but this `event_id` is already in the database. Then we return `200`.

Example: 11 valid events. 9 are new. 2 were already saved before.

```json
{
  "inserted": 9,
  "duplicates": 2
}
```

We ignore the 2 duplicates. We do not update them. Totals do not change.

Only `status = "completed"` is added to payout.

### GET /drivers/{driver_id}/summary

```json
{
  "driver_id": "abc",
  "total_payout_amount": 87.50,
  "trips_count": 3
}
```

`trips_count` = all stored events for that driver.

`total_payout_amount` = sum of completed trips only.

## How we keep data safe

**Same event twice (idempotency)**

`event_id` is unique in the database.

If the same id comes again, the insert is skipped.

Totals do not change.

**Two requests at the same time (concurrency)**

The unique key stops two workers from inserting the same id.

We save inside a transaction.

The summary then stays correct.

## Run the app

(Commands will be added when the project is set up.)

Local:

```bash
make run
```

Tests:

```bash
make test
```

Docker:

```bash
docker compose up --build
```

## Curl examples

```bash
curl -X POST http://localhost:8000/trips \
  -H "Content-Type: application/json" \
  -d '{"events":[{"event_id":"e1","driver_id":"d1","fare_amount":87.50,"status":"completed","completed_at":"2026-03-04T18:30:00Z"}]}'
```

```bash
curl http://localhost:8000/drivers/d1/summary
```
