import os
import hou
import subprocess
import shutil

def fae_warning(msg: str) -> None:
    
    hou.ui.displayMessage( 
                            msg,
                            buttons=( "Ok", ), 
                            title="FAE Warning" )


def fill_flipbook_player_parms(cur_node: hou.Node) -> None:
    
    if not cur_node.parm("folder_path").eval():
        
        fae_warning("Please Fill the Folder Path")
    
    else:
         
        exr_root_folder_path = cur_node.parm("folder_path").eval()
        exr_folder_paths= []
        for root, _ , files in os.walk(exr_root_folder_path):
            for file in files:
                if file.endswith(".exr"):
                    exr_folder_paths.append(root)
                    break
        
        cur_node.parm("seq_paths_0").set(
                    len(exr_folder_paths)
        )
        for num, exr_folder_path in enumerate(exr_folder_paths):
            cur_node.parm(f"enable_{num+1}").set(True)
            cur_node.parm(f"flipbook_path_{num+1}").set(exr_folder_path)
            
def play(cur_node: hou.Node) -> None:
    
    rv = r"C:\Program Files\ShotGrid\RV-2022.2.0\bin\rv.exe"
    rv_exe = f'"{rv}"'        
    
    flip_book_paths = []
    rv_exists = lambda: shutil.which(rv) is not None
    flip_path_count = cur_node.parm("seq_paths_0").eval()
    
    if not rv_exists:
        fae_warning("RV Not configured or NOt installed Contact Production")
    elif not flip_path_count:
        fae_warning("No Flip book Folder paths Added")
    else:
        
        parm_dict = {}
        param_instances = cur_node.parm("seq_paths_0").multiParmInstances()

        parm_lbl_index = 0
        while  parm_lbl_index < len(param_instances):
            parm_dict[param_instances[parm_lbl_index]] = \
                param_instances[parm_lbl_index+1]
            parm_lbl_index = parm_lbl_index + 2    


        for key, value in parm_dict.items():
            if key.eval():
                flip_book_paths.append(value.eval())
        
        rv_string = "%s -sRGB %s" %(rv_exe,
                              " ".join(flip_book_paths))
        subprocess.Popen(rv_string)
        
        
        