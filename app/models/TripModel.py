from app.helpers.Util import dbExecute


class TripModel:
    def save_events(self, events):
        try:
            if not events:
                return {
                    "inserted": 0,
                    "duplicates": 0,
                }

            sql = """
                INSERT IGNORE INTO trip_events
                    (event_id, driver_id, fare_amount, status, completed_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            rows = [
                (
                    event["event_id"],
                    event["driver_id"],
                    event["fare_amount"],
                    event["status"],
                    event["completed_at"],
                )
                for event in events
            ]
            inserted = dbExecute(sql, "executemany", rows)
            return {
                "inserted": inserted,
                "duplicates": len(events) - inserted,
            }
        except Exception as e:
            raise Exception(str(e))

    def get_driver_summary(self, driver_id):
        try:
            sql = """
                SELECT
                    COUNT(*) AS trips_count,
                    COALESCE(
                        SUM(CASE WHEN status = 'completed' THEN fare_amount ELSE 0 END),
                        0
                    ) AS total_payout_amount
                FROM trip_events
                WHERE driver_id = %s
            """
            row = dbExecute(sql, "fetchone", (driver_id,))
            return {
                "driver_id": driver_id,
                "total_payout_amount": row["total_payout_amount"] if row else 0,
                "trips_count": int(row["trips_count"]) if row else 0,
            }
        except Exception as e:
            raise Exception(str(e))
