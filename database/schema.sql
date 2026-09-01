CREATE TABLE IF NOT EXISTS trip_events (
    event_id VARCHAR(64) NOT NULL,
    driver_id VARCHAR(64) NOT NULL,
    fare_amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(32) NOT NULL,
    completed_at DATETIME(6) NOT NULL,
    PRIMARY KEY (event_id),
    INDEX idx_trip_events_driver_id (driver_id)
);
