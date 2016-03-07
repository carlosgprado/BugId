# Some invalid handles happen quite often and don't appear to be error at all:
dtxErrorTranslations = {
  None: (
    None,
    None,
    [
      # When a 32-bit application is running on a 64-bit OS, any new processes will generate a STATUS_BREAKPOINT and
      # a status STATUS_WX86_BREAKPOINT exception. The former is recognized as the initial process breakpoint, and the
      # new process is registered. The later is not, but it can be recognized by its stack and should be ignored:
      [
        "ntdll.dll!LdrpDoDebuggerBreak",
        "ntdll.dll!LdrpInitializeProcess",
      ],
      [ # Chrome Asan builds trigger a breakpoint in __sanitizer_cov, apparently to determine the return address.
        "chrome.dll!__sanitizer_cov",
      ],
      [
        "chrome_child.dll!__sanitizer_cov",
      ],
    ],
  ),
};

# Hide some functions at the top of the stack that are merely helper functions and not relevant to the error:
asHiddenTopFrames = [
  "KERNELBASE.dll!RaiseException",
];
def cErrorReport_foSpecialErrorReport_STATUS_INVALID_HANDLE(oErrorReport, oCdbWrapper):
  oErrorReport = oErrorReport.foTranslateError(dtxErrorTranslations);
  if oErrorReport:
    oErrorReport.oStack.fHideTopFrames(asHiddenTopFrames);
  return oErrorReport;


