import sys
import trackD_twoprime as TW

TW.TARGETS = "trackD_targets_waveA.json"
TW.STATE = "waveA_state.json"
sys.argv = ["run_waveA", "900"]
TW.main()
