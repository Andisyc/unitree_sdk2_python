import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient
import math
from dataclasses import dataclass

# 装饰器相当于将装饰的函数或类作为参数输入进装饰器函数或类中形成新对象
@dataclass
class TestOption:
    name: str
    id: int

option_list = [
    TestOption(name="damp", id=0),         
    TestOption(name="Squat2StandUp", id=1),     
    TestOption(name="StandUp2Squat", id=2),   
    TestOption(name="move forward", id=3),         
    TestOption(name="move lateral", id=4),    
    TestOption(name="move rotate", id=5),  
    TestOption(name="low stand", id=6),  
    TestOption(name="high stand", id=7),    
    TestOption(name="zero torque", id=8),
    TestOption(name="wave hand1", id=9), # wave hand without turning around
    TestOption(name="wave hand2", id=10), # wave hand and trun around  
    TestOption(name="shake hand", id=11),     
    TestOption(name="Lie2StandUp", id=12),     
]

class UserInterface:
    def __init__(self):
        self.test_option_ = None

    def convert_to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError:
            return None

    def terminal_handle(self):
        # receive user input
        input_str = input("Enter id or name: \n")

        # let user check out all options
        if input_str == "list":
            self.test_option_.name = None
            self.test_option_.id = None
            for option in option_list:
                print(f"{option.name}, id: {option.id}")
            return

        # choosing option
        for option in option_list:
            if input_str == option.name or self.convert_to_int(input_str) == option.id:
                self.test_option_.name = option.name
                self.test_option_.id = option.id
                print(f"Test: {self.test_option_.name}, test_id: {self.test_option_.id}")
                return

        print("No matching test option found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} networkInterface")
        sys.exit(-1)

    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")

    # read in user input
    ChannelFactoryInitialize(0, sys.argv[1])

    # initialize empty data container
    test_option = TestOption(name=None, id=None)

    # initialize user interface
    user_interface = UserInterface()
    user_interface.test_option_ = test_option

    # initialize action interface
    sport_client = LocoClient()
    sport_client.SetTimeout(10.0)
    sport_client.Init()

    print("Input \"list\" to list all test option ...")

    while True: # main loop
        # receive and select user input
        user_interface.terminal_handle()

        print(f"Updated Test Option: Name = {test_option.name}, ID = {test_option.id}")

        # slow down motion to safty
        if test_option.id == 0:
            sport_client.Damp()
        
        # get down then stand up
        elif test_option.id == 1:
            sport_client.Damp()
            time.sleep(0.5)
            sport_client.Squat2StandUp()
        
        # stand up then get down
        elif test_option.id == 2:
            sport_client.StandUp2Squat()
        
        # move forward
        elif test_option.id == 3:
            sport_client.Move(0.3,0,0)
        
        # move backward
        elif test_option.id == 4:
            sport_client.Move(0,0.3,0)
        
        # rotate body
        elif test_option.id == 5:
            sport_client.Move(0,0,0.3)
        
        # roughly horse stand
        elif test_option.id == 6:
            sport_client.LowStand()

        # roughly normal stand
        elif test_option.id == 7:
            sport_client.HighStand()
        
        # zero out all
        elif test_option.id == 8:
            sport_client.ZeroTorque()
        
        # wave hand without rotate
        elif test_option.id == 9:
            sport_client.WaveHand()
        
        # wave hand with rotate
        elif test_option.id == 10:
            sport_client.WaveHand(True)
        
        # shake hand
        elif test_option.id == 11:
            sport_client.ShakeHand()
            time.sleep(3)
            sport_client.ShakeHand()
        
        # stand up from lie down
        elif test_option.id == 12:
            sport_client.Damp()
            time.sleep(0.5)
            sport_client.Lie2StandUp() # When using the Lie2StandUp function, ensure that the robot faces up and the ground is hard, flat and rough.

        time.sleep(1)