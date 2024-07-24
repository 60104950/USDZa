import zipfile
from os import listdir, rename, mkdir
from pxr import Usd, UsdUtils, Sdf

#unzip the usdz file
def unnzipUSDZFile(modelName):
    #store the file as variable

    path = f"./models/{modelName}"
    try:
        zf = zipfile.ZipFile(f"{path}/{modelName}.usdz")
    except FileNotFoundError:
        print("file USDZ not found")
        return False
    #extract the usdz file
    zf.extractall(path)



def convert_usd_file(modelName):
    #look for the usdc file 
    path = f'./models/{modelName}'
    dir_list = listdir(path)# get a list of what inside the dir
    for i in range(1, len(dir_list)):#loop on the list
        #check if its a file or folder if its a file takes the one that has extension of usdc
        fileSplited = dir_list[i].split(".")
        if  fileSplited[1] == "usdc":
            usdcFile = dir_list[i]
            break
        #if it finds that UDSA already exits then it will rename the folder and skip the converstion from USDC to USDA
        elif fileSplited[1] == "usda":
            try:
                rename(f"{path}/{dir_list[i]}", f"{path}/convertedMesh.usda")
            except FileExistsError:
                print("File already exits")
            return
    
    # Open the input USDC(binary format) file
    stage = Usd.Stage.Open(f"./models/{modelName}/{usdcFile}")

    # Save the stage in the USDA(text format)
    stage.GetRootLayer().Export(f"./models/{modelName}/convertedMesh.usda")


def convert_usd_to_usdz(modelName):
    #open the USDA file
    input_path = f"./models/{modelName}/convertedMesh.usda"
    stage = Usd.Stage.Open(input_path)
    if not stage:
        raise RuntimeError(f"Failed to open USD file at {input_path}")
    

    # Create a new SdfAssetPath for the input file
    asset_path = Sdf.AssetPath(input_path)

    #zip the usda with 0(texture folder) to USDZ
    output_path = f"./models/{modelName}/converted{modelName.capitalize()}.usdz"
    result = UsdUtils.CreateNewUsdzPackage(asset_path, output_path)
    if not result:
        raise RuntimeError(f"Failed to create USDZ package at {output_path}")
    print(f"Successfully converted {input_path} to {output_path}")




def main(modelName):
    if unnzipUSDZFile(modelName) is not False:
        convert_usd_file(modelName)
        convert_usd_to_usdz(modelName)

main("chips")


