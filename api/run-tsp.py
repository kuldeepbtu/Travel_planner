import json
import math
from http.server import BaseHTTPRequestHandler
from app import SPOTS, road_dist

def solve_tsp(selected):
    n = len(selected)
    if n < 2:
        raise ValueError("Select at least 2 spots.")
    if n > 12:
        raise ValueError("Select at most 12 spots for exact TSP.")

    # Held-Karp dynamic programming: exact TSP, fixed start at first selected spot.
    # State key is (visited_mask, last_index); value is (cost, path).
    dp = {}
    for j in range(1, n):
        dp[(1 << j, j)] = (road_dist(selected[0], selected[j]), [0, j])

    for mask in range(1 << n):
        if mask & 1:
            for last in range(1, n):
                state = dp.get((mask, last))
                if state is None:
                    continue
                cost, path = state
                for nxt in range(1, n):
                    bit = 1 << nxt
                    if mask & bit:
                        continue
                    new_mask = mask | bit
                    new_cost = cost + road_dist(selected[last], selected[nxt])
                    key = (new_mask, nxt)
                    old = dp.get(key)
                    if old is None or new_cost < old[0]:
                        dp[key] = (new_cost, path + [nxt])

    full_mask = (1 << n) - 1
    best_cost = None
    best_path = None
    for last in range(1, n):
        state = dp.get((full_mask, last))
        if state is None:
            continue
        total = state[0] + road_dist(selected[last], selected[0])
        if best_cost is None or total < best_cost:
            best_cost, best_path = total, state[1] + [0]

    if best_path is None:
        raise ValueError("No valid route could be calculated.")

    route = []
    cumulative = 0
    for position, index in enumerate(best_path):
        if position:
            cumulative += road_dist(selected[best_path[position - 1]], selected[index])
        spot = selected[index]
        route.append({
            "step": str(position + 1),
            "name": spot["name"],
            "cumulative_km": str(cumulative),
            "lat": spot["lat"],
            "lng": spot["lng"],
            "cat": spot.get("cat", ""),
            "emoji": spot.get("emoji", "📍"),
            "desc": spot.get("desc", "")
        })
    return {"route": route, "total_km": best_cost}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100000:
                raise ValueError("Invalid request body.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            requested = payload.get("spots", [])
            if not isinstance(requested, list):
                raise ValueError("Spots must be a list.")

            # Use server-owned coordinates and metadata, not client-supplied values.
            known = {spot["name"]: spot for spot in SPOTS}
            selected = []
            seen = set()
            for item in requested:
                name = item.get("name") if isinstance(item, dict) else None
                if name not in known:
                    raise ValueError("One or more selected locations are invalid.")
                if name in seen:
                    raise ValueError("Duplicate locations are not allowed.")
                seen.add(name)
                selected.append(known[name])

            result = solve_tsp(selected)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
        except (ValueError, json.JSONDecodeError, TypeError) as error:
            body = json.dumps({"error": str(error)}, ensure_ascii=False).encode("utf-8")
            self.send_response(400)
        except Exception:
            body = json.dumps({"error": "Unable to calculate the route. Please try again."}).encode("utf-8")
            self.send_response(500)

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "POST, OPTIONS")
        self.end_headers()
