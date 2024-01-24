#!/usr/bin/env python3
import matplotlib.pyplot as plt
import hebi
from math import pi, sin
from time import sleep, time
import math

lookup = hebi.Lookup()

# Wait 2 seconds for the module list to populate
sleep(2.0)

print('Modules found on network:')
for entry in lookup.entrylist:
    print(f'{entry.family} | {entry.name}')

family_name = "X5-9"
module_name1 = "X1"
module_name2 = "X2"
module_name3 = "X3"

# Create a group from a set of names
#group = lookup.get_group_from_names(['Family'], ['name1', 'name2'])
group1 = lookup.get_group_from_names([family_name], [module_name1])
group2 = lookup.get_group_from_names([family_name], [module_name2])
group3 = lookup.get_group_from_names([family_name], [module_name3])

if group1 and group2 and group3 is None:
    print('Group not found: Did you forget to set the module family and name above?')
    exit(1)

group_command1 = hebi.GroupCommand(group3.size)
group_feedback1 = hebi.GroupFeedback(group3.size)
group_command2 = hebi.GroupCommand(group2.size)
group_feedback2 = hebi.GroupFeedback(group2.size)
group_command3 = hebi.GroupCommand(group1.size)
group_feedback3 = hebi.GroupFeedback(group1.size)

# Start logging in the background
group1.start_log('logs', mkdirs=True)
group2.start_log('logs', mkdirs=True)
group3.start_log('logs', mkdirs=True)

# freq_hz = 0.5              # [Hz]
# freq = freq_hz * 2.0 * pi  # [rad / sec]
# amp = 1.0                  # [rad]
a = math.radians(30)
w = math.radians(150)
d = math.radians(25)

duration = 20               # [sec]
start = time()
t = time() - start
group1.command_lifetime = 100.0

while t < duration:
        # Even though we don't use the feedback, getting feedback conveniently
        # limits the loop rate to the feedback frequency
        group1.get_next_feedback(reuse_fbk=group_feedback1)
        t = time() - start
        print(t)
        group_command1.position = a * sin(w * t + 0 * d)
        group_command1.velocity = 1.5 #sin((w * t))
        group1.send_command(group_command1)
        group_command2.position = a * sin(w * t + 2 * d)
        group_command2.velocity = 1.5
        group2.send_command(group_command2)
        group_command3.position = a * sin(w * t + 4 * d)
        group_command3.velocity = 1.5
        group3.send_command(group_command3)
        sleep(0.01)


# Stop logging. `log_file` contains the contents of the file
log_file = group1.stop_log()

if log_file is not None:
    hebi.util.plot_logs(log_file, 'position')
