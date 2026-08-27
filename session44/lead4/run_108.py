import sys
import trackD_twoprime as TW

TW.TARGETS = "trackD_targets_108.json"
TW.STATE = "state_108.json"
sys.argv = ["run_108", "3600"]
TW.main()
