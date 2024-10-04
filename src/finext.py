import json
import evds_reader
import evds_data_tour


def main():
    with open('config.json', 'r') as file:
        config = json.load(file)

    while True:
        mode = input("Choose mode (Data Tour: t | Export Data: e): ")
        if mode == "t":
            tour = evds_data_tour.EvdsExplorer(config)
            tour.get_main_categories()
            break
        elif mode == "e":
            df = evds_reader.read_evds_data("TP.FG.J0")
            evds_reader.write_evds_data(df, "cpi.csv")
            break
        else:
            print("Please choose a valid mode")


if __name__ == '__main__':
    main()
