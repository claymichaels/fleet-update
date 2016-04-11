#!/usr/bin/python

# fleetUpdate.py
# Clay Michaels
# Dec 2014
#
# VERSION LOG
# -----
# version 1.0
# Imports fleets from file
# Optimized lookup of fleets
# -----
# version 0.9
# Added completion %
# Added location argument (/conf/ was previously hardcoded)
# -----
# version 0.8
# Added Facebook
# Added error checking for file existing and fleet matching
# -----
# version 0.7
# added Acela
# -----
# version 0.6
# fixed log import
#
# USAGE
# -----
# python fleetUpdate.py <FLEETNAME> <FILETOTRANSFER> <DESTINATION LOCATION>
#
# ex:
# python fleetUpdate.py acela PROJECT.conf /conf/
#
# Note that the script uses the host's OS etc/hosts file, so <FLEETNAME> should match that file.
# 
# TODO
# Implement import of fleets from config file
# Optimize the fleet lookup


import os               # For basic interactions with host OS
import sys              # For sys.exit() which exits the script
import subprocess       # Send native commands to with host OS
import csv              # Read and write CSV files easily
import ast              # Turn a string into a variable

vehiclesUpdated = [  ]

# CHECK ARGUMENT COUNT
if not len( sys.argv ) == 4:
        print 'ERROR: Arguments missing!'
        print 'USAGE:'
        print '\tpython fleetUpdate.py [fleet] [file to transfer] [destination location]'
        print '\tEx:'
        print '\tpython fleetUpdate.py acela PROJECT.conf /conf/'
        print '\tUse the same fleet names as the hosts file. (nocal, amfleet1, apple...)'
        sys.exit(  )


# GET FLEET VEHICLE LISTS FROM CONFIG FILE
with open( 'fleet_config_file', 'r' ) as fleetFileContents:
        fleets = ast.literal_eval( fleetFileContents.read(  ).replace( '\n','' ).replace( '\r','' ) )
fleetname = sys.argv[ 1 ].upper(  )
if not fleetname in fleets:
        print 'ERROR: Fleet not found!'
        print '\tCheck the fleet named in arguments.'
        print '\tNote that the fleet name is case-insensitive.'
        print '\t(Recieved "' + sys.argv[ 1 ] + '")'
        sys.exit(  )
else:
        fleet = fleets[ fleetname ]  # Get Dict from List of Dicts where Key = fleetname
        trackingSheet = fleetname + 'UpdateLog.csv'


# CHECK THAT FILE EXISTS
fileToBeTransferred = sys.argv[ 2 ]
if not os.path.isfile( sys.argv[ 2 ] ):
        print 'ERROR: Source file not found!'
        print '\tCheck the file named in arguments.'
        print '\t(Recieved "' + sys.argv[ 2 ] + '")'
        sys.exit(  )

destinationLocation = sys.argv[ 3 ]


# FUNCTION TO CONNECT TO HOST OS AND RUN RSYNC
def do_rsync(command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        exitCode = process.returncode
        output = ''

        # Record the results
        if (exitCode == 0):
                return 'File transferred successfully.'
        else:
                return 'Unable to connect to vehicle.'


# IMPORT OR CREATE TRACKING SHEET
if not os.path.isfile( trackingSheet ):
	print 'Tracking Sheet ', trackingSheet, 'does not exist.'
	print 'Creating', trackingSheet
	file = open( trackingSheet, 'wb' )
	print 'Done.'
else:
        print 'Reading in Tracking Sheet: ' + trackingSheet
        file = open( trackingSheet, 'rb' )
        reader = csv.reader( file, delimiter=',' )
        for row in reader:
                for item in row:
                        vehiclesUpdated.append( item )
        print 'Done.'
        file.close(  )
        file = open( trackingSheet, 'wb' )


# UPDATE ONE AT A TIME
for vehicle in fleet:
        # Check if the vehicle (from the fleet constant) is also in the list of vehicles already done
        #       (from the imported tracking sheet)
        print '----------'
        print vehicle
        if vehicle in vehiclesUpdated:
                # Remove the already-done vehicle from the list of vehicles to do. (The fleet constant)
                print 'Already done.'
        else:
                print 'Attempting to connect...'
                commandToRun = 'rsync --timeout=10 ' + fileToBeTransferred + ' ' + fleetname.lower(  ) + "." + vehicle + ':' +  destinationLocation
                output = do_rsync( commandToRun )
                print output
                if 'successfully' in output:
                        vehiclesUpdated.append( vehicle )


print '----------'
print 'All online vehicles updated.'
print 'Completion:', str( len( vehiclesUpdated ) ) + '/' + str( len( fleet ) ),str( ( len( vehiclesUpdated ) / len( fleet ) )*100 ) + '%'
writer = csv.writer( file )
writer.writerow( vehiclesUpdated )
file.close(  )     #Close the tracking text file


