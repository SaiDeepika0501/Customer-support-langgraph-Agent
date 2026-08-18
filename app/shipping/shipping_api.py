# from datetime import datetime, timedelta


# # Simulated external shipping database/API
# SHIPPING_DATA = {
#     "TRK123456": {
#         "tracking_number": "TRK123456",
#         "carrier": "FedEx",
#         "current_location": "Hyderabad, India",
#         "status": "In Transit",
#         "estimated_delivery": "2026-08-20",
#         "latest_event": "Package departed Hyderabad sorting facility",
#     },
#     "TRK987654": {
#         "tracking_number": "TRK987654",
#         "carrier": "DHL",
#         "current_location": "Bengaluru, India",
#         "status": "Out for Delivery",
#         "estimated_delivery": "2026-08-17",
#         "latest_event": "Package is out for delivery",
#     },
# }


# def track_shipment(tracking_number: str):
#     """
#     Simulates an external shipping API.

#     In a real application this function would make an HTTP request
#     to FedEx, UPS, DHL, Shippo, EasyPost, etc.
#     """

#     shipment = SHIPPING_DATA.get(tracking_number)

#     if not shipment:
#         return {
#             "success": False,
#             "tracking_number": tracking_number,
#             "message": "Tracking number not found."
#         }

#     return {
#         "success": True,
#         **shipment
#     }


# app/shipping/shipping_api.py

"""
Simulated external shipping API.

The tracking numbers here intentionally match the tracking numbers
stored in database/support.db.

In a real production system, this data would come from an external
carrier/shipping provider instead of this local dictionary.
"""

SHIPPING_DATA = {
    "TRK-111": {
        "tracking_number": "TRK-111",
        "carrier": "FedEx",
        "current_location": "Bengaluru, India",
        "status": "Out for Delivery",
        "estimated_delivery": "2026-08-18",
        "latest_event": "Package is out for delivery",
    },

    "TRK-222": {
        "tracking_number": "TRK-222",
        "carrier": "DHL",
        "current_location": "Chennai, India",
        "status": "Processing",
        "estimated_delivery": "2026-08-21",
        "latest_event": "Package is being processed at the Chennai facility",
    },

    "TRK-555": {
        "tracking_number": "TRK-555",
        "carrier": "FedEx",
        "current_location": "Hyderabad, India",
        "status": "Delivered",
        "estimated_delivery": "2026-08-16",
        "latest_event": "Package was delivered successfully",
    },
}


def track_shipment(tracking_number: str):
    """
    Simulates a request to an external shipping provider.
    """

    shipment = SHIPPING_DATA.get(tracking_number)

    if not shipment:
        return {
            "success": False,
            "tracking_number": tracking_number,
            "message": "Tracking number not found.",
        }

    return {
        "success": True,
        **shipment,
    }