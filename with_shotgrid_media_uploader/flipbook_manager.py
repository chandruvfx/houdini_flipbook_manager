import os
import hou
import sgtk
import subprocess
import toolutils
from pathlib import Path


def use_current_viewport_camera(flipbook_node: hou.Node) -> None:
    
    activeCam = toolutils.sceneViewer().curViewport().camera()
    flipbook_node.parm("camera").set(activeCam.path())
    

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
        
        make_mov = cur_node.parm("make_mov").eval()
        publish_mov = cur_node.parm("publish_mov").eval()
        
        start_frame =  int(cur_node.parm("f1").eval())
        end_frame =  int(cur_node.parm("f2").eval())
        steps =  int(cur_node.parm("f3").eval())
        OutputFilename_0 = "%s.####.exr" %(job_name)
                 
        deadline_files = []
        flipbook_version_py_files = []
        messages = []
        houdini_temp_dir = "Y:/pipeline/studio/temp/" + \
                            hou.userName() + "/" +\
                            "houdini_" + os.environ["HOUDINI_MINOR"]  + "/"   
                              
        
        def crete_directory(folder_path: str):
            
            dir_exist = os.path.exists(folder_path)
            if not dir_exist:
                os.makedirs(folder_path)
                
        
        def write_job_file(filename, data, job_type=''):
            
            dl_job_dir =  houdini_temp_dir + \
                          "/%s/deadline_job_files" %job_type
            crete_directory(dl_job_dir)
            
            job_file = os.path.join(dl_job_dir, filename)
                
            with open(job_file, "w") as write_file:
                for key, value in data.items():
                    write_file.write(key +"=" + value + "\n") 
            deadline_files.append(job_file)
            return job_file
       
       
        def file_job_info(job_type='', dep_job_id=''):
            
            if job_type == 'houdini':
                plugin = 'Houdini'
            elif job_type == 'draft':
                plugin = 'DraftPlugin'
            elif job_type == 'version_publish':
                plugin = 'Python'
            
            dl_job_info = {
                "BatchName": hou.hipFile.basename(),
                "Name": job_name + "_" + job_type,
                "Comment" : comment,
                "ChunkSize" : str(chunksize),
                "Plugin" :plugin,
                "Pool": pool,
                "SecondaryPool": sec_pool,
                "EnvironmentKeyValue0" : "PYTHONPATH=Y:/pipeline/apps/houdini/19.5.534/deadline"
            }
            if job_type == 'houdini':
                dl_job_info['Frames'] = "%s-%severy%s" %(str(start_frame), str(end_frame), str(steps))
                dl_job_info["OutputDirectory0"] = os.path.join(cache_folder_path , job_name)
                dl_job_info["OutputFilename0"] = OutputFilename_0
                
            elif job_type == 'draft' or \
                        job_type == 'version_publish':
                dl_job_info['JobDependency0'] = dep_job_id

            job_info_file = write_job_file("job_info_%s_%s.job" 
                                            %(cur_node.parent().name(), 
                                              cur_node.name()), 
                                            dl_job_info,
                                            job_type)
            return job_info_file
        
            
        def plugin_job_info(job_type='', exr_path='', mov_path=''):
            
            if job_type == 'houdini':
                dl_plugin_job_info = {
                    "Output": full_path,
                    "OutputDriver": "/obj/%s/ropnet1/opengl1" %cur_node.name(),
                    "SceneFile" : hou.hipFile.path(),
                    "Version" : "19.5",
                }
            elif job_type == 'draft':
                
                dl_plugin_job_info = {
                    'scriptFile': str(Path(__file__).parent.absolute()) +"/convert.py",
                    'ScriptArg0=mov': mov_path,
                    'ScriptArg1=exr': exr_path,
                    'ScriptArg2=start_frame': str(start_frame),
                    'ScriptArg3=end_frame':str(end_frame)   
                }
                
            elif job_type == 'version_publish':
                dl_plugin_job_info = {
                    'Arguments' : ' ',
                    'SingleFramesOnly': 'False',
                    'Version': '3.7'
                }
                
            plugin_info_file = write_job_file("plugin_info_%s_%s.job" 
                                                %(cur_node.parent().name(), 
                                                cur_node.name()),
                                                 dl_plugin_job_info,
                                                 job_type)
            return plugin_info_file
        
        
        def submit(auxiliary_files = None):
            
            dl_path = os.environ['DEADLINE_PATH'] 
            dl_path = dl_path.replace(r"/", "//") + "//deadlinecommand.exe"
            dl_path = '"%s"' %dl_path
            if not auxiliary_files:
                dl_command = '%s %s' %(dl_path, " ".join(deadline_files))
            else:
                dl_command = '%s %s %s' %(dl_path, 
                                          " ".join(deadline_files),
                                          " ".join(auxiliary_files))      
            result = subprocess.run(dl_command, 
                                    stdout=subprocess.PIPE, 
                                    shell=True,
                                    text=True)
            jobid = [id for id in result.stdout.split() if 'JobID' in id]
            return jobid[0]
        
        
        file_job_info(job_type='houdini')
        plugin_job_info(job_type='houdini')
        job_id = submit()
        messages.append(f"Deadline Flipbook {job_id} Submitted")
        
        if make_mov:
            deadline_files[:] = []
            mov_path = cache_folder_path + "/" + cache_name + "/" + cache_name + ".mov"
            
            file_job_info(job_type='draft', dep_job_id=job_id.split('=')[-1])
            plugin_job_info(job_type='draft', 
                            exr_path=full_path, 
                            mov_path=mov_path)
            draft_job_id = submit()
            messages.append(f"Deadline Draft {draft_job_id} Submitted")
            
            if publish_mov:
            # Job submission script for Version publish inside Shotgrid
                engine = sgtk.platform.current_engine()
                shot = engine.context.entity
                shot_id = shot['id']
                seq = engine.shotgun.find("Shot", 
                                        [['id', 'is', shot_id ]],
                                        ['sg_sequence'])[0]['sg_sequence']['name']
                task = engine.context.task
                project = engine.context.project
                user = engine.context.user
                exr_path = full_path.split("$F4")
                exr_path = exr_path[0] + '####.exr'
                publish_script = """ 
import shotgun_api3
shotgun_api3.shotgun.NO_SSL_VALIDATION= True
sg = shotgun_api3.Shotgun("https://future-associate.shotgunstudio.com",
                        script_name="deadline_integration5",
                        api_key="wjtuuZdl4gqivbndwiqecow$f",
                        http_proxy="proxy01.future.associate:3128")
data = { 'project': %s,
        'code': '%s',
        'description': r'%s',
        'sg_path_to_frames': r'%s',
        'sg_path_to_movie': r'%s',
        'sg_status_list': 'rev',
        'entity': %s,
        'sg_task': %s,
        'user': %s }
version_id = sg.create("Version", data) 
sg.upload("Version", version_id['id'], r'%s', field_name="sg_uploaded_movie")                        
                """%(project, 
                    cache_name, 
                    comment, 
                    exr_path.replace("/", "\\"), 
                    mov_path.replace("/", "\\"),
                    shot, 
                    task,
                    user,
                    mov_path.replace("/", "\\"),
                    )

                flipbook_version_py_dir =   houdini_temp_dir + \
                                            "flipbook/" + project['name'] + "/" + \
                                            seq + "/" + shot['name'] 
                crete_directory(flipbook_version_py_dir) 
                flipbook_version_py_file =  os.path.join(flipbook_version_py_dir, cache_name + ".py")
                with open(flipbook_version_py_file, "w") as flipbook_file:
                    flipbook_file.write(publish_script)
            
                deadline_files[:] = []
                
                file_job_info(job_type='version_publish', dep_job_id=draft_job_id.split('=')[-1])
                plugin_job_info(job_type='version_publish', 
                                exr_path=full_path, 
                                mov_path=mov_path)
                
                flipbook_version_py_files.append(flipbook_version_py_file)
                version_publish_job_id = submit(flipbook_version_py_files)
                messages.append(f"Publish Version Job {version_publish_job_id} Submitted")
                
                                       
        hou.ui.displayMessage("\n".join(messages),                      
                              buttons=('OK',), 
                              severity=hou.severityType.Message,
                              title="FAE_Message")