# trip-settlement-service

This API receives trip events and shows a payout summary per driver.

Stack: Python, Flask, MySQL.

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

If all events are valid:

```json
{
  "inserted": 9,
  "duplicates": 2
}
```

If any event is invalid: `400` and nothing is saved.

Same `event_id` again is a duplicate. We ignore it. We do not update it.

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
curl -X POST http://localhost:5000/trips \
  -H "Content-Type: application/json" \
  -d '{"events":[{"event_id":"e1","driver_id":"d1","fare_amount":87.50,"status":"completed","completed_at":"2026-03-04T18:30:00Z"}]}'
```

```bash
curl http://localhost:5000/drivers/d1/summary
```
