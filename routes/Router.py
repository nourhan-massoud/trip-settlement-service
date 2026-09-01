from flask import current_app as app, request
from flask_restful import Api, Resource

from app.controllers.TripController import TripController


class Router:
    """Basic Routes Handler"""

    def init_app_routes(self):
        api = Api(app)
        api.add_resource(
            App,
            "/",
            "/trips",
            "/drivers/<string:driver_id>/summary",
        )


class App(Resource):
    """
    Application Requests Routes Handler
    """

    def get(self, driver_id=None):
        route = request.url_rule.rule
        trip_controller = TripController()

        if route == "/":
            return {
                "success": "true",
                "result": "Hello from trip settlement service",
            }, 200

        if route == "/drivers/<string:driver_id>/summary":
            return trip_controller.get_driver_summary(driver_id)

        return {"error": "Not found"}, 404

    def post(self):
        route = request.url_rule.rule
        trip_controller = TripController()

        if route == "/trips":
            return trip_controller.ingest_trips()

        return {"error": "Not found"}, 404
