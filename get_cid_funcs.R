library(CycleInfraLnd)
?get_cid_lines
cid_asl = get_cid_lines(type = "advanced_stop_line")
cid_cycle_lanes = get_cid_lines(type = "cycle_lane_track")

cid_signal = get_cid_points(type = "signal")
cid_crossing = get_cid_points(type = "crossing")
cid_parking = get_cid_points(type = "parking")
