#!/bin/bash
#title          :start_controller.sh
#description    :Start the controller for the test harness.
#author         :Jarrod N. Bakker
#date           :08/03/2016
#usage          :bash start_controller.sh
#========================================================================
clear ;
# The paths below may need to edited, this should be changed!
cd ;
cd ryu && ./bin/ryu-manager --verbose /home/ubuntu/PycharmProjects/Test_Env_Topo/controller/test_env_app ;