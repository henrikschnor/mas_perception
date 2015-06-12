#!/usr/bin/env python

PACKAGE = 'mcr_object_detection'

import roslib
roslib.load_manifest(PACKAGE)
import rospy

from smach import cb_interface, State
from smach_ros import ServiceState

import mcr_perception_msgs.srv as srv
import topic_tools.srv

find_workspace = ServiceState('/mcr_perception/workspace_finder/find_workspace',
                              srv.FindWorkspace,
                              response_slots=['polygon'])

accumulate_tabletop_cloud = ServiceState('/mcr_perception/tabletop_cloud_accumulator/accumulate_tabletop_cloud',
                                         srv.AccumulateTabletopCloud,
                                         request_slots=['polygon'],
                                         response_slots=['cloud'])
cluster_tabletop_cloud = ServiceState('/mcr_perception/tabletop_cloud_clusterer/cluster_tabletop_cloud',
                                      srv.ClusterTabletopCloud,
                                      request_slots=['cloud', 'polygon'],
                                      response_slots=['clusters'])


@cb_interface(input_keys=['clusters', 'polygon'])
def make_boxes_request_cb(userdata, request):
    r = srv.MakeBoundingBoxesRequest()
    r.clouds = userdata.clusters
    r.axis.x = userdata.polygon.coefficients[0]
    r.axis.y = userdata.polygon.coefficients[1]
    r.axis.z = userdata.polygon.coefficients[2]
    return r


@cb_interface(input_keys=['bounding_boxes'], output_keys=['bounding_boxes'])
def make_boxes_response_cb(userdata, response):
    userdata.bounding_boxes = response.bounding_boxes
    for b in userdata.bounding_boxes:
        b.dimensions.x += 0.01

make_bounding_boxes = ServiceState('/mcr_perception/bounding_box_maker/make_bounding_boxes',
                                   srv.MakeBoundingBoxes,
                                   request_cb=make_boxes_request_cb,
                                   response_cb=make_boxes_response_cb)

class PointCloudSubscription(State):
    def __init__(self, subscribe=False):
        State.__init__(self,
                       outcomes=['done','failed'])
        self.subscribe = subscribe
        self.mux_service = rospy.ServiceProxy('/mcr_perception/mux_pointcloud/select', topic_tools.srv.MuxSelect)

    def execute(self, ud):
        if self.subscribe:
            topic = '/tower_cam3d/depth_registered/points'
        else:
            topic = '/empty_topic'
        try:
            resp = self.mux_service(topic)
        except rospy.ServiceException as exc:
            print "Service exception ", str(exc)
            return 'failed'
        return 'done'
