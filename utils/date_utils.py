from datetime import datetime
import dateparser

def parse_relative_date(text: str) -> str:
    parsed = dateparser.parse(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'DATE_ORDER': 'DMY',
            'STRICT_PARSING': True
        }
    )

    if not parsed:
        raise ValueError(f"❌ Could not parse or interpret date: '{text}'")

    today = datetime.now().date()
    parsed_date = parsed.date()
    print(parsed_date)
    print(today)
    print(parsed_date<today)

    if parsed_date < today:
        print("coming to error")
        raise ValueError(f"❌ The date '{parsed_date}' is in the past. Please choose a future date.")

    return parsed_date.strftime("%Y-%m-%d")
