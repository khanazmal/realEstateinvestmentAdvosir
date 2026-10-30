# 25 SQL Queries with Explanations — Real Estate Investment Advisor

The included app currently reads CSV data for easy local setup. These queries are a SQL extension for MySQL/SQLite-style learning. Create the table using `schema.sql`; adjust `AUTO_INCREMENT`/data types if using SQLite.

## Schema
See `schema.sql`.

## 1. Show all properties
```sql
SELECT * FROM properties;
```
**Explanation:** Returns all stored property records.

## 2. Count properties
```sql
SELECT COUNT(*) AS total_properties FROM properties;
```
**Explanation:** Counts rows in the properties table.

## 3. Average property price
```sql
SELECT AVG(price_inr) AS average_price FROM properties;
```
**Explanation:** Calculates the average listed/sample price.

## 4. Minimum and maximum price
```sql
SELECT MIN(price_inr) AS min_price, MAX(price_inr) AS max_price FROM properties;
```
**Explanation:** Shows price range.

## 5. Median-like price ranking (MySQL 8+)
```sql
SELECT price_inr FROM properties ORDER BY price_inr LIMIT 1 OFFSET (SELECT FLOOR(COUNT(*)/2) FROM properties);
```
**Explanation:** Gets the middle ordered value for an odd/even-size approximation; exact median handling can differ by database.

## 6. Average price by city
```sql
SELECT city, AVG(price_inr) AS avg_price FROM properties GROUP BY city ORDER BY avg_price DESC;
```
**Explanation:** Compares average prices across cities.

## 7. Median proxy by city
```sql
SELECT city, AVG(price_inr) AS mean_price FROM properties GROUP BY city ORDER BY mean_price DESC;
```
**Explanation:** Uses mean as a simple city-level summary; use percentile functions for exact median.

## 8. Properties above average price
```sql
SELECT * FROM properties WHERE price_inr > (SELECT AVG(price_inr) FROM properties);
```
**Explanation:** Finds rows priced above overall average.

## 9. Properties below ₹50 lakh
```sql
SELECT * FROM properties WHERE price_inr < 5000000;
```
**Explanation:** Filters affordable properties by threshold.

## 10. Large properties
```sql
SELECT * FROM properties WHERE area_sqft >= 1500 ORDER BY area_sqft DESC;
```
**Explanation:** Lists larger homes.

## 11. Three-bedroom homes
```sql
SELECT * FROM properties WHERE bedrooms = 3;
```
**Explanation:** Filters three-bedroom properties.

## 12. Newer properties
```sql
SELECT * FROM properties WHERE property_age_years <= 5;
```
**Explanation:** Finds relatively new properties.

## 13. Higher rent yield
```sql
SELECT * FROM properties WHERE annual_rent_yield_pct >= 4.0 ORDER BY annual_rent_yield_pct DESC;
```
**Explanation:** Finds rows with yield at least 4%.

## 14. Price per square foot
```sql
SELECT property_id, city, price_inr / NULLIF(area_sqft, 0) AS price_per_sqft FROM properties ORDER BY price_per_sqft DESC;
```
**Explanation:** Calculates price density while avoiding division by zero.

## 15. Average area by city
```sql
SELECT city, AVG(area_sqft) AS avg_area FROM properties GROUP BY city;
```
**Explanation:** Compares property sizes by city.

## 16. Bedroom distribution
```sql
SELECT bedrooms, COUNT(*) AS property_count FROM properties GROUP BY bedrooms ORDER BY bedrooms;
```
**Explanation:** Counts properties by bedroom count.

## 17. Price range groups
```sql
SELECT CASE WHEN price_inr < 3000000 THEN 'Under 30L' WHEN price_inr < 7000000 THEN '30L-70L' ELSE '70L+' END AS price_band, COUNT(*) AS total FROM properties GROUP BY price_band;
```
**Explanation:** Groups properties into broad price bands.

## 18. High location score
```sql
SELECT * FROM properties WHERE location_score >= 8 ORDER BY price_inr DESC;
```
**Explanation:** Filters highly rated locations.

## 19. Amenities and price
```sql
SELECT amenities_count, AVG(price_inr) AS avg_price FROM properties GROUP BY amenities_count ORDER BY amenities_count;
```
**Explanation:** Explores association between amenities and price.

## 20. Age and price
```sql
SELECT property_age_years, AVG(price_inr) AS avg_price FROM properties GROUP BY property_age_years ORDER BY property_age_years;
```
**Explanation:** Summarizes price by property age.

## 21. City-wise count
```sql
SELECT city, COUNT(*) AS total FROM properties GROUP BY city ORDER BY total DESC;
```
**Explanation:** Counts rows in each city.

## 22. Potential investment shortlist
```sql
SELECT * FROM properties WHERE annual_rent_yield_pct >= 4 AND property_age_years <= 10 AND location_score >= 7 ORDER BY annual_rent_yield_pct DESC;
```
**Explanation:** Creates a rule-based exploratory shortlist, not financial advice.

## 23. Top ten by price
```sql
SELECT * FROM properties ORDER BY price_inr DESC LIMIT 10;
```
**Explanation:** Returns ten highest-priced records.

## 24. Top ten by rent yield
```sql
SELECT * FROM properties ORDER BY annual_rent_yield_pct DESC LIMIT 10;
```
**Explanation:** Returns ten highest-yield records.

## 25. Data quality check
```sql
SELECT COUNT(*) AS total_rows, SUM(CASE WHEN price_inr IS NULL THEN 1 ELSE 0 END) AS missing_prices, SUM(CASE WHEN area_sqft <= 0 THEN 1 ELSE 0 END) AS invalid_areas FROM properties;
```
**Explanation:** Checks row count, missing prices and invalid areas.

