import sys
import trackD_twoprime as TW

TW.TARGETS = "trackD_targets_dim3.json"
sys.argv = ["run_dim3", "--control"] if "--control" in sys.argv else ["run_dim3", "1800"]
TW.main()
