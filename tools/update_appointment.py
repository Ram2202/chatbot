import pyodbc

def update_appointment(name, old_date, new_date, new_time):
    try:
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=...;DATABASE=...;UID=...;PWD=...")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Appointments
            SET date = ?, time = ?
            WHERE name = ? AND date = ?
        """, (new_date, new_time, name, old_date))

        if cursor.rowcount == 0:
            return f"❌ No appointment found for {name} on {old_date}."

        conn.commit()
        conn.close()
        return f"✅ Appointment for {name} updated to {new_date} at {new_time}."
    except Exception as e:
        return f"❌ Failed to update appointment: {e}"
