import sys
import glob
import pandas as pd

# VidaExport.py tlc_filepath rv_filepath output_filepath

class VidaExport:
    def __init__(self, tlc_filepath, rv_filepath, output_filepath):
        
        self.name = tlc_filepath.split("\\")[-1].split("_")[0] + '_' + rv_filepath.split("\\")[-1].split("_")[-1]
        self.tlc_filepath = tlc_filepath
        self.rv_filepath = rv_filepath
        self.output_filepath = output_filepath

        self.tlc_reports_path = self.tlc_filepath + "\\reports\\"
        self.rv_reports_path = self.rv_filepath + "\\reports\\"

        self.ouput = []
        self.ouput.append([self.name, ''])
        self.ouput.append(["Variable", "Value"])

        self.tlc_data = []
        self.rv_data = []

    def retrieve_TLC_variables(self):
        
        # TVV
        vessel_path = glob.glob(self.tlc_reports_path + "*vida-vessels.csv")
        vessel_data = pd.read_csv(vessel_path[0])

        vessel_locations = vessel_data['location']
        vessel_cc = vessel_data['total.vessel.volume.cc']

        # TPVV
        # na

        # MLD
        histo_path = glob.glob(self.tlc_reports_path + "*vida-histo.csv")
        histo_data = pd.read_csv(histo_path[0])

        mld_locations = histo_data['location']
        mld_mean = histo_data['mean']
        # Tissue Vol
        tv_locations = histo_data['location']
        tv_data = histo_data['tissue-volume-cm3']

        # LAA950
        laa = histo_data['percent-below_-950']

        # Lumen Area
        airmeas_path = glob.glob(self.tlc_reports_path + "*vida-airmeas.csv")
        airmeas_data = pd.read_csv(airmeas_path[0])

        # kind of funky data might have to come back
        lumen_locations = airmeas_data['anatomicalName']
        lumen_areas = airmeas_data['avgInnerArea']

        # Wall Thickness
        wall_locations = airmeas_data['anatomicalName']
        wall_thicknesses = airmeas_data['avgAvgWallThickness']

        # add TLC values to output
        self.add_to_csv(vessel_locations, vessel_cc, "TLC_Vessel_CC")
        self.add_to_csv(lumen_locations, lumen_areas, "TLC_Lumen_Area")
        self.add_to_csv(wall_locations, wall_thicknesses, "TLC_Wall_Thickness")
        self.add_to_csv(mld_locations, mld_mean, "TLC_MLD")
        self.add_to_csv(tv_locations, tv_data, "TLC_Tissue_Volume")
        self.add_to_csv(vessel_locations, laa, "TLC_LAA950")

    def retrieve_RV_variables(self):
        
        # MLD
        histo_path = glob.glob(self.tlc_reports_path + "*vida-histo.csv")
        histo_data = pd.read_csv(histo_path[0])

        mld_locations = histo_data['location']
        mld_mean = histo_data['mean']
       
        # Tissue Vol
        tv_locations = histo_data['location']
        tv_data = histo_data['tissue-volume-cm3']

        # LA856
        la_locations = histo_data['location']
        la_data = histo_data['percent-below_-856']

        # Lumen Area
        airmeas_path = glob.glob(self.tlc_reports_path + "*vida-airmeas.csv")
        airmeas_data = pd.read_csv(airmeas_path[0])

        # kind of funky data might have to come back
        lumen_locations = airmeas_data['anatomicalName']
        lumen_areas = airmeas_data['avgInnerArea']

        # Wall Thickness
        wall_locations = airmeas_data['anatomicalName']
        wall_thicknesses = airmeas_data['avgAvgWallThickness']

        # DPM_GasT
        registration_path = self.rv_filepath + "\\registration\\"

        dis_map_path = glob.glob(registration_path + "**\\*disease_map_summary.csv", recursive=True)
        gasT_data = pd.read_csv(dis_map_path[0])

        gasT_locations = gasT_data['location']
        gasT_vals = gasT_data['DPM_AirTrap(%)']

        # DPM_EMP
        emp_vals = gasT_data['DPM_Emphysema(%)']

        self.add_to_csv(mld_locations, mld_mean, "RV_MLD")
        self.add_to_csv(tv_locations, tv_data, "RV_Tissue_Volume")
        self.add_to_csv(la_locations, la_data, "RV_LA856")
        self.add_to_csv(lumen_locations, lumen_areas, "RV_Lumen_Area")
        self.add_to_csv(wall_locations, wall_thicknesses, "RV_Wall_Thickness")
        self.add_to_csv(gasT_locations, gasT_vals, "RV_DPM_GasT")
        self.add_to_csv(gasT_locations, emp_vals, "RV_DPM_EMP")

    def add_to_csv(self, locations, data, name):
        for idx, loc in enumerate(locations):
            self.ouput.append([name + "_" + loc , data[idx]])

def main():
    
    if len(sys.argv) != 4:
        print("Usage: python VidaExport.py TLC_filepath RV_filepath output_filepath")
        return
    else:

        vidaExport = VidaExport(sys.argv[1], sys.argv[2], sys.argv[3])
        vidaExport.retrieve_TLC_variables()
        vidaExport.retrieve_RV_variables()

        df = pd.DataFrame(vidaExport.ouput, columns=vidaExport.ouput[0])
        df = df.transpose()
        df.to_csv(vidaExport.output_filepath, index=False)

if __name__ == '__main__':
    main()