# Python Examples for Google APIs

These Python modules are basic examples for connecting to and requesting data from popular Google APIs.  Authorization methods may vary by API and will typically require a Google account for access.

## App Engine User Example

Identify your app engine users via the internal `X-Goog-Authenticated-User` HTTP headers and create their own dataset in BigQuery.  This wrapper allows an App Engine app to export and share data with logged-in users in BigQuery.  Exported data can be confined to individual users to later retrieval and processing.

## Cloud Tasks Example

App Engine example of pushing a new task to an existing Google Cloud Task queue.  When the task is ready to process Google Cloud Tasks will call the internal App Engine URL passed via `relative_uri`.  Using Cloud Tasks can separate longer or scheduled processes from the App Engine user interface.

## Google Sheets & Google Drive Example

This Python module allows for basic creation and sharing of Google Sheets via Google Drive.  A service worker account creates and populates spread sheet data and then shares the completed sheet with the designated user.  This configuration allows for user-specific datasets that are accessible via Google Drive and Google Sheets - including the interface and any additional integrations.

## Keyword Planner Example

This Python module allows for large volume requests of keyword data from the Google Ads Keyword Planner.  Keyword data includes average search volume, 12 month search volume history, estimated cost per click, expected competition, Google Ads category IDs, and year over year change in keyword search volume.

## Google My Business Reporting Example

This Python module allows for basic reporting on location metrics, driving requests, and reviews for Google My Business locations.  This data can be used to understand how users are finding business, how often they actually visit or call the business, and any questions or reviews they may have submitted through a Google My Business listing.

## Google Search Console Reporting Example

This Python module allows for large-scale (beyond 1000 rows) requests for organic keyword data via the Google Search Console API.  Organic data can be segmented by landing page, date, and device.  This module reports on monthly and daily keyword metrics within a given date range or range of months.

## Senitment Analysis

Submit strings of content to Google's Natural Language Processing API to return sentiment and magnitude.
