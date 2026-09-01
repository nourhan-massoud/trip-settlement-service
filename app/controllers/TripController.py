from flask import request


class TripController:
    def ingest_trips(self):
        return {"message": "POST /trips is not ready yet"}, 501

    def get_driver_summary(self, driver_id):
        if not driver_id:
            driver_id = (request.view_args or {}).get("driver_id", "")
        return {
            "message": "GET /drivers/{driver_id}/summary is not ready yet",
            "driver_id": driver_id,
        }, 501
