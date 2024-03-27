from flask import Flask, request, jsonify
from flask_caching import Cache
from celery import Celery
import redis

app = Flask(__name__)

# Initialize Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Initialize Celery
celery = Celery(app.name, broker='redis://localhost:6379/0')

# Initialize Redis connection
r = redis.Redis(host='redis-11078.c305.ap-south-1-1.ec2.cloud.redislabs.com', 
                port=11078, 
                db=0, 
                password='H3EK8ms2ZGDqfPugAbB14cX7N3BvOO9A')

@app.route('/closest-bicycle', methods=['GET'])
@cache.cached(timeout=60)  # Cache the result for 60 seconds
def find_closest_bicycle():
    try:
        # Extract latitude and longitude from the request
        lat_str = request.args.get('latitude')
        lon_str = request.args.get('longitude')

        if not lat_str or not lon_str:
            return jsonify({'error': 'Latitude and longitude parameters are required.'}), 400

        lat = float(lat_str)
        lon = float(lon_str)
        
        # Query Redis for the closest bicycle
        closest_bicycle = r.georadius('bicycles', lon, lat, radius=1000, unit='m', withdist=True, sort='ASC', count=1)
        
        # Return information about the closest bicycle
        if closest_bicycle:
            bicycle_id, distance = closest_bicycle[0]
            return jsonify({'bicycle_id': bicycle_id, 'distance_meters': distance})
        else:
            return jsonify({'message': 'No bicycles found nearby'})
    except ValueError:
        return jsonify({'error': 'Latitude and longitude must be valid floating-point numbers.'}), 400

@celery.task
def update_bicycle_locations():
    # Implement code to update bicycle locations asynchronously
    pass

if __name__ == '__main__':
    app.run(debug=True)
