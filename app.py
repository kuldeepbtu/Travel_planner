import os, sys, csv, subprocess, math
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPOTS = [
    {
        "name": "Taj Mahal",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "lat": 27.1751,
        "lng": 78.0421,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "UNESCO-listed white marble mausoleum"
    },
    {
        "name": "Varanasi Ghats",
        "city": "Varanasi",
        "state": "Uttar Pradesh",
        "lat": 25.306,
        "lng": 83.0107,
        "cat": "city",
        "emoji": "🛕",
        "desc": "Historic riverfront and spiritual centre"
    },
    {
        "name": "Jaipur City Palace",
        "city": "Jaipur",
        "state": "Rajasthan",
        "lat": 26.9258,
        "lng": 75.8237,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Palaces and heritage in the Pink City"
    },
    {
        "name": "Jaisalmer Fort",
        "city": "Jaisalmer",
        "state": "Rajasthan",
        "lat": 26.9124,
        "lng": 70.912,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Living golden sandstone fort in the Thar Desert"
    },
    {
        "name": "Udaipur City Palace",
        "city": "Udaipur",
        "state": "Rajasthan",
        "lat": 24.5764,
        "lng": 73.6835,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Lakefront royal palace complex"
    },
    {
        "name": "Mehrangarh Fort",
        "city": "Jodhpur",
        "state": "Rajasthan",
        "lat": 26.2971,
        "lng": 73.0183,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Hilltop fort overlooking the Blue City"
    },
    {
        "name": "Ranthambore National Park",
        "city": "Sawai Madhopur",
        "state": "Rajasthan",
        "lat": 26.0173,
        "lng": 76.5026,
        "cat": "park",
        "emoji": "🐅",
        "desc": "Tiger reserve and historic fort"
    },
    {
        "name": "Mount Abu",
        "city": "Mount Abu",
        "state": "Rajasthan",
        "lat": 24.5926,
        "lng": 72.7156,
        "cat": "hill",
        "emoji": "⛰️",
        "desc": "Hill station in the Aravalli Range"
    },
    {
        "name": "Golden Temple",
        "city": "Amritsar",
        "state": "Punjab",
        "lat": 31.62,
        "lng": 74.8765,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Sacred Sikh shrine and sarovar"
    },
    {
        "name": "Dal Lake",
        "city": "Srinagar",
        "state": "Jammu and Kashmir",
        "lat": 34.0837,
        "lng": 74.7973,
        "cat": "lake",
        "emoji": "🏞️",
        "desc": "Iconic Himalayan lake with houseboats"
    },
    {
        "name": "Gulmarg",
        "city": "Baramulla",
        "state": "Jammu and Kashmir",
        "lat": 34.0484,
        "lng": 74.3805,
        "cat": "hill",
        "emoji": "⛷️",
        "desc": "Mountain resort and gondola"
    },
    {
        "name": "Vaishno Devi",
        "city": "Katra",
        "state": "Jammu and Kashmir",
        "lat": 33.03,
        "lng": 74.949,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Major pilgrimage shrine in Trikuta hills"
    },
    {
        "name": "Pangong Tso",
        "city": "Leh",
        "state": "Ladakh",
        "lat": 33.7595,
        "lng": 78.667,
        "cat": "lake",
        "emoji": "🏞️",
        "desc": "High-altitude Himalayan lake"
    },
    {
        "name": "Nubra Valley",
        "city": "Leh",
        "state": "Ladakh",
        "lat": 34.683,
        "lng": 77.565,
        "cat": "desert",
        "emoji": "🏜️",
        "desc": "Cold desert with dunes and mountain views"
    },
    {
        "name": "India Gate",
        "city": "New Delhi",
        "state": "Delhi",
        "lat": 28.6129,
        "lng": 77.2295,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "War memorial on Kartavya Path"
    },
    {
        "name": "Qutub Minar",
        "city": "New Delhi",
        "state": "Delhi",
        "lat": 28.5245,
        "lng": 77.1855,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "UNESCO-listed medieval minaret"
    },
    {
        "name": "Gateway of India",
        "city": "Mumbai",
        "state": "Maharashtra",
        "lat": 18.922,
        "lng": 72.8347,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "Waterfront arch overlooking the Arabian Sea"
    },
    {
        "name": "Marine Drive",
        "city": "Mumbai",
        "state": "Maharashtra",
        "lat": 18.943,
        "lng": 72.8238,
        "cat": "beach",
        "emoji": "🌊",
        "desc": "Famous curved seafront promenade"
    },
    {
        "name": "Ajanta Caves",
        "city": "Aurangabad",
        "state": "Maharashtra",
        "lat": 20.5519,
        "lng": 75.7033,
        "cat": "cave",
        "emoji": "🕳️",
        "desc": "Ancient Buddhist rock-cut cave complex"
    },
    {
        "name": "Ellora Caves",
        "city": "Aurangabad",
        "state": "Maharashtra",
        "lat": 20.0268,
        "lng": 75.179,
        "cat": "cave",
        "emoji": "🕳️",
        "desc": "Rock-cut temples including Kailasa"
    },
    {
        "name": "Hampi",
        "city": "Vijayanagara",
        "state": "Karnataka",
        "lat": 15.335,
        "lng": 76.46,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "UNESCO ruins of the Vijayanagara Empire"
    },
    {
        "name": "Mysore Palace",
        "city": "Mysuru",
        "state": "Karnataka",
        "lat": 12.3052,
        "lng": 76.6552,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Illuminated royal palace"
    },
    {
        "name": "Coorg",
        "city": "Kodagu",
        "state": "Karnataka",
        "lat": 12.3375,
        "lng": 75.8069,
        "cat": "hill",
        "emoji": "🌿",
        "desc": "Coffee estates and Western Ghats scenery"
    },
    {
        "name": "Jog Falls",
        "city": "Shivamogga",
        "state": "Karnataka",
        "lat": 14.229,
        "lng": 74.81,
        "cat": "waterfall",
        "emoji": "🌊",
        "desc": "Spectacular Sharavathi River waterfall"
    },
    {
        "name": "Charminar",
        "city": "Hyderabad",
        "state": "Telangana",
        "lat": 17.3616,
        "lng": 78.4747,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "Iconic four-minaret monument"
    },
    {
        "name": "Golconda Fort",
        "city": "Hyderabad",
        "state": "Telangana",
        "lat": 17.3833,
        "lng": 78.4011,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Historic hilltop fort"
    },
    {
        "name": "Brihadeeswarar Temple",
        "city": "Thanjavur",
        "state": "Tamil Nadu",
        "lat": 10.7828,
        "lng": 79.1318,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "UNESCO Chola-era temple"
    },
    {
        "name": "Meenakshi Amman Temple",
        "city": "Madurai",
        "state": "Tamil Nadu",
        "lat": 9.9195,
        "lng": 78.1193,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Famed temple with colourful gopurams"
    },
    {
        "name": "Marina Beach",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "lat": 13.05,
        "lng": 80.2824,
        "cat": "beach",
        "emoji": "🏖️",
        "desc": "Long urban beach on the Bay of Bengal"
    },
    {
        "name": "Ooty",
        "city": "Nilgiris",
        "state": "Tamil Nadu",
        "lat": 11.4102,
        "lng": 76.695,
        "cat": "hill",
        "emoji": "⛰️",
        "desc": "Nilgiri hill station and toy train"
    },
    {
        "name": "Kanyakumari",
        "city": "Kanniyakumari",
        "state": "Tamil Nadu",
        "lat": 8.0883,
        "lng": 77.5385,
        "cat": "beach",
        "emoji": "🌅",
        "desc": "Southern tip of mainland India"
    },
    {
        "name": "Munnar",
        "city": "Idukki",
        "state": "Kerala",
        "lat": 10.0889,
        "lng": 77.0595,
        "cat": "hill",
        "emoji": "🌿",
        "desc": "Tea gardens in the Western Ghats"
    },
    {
        "name": "Alleppey Backwaters",
        "city": "Alappuzha",
        "state": "Kerala",
        "lat": 9.4981,
        "lng": 76.3388,
        "cat": "lake",
        "emoji": "🛶",
        "desc": "Backwater canals and houseboat cruises"
    },
    {
        "name": "Fort Kochi",
        "city": "Kochi",
        "state": "Kerala",
        "lat": 9.9658,
        "lng": 76.2421,
        "cat": "monument",
        "emoji": "🏘️",
        "desc": "Historic coastal quarter and Chinese fishing nets"
    },
    {
        "name": "Athirappilly Falls",
        "city": "Thrissur",
        "state": "Kerala",
        "lat": 10.285,
        "lng": 76.569,
        "cat": "waterfall",
        "emoji": "🌊",
        "desc": "Large waterfall on the Chalakudy River"
    },
    {
        "name": "Bodh Gaya Mahabodhi Temple",
        "city": "Gaya",
        "state": "Bihar",
        "lat": 24.6959,
        "lng": 84.9911,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Place associated with Buddha's enlightenment"
    },
    {
        "name": "Nalanda Mahavihara",
        "city": "Nalanda",
        "state": "Bihar",
        "lat": 25.1367,
        "lng": 85.4439,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "Ancient university archaeological site"
    },
    {
        "name": "Victoria Memorial",
        "city": "Kolkata",
        "state": "West Bengal",
        "lat": 22.5448,
        "lng": 88.3426,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "Marble museum and landmark"
    },
    {
        "name": "Darjeeling",
        "city": "Darjeeling",
        "state": "West Bengal",
        "lat": 27.041,
        "lng": 88.2663,
        "cat": "hill",
        "emoji": "🚂",
        "desc": "Tea gardens and Himalayan toy train"
    },
    {
        "name": "Sundarbans National Park",
        "city": "South 24 Parganas",
        "state": "West Bengal",
        "lat": 21.9497,
        "lng": 89.1833,
        "cat": "park",
        "emoji": "🐅",
        "desc": "Mangrove forest and Bengal tiger habitat"
    },
    {
        "name": "Konark Sun Temple",
        "city": "Puri",
        "state": "Odisha",
        "lat": 19.8876,
        "lng": 86.0945,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "UNESCO stone chariot temple"
    },
    {
        "name": "Jagannath Temple",
        "city": "Puri",
        "state": "Odisha",
        "lat": 19.8048,
        "lng": 85.8175,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Major Hindu pilgrimage temple"
    },
    {
        "name": "Chilika Lake",
        "city": "Puri",
        "state": "Odisha",
        "lat": 19.7,
        "lng": 85.32,
        "cat": "lake",
        "emoji": "🦩",
        "desc": "Large brackish lagoon and bird habitat"
    },
    {
        "name": "Kaziranga National Park",
        "city": "Golaghat",
        "state": "Assam",
        "lat": 26.5775,
        "lng": 93.1711,
        "cat": "park",
        "emoji": "🦏",
        "desc": "UNESCO reserve famous for one-horned rhinos"
    },
    {
        "name": "Kamakhya Temple",
        "city": "Guwahati",
        "state": "Assam",
        "lat": 26.1664,
        "lng": 91.705,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Historic Shakti shrine on Nilachal Hill"
    },
    {
        "name": "Majuli Island",
        "city": "Majuli",
        "state": "Assam",
        "lat": 26.95,
        "lng": 94.17,
        "cat": "island",
        "emoji": "🏝️",
        "desc": "River island known for satras and culture"
    },
    {
        "name": "Tawang Monastery",
        "city": "Tawang",
        "state": "Arunachal Pradesh",
        "lat": 27.586,
        "lng": 91.859,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Large Buddhist monastery in the Himalayas"
    },
    {
        "name": "Ziro Valley",
        "city": "Lower Subansiri",
        "state": "Arunachal Pradesh",
        "lat": 27.594,
        "lng": 93.838,
        "cat": "hill",
        "emoji": "🌄",
        "desc": "Scenic valley and Apatani cultural landscape"
    },
    {
        "name": "Nathula Pass",
        "city": "Gangtok",
        "state": "Sikkim",
        "lat": 27.386,
        "lng": 88.831,
        "cat": "hill",
        "emoji": "🏔️",
        "desc": "High mountain pass on the India–China border"
    },
    {
        "name": "Tsomgo Lake",
        "city": "Gangtok",
        "state": "Sikkim",
        "lat": 27.374,
        "lng": 88.772,
        "cat": "lake",
        "emoji": "🏞️",
        "desc": "Glacial lake in the East Sikkim Himalayas"
    },
    {
        "name": "Gurudongmar Lake",
        "city": "Mangan",
        "state": "Sikkim",
        "lat": 28.014,
        "lng": 88.707,
        "cat": "lake",
        "emoji": "🏞️",
        "desc": "High-altitude sacred lake"
    },
    {
        "name": "Living Root Bridges",
        "city": "East Khasi Hills",
        "state": "Meghalaya",
        "lat": 25.2333,
        "lng": 91.7167,
        "cat": "bridge",
        "emoji": "🌉",
        "desc": "Traditional living bridges grown from tree roots"
    },
    {
        "name": "Nohkalikai Falls",
        "city": "East Khasi Hills",
        "state": "Meghalaya",
        "lat": 25.2547,
        "lng": 91.6893,
        "cat": "waterfall",
        "emoji": "🌊",
        "desc": "Tall plunge waterfall near Sohra"
    },
    {
        "name": "Shillong",
        "city": "East Khasi Hills",
        "state": "Meghalaya",
        "lat": 25.5788,
        "lng": 91.8933,
        "cat": "city",
        "emoji": "🏙️",
        "desc": "Hill city known as Scotland of the East"
    },
    {
        "name": "Loktak Lake",
        "city": "Bishnupur",
        "state": "Manipur",
        "lat": 24.55,
        "lng": 93.8,
        "cat": "lake",
        "emoji": "🏞️",
        "desc": "Floating phumdis and Keibul Lamjao"
    },
    {
        "name": "Kangla Fort",
        "city": "Imphal",
        "state": "Manipur",
        "lat": 24.8074,
        "lng": 93.9368,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Historic seat of Manipuri rulers"
    },
    {
        "name": "Dzukou Valley",
        "city": "Kohima",
        "state": "Nagaland",
        "lat": 25.553,
        "lng": 94.01,
        "cat": "hill",
        "emoji": "🌸",
        "desc": "High-altitude valley known for seasonal flowers"
    },
    {
        "name": "Unakoti",
        "city": "Unakoti",
        "state": "Tripura",
        "lat": 24.327,
        "lng": 92.07,
        "cat": "monument",
        "emoji": "🗿",
        "desc": "Ancient rock-cut Shaivite sculptures"
    },
    {
        "name": "Neermahal",
        "city": "Melaghar",
        "state": "Tripura",
        "lat": 23.49,
        "lng": 91.33,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Water palace in Rudrasagar Lake"
    },
    {
        "name": "Aizawl",
        "city": "Aizawl",
        "state": "Mizoram",
        "lat": 23.7271,
        "lng": 92.7176,
        "cat": "city",
        "emoji": "🏙️",
        "desc": "Capital city set along forested ridges"
    },
    {
        "name": "Phawngpui Blue Mountain",
        "city": "Saiha",
        "state": "Mizoram",
        "lat": 22.67,
        "lng": 93.02,
        "cat": "hill",
        "emoji": "🏔️",
        "desc": "Highest peak in Mizoram"
    },
    {
        "name": "Chitrakote Falls",
        "city": "Jagdalpur",
        "state": "Chhattisgarh",
        "lat": 19.204,
        "lng": 81.701,
        "cat": "waterfall",
        "emoji": "🌊",
        "desc": "Broad waterfall on the Indravati River"
    },
    {
        "name": "Kanger Valley National Park",
        "city": "Bastar",
        "state": "Chhattisgarh",
        "lat": 18.8,
        "lng": 81.9,
        "cat": "park",
        "emoji": "🌳",
        "desc": "Forest, caves and biodiversity"
    },
    {
        "name": "Sanchi Stupa",
        "city": "Raisen",
        "state": "Madhya Pradesh",
        "lat": 23.4793,
        "lng": 77.7397,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "UNESCO Buddhist monument"
    },
    {
        "name": "Khajuraho Temples",
        "city": "Chhatarpur",
        "state": "Madhya Pradesh",
        "lat": 24.8318,
        "lng": 79.9199,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "UNESCO temples with intricate carvings"
    },
    {
        "name": "Bhedaghat Marble Rocks",
        "city": "Jabalpur",
        "state": "Madhya Pradesh",
        "lat": 23.13,
        "lng": 79.8,
        "cat": "canyon",
        "emoji": "🪨",
        "desc": "Marble cliffs along the Narmada"
    },
    {
        "name": "Rann of Kutch",
        "city": "Kutch",
        "state": "Gujarat",
        "lat": 23.8,
        "lng": 69.5,
        "cat": "desert",
        "emoji": "🏜️",
        "desc": "Vast seasonal white salt desert"
    },
    {
        "name": "Statue of Unity",
        "city": "Narmada",
        "state": "Gujarat",
        "lat": 21.838,
        "lng": 73.7191,
        "cat": "monument",
        "emoji": "🗿",
        "desc": "World's tallest statue"
    },
    {
        "name": "Somnath Temple",
        "city": "Gir Somnath",
        "state": "Gujarat",
        "lat": 20.888,
        "lng": 70.4012,
        "cat": "temple",
        "emoji": "🛕",
        "desc": "Historic temple on the Arabian Sea"
    },
    {
        "name": "Gir National Park",
        "city": "Junagadh",
        "state": "Gujarat",
        "lat": 21.1243,
        "lng": 70.8242,
        "cat": "park",
        "emoji": "🦁",
        "desc": "Last natural habitat of Asiatic lions"
    },
    {
        "name": "Diu Fort",
        "city": "Diu",
        "state": "Dadra and Nagar Haveli and Daman and Diu",
        "lat": 20.7144,
        "lng": 70.9874,
        "cat": "monument",
        "emoji": "🏰",
        "desc": "Portuguese-era sea fort"
    },
    {
        "name": "Cellular Jail",
        "city": "Port Blair",
        "state": "Andaman and Nicobar Islands",
        "lat": 11.673,
        "lng": 92.75,
        "cat": "monument",
        "emoji": "🏛️",
        "desc": "Historic freedom struggle memorial"
    },
    {
        "name": "Radhanagar Beach",
        "city": "Swaraj Dweep",
        "state": "Andaman and Nicobar Islands",
        "lat": 11.983,
        "lng": 92.95,
        "cat": "beach",
        "emoji": "🏖️",
        "desc": "Famous tropical beach"
    },
    {
        "name": "Kavaratti Lagoon",
        "city": "Kavaratti",
        "state": "Lakshadweep",
        "lat": 10.5667,
        "lng": 72.6369,
        "cat": "beach",
        "emoji": "🏝️",
        "desc": "Turquoise lagoon and coral reefs"
    }
]

def road_dist(s1, s2):
    R = 6371
    lat1,lng1 = math.radians(s1['lat']),math.radians(s1['lng'])
    lat2,lng2 = math.radians(s2['lat']),math.radians(s2['lng'])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lng2-lng1)/2)**2
    return max(1, round(2*R*math.asin(math.sqrt(a)) * 1.5))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/spots')
def api_spots():
    return jsonify(SPOTS)

@app.route('/api/run-tsp', methods=['POST'])
def api_run_tsp():
    selected = request.get_json(force=True).get('spots', [])
    if len(selected) < 2:
        return jsonify({'error': 'Select at least 2 spots.'}), 400
    if len(selected) > 12:
        return jsonify({'error': 'Select at most 12 spots for exact TSP.'}), 400

    n     = len(selected)
    names = [s['name'] for s in selected]
    adj   = [[road_dist(selected[i],selected[j]) if i!=j else 0 for j in range(n)] for i in range(n)]

    with open(os.path.join(BASE_DIR, 'input.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['']+names)
        for i in range(n):
            w.writerow([names[i]]+adj[i])
    print("  input.csv written.")

    exe = os.path.join(BASE_DIR, 'tsp_csv.exe' if sys.platform == 'win32' else 'tsp_csv')
    if not os.path.isfile(exe):
        return jsonify({'error': f'TSP exe not found. Compile with: g++ -O2 -o tsp_csv tsp_csv.cpp'}), 500

    try:
        proc = subprocess.run([exe], capture_output=True, text=True, timeout=120, cwd=BASE_DIR)
    except FileNotFoundError:
        return jsonify({'error': f'Cannot execute {exe}.'}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'TSP timed out. Try fewer spots.'}), 500

    if proc.returncode != 0:
        return jsonify({'error': f'TSP failed:\n{proc.stderr or proc.stdout}'}), 500

    name_map    = {s['name']:s for s in selected}
    route_steps = []
    total_km    = None

    with open(os.path.join(BASE_DIR, 'output.csv'), 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            step    = row.get('Step','').strip()
            name    = row.get('District','').strip().strip('"')
            cum_str = row.get('Cumulative Distance (km)','').strip().strip('"')
            if step.upper()=='TOTAL':
                try:    total_km = int(cum_str.replace(' km',''))
                except: total_km = cum_str
                continue
            spot = name_map.get(name,{})
            route_steps.append({
                'step':step,'name':name,'cumulative_km':cum_str,
                'lat':spot.get('lat'),'lng':spot.get('lng'),
                'cat':spot.get('cat',''),'emoji':spot.get('emoji','📍'),
                'desc':spot.get('desc',''),
            })

    return jsonify({'route':route_steps,'total_km':total_km})

if __name__=='__main__':
    exe = os.path.join(BASE_DIR, 'tsp_csv.exe' if sys.platform=='win32' else 'tsp_csv')
    print("\n"+"="*54)
    print("   TripTrekker  ·  India Route Planner")
    print("="*54)
    print(f"   TSP exe : {'OK' if os.path.isfile(exe) else 'MISSING  → g++ -O2 -o '+exe+' tsp_csv.cpp'}")
    print(f"   Spots   : {len(SPOTS)} destinations across India (no API)")
    print("   URL     : http://localhost:5000")
    print("="*54+"\n")
    app.run(debug=True, port=5000)
    