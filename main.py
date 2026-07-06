from _1_Create_tables import main as create_tables
from _2_Filling_data import main as filling_data
from _3_Prepare import main as prepare
from _4_Processing import main as processing

def main():
    create_tables()
    filling_data()
    prepare()
    processing()


if __name__ == "__main__":
    main()