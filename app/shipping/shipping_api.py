from datetime import datetime, timedelta


# Simulated external shipping database/API
SHIPPING_DATA = {
    "TRK123456": {
        "tracking_number": "TRK123456",
        "carrier": "FedEx",
        "current_location": "Hyderabad, India",
        "status": "In Transit",
        "estimated_delivery": "2026-08-20",
        "latest_event": "Package departed Hyderabad sorting facility",
    },
    "TRK987654": {
        "tracking_number": "TRK987654",
        "carrier": "DHL",
        "current_location": "Bengaluru, India",
        "status": "Out for Delivery",
        "estimated_delivery": "2026-08-17",
        "latest_event": "Package is out for delivery",
    },
}


def track_shipment(tracking_number: str):
    """
    Simulates an external shipping API.

    In a real application this function would make an HTTP request
    to FedEx, UPS, DHL, Shippo, EasyPost, etc.
    """

    shipment = SHIPPING_DATA.get(tracking_number)

    if not shipment:
        return {
            "success": False,
            "tracking_number": tracking_number,
            "message": "Tracking number not found."
        }

    return {
        "success": True,
        **shipment
    }