from datetime import date

from src.nonprofit_service import aggregate_listings, campaign_report, donor_receipt, embed_text, volunteer_reminder


def main() -> None:
    listings = aggregate_listings([
        {"name": "River Aid", "mission": "Clean water", "source": "city-feed", "volunteer_slots": 4},
        {"name": "Food Shelf", "mission": "Meals for neighbors", "source": "directory", "volunteer_slots": 2},
    ])
    receipt = donor_receipt("Alex", listings[0], 40.0, date(2026, 9, 3))
    print(campaign_report(listings, [receipt]))
    print(volunteer_reminder(listings[1], date(2026, 9, 15)))
    embedding = embed_text("Clean water and meals for neighbors")
    print({"embedding_dimensions": len(embedding)})


if __name__ == "__main__":
    main()
