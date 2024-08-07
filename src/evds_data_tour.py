import os
from evds import evdsAPI

class EvdsExplorer:
    def __init__(self, config):
        self.evds = evdsAPI(os.environ.get("EVDS_API"))
        self.config = config

    def read_export_evds_data(self, series_code, series_name, start_date:str="01-01-2020", end_date:str="01-10-3024"):
        os.makedirs("../data_exports", exist_ok=True)
        data = self.evds.get_data([series_code], start_date, end_date)
        data.to_csv(f"../data_exports/{series_name}__{start_date}__{end_date}.csv", index=False, sep=";")
        
    def get_main_categories(self):
        mcdf = self.evds.main_categories
        mcdf = mcdf.sort_values("CATEGORY_ID")
        message = "Input an ID to look into a category ( e:exit )\n"
        print("### TCMB EVDS MAIN CATEGORIES ###")
        for row in mcdf.iterrows():
            print(f"MCID: {row[1].CATEGORY_ID} NAME: {row[1].TOPIC_TITLE_TR}")

        while True:
            next = input(message)
            try: next = int(next)
            except: pass

            if next == "e":
                return 0
            elif next in mcdf.CATEGORY_ID.values:
                mc_name = mcdf[mcdf.CATEGORY_ID == next].TOPIC_TITLE_TR.values[0]
                self.get_sub_categories(next, mc_name)
            else:
                print(f"Invalid input! ({next})")
                print(mcdf.CATEGORY_ID.values)

    def get_sub_categories(self, mcid, mc_name):
        scdf = self.evds.get_sub_categories(mcid)
        message = "Input an ID to look into a sub-category (b: back - e:exit )\n"
        print(f"\n\n### TCMB EVDS SUB CATEGORIES OF {mc_name}###")
        for i, row in enumerate(scdf.iterrows()):
            print(f"SCID: {i} NAME: {row[1].DATAGROUP_NAME}")
        while True:
            next = input(message)
            try:
                next = int(next)
            except:
                pass
            if next == "e":
                return 0
            elif next == "b":
                self.get_main_categories()
            elif next in scdf.CATEGORY_ID:
                group_code = scdf.loc[next, "DATAGROUP_CODE"]
                group_name = scdf.loc[next, "DATAGROUP_NAME"]
                self.get_series(group_code, group_name, mcid, mc_name)
            else:
                print("Invalid input!")

    def get_series(self, group_code, group_name, mc_id, mc_name):
        sdf = self.evds.get_series(group_code)
        message = "Pick an ID from the list to export the file (b: back - e:exit )\n"
        print(f"\n\n### TCMB EVDS SERIES OF {group_name}###")
        sdf_row_count = sdf.shape[0]
        for i, row in enumerate(sdf.iterrows()):
            print(f"ID:{i} --- SERIE CODE : {row[1].SERIE_CODE} --- NAME: {row[1].SERIE_NAME} --- START DATE: {row[1].START_DATE}")
        
        while True:
            next = input(message)
            try:
                next = int(next)
                if (next >= sdf_row_count) or (next < 0):
                    print("Please enter a valid id!")
                else:
                    self.read_export_evds_data(sdf.iloc[next].SERIE_CODE, sdf.iloc[next].SERIE_NAME,
                                               self.config["start_date"], self.config["end_date"])
                    continue

            except:
                print("Error")
                pass
    
            if next == "e":
                return 0
            elif next == "b":
                self.get_sub_categories(mc_id, mc_name)
            else:
                print("Please enter a valid response!")
