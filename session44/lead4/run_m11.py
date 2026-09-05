import sys
import trackD_twoprime as TW

TW.TARGETS = "trackD_targets_missing11.json"
TW.STATE = "m11_state.json"
sys.argv = ["run_m11", "600"]
TW.main()
