import os
import re
import time
import shutil
import sys
import subprocess
import O4_File_Names as FNAMES
import O4_UI_Utils as UI

# the following is meant to be modified directly by users who need it (in the config window, not here!)
ovl_exclude_pol=[0]
ovl_exclude_net=[]
ovl_transparent_roads=False

# the following is meant to be modified by the CFG module at run time
custom_overlay_src=''
xplane_install_dir=''

if 'dar' in sys.platform:
    unzip_cmd    = "7z "
    dsftool_cmd  = os.path.join(FNAMES.Utils_dir,"DSFTool.app ")
elif 'win' in sys.platform:
    unzip_cmd    = os.path.join(FNAMES.Utils_dir,"7z.exe ")
    dsftool_cmd  = os.path.join(FNAMES.Utils_dir,"DSFTool.exe ")
else:
    unzip_cmd    = "7z "
    dsftool_cmd  = os.path.join(FNAMES.Utils_dir,"DSFTool ")

##############################################################################
def build_overlay(lat,lon):
    if UI.is_working: return 0
    UI.is_working=1
    timer=time.time()
    UI.logprint("Step 4 for tile lat=",lat,", lon=",lon,": starting.")
    UI.vprint(0,"\nStep 4 : Extracting overlay for tile "+FNAMES.short_latlon(lat,lon)+" : \n--------\n")
    basefile_to_sniff=FNAMES.long_latlon(lat,lon)+'.dsf'
    file_to_sniff=os.path.join(custom_overlay_src,"Earth nav data",basefile_to_sniff)
    if not os.path.exists(file_to_sniff):
        UI.lvprint(1,"   ERROR: file ",basefile_to_sniff,"not found in overlay source directory. Trying with global scenery overlay.")
        file_to_sniff=os.path.join(xplane_install_dir,"Global Scenery/X-Plane 11 Global Scenery/Earth nav data",basefile_to_sniff)
        if not os.path.exists(file_to_sniff):
            UI.exit_message_and_bottom_line("   ERROR: file ",basefile_to_sniff,"not found in global scenery. Incorrect overlay source and/or X-Plane install directories in configuration window?")
            return 0
    file_to_sniff_loc=os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'.dsf')
    UI.vprint(1,"-> Making a copy of the original overlay DSF in tmp dir")
    try:
        shutil.copy(file_to_sniff,file_to_sniff_loc)
    except:
        UI.exit_message_and_bottom_line("   ERROR: could not copy it. Disk full, write permissions, erased tmp dir ?")
        return 0
    f = open(file_to_sniff_loc,'rb')
    dsfid = f.read(2).decode('ascii')
    f.close()
    if dsfid == '7z':
        UI.vprint(1,"-> The original DSF is a 7z archive, uncompressing...")
        os.rename(file_to_sniff_loc,file_to_sniff_loc+'.7z')
        os.system(unzip_cmd+' e -o'+FNAMES.Tmp_dir+' "'+file_to_sniff_loc+'.7z"')
    UI.vprint(1,"-> Converting the copy to text format")
    dsfconvertcmd=[dsftool_cmd.strip(),' -dsf2text '.strip(),file_to_sniff_loc,os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf.txt')]
    fingers_crossed=subprocess.Popen(dsfconvertcmd,stdout=subprocess.PIPE,bufsize=0)
    while True:
        line = fingers_crossed.stdout.readline()
        if not line:
            break
        else:
            UI.vprint(1,'     '+line.decode("utf-8")[:-1])
    if fingers_crossed.returncode:
        UI.exit_message_and_bottom_line("   ERROR: DSFTool crashed.")
        return 0
    UI.vprint(1,"-> Selecting overlays for copy/paste")
    f=open(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf.txt'),'r')
    g=open(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf_without_mesh.txt'),'w')
    line=f.readline()
    g.write('PROPERTY sim/overlay 1\n')
    pol_type=0
    pol_dict={}
    exclude_set_updated=False
    full_ovl_exclude_pol=set(ovl_exclude_pol)
    while line:
        if 'PROPERTY' in line:
            g.write(line)
        elif 'POLYGON_DEF' in line:
            level=2 if 'facade' not in line else 3
            pol_dict[pol_type]=line.split()[1]
            UI.vprint(level,pol_type,":",pol_dict[pol_type])
            pol_type+=1
            g.write(line)
        elif 'NETWORK_DEF' in line:
            g.write(line)
        elif 'BEGIN_POLYGON' in line:
            if not exclude_set_updated:
                tmp=set()
                for item in full_ovl_exclude_pol:
                    if isinstance(item,int):
                        tmp.add(item)
                    elif isinstance(item,str):
                        if item and item[0]=='!':
                            item=item[1:]
                            tmp=tmp.union([k for k in pol_dict if item not in pol_dict[k]])
                        else:
                            tmp=tmp.union([k for k in pol_dict if item in pol_dict[k]])
                full_ovl_exclude_pol=tmp
                UI.vprint(2,"Excluded polygon types: ", full_ovl_exclude_pol)
                exclude_set_updated=True
            pol_type = int(line.split()[1])
            if pol_type not in full_ovl_exclude_pol:
                while line and ('END_POLYGON' not in line):
                    g.write(line)
                    line=f.readline()
                g.write(line)
            else:
                while line and ('END_POLYGON' not in line):
                    line=f.readline()
        elif 'BEGIN_SEGMENT' in line:
            road_type = int(line.split()[2])
            if road_type not in ovl_exclude_net and '' not in ovl_exclude_net and '*' not in ovl_exclude_net:
                while line and ('END_SEGMENT' not in line):
                    g.write(line)
                    line=f.readline()
                g.write(line)
            else:
                while line and ('END_SEGMENT' not in line):
                    line=f.readline()
        line=f.readline()
    f.close()
    g.close()
    UI.vprint(1,"-> Converting back the text DSF to binary format")
    dsfconvertcmd=[dsftool_cmd.strip(),' -text2dsf '.strip(),os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf_without_mesh.txt'),os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf_without_mesh.dsf')]
    fingers_crossed=subprocess.Popen(dsfconvertcmd,stdout=subprocess.PIPE,bufsize=0)
    while True:
        line = fingers_crossed.stdout.readline()
        if not line:
            break
        else:
            print('     '+line.decode("utf-8")[:-1])
    dest_dir=os.path.join(FNAMES.Overlay_dir,"Earth nav data",FNAMES.round_latlon(lat,lon))
    UI.vprint(1,"-> Coping the final overlay DSF in "+dest_dir)
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
        except:
            UI.exit_message_and_bottom_line("   ERROR: could not create destination directory "+str(dest_dir))
            return 0
    shutil.copy(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf_without_mesh.dsf'),os.path.join(dest_dir,FNAMES.short_latlon(lat,lon)+'.dsf'))
    os.remove(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf_without_mesh.dsf'))
    os.remove(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf_without_mesh.txt'))
    os.remove(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf.txt'))
    os.remove(file_to_sniff_loc)
    try:
        os.remove(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf.txt.elevation.raw'))
        os.remove(os.path.join(FNAMES.Tmp_dir,FNAMES.short_latlon(lat,lon)+'_tmp_dsf.txt.sea_level.raw'))
    except:
        pass
    if dsfid == '7z':
        os.remove(file_to_sniff_loc+'.7z')
    if ovl_transparent_roads:
        add_transparent_roads(lat, lon)
    UI.timings_and_bottom_line(timer)
    return 1
##############################################################################

##############################################################################
def del_overlay(lat,lon):
    dest_dir=os.path.join(FNAMES.Overlay_dir,"Earth nav data",FNAMES.round_latlon(lat,lon))
    if os.path.exists(dest_dir) and os.path.isdir(dest_dir):
        # Overlay File
        dest_file=os.path.join(dest_dir,FNAMES.short_latlon(lat,lon)+'.dsf')
        if os.path.exists(dest_file):
            os.remove(dest_file)
        # And directory if empty
        if not os.listdir(dest_dir):
            os.rmdir(dest_dir)
    return 1
##############################################################################

# Based on https://github.com/melb00m/Transparency4Ortho code at 143b51d
##############################################################################
def add_transparent_roads(lat, lon):
    # Check and create Library
    enabled_groups = ["GRPLocal", "GRPLocalOneWay", "GRPPrimary", "GRPPrimaryOneWay", "GRPSecondary", "GRPSecondaryOneWa", "GRPSingleLane", "GRPSingleLaneOneway", "GRP_PlugsPri", "GRP_PlugsSec", "GRP_PlugsLoc", "GRP_PlugsRural", "GRP_JuncComp_EU", "GRP_JuncPlugs_EU", "GRPCompJunctionsDrp", "GRP_TransitionBYTs", "GRP_Centers", "GRP_Corners", "GRP_Stubs", "GRP_DeadEnds", "GRP_Approaches"]
    roads_library = os.path.join(FNAMES.Overlay_dir, "Resources/1000_roads")
    if not os.path.exists(roads_library):
        UI.vprint(1,"-> Creating transparent roads library")
        shutil.copytree(os.path.join(xplane_install_dir, "Resources/default scenery/1000 roads"), roads_library)
        for ftr in ["library.lib", "library.txt"]:
            file_path=os.path.join(roads_library, ftr)
            if os.path.exists(file_path):
                os.remove(file_path)

        for ft in ["roads.net", "roads_EU.net"]:
            new_file_content=""
            uncomment_enabled_block=False
            with open(os.path.join(roads_library, ft), "r", encoding="utf-8") as input_file:
                file_content = input_file.readlines()
            for line in file_content:
                matcher = re.match(r'(#\s+Group:\s+)(\w+)', line)
                if matcher:
                    uncomment_enabled_block = matcher.group(2) in enabled_groups
                if uncomment_enabled_block:
                    line = re.sub(r'^(QUAD|TRI|SEGMENT_DRAPED)', r'#(Transparency) \1', line)
                new_file_content += line

            with open(os.path.join(roads_library, ft), "w", encoding="utf-8") as output_file:
                output_file.writelines(new_file_content)

    # Process library.txt and add tile if needed
    library_txt = os.path.join(FNAMES.Overlay_dir, "library.txt")
    library_regions = []
    UI.vprint(1,"-> Updating transparent roads library.txt for tile "+FNAMES.short_latlon(lat,lon))
    if os.path.exists(library_txt):
        with open(library_txt, "r", encoding="utf-8") as input_file:
            library_regions = [line for line in input_file if re.search(r'^REGION_RECT',line)]

    line="REGION_RECT {lon:+04d} {lat:+03d} {lon:+04d} {lat:+03d}\n".format(lat=lat,lon=lon)
    if not line in library_regions:
        library_regions.append(line)
    library_regions.sort()
    with open(library_txt, "w", encoding="utf-8") as output_file:
        output_file.write("A\n800\nLIBRARY\n\nREGION_DEFINE yOrtho4XP_Overlays\n")
        output_file.writelines(library_regions)
        output_file.write("\nREGION yOrtho4XP_Overlays\n")
        output_file.write("EXPORT_EXCLUDE lib/g10/roads.net Resources/1000_roads/roads.net\n")
        output_file.write("EXPORT_EXCLUDE lib/g10/roads_EU.net Resources/1000_roads/roads_EU.net")

##############################################################################
def del_transparent_roads(lat, lon):
    pass
##############################################################################
