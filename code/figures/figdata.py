"""All numbers drawn in the figures, with their source. Nothing here is estimated."""

# Case 1: 17-patient development pipeline (A manuscript; frozen_results.json of the A repository)
CASE1 = dict(patients=17,
             supplied=dict(train_only=0, val_only=0, both=17, accuracy=0.990),
             repair1=dict(train_only=12, val_only=5, both=0, accuracy=None, cutting_support=0),
             repair2=dict(train_only=13, val_only=4, both=0, accuracy=0.758, val_clips=726, classes=5))

# Case 2 archive content audit (A manuscript Fig. 2; frozen_results.json: cross_prefix_records = 287)
ARCHIVE = dict(records=781, unique=476, repeated=305, dup_groups=254, cross_groups=118, within_groups=136,
               cross_records=287, json_extra=1)
# derived: records in duplicate groups = groups + repeats = 559; singletons = 781 - 559 = 222
# repeats inside cross-prefix groups = 287 - 118 = 169; repeats inside within-prefix groups = 305 - 169 = 136

# Case 2 archived output frequencies, % of frames (C manuscript, Table 2)
FIRING = [  # class, ZH >=0.05, Macau >=0.05, ZH >=0.25, Macau >=0.25
    ("Grasping forceps", 90.2, 81.9, 14.0, 1.4),
    ("Ultrasonic scalpel", 92.7, 1.1, 33.8, 0.0),
    ("Colon", 80.0, 27.5, 42.7, 2.5),
    ("PPL feature", 80.0, 4.2, 78.7, 0.6),
    ("P9 landmark", 54.9, 0.8, 48.9, 0.3),
]

# Case 2 Macau reference (C manuscript, Methods and Results)
MACAU = dict(unique_images=477, annotated_images=155, shapes=527, polygons=357, line_strips=115, lines=55,
             mappable_polygons=247, mappable_classes=10)

# Case 2 source adequacy (C manuscript)
SOURCE = dict(historical_map50=0.316, recon15_ap50=0.0257, twoclass_ap50=0.000108831,
              twoclass_grasper=0.000186961, twoclass_scalpel=0.000030701,
              split=(195, 53, 52), boundary_excluded=43, eval_images=529, predictions=155157,
              epochs=48, selected_epoch=28, matching_cells=90, H1_images=343, H1_boxes=2272)

# Public resources (A manuscript Fig. 4): content, video/source, procedure, patient linkage
# 2 = explicit/reconstructable, 1 = partial, 0 = not established
RESOURCES = [
    ("Case 2 archive", 2, 2, 1, 0),
    ("CholecSeg8k", 2, 2, 0, 0),
    ("Endoscapes2023", 2, 2, 2, 0),
    ("HeiChole", 2, 2, 2, 0),
    ("HeiCo", 2, 2, 2, 0),
    ("SLAM", 2, 2, 1, 2),
]
