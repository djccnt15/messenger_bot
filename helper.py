from src.common.utils import LogEnum, logger
from src.config import RESOURCES
from src.db import database
from src.domain import user_process
from src.security import key

WELCOME_MSG = """Hello World!

1. print DB URL
2. create RSA Key for encrypt
3. create user info to DB from csv file
4. decrypt first user info from db
"""
BASE_INPUT_MSG = "select function you want to activate(enter nothing to quit): "
FILENAME_INPUT_MSG = "input user file list(default: user_list.csv): "
MESSENGER_COL_NAME = "input messenger column name of your source(default: messenger): "


def main():
    logger.info(LogEnum.START)
    while True:
        print(WELCOME_MSG)

        user_input = input(BASE_INPUT_MSG)
        logger.info(LogEnum.USER_INPUT % user_input)

        if not user_input:
            logger.info(LogEnum.FINISH)
            break
        elif user_input == "1":
            try:
                print(database.SQLALCHEMY_DATABASE_URL)
            except Exception as e:
                logger.exception(e)
            print()
        elif user_input == "2":
            try:
                key.create_keys_rsa(
                    private_key=RESOURCES / "private.pem",
                    public_key=RESOURCES / "public.pem",
                )
            except Exception as e:
                logger.exception(e)
            print()
        elif user_input == "3":
            try:
                filename_input = input(FILENAME_INPUT_MSG)
                filename = filename_input if filename_input else "user_list.csv"
                messenger_col_name = input(MESSENGER_COL_NAME)
                messenger_col_name = (
                    messenger_col_name if messenger_col_name else "messenger"
                )
                user_process.create_user(file=filename, col=messenger_col_name)
            except Exception as e:
                logger.exception(e)
            print()
        elif user_input == "4":
            try:
                first_user = user_process.read_first_user()
                logger.info(f"stdout: {first_user}")
                print(first_user)
            except Exception as e:
                logger.exception(e)
            print()


if __name__ == "__main__":
    main()
