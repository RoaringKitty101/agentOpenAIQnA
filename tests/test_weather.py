from get_weather.weather import get_weather


def test_empty_location():
    assert get_weather.invoke({"location": "  "}) == "Please provide a location name."
