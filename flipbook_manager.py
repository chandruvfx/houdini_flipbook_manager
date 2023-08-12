import os
import hou
import subprocess

def camera_eval_info(flipbook_node: hou.Node) -> None:
    
    if flipbook_node.parm("camera").eval():
        camera_entry = flipbook_node.parm("camera").eval()
        camera = hou.node(camera_entry)
        near_clip = camera.parm('near').eval()
        if near_clip > 0.001:
            hou.ui.displayMessage( 
                            "Near clip for the given camera is %s.\n Hud Text might not appear.\nPlease set near clip value for selected camera to 0.001" %near_clip,
                            buttons=( "Ok", ), 
                            title="FAE Warning" )
            
            
            
def submit_to_deadline(cur_node: hou.Node) -> None:

    hou.hipFile.save()
    
    cache_folder_path = cur_node.parm("folder_path").evalAsString().replace(os.sep, "/")
    cache_name = cur_node.parm("flip_book_name").evalAsString()
    pool = cur_node.parm("dl_pool").evalAsString()
    full_path = cache_folder_path + "/" + cache_name + "/" + cache_name + ".$F4.exr"
    
    if not cache_folder_path \
                or not cache_name \
                or not pool \
                or not cur_node.parm("camera").eval():
                
        hou.ui.displayMessage( 
        "Please Fill All Neccessary fields. Folder Path, Camera, Pool and Cache Name", 
                            buttons=( "Ok", ), 
                            title="FAE message" ) 
    else:
        job_name = cache_name
        comment = cur_node.parm("dl_comment").evalAsString()
        sec_pool = cur_node.parm("dl_secondary_pool").evalAsString()
        group = cur_node.parm("dl_group").evalAsString()
        priority = cur_node.parm("dl_priority").eval()
        chunksize = cur_node.parm("dl_chunk_size").eval()
        
        start_frame =  int(cur_node.parm("f1").eval())
        end_frame =  int(cur_node.parm("f2").eval())
        steps =  int(cur_node.parm("f3").eval())
        OutputFilename_0 = "%s.####.jpg" %(job_name)
                 
        deadline_files = []    
        
        def write_job_file(filename, data):
            
            dl_job_dir =  "Y:/pipeline/studio/temp/" + \
                          hou.userName() + \
                          "/houdini/deadline_job_files"
            dir_exist = os.path.exists(dl_job_dir)
            if not dir_exist:
                os.makedirs(dl_job_dir)
            
            job_file = os.path.join(dl_job_dir, filename)
                
            with open(job_file, "w") as write_file:
                for key, value in data.items():
                    write_file.write(key +"=" + value + "\n") 
            deadline_files.append(job_file)
            return job_file
       
        def file_job_info():
        
            dl_job_info = {
                "BatchName": hou.hipFile.basename(),
                "Name": job_name,
                "Comment" : comment,
                "ChunkSize" : str(chunksize),
                "Frames" : "%s-%severy%s" %(str(start_frame), str(end_frame), str(steps)),
                "Plugin" :"Houdini",
                "Pool": pool,
                "OutputDirectory0": cache_folder_path + "/" + job_name,
                "OutputFilename0" : OutputFilename_0,
                "EnvironmentKeyValue0" : "PYTHONPATH=Y:/pipeline/apps/houdini/19.5.534/deadline"
            }
            job_info_file = write_job_file("job_info_%s_%s.job" 
                                            %(cur_node.parent().name(), cur_node.name()), dl_job_info)
            return job_info_file
            
        def plugin_job_info():
        
            dl_plugin_job_info = {
                "Output": full_path,
                "OutputDriver": "/obj/%s/ropnet1/opengl1" %cur_node.name(),
                "SceneFile" : hou.hipFile.path(),
                "Version" : "19.5",
            }
            plugin_info_file = write_job_file("plugin_info_%s_%s.job" 
                                                %(cur_node.parent().name(), cur_node.name()), dl_plugin_job_info)
            return plugin_info_file
        
          
        file_job_info()
        plugin_job_info()
        
        dl_path = os.environ['DEADLINE_PATH'] 
        dl_path = dl_path.replace(r"/", "//") + "//deadlinecommand.exe"
        dl_path = '"%s"' %dl_path
        dl_command = '%s %s' %(dl_path, " ".join(deadline_files))
        result = subprocess.run(dl_command, 
                                stdout=subprocess.PIPE, 
                                shell=True,
                                text=True)
        job_id = [id for id in result.stdout.split() if 'JobID' in id]
        
        
        hou.ui.displayMessage("Deadline \n\n%s\n\n Submitted" %job_id[0],
                              buttons=('OK',), 
                              severity=hou.severityType.Message,
                              title="FAE_Message")