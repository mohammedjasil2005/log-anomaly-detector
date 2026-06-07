import random
import datetime
import os

random.seed(42)

log_templates = {
    "INFO": [
        "User login successful for user_id={}",
        "Database query completed in {}ms",
        "Cache hit for key={}",
        "API request processed successfully endpoint=/api/v1/{}",
        "Scheduled job completed: {}",
    ],
    "WARNING": [
        "High memory usage detected: {}%",
        "Slow query detected: {}ms",
        "Retry attempt {} for service={}",
    ],
    "ERROR": [
        "Connection timeout to database host={}",
        "Disk read failed on partition={}",
        "Null pointer exception in module={}",
        "Failed to connect to service={}",
    ]
}

def generate_logs(n=1000, anomaly_bursts=5):
    logs = []
    timestamp = datetime.datetime(2024, 1, 15, 0, 0, 0)

    for i in range(n):
        timestamp += datetime.timedelta(seconds=random.randint(1, 5))

        if i in [200, 400, 600, 750, 900]:
            for _ in range(random.randint(15, 25)):
                timestamp += datetime.timedelta(seconds=0.1)
                msg = random.choice(log_templates["ERROR"]).format(
                    random.choice(["db-01", "db-02", "svc-auth", "svc-payments"]),
                )
                logs.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}  ERROR  {msg}")
        else:
            level = random.choices(
                ["INFO", "INFO", "INFO", "INFO", "WARNING", "ERROR"],
                weights=[60, 60, 60, 60, 15, 5]
            )[0]
            template = random.choice(log_templates[level])
            msg = template.format(random.randint(1, 999), random.randint(1, 500))
            logs.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}  {level}  {msg}")

    return logs

if __name__ == "__main__":
    logs = generate_logs()
    path = os.path.join(os.path.dirname(__file__), "data", "server.log")
    with open(path, "w") as f:
        f.write("\n".join(logs))
    print(f"Generated {len(logs)} log lines -> data/server.log")
