from NTSTATUS import *;

daxExceptionHandling = {
  "sxe": [ # break on first chance exceptions
    # To be able to track which processes are running at any given time while the application being debugged, cpr and
    # epr must be enabled. Additionally, if epr is disabled the debugger will silently exit when the application
    # terminates. To distinguish this from other unexpected terminations of the debugger, epr must also be enabled.
    "cpr", "ibp", "epr",
    "aph", # Application has stopped responding
    STATUS_ACCESS_VIOLATION,
    STATUS_ASSERTION_FAILURE,
    STATUS_BREAKPOINT,
    STATUS_ARRAY_BOUNDS_EXCEEDED,
    STATUS_DATATYPE_MISALIGNMENT,
    STATUS_FAIL_FAST_EXCEPTION,
    STATUS_GUARD_PAGE_VIOLATION,
    STATUS_ILLEGAL_INSTRUCTION,
    STATUS_IN_PAGE_ERROR,
    STATUS_PRIVILEGED_INSTRUCTION,
    STATUS_SINGLE_STEP,
    STATUS_STACK_BUFFER_OVERRUN,
    STATUS_STACK_OVERFLOW,
    STATUS_WX86_BREAKPOINT,
    STATUS_WX86_SINGLE_STEP,
    STATUS_WAKE_SYSTEM_DEBUGGER,
  ],
  "sxd": [ # break on second chance exceptions
    CPP_EXCEPTION_CODE,
    STATUS_INTEGER_DIVIDE_BY_ZERO,
    STATUS_INTEGER_OVERFLOW, 
    STATUS_INVALID_HANDLE, 
  ],
  "sxi": [ # ignored
    "ld", "ud", # Load/unload module
  ],
};
