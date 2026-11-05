"""Drive-time routing. The provider can be swapped; callers never see a vendor URL or token.

Results are minutes only. This module does not write coordinates anywhere.
"""
import json
import urllib.error
import urllib.parse
import urllib.request
import datetime as dt
import math

TRAFFIC_WINDOW = dt.timedelta(hours=3)
CACHE_FOR = dt.timedelta(minutes=15)


class AuthError(Exception):
    """The provider rejected the credential. Callers should stop using it."""


class RouteError(Exception):
    """A route could not be fetched. The message is a status, never a URL."""


class Route:
    def __init__(self, minutes, traffic=False, estimated=False):
        self.minutes = max(1, int(minutes))
        self.traffic = bool(traffic) and not estimated
        self.estimated = bool(estimated)


def haversine_km(origin, dest):
    lat1, lng1 = math.radians(origin[0]), math.radians(origin[1])
    lat2, lng2 = math.radians(dest[0]), math.radians(dest[1])
    dlat, dlng = lat2 - lat1, lng2 - lng1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * 6371 * math.asin(min(1, math.sqrt(h)))


def estimate_minutes(origin, dest):
    """Straight-line distance, stretched for roads, at a city pace. Not live traffic."""
    km = haversine_km(origin, dest) * 1.3
    return max(1, int(round(km / 40 * 60)))


def wants_traffic(arrive_at, now):
    """Live traffic only when the event starts within the next three hours."""
    if arrive_at is None or now is None:
        return False
    delta = arrive_at - now
    return dt.timedelta(0) <= delta <= TRAFFIC_WINDOW


class MapboxProvider:
    """Mapbox Directions. The token stays on this object and is never put in errors."""

    def __init__(self, token, opener=None):
        self.token = token
        self.opener = opener or urllib.request.urlopen

    def _directions(self, origin, dest, profile, geometry):
        olng, olat = origin[1], origin[0]
        dlng, dlat = dest[1], dest[0]
        coords = "%s,%s;%s,%s" % (olng, olat, dlng, dlat)
        query = urllib.parse.urlencode({
            "access_token": self.token,
            "overview": "simplified" if geometry else "false",
            "geometries": "geojson",
            "alternatives": "false",
        })
        url = "https://api.mapbox.com/directions/v5/mapbox/%s/%s?%s" % (profile, coords, query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        try:
            with self.opener(req, timeout=4) as resp:
                data = json.loads(resp.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            code = getattr(e, "code", 0) or 0
            try:
                e.close()
            except Exception:
                pass
            if code == 401:
                raise AuthError()
            raise RouteError(str(code))
        except AuthError:
            raise
        except Exception:
            raise RouteError("unavailable")
        routes = data.get("routes") or []
        if not routes or routes[0].get("duration") is None:
            return None
        minutes = max(1, int(round(float(routes[0]["duration"]) / 60)))
        if not geometry:
            return minutes
        coords = ((routes[0].get("geometry") or {}).get("coordinates") or [])
        points = [[round(float(pair[1]), 5), round(float(pair[0]), 5)] for pair in coords if isinstance(pair, (list, tuple)) and len(pair) >= 2]
        return minutes, points

    def route(self, origin, dest, profile):
        return self._directions(origin, dest, profile, False)

    def route_line(self, origin, dest):
        """Plain driving geometry. No traffic and no turn-by-turn steps."""
        return self._directions(origin, dest, "driving", True)


class RoutingService:
    """Pick a profile, honor the daily cap and a short cache, and fall back to an estimate."""

    def __init__(self, provider, cap):
        self.provider = provider
        self.cap = cap
        self.auth_failed = False
        self.cache = {}

    def drive(self, origin, dest, now):
        """Live traffic. The caller only invokes this inside the home drive window."""
        return self._fetch(origin, dest, "driving-traffic", True, now)

    def line(self, origin, dest, now):
        """One plain-driving road line. None when the provider cannot be called."""
        if self.provider is None or self.auth_failed or not hasattr(self.provider, "route_line"):
            return None
        if self.cap is not None and not self.cap.try_take(now):
            return None
        try:
            return self.provider.route_line(origin, dest)
        except AuthError:
            self.auth_failed = True
            return None
        except RouteError:
            return None

    def _fetch(self, origin, dest, profile, traffic, now):
        if self.provider is None or self.auth_failed:
            return Route(estimate_minutes(origin, dest), estimated=True)
        if self.cap is not None and not self.cap.try_take(now):
            return Route(estimate_minutes(origin, dest), estimated=True)
        try:
            minutes = self.provider.route(origin, dest, profile)
        except AuthError:
            self.auth_failed = True
            return Route(estimate_minutes(origin, dest), estimated=True)
        except RouteError:
            return Route(estimate_minutes(origin, dest), estimated=True)
        if minutes is None:
            return Route(estimate_minutes(origin, dest), estimated=True)
        return Route(minutes, traffic=traffic, estimated=False)
