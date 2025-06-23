import re
from datetime import datetime

LOG_FILE = "app.log"

# Regular expression to parse the log lines
log_pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - "
    r"(?P<level>[A-Z]+) - (?P<signature_status>[A-Z]+) \| "
    r"(?:(?P<message>.*?) \| )?client: (?P<client>[^|]+) \| event: (?P<event>\S+)"
)


def parse_logs():
    """Parses logs for use in a view"""
    parsed_logs = []
    with open(LOG_FILE, "r") as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                data = match.groupdict()
                # Normalize timestamp format
                data["timestamp"] = datetime.strptime(
                    data["timestamp"], "%Y-%m-%d %H:%M:%S,%f"
                ).isoformat()
                parsed_logs.append(data)

    parsed_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    return parsed_logs
