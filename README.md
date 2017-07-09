# LLDB Plugin for Jailbreak Debugging.

LLDB Python scripts with a few helpers that I use when debugging jailbroken devices.

`jailbreak` - Connects to jailbroken device via USB at port 6666.

(WIP) `swizzle` - (Requires MobileSubstrate) Swizzles a method. Example: `swizzle --class LoginViewController --selector validateLogin: --arg-count 1 --method 'if (arg1 == 0) { return YES; } return NO;'`
