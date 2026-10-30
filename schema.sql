CREATE TABLE properties (
    property_id INTEGER PRIMARY KEY,
    city VARCHAR(80) NOT NULL,
    area_sqft INTEGER NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    property_age_years INTEGER NOT NULL,
    location_score INTEGER NOT NULL,
    amenities_count INTEGER NOT NULL,
    annual_rent_yield_pct DECIMAL(5,2) NOT NULL,
    price_inr BIGINT NOT NULL
);
