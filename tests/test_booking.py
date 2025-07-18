# tests/test_booking.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.book_appointment import book_appointment_sync

result = book_appointment_sync("Alice", "2025-07-10", "14:00")
print(result)
