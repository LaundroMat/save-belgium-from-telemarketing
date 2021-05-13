import requests
from loguru import logger

from core import UserRecord, create_account, fake, generate_phone_numbers

if __name__ == '__main__':
    print("Which area codes do you want to cover?")
    area_codes = [ac.strip() for ac in input("E.g. 050 or 02,03,0474 [leave empty to do all area_codes]: ").split(',') if ac.strip()]

    range_start = int(input("Start at [leave empty to start at 0]: ") or 0)
    range_end = int(input("End at [leave empty to end at highest possible]: ") or 0)

    really_do_this = input("Do you really want to do this? [y/N] ").casefold() == "y"

    user_record = create_account() if really_do_this else UserRecord(id=fake.md5(), auth_token=fake.md5(), email=fake.email())

    for phone_number in generate_phone_numbers(area_codes, range_start, range_end):
        data = {
            "name": f"{fake.first_name()} {fake.last_name()}",
            "number": f"+32 {phone_number}",
            "user": user_record.id
        }

        if really_do_this:
            response = requests.post(
                "https://www.dncm.be/wp-json/app/v1/number",
                headers={
                    "Authorization": f"Bearer {user_record.auth_token}"
                },
                json=data
            )

            assert response.status_code == requests.codes.created

        log_msg = f"Added +32 {phone_number}" if really_do_this else f"Would have added +32 {phone_number}"
        logger.info(log_msg)
