from src.logics import *
from src.loadenvs import get_env_data, sys



def start_preplybot():
    try:
        client = get_env_data()
        chatlogs_dir()
        wait(2)
        main_loop(client)

    except KeyboardInterrupt:
        logger.error("skript was stopped")
        sys.exit(1)
    except Exception as e:
        logger.error(f"uknown error: {e}", exc_info=True)
        sys.exit(1)




# ================== RUN SOLO ==================
'''this part is for starting bot without telegram'''
if __name__ == '__main__':
    try:
        client = get_env_data()
        chatlogs_dir()
        wait(1)
        print("\n")
        print("=" * 60)
        print("Preply Teacher Bot")
        print("=" * 60)
        print("\nscript sucessfully started!")
        print("you have 20 seconds to go into your preply inbox")
        print("at that point the script runs automatically.\n")
        print("=" * 60)

        wait(1)
        logger.info("script has been started...")
        wait(20)
        main_loop(client)

    except KeyboardInterrupt:
        logger.error("script has been stopped")
        sys.exit(1)
    except Exception as e:
        logger.error(f"uknown error: {e}", exc_info=True)
        sys.exit(1)



