#!/bin/bash
cd /tmp/wt/charts
for job in "s4f232a 65521 6" "s4f232a 1000003 6" "s4f232a 1000033 6" "sab7d9e 65521 6" "scb0881 65521 6" "s20640c 65521 6" "s440259 65521 6" "sab7d9e 1000003 6" "scb0881 1000003 6"; do ./decide_shape.sh $job; done
echo SHAPE_QUEUE_DONE >> decide_shape.log
