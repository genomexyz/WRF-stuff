#!/bin/bash

#########
#setting#
#########
WRFworkdir="/home/genomexyz/WRF/Build_WRF/"
WPS="WPS/"
WPSdomain="palu/"
WRFARWrun="WRFV3/run/"
#time adjustment
timemode2="_12:00:00"
timemode1="_00:00:00"
tahun=2016
startmonth=1
startday=1
endmonth=1
endday=1

#running geogrid.exe

#echo $WRFworkdir$WPS$WPSdomain

for ((i=$(($startmonth)); i<=$endmonth; i++)); do
	if (( $i == $endmonth )); then
		let endday=$endday
	else
		let endday=30
	fi
	for ((j=$(($startday)); j<=$endday; j++)); do
		for ((k=0; k<2; k++)); do
#numbering purpose
			if (( $i < 10 )); then
				bulan=0$i
			else
				bulan=$i
			fi
			if (( $j < 10 )); then
				hari=0$j
			else
				hari=$j
			fi
			if (( $k == 0 )); then
				gfsdata="_0000_"
				dayinput=$j
				dayinputend=$j
				hourinput=0
				hourinputend=12
				jam=$timemode1
				jam2=$timemode2
				if (( $j < 10 )); then
					hari2=0$j
				else
					hari2=$j
				fi
			else
				gfsdata="_1200_"
				dayinput=$j
				dayinputend=$(($j+1))
				hourinput=12
				hourinputend=0
				jam=$timemode2
				jam2=$timemode1
				if (( $j < 10 )); then
					hari2=0$(($j+1))
				else
					hari2=$(($j+1))
				fi
			fi
			echo $hari
			echo bulan $bulan $jam $jam2 $hari2
			cat > namelist.wps << EOF
&share
 wrf_core = 'ARW',
 max_dom = 3,
 start_date = '$tahun-$bulan-$hari$jam', '$tahun-$bulan-$hari$jam', '$tahun-$bulan-$hari$jam', 
 end_date   = '$tahun-$bulan-$hari2$jam2', '$tahun-$bulan-$hari2$jam2', '$tahun-$bulan-$hari2$jam2', 
 interval_seconds = 10800,
 io_form_geogrid = 2,
 opt_output_from_geogrid_path = '/home/genomexyz/WRF/Build_WRF/WPS/palu/',
 debug_level = 0,
/

&geogrid
 parent_id         = 1,1,2,
 parent_grid_ratio = 1,3,3,
 i_parent_start    = 1,6,7,
 j_parent_start    = 1,8,6,
 e_we          = 20,25,40,
 e_sn          = 20,22,34,
 geog_data_res = '5m','5m','5m',
 dx = 30000,
 dy = 30000,
 map_proj =  'mercator',
 ref_lat   = -1.369,
 ref_lon   = 120.059,
 truelat1  = -1.369,
 truelat2  = 0,
 stand_lon = 120.059,
 geog_data_path = '/home/genomexyz/WRF/Build_WRF/WPS_GEOG',
 opt_geogrid_tbl_path = '/home/genomexyz/WRF/Build_WRF/WPS/palu/',
 ref_x = 10.0,
 ref_y = 10.0,
/

&ungrib
 out_format = 'WPS',
 prefix = 'FILE',
/

&metgrid
 fg_name = 'FILE',
 io_form_metgrid = 2,
 opt_output_from_metgrid_path = '/home/genomexyz/WRF/Build_WRF/WPS/palu/',
 opt_metgrid_tbl_path = '/home/genomexyz/WRF/Build_WRF/WPS/palu/',
/

&mod_levs
 press_pa = 201300 , 200100 , 100000 ,
             95000 ,  90000 ,
             85000 ,  80000 ,
             75000 ,  70000 ,
             65000 ,  60000 ,
             55000 ,  50000 ,
             45000 ,  40000 ,
             35000 ,  30000 ,
             25000 ,  20000 ,
             15000 ,  10000 ,
              5000 ,   1000
 /


&domain_wizard
 grib_data_path = '/home/genomexyz/WRF/Build_WRF/DATA/XXX',
 grib_vtable = 'Vtable.GFS',
 dwiz_name    =palu
 dwiz_desc    =
 dwiz_user_rect_x1 =1659
 dwiz_user_rect_y1 =482
 dwiz_user_rect_x2 =1718
 dwiz_user_rect_y2 =546
 dwiz_show_political =true
 dwiz_center_over_gmt =true
 dwiz_latlon_space_in_deg =10
 dwiz_latlon_linecolor =-8355712
 dwiz_map_scale_pct =12.5
 dwiz_map_vert_scrollbar_pos =0
 dwiz_map_horiz_scrollbar_pos =0
 dwiz_gridpt_dist_km =30.0
 dwiz_mpi_command =
 dwiz_tcvitals =null
 dwiz_bigmap =Y
/
EOF
			cat > namelist.input << EOF
&time_control            
run_days                 = 0,
run_hours                = 12,
run_minutes              = 0,
run_seconds              = 0,
start_year               = $tahun,     $tahun,     $tahun,
start_month              = $bulan,       $bulan,       $bulan,
start_day                = $dayinput,        $dayinput,        $dayinput,
start_hour               = $hourinput,       $hourinput,       $hourinput,
start_minute             = 00,       00,       00,
start_second             = 00,       00,       00,
end_year                 = $tahun,     $tahun,     $tahun,
end_month                = $bulan,       $bulan,       $bulan,
end_day                  = $dayinputend,        $dayinputend,        $dayinputend,
end_hour                 = $hourinputend,        $hourinputend,        $hourinputend,
end_minute               = 00,        0,       00,
end_second               = 00,       00,       00,
interval_seconds         = 10800,
input_from_file          = .true.,   .true.,   .true.,
history_interval         = 180,       60,       60,
frames_per_outfile       = 1,        1,        1,
restart                  = .false.,
restart_interval         = 5000,
io_form_history          = 2,
io_form_restart          = 2,
io_form_input            = 2,
io_form_boundary         = 2,
debug_level              = 0,
/

&domains                 
time_step                = 180,
time_step_fract_num      = 0,
time_step_fract_den      = 1,
max_dom                  = 3,
e_we                     = 20,       25,       40,
e_sn                     = 20,       22,       34,
e_vert                   = 30,       30,       30,
p_top_requested          = 5000,
num_metgrid_levels       = 27,
num_metgrid_soil_levels  = 4,
dx                       = 30000,    10000, 3333.333,
dy                       = 30000,    10000, 3333.333,
grid_id                  = 1,        2,        3,
parent_id                = 1,        1,        2,
i_parent_start           = 1,        6,        7,
j_parent_start           = 1,        8,        6,
parent_grid_ratio        = 1,        3,        3,
parent_time_step_ratio   = 1,        3,        3,
feedback                 = 1,
smooth_option            = 0,
/

&physics                 
mp_physics               = 6,        6,        6,
ra_lw_physics            = 1,        1,        1,
ra_sw_physics            = 1,        1,        1,
radt                     = 30,       30,       30,
sf_sfclay_physics        = 1,        1,        1,
sf_surface_physics       = 2,        2,        2,
bl_pbl_physics           = 1,        1,        1,
bldt                     = 0,        0,        0,
cu_physics               = 1,        1,        0,
cudt                     = 5,        5,        5,
isfflx                   = 1,
ifsnow                   = 0,
icloud                   = 1,
surface_input_source     = 1,
num_soil_layers          = 4,
sf_urban_physics         = 0,        0,        0,
maxiens                  = 1,
maxens                   = 3,
maxens2                  = 3,
maxens3                  = 16,
ensdim                   = 144,
/

&fdda                    
/

&dynamics                
w_damping                = 0,
diff_opt                 = 1,
km_opt                   = 4,
diff_6th_opt             = 0,        0,        0,
diff_6th_factor          = 0.12,     0.12,     0.12,
base_temp                = 290.,
damp_opt                 = 0,
zdamp                    = 5000.,    5000.,    5000.,
dampcoef                 = 0.2,      0.2,      0.2,
khdif                    = 0,        0,        0,
kvdif                    = 0,        0,        0,
non_hydrostatic          = .true.,   .true.,   .true.,
moist_adv_opt            = 1,        1,        1,
scalar_adv_opt           = 1,        1,        1,
/

&bdy_control             
spec_bdy_width           = 5,
spec_zone                = 1,
relax_zone               = 4,
specified                = .true.,  .false.,  .false.,
nested                   = .false.,   .true.,   .true.,
/

&grib2                   
/

&namelist_quilt          
nio_tasks_per_group      = 0,
nio_groups               = 1,
/
                                                                                                                                                      

EOF
#RUNNING WPS
			#time ./geogrid.exe
			#ln -s $WRFworkdir$WPS"ungrib/Variable_Tables/Vtable.GFS" $WRFworkdir$WPS$WPSdomain"Vtable"
			$WRFworkdir$WPS"link_grib.csh" "/home/genomexyz/WRF/Build_WRF/DATA/XXX/gfs_4_"$tahun$bulan$hari$gfsdata
			time ./ungrib.exe
			time ./metgrid.exe
#RUNNING WRF
			cd $WRFworkdir$WRFARWrun
			ln -sf /home/genomexyz/WRF/Build_WRF/WPS/palu/namelist* .
			ln -sf /home/genomexyz/WRF/Build_WRF/WPS/palu/met_em* .
			time mpirun -np 4 ./real.exe
			time mpirun -np 4 ./wrf.exe
#cleaning
			rm -f met_em*
			cd $WRFworkdir$WPS$WPSdomain
			rm -f met_em*
		done
	done
done
