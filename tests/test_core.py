import core


def test_generate_numbers():
    assert (list(core.generate_phone_numbers(selected_area_codes=["02"], range_start=0, range_end=1))) == ["+3220000000", "+3220000001"]
    assert (list(core.generate_phone_numbers(selected_area_codes=["050"], range_start=0, range_end=1))) == ["+3250000000", "+3250000001"]
    assert (list(core.generate_phone_numbers(selected_area_codes=["0475"], range_start=0, range_end=1))) == ["+32475000000", "+32475000001"]

