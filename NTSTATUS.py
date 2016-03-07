# Sources:
# http://deusexmachina.uk/ntstatus.html
# http://errco.de/win32/ntstatus-h/
# https://lists.samba.org/archive/jcifs/2004-February/003039.html
STATUS_WX86_SINGLE_STEP = 0x4000001E;
STATUS_WX86_BREAKPOINT = 0x4000001F;
STATUS_GUARD_PAGE_VIOLATION = 0x80000001;
STATUS_DATATYPE_MISALIGNMENT = 0x80000002;
STATUS_BREAKPOINT = 0x80000003;
STATUS_SINGLE_STEP = 0x80000004;
STATUS_WAKE_SYSTEM_DEBUGGER = 0x80000007;
STATUS_NOT_IMPLEMENTED = 0xC0000002;
STATUS_ACCESS_VIOLATION = 0xC0000005;
STATUS_IN_PAGE_ERROR = 0xC0000006;
STATUS_PAGEFILE_QUOTA = 0xC0000007;
STATUS_INVALID_HANDLE = 0xC0000008;
STATUS_NO_MEMORY = 0xC0000017;
STATUS_INVALID_SYSTEM_SERVICE = 0xC000001C;
STATUS_ILLEGAL_INSTRUCTION = 0xC000001D;
STATUS_INVALID_LOCK_SEQUENCE = 0xC000001E;
STATUS_NONCONTINUABLE_EXCEPTION = 0xC0000025;
STATUS_INVALID_DISPOSITION = 0xC0000026;
STATUS_ARRAY_BOUNDS_EXCEEDED = 0xC000008C;
STATUS_FLOAT_DENORMAL_OPERAND = 0xC000008D;
STATUS_FLOAT_DIVIDE_BY_ZERO = 0xC000008E;
STATUS_FLOAT_INEXACT_RESULT = 0xC000008F;
STATUS_FLOAT_INVALID_OPERATION = 0xC0000090;
STATUS_FLOAT_OVERFLOW = 0xC0000091;
STATUS_FLOAT_STACK_CHECK = 0xC0000092;
STATUS_FLOAT_UNDERFLOW = 0xC0000093;
STATUS_INTEGER_DIVIDE_BY_ZERO = 0xC0000094;
STATUS_INTEGER_OVERFLOW = 0xC0000095;
STATUS_PRIVILEGED_INSTRUCTION = 0xC0000096;
STATUS_STACK_OVERFLOW = 0xC00000FD;
STATUS_ILLEGAL_FLOAT_CONTEXT = 0xC000014A;
STATUS_POSSIBLE_DEADLOCK = 0xC0000194;
STATUS_STOWED_EXCEPTION = 0xC000027B 
STATUS_FLOAT_MULTIPLE_FAULTS = 0xC00002B4;
STATUS_FLOAT_MULTIPLE_TRAPS = 0xC00002B5;
STATUS_DATATYPE_MISALIGNMENT_ERROR = 0xC00002C5;
STATUS_REG_NAT_CONSUMPTION = 0xC00002C9;
STATUS_STACK_BUFFER_OVERRUN = 0xC0000409;
STATUS_FATAL_USER_CALLBACK_EXCEPTION = 0xC000041D;
STATUS_ASSERTION_FAILURE = 0xC0000420;
STATUS_VERIFIER_STOP = 0xC0000421;
STATUS_FAIL_FAST_EXCEPTION = 0xC0000602;

# Not strictly part of ntstatus
# Source: http://blogs.microsoft.co.il/sasha/2008/08/20/converting-win32-and-c-exceptions-to-managed-exceptions/
CLR_EXCEPTION_CODE = 0xE0434F4D
CPP_EXCEPTION_CODE = 0xE06D7363