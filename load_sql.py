import pymysql
import json

myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='12345678',database = "airbnb")

file_path = 'C:/Users/moham/Music/Airbnb/sample_airbnb.json'

with open(file_path, 'r') as file:
    # Load the JSON data
    data = json.load(file)

for a in data:
    sql = "insert into airbnb.hotel values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (
        a.get('_id'),
        a.get('listing_url'),
        a.get('name'),
        a.get('summary'),
        a.get('space'),
        a.get('description'),
        a.get('neighborhood_overview'),
        a.get('notes'),
        a.get('transit'),
        a.get('access'),
        a.get('interaction'),
        a.get('house_rules'),
        a.get('property_type'),
        a.get('room_type'),
        a.get('bed_type'),
        a.get('minimum_nights'),
        a.get('maximum_nights'),
        a.get('cancellation_policy'),
        a.get('last_scraped'),
        a.get('calendar_last_scraped'),
        a.get('last_review'),
        a.get('first_review'),
        a.get('accommodates'),
        a.get('bedrooms'),
        a.get('beds'),
        a.get('number_of_reviews'),
        a.get('bathrooms'),
        str(a.get('amenities')),
        a.get('price'),
        a.get('security_deposit'),
        a.get('cleaning_fee'),
        a.get('extra_people'),
        a.get('guests_included'),
        a.get('monthly_price'),
        a.get('reviews_per_month'),
        a.get('weekly_price') 
    )
    myconnection.cursor().execute(sql,values)
    myconnection.commit()

    if a['address'] != []:
        sql = "insert into airbnb.address values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        address = a.get('address', {})
        location = address.get('location', {})
        coordinates = location.get('coordinates', [None, None])
        
        values = (
            a.get('_id'), 
            address.get('country'),
            address.get('country_code'),
            address.get('street'),
            address.get('government_area'),
            address.get('market'),
            address.get('suburb'),
            coordinates[0] if len(coordinates) > 0 else None,
            coordinates[1] if len(coordinates) > 1 else None,
            location.get('is_location_exact'),
            location.get('type')
        )
        
        myconnection.cursor().execute(sql,values)
        myconnection.commit()

    if a['availability'] != []:
        sql = "insert into airbnb.availability values (%s,%s,%s,%s,%s)"
        values = (
            a.get('_id'),
            a.get('availability', {}).get('availability_30'),
            a.get('availability', {}).get('availability_60'),
            a.get('availability', {}).get('availability_90'),
            a.get('availability', {}).get('availability_365')
        )
        myconnection.cursor().execute(sql,values)
        myconnection.commit()

    if a['host'] != []:
        sql = "insert into airbnb.host values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (
            a.get('_id'),
            a.get('host', {}).get('host_id'),
            a.get('host', {}).get('host_url'),
            a.get('host', {}).get('host_name'),
            a.get('host', {}).get('host_location'),
            a.get('host', {}).get('host_about'),
            a.get('host', {}).get('host_response_rate'),
            a.get('host', {}).get('host_thumbnail_url'),
            a.get('host', {}).get('host_picture_url'),
            a.get('host', {}).get('host_neighbourhood'),
            a.get('host', {}).get('host_response_rate'),
            a.get('host', {}).get('host_is_superhost'),
            a.get('host', {}).get('host_has_profile_pic'),
            a.get('host', {}).get('host_identity_verified'),
            a.get('host', {}).get('host_listings_count'),
            a.get('host', {}).get('host_total_listings_count'),
            str(a.get('host', {}).get('host_verifications'))
        )
        myconnection.cursor().execute(sql,values)
        myconnection.commit()

    if a['images'] != []:
        sql = "insert into airbnb.image values (%s,%s,%s,%s,%s)"
        values = (
            a.get('_id'),
            a.get('images', {}).get('medium_url'),
            a.get('images', {}).get('picture_url'),
            a.get('images', {}).get('thumbnail_url'),
            a.get('images', {}).get('xl_picture_url')
        )
        myconnection.cursor().execute(sql,values)
        myconnection.commit()

    if a['review_scores'] != []:
        sql = "insert into airbnb.review_score values (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (
            a.get('_id'),
            a.get('review_scores', {}).get('review_scores_accuracy'),
            a.get('review_scores', {}).get('review_scores_checkin'),
            a.get('review_scores', {}).get('review_scores_cleanliness'),
            a.get('review_scores', {}).get('review_scores_communication'),
            a.get('review_scores', {}).get('review_scores_location'),
            a.get('review_scores', {}).get('review_scores_rating'),
            a.get('review_scores', {}).get('review_scores_value')
        )
        myconnection.cursor().execute(sql,values)
        myconnection.commit()

    sql = "insert into airbnb.review values (%s,%s,%s,%s,%s,%s,%s)"
    if a['reviews'] == []:
        continue
    for review in a.get('reviews', []):
        values = (
            a.get('_id'),
            review.get('_id'),
            review.get('date'),
            review.get('listing_id'),
            review.get('reviewer_id'),
            review.get('reviewer_name'),
            review.get('comments')
        )
        myconnection.cursor().execute(sql,values)
        myconnection.commit()  
