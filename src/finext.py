import evds_reader
import evds_data_tour

def main():
    #tour = evds_data_tour.EvdsExplorer()
    #tour.get_main_categories()

    df = evds_reader.read_evds_data("TP.FG.J0")
    evds_reader.write_evds_Data(df, "cpi.csv")

if __name__ == '__main__':
    main()