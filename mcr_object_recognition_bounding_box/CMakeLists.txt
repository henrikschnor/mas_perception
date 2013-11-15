cmake_minimum_required(VERSION 2.8.3)
project(mcr_object_recognition_bounding_box)

find_package(PCL 1.6 REQUIRED)

find_package(catkin REQUIRED 
  COMPONENTS
    mcr_perception_msgs
    roscpp
    pcl_ros
)

catkin_package(
  CATKIN_DEPENDS
    mcr_perception_msgs
    rospy
    smach
    smach_ros
)

#...: gnu++0x
if(CMAKE_COMPILER_IS_GNUCXX)
    execute_process(COMMAND ${CMAKE_C_COMPILER} -dumpversion OUTPUT_VARIABLE GCC_VERSION)
    if(GCC_VERSION VERSION_GREATER 4.6 OR GCC_VERSION VERSION_EQUAL 4.6)
        add_definitions(-std=gnu++0x)
    else(GCC_VERSION VERSION_GREATER 4.6 OR GCC_VERSION VERSION_EQUAL 4.6)
        message(SEND_ERROR "You need GCC version 4.6 or greater to compile this package.")
    endif(GCC_VERSION VERSION_GREATER 4.6 OR GCC_VERSION VERSION_EQUAL 4.6)
endif(CMAKE_COMPILER_IS_GNUCXX)

#...: enable all but certain warnings
add_definitions(-Wall)
add_definitions(-Wno-unknown-pragmas)
add_definitions(-Wno-deprecated)
add_definitions(-fpermissive)

include_directories(
  ${PCL_INCLUDE_DIRS}
)

add_executable(cloud_color_analyzer
  ros/src/cloud_color_analyzer_node.cpp
)
add_dependencies(cloud_color_analyzer
  ${catkin_EXPORTED_TARGETS}
)
target_link_libraries(cloud_color_analyzer
  ${catkin_LIBRARIES}
  ${PCL_LIBRARIES}
)


install(PROGRAMS
  ros/scripts/object_recognizer
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(TARGETS cloud_color_analyzer
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY common/config/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/common/config
)
install(DIRECTORY common/data/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/common/data
)
install(DIRECTORY ros/launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/ros/launch
)
install(DIRECTORY ros/scripts/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/ros/scripts
)
install(DIRECTORY ros/tools/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/ros/tools
)