/*
 * Copyright 2018 Bonn-Rhein-Sieg University
 *
 * Author: Minh Nguyen
 *
 */
#ifndef MAS_PERCEPTION_LIBS_ALIASES_H
#define MAS_PERCEPTION_LIBS_ALIASES_H

#include <pcl/point_types.h>
#include <pcl/point_cloud.h>

typedef pcl::PointXYZRGB PointT;
typedef pcl::PointCloud<PointT> PointCloud;
typedef pcl::PointCloud<pcl::PointNormal> PointCloudNormal;

#endif  // MAS_PERCEPTION_LIBS_ALIASES_H
