# Booking contract
start is a naive ISO local timestamp, zone an IANA name, interval_days and count positive integers. exclude contains local ISO dates. ambiguous is earlier or later. Nonexistent local times are skipped with a reason. Count is the number of candidate local dates including exclusions. Output includes the chosen UTC time and offset.
