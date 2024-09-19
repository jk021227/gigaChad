# Ethics Statement

## Purpose of Data Collection
We are collecting restaurant and menu data from Deliveroo to create dietary recommendations based on users' nutritional goals. The data will be used solely for educational and research purposes.

## Why Are We Collecting This Data?
The data is being collected to analyze restaurant offerings and map them to specific dietary needs. This will allow us to provide users with tailored food choices to help them achieve their nutritional objectives.

## Data Sources and Robots.txt Compliance
We are scraping data from the Deliveroo website based in the UAE. In compliance with Deliveroo's `robots.txt` file:

- We will not scrape URLs that are disallowed in the robots.txt file, including:
  - /admin/
  - /api/
  - /account
  - /login
  - Any URL with parameters such as `?redeem_credit_token`, `?sp_id=`, and others.
  
- We will respect the `noindex` directives mentioned in the robots.txt file and avoid scraping restricted pages.

For reference, the `robots.txt` file for Deliveroo can be found [here](https://deliveroo.ae/robots.txt).

## Collection Practices
- We will limit scraping activities to avoid any disruption to Deliveroo’s services.
- We will only scrape the top 10 restaurants from each cuisine's "top offers" section.
- We will not bypass any password protection or access restricted areas, such as `/account` or `/orders/`.
  
## Data Handling and Privacy
- No Personally Identifiable Information (PII) will be collected during this project. We will only collect publicly available restaurant and menu data.
- Any collected data will be stored securely and excluded from version control through the use of `.gitignore` files to protect sensitive or large datasets.

## Data Usage
- All collected data will be used solely for educational and research purposes in the context of this project.
- Data will not be used for commercial purposes or shared with third parties.