from datetime import date

from src.nonprofit_service import aggregate_listings, campaign_report, donor_receipt, volunteer_reminder


def test_duplicate_feeds_are_collapsed_and_reported():
    listings = aggregate_listings([
        {"name": "River Aid", "mission": "Clean water", "source": "city-feed", "volunteer_slots": 4},
        {"name": "river aid", "mission": "Clean water", "source": "directory", "volunteer_slots": 4},
        {"name": "Food Shelf", "mission": "Meals", "source": "directory", "volunteer_slots": 2},
    ])
    receipts = [donor_receipt("Sam", listings[0], 25, date(2026, 9, 3))]
    assert campaign_report(listings, receipts) == {"nonprofits": 2, "donations": 1, "total_amount": 25.0, "sources": ["city-feed", "directory"]}
    assert volunteer_reminder(listings[0], date(2026, 9, 10))["send_on"] == "2026-09-08"
