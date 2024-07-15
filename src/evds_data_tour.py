import os
from evds import evdsAPI

class EvdsExplorer:
    def __init__(self):
        self.evds = evdsAPI(os.environ.get("EVDS_API"))

    def get_main_categories(self):
        mcdf = self.evds.main_categories
        mcdf = mcdf.sort_values("CATEGORY_ID")
        message = "Input an ID to look into a category ( e:exit)\n"
        print("### TCMB EVDS MAIN CATEGORIES ###")
        for row in mcdf.iterrows():
            print(f"MCID: {row[1].CATEGORY_ID} NAME: {row[1].TOPIC_TITLE_TR}")

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
        message = "Input an ID to look into a sub-category (b: back - e:exit)\n"
        print(f"### TCMB EVDS SUB CATEGORIES OF {mc_name}###")
        for i, row in enumerate(scdf.iterrows()):
            print(f"SCID: {i} NAME: {row[1].DATAGROUP_NAME}")
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
        message = "(b: back - e:exit)\n"
        print(f"### TCMB EVDS SERIES OF {group_name}###")
        for i, row in enumerate(sdf.iterrows()):
            print(f"SERIE CODE : {row[1].SERIE_CODE} --- NAME: {row[1].SERIE_NAME} --- START DATE: {row[1].START_DATE}")

        next = input(message)
        try:
            next = int(next)
        except:
            pass

        if next == "e":
            return 0
        elif next == "b":
            self.get_sub_categories(mc_id, mc_name)