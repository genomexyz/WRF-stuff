#!/bin/bash

if [ $# -lt 3 ]
then
	echo "usage: ./ujiskema.sh skema_microphyscis skema_cumulus skema_cumulus3"
	exit
fi

cumulus=$2
cumulus3=$3
mp=$1

cat > namelist.input << EOF
 &time_control
 run_days                            = 0,
 run_hours                           = 36,
 run_minutes                         = 0,
 run_seconds                         = 0,
 start_year                          = 2017, 2017, 2017,
 start_month                         = 02,   02,   02,
 start_day                           = 08,   08,   08,
 start_hour                          = 12,   12,   12,
 start_minute                        = 00,   00,   00,
 start_second                        = 00,   00,   00,
 end_year                            = 2017, 2017, 2017,
 end_month                           = 02,   02,   02,
 end_day                             = 10,   10,   10,
 end_hour                            = 00,   00,   00,
 end_minute                          = 00,   00,   00,
 end_second                          = 00,   00,   00,
 interval_seconds                    = 21600
 input_from_file                     = .true.,.true.,.true.,
 history_interval                    = 180,  60,   60,
 frames_per_outfile                  = 1000, 1000, 1000,
 restart                             = .false.,
 restart_interval                    = 5000,
 io_form_history                     = 2
 io_form_restart                     = 2
 io_form_input                       = 2
 io_form_boundary                    = 2
 debug_level                         = 0
 /

 &domains
 time_step                           = 120,
 time_step_fract_num                 = 0,
 time_step_fract_den                 = 1,
 max_dom                             = 3,
 e_we                                = 100,    88,   76,
 e_sn                                = 100,    88,   76,
 e_vert                              = 30,    30,   30,
 p_top_requested                     = 5000,
 num_metgrid_levels                  = 32,
 num_metgrid_soil_levels             = 4,
 dx                                  = 27000, 9000,  3000,
 dy                                  = 27000, 9000,  3000,
 grid_id                             = 1,     2,     3,
 parent_id                           = 0,     1,     2,
 i_parent_start                      = 1,     36,    32,
 j_parent_start                      = 1,     36,    32,
 parent_grid_ratio                   = 1,     3,     3,
 parent_time_step_ratio              = 1,     3,     3,
 feedback                            = 1,
 smooth_option                       = 0
 /

 &physics
mp_physics               = $mp,        $mp,        $mp,
ra_lw_physics            = 1,        1,        1,
ra_sw_physics            = 1,        1,        1,
radt                     = 30,       30,       30,
sf_sfclay_physics        = 1,        1,        1,
sf_surface_physics       = 2,        2,        2,
bl_pbl_physics           = 1,        1,        1,
bldt                     = 0,        0,        0,
cu_physics               = $cumulus,        $cumulus,        $cumulus3,
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
 w_damping                           = 0,
 diff_opt                            = 1,      1,      1,
 km_opt                              = 4,      4,      4,
 diff_6th_opt                        = 0,      0,      0,
 diff_6th_factor                     = 0.12,   0.12,   0.12,
 base_temp                           = 290.
 damp_opt                            = 0,
 zdamp                               = 5000.,  5000.,  5000.,
 dampcoef                            = 0.2,    0.2,    0.2
 khdif                               = 0,      0,      0,
 kvdif                               = 0,      0,      0,
 non_hydrostatic                     = .true., .true., .true.,
 moist_adv_opt                       = 1,      1,      1,     
 scalar_adv_opt                      = 1,      1,      1,     
 gwd_opt                             = 1,
 /

 &bdy_control
 spec_bdy_width                      = 5,
 spec_zone                           = 1,
 relax_zone                          = 4,
 specified                           = .true., .false.,.false.,
 nested                              = .false., .true., .true.,
 /

 &grib2
 /

 &namelist_quilt
 nio_tasks_per_group = 0,
 nio_groups = 1,
 /
 
EOF

time mpirun -np 4 ./real.exe
time mpirun -np 4 ./wrf.exe

#moving out
mkdir "skema_mp-"$mp"_cumulus-"$cumulus"_cumulus3-"$cumulus3"/"
mv wrfout* "skema_mp-"$mp"_cumulus-"$cumulus"_cumulus3-"$cumulus3"/"
