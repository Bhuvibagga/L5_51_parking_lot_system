
"""Parking lot management system with improved safety and code quality."""

import hashlib
import math
import os
import secrets

PARKING_SLOTS = {
    "P01": {
        "plate": "KA01AB1234",
        "hours": 2,
        "rate": 20.0,
        "is_occupied": True,
    },
    "P02": {
        "plate": "TN07CD5678",
        "hours": 0,
        "rate": 20.0,
        "is_occupied": False,
    },
    "P03": {
        "plate": "MH02EF9012",
        "hours": 4,
        "rate": 30.0,
        "is_occupied": True,
    },
}


class ParkingLot:
    """Manage parking slots and total collections."""

    def __init__(self, slots):
        """Initialize the parking lot."""
        self.slots = slots
        self.total_collections = 0.0

    def park_vehicle(self, slot_id, plate_no, hours_booked=1, entry_logs=None):
        """Park a vehicle if the requested slot is available."""
        if entry_logs is None:
            entry_logs = []

        if slot_id not in self.slots:
            return False

        if self.slots[slot_id]["is_occupied"]:
            return False

        if (
            not isinstance(hours_booked, int)
            or isinstance(hours_booked, bool)
            or hours_booked <= 0
        ):
            return False

        if not isinstance(plate_no, str) or not plate_no.strip():
            return False

        slot = self.slots[slot_id]
        slot["plate"] = plate_no
        slot["hours"] = hours_booked
        slot["is_occupied"] = True

        self.total_collections += slot["rate"] * hours_booked

        entry_logs.append(
            f"Vehicle {plate_no} parked at slot {slot_id} "
            f"for {hours_booked} hours"
        )
        return True

    def release_slot(self, slot_id):
        """Release an occupied parking slot."""
        if slot_id not in self.slots:
            return False

        slot = self.slots[slot_id]

        if not slot["is_occupied"]:
            return False

        slot["is_occupied"] = False
        slot["plate"] = ""
        slot["hours"] = 0
        return True

    def check_slot_availability(self, slot_id):
        """Check whether a parking slot is available."""
        if slot_id not in self.slots:
            return False

        return not self.slots[slot_id]["is_occupied"]

    def calculate_parking_fee(self, slot_id, surge_multiplier=1.0):
        """Calculate the base parking rate and surge multiplier."""
        if slot_id not in self.slots:
            raise ValueError("Invalid parking slot")

        if (
            isinstance(surge_multiplier, bool)
            or not isinstance(surge_multiplier, (int, float))
            or not math.isfinite(surge_multiplier)
            or surge_multiplier < 0
        ):
            raise ValueError("Invalid surge multiplier")

        return self.slots[slot_id]["rate"] * surge_multiplier

    def get_available_summary(self):
        """Count the unoccupied parking slots."""
        return sum(
            not details["is_occupied"]
            for details in self.slots.values()
        )


def generate_vehicle_hash(plate_no):
    """Generate a SHA-256 hash of a vehicle registration number."""
    return hashlib.sha256(plate_no.encode("utf-8")).hexdigest()


def generate_ticket_pin():
    """Generate a secure four-digit ticket PIN."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(slots, filename="parking_manifest.txt"):
    """Export parking slot information to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(slots))

    print(f"Parking manifest exported to: {filename}")


def main():
    """Run a demonstration of the parking lot system."""
    parking_lot = ParkingLot(PARKING_SLOTS)
    gate_barrier_key = os.getenv("BARRIER_GATE_SECRET_TOKEN")

    parking_lot.park_vehicle("P02", "DL03GH3456", 3)
    parking_lot.release_slot("P01")

    print(
        "Is P02 available:",
        parking_lot.check_slot_availability("P02"),
    )
    print(
        "Surge Parking Fee:",
        parking_lot.calculate_parking_fee("P03", 1.50),
    )
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    print("Total Collections:", parking_lot.total_collections)

    export_parking_manifest(parking_lot.slots)
    print("Vacant slots:", parking_lot.get_available_summary())
    print("Barrier Key configured:", bool(gate_barrier_key))


if __name__ == "__main__":
    main()
