import sys
import os

# Add the root directory (project folder) to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from dateutil import parser as date_parser

from utils.date_utils import parse_relative_date
from db.connection import get_connection

def book_appointment_sync(response: str) -> str:
    try:
        # Handle both old format and direct parameters
        if response.startswith("BOOKING:"):
            raw = response[9:].strip()  # Remove "BOOKING: " prefix
        else:
            raw = response[10:-1]  # Keep existing logic for backward compatibility
        
        name, date_text, time_text = [x.strip() for x in raw.split(",")]

        if not name or name.lower() in ["", "none", "null"]:
                return "Please provide a valid name to book the appointment."

            # Parse date (e.g., "tomorrow" → "2025-07-15")
        date = parse_relative_date(date_text)

            # Reject past dates
        if datetime.strptime(date, "%Y-%m-%d").date() < datetime.now().date():
                return f" The date '{date}' is in the past. Please choose a future date."

            # Validate booking time between 06:00 and 21:00
        try:
                booking_time = datetime.strptime(time_text, "%H:%M").time()
        except ValueError:
                return f"{e}"

        if not (datetime.strptime("06:00", "%H:%M").time() <= booking_time <= datetime.strptime("21:00", "%H:%M").time()):
                return f"Invalid time: {time_text}. You can only book between 06:00 and 21:00."
        # Parse date/time flexibly
        clean_date = date_parser.parse(date, fuzzy=True).date()
        clean_time = date_parser.parse(time_text, fuzzy=True).time()

        conn = get_connection()
        cursor = conn.cursor()

        # Check if slot is already booked
        cursor.execute(
            "SELECT COUNT(*) FROM appointments WHERE date = ? AND time = ?",
            (clean_date, clean_time)
        )
        (count,) = cursor.fetchone()
        if count > 0:
            return f"❌ Sorry, the slot on {clean_date} at {clean_time} is already booked."

        # Insert appointment
        cursor.execute(
            "INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)",
            (name, clean_date, clean_time)
        )
        conn.commit()
        conn.close()

        return f"✅ Appointment booked for {name} on {clean_date} at {clean_time}."

    except ValueError as e:
        return f"{e}."
    except Exception as e:
        return f"❌ Booking failed due to server error: {str(e)}"

