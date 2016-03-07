import hashlib;
from cErrorReport_foSpecialErrorReport_CppException import cErrorReport_foSpecialErrorReport_CppException;
from cErrorReport_foSpecialErrorReport_STATUS_ACCESS_VIOLATION import cErrorReport_foSpecialErrorReport_STATUS_ACCESS_VIOLATION;
from cErrorReport_foSpecialErrorReport_STATUS_BREAKPOINT import cErrorReport_foSpecialErrorReport_STATUS_BREAKPOINT;
from cErrorReport_foSpecialErrorReport_STATUS_INVALID_HANDLE import cErrorReport_foSpecialErrorReport_STATUS_INVALID_HANDLE;
from cErrorReport_foSpecialErrorReport_STATUS_FAIL_FAST_EXCEPTION import cErrorReport_foSpecialErrorReport_STATUS_FAIL_FAST_EXCEPTION;
from cErrorReport_foSpecialErrorReport_STATUS_STACK_BUFFER_OVERRUN import cErrorReport_foSpecialErrorReport_STATUS_STACK_BUFFER_OVERRUN;
from cErrorReport_foSpecialErrorReport_STATUS_STACK_OVERFLOW import cErrorReport_foSpecialErrorReport_STATUS_STACK_OVERFLOW;
from cErrorReport_foSpecialErrorReport_STATUS_STOWED_EXCEPTION import cErrorReport_foSpecialErrorReport_STATUS_STOWED_EXCEPTION;
from cErrorReport_foSpecialErrorReport_STATUS_WX86_BREAKPOINT import cErrorReport_foSpecialErrorReport_STATUS_WX86_BREAKPOINT;
from cErrorReport_foTranslateError import cErrorReport_foTranslateError;
from cException import cException;
from cProcess import cProcess;
from mHTML import *;
from NTSTATUS import *;

dfoSpecialErrorReport_uExceptionCode = {
  CPP_EXCEPTION_CODE: cErrorReport_foSpecialErrorReport_CppException,
  STATUS_ACCESS_VIOLATION: cErrorReport_foSpecialErrorReport_STATUS_ACCESS_VIOLATION,
  STATUS_BREAKPOINT: cErrorReport_foSpecialErrorReport_STATUS_BREAKPOINT,
  STATUS_INVALID_HANDLE: cErrorReport_foSpecialErrorReport_STATUS_INVALID_HANDLE,
  STATUS_FAIL_FAST_EXCEPTION: cErrorReport_foSpecialErrorReport_STATUS_FAIL_FAST_EXCEPTION,
  STATUS_STACK_BUFFER_OVERRUN: cErrorReport_foSpecialErrorReport_STATUS_STACK_BUFFER_OVERRUN,
  STATUS_STACK_OVERFLOW: cErrorReport_foSpecialErrorReport_STATUS_STACK_OVERFLOW,
  STATUS_STOWED_EXCEPTION: cErrorReport_foSpecialErrorReport_STATUS_STOWED_EXCEPTION,
  STATUS_WX86_BREAKPOINT: cErrorReport_foSpecialErrorReport_STATUS_WX86_BREAKPOINT,
};
# Hide some functions at the top of the stack that are merely helper functions and not relevant to the error:
asHiddenTopFrames = [
  "KERNELBASE.dll!RaiseException",
  "ntdll.dll!KiUserExceptionDispatch",
  "ntdll.dll!NtRaiseException",
  "ntdll.dll!RtlDispatchException",
  "ntdll.dll!RtlpExecuteHandlerForException",
  "ntdll.dll!ZwRaiseException",
];
class cErrorReport(object):
  def __init__(oErrorReport, oCdbWrapper, sErrorTypeId, sErrorDescription, sSecurityImpact, oException, oStack, asImportantStdErrLines):
    oErrorReport.oCdbWrapper = oCdbWrapper;
    oErrorReport.sErrorTypeId = sErrorTypeId;
    oErrorReport.sErrorDescription = sErrorDescription;
    oErrorReport.sSecurityImpact = sSecurityImpact;
    oErrorReport.oException = oException;
    oErrorReport.oStack = oStack;
    oErrorReport.asImportantStdErrLines = asImportantStdErrLines;
    oErrorReport.sStackId = None;
    oErrorReport.sCodeId = None;
    oErrorReport.sCodeDescription = None;
    oErrorReport.atsAdditionalInformation = [];
  
  @property
  def sProcessBinaryName(oErrorReport):
    return oErrorReport.oException.oProcess and oErrorReport.oException.oProcess.sBinaryName;
  
  def fsGetId(oErrorReport):
    if not oErrorReport.sProcessBinaryName or oErrorReport.sCodeId.startswith(oErrorReport.sProcessBinaryName + "!"):
      # If we do not know the process binary ot it's the module in which the error happened, do not mentioning it.
      return "%s %s %s" % (oErrorReport.sStackId, oErrorReport.sErrorTypeId, oErrorReport.sCodeId);
    return "%s %s %s!%s" % (oErrorReport.sStackId, oErrorReport.sErrorTypeId, oErrorReport.sProcessBinaryName, oErrorReport.sCodeId);
  sId = property(fsGetId);
  
  def foTranslateError(oErrorReport, dtxTranslations):
    return cErrorReport_foTranslateError(oErrorReport, dtxTranslations);
  
  def fHideTopStackFrames(oErrorReport, dasHiddenFrames_by_sErrorTypeIdRegExp):
    for (sErrorTypeIdRegExp, asHiddenFrames) in dasHiddenFrames_by_sErrorTypeIdRegExp.items():
      if re.match("^(%s)$" % sErrorTypeIdRegExp, oErrorReport.sErrorTypeId):
        oErrorReport.oStack.fHideTopFrames(asHiddenFrames);
  
  @property
  def sHTMLDetails(oErrorReport):
    if not hasattr(oErrorReport, "_sHTMLDetails"):
      # Turn cdb output into formatted HTML. It is separated into blocks, one for the initial cdb output and one for each
      # command executed.
      sHTMLCdbStdIO = '<hr class="StdIOSeparator"/>'.join(oErrorReport.oCdbWrapper.asHTMLCdbStdIOBlocks);
      del oErrorReport.oCdbWrapper.asHTMLCdbStdIOBlocks;
      # Create HTML details
      oErrorReport._sHTMLDetails = sHTMLDetailsTemplate % {
        "sId": fsHTMLEncode(oErrorReport.sId),
        "sExceptionDescription": fsHTMLEncode(oErrorReport.sErrorDescription),
        "sProcessBinaryName": fsHTMLEncode(oErrorReport.sProcessBinaryName),
        "sCodeDescription": fsHTMLEncode(oErrorReport.sCodeDescription),
        "sSecurityImpact": oErrorReport.sSecurityImpact and \
              '<span class="SecurityImpact">%s</span>' % fsHTMLEncode(oErrorReport.sSecurityImpact) or "None",
        "sImportantStdErrLines": oErrorReport.asImportantStdErrLines and \
              '<span class="CDBStdErr">%s</span>' % "<br/>".join([fsHTMLEncode(x) for x in oErrorReport.asImportantStdErrLines]) or "None",
              
        "sStack": oErrorReport.sHTMLStack,
        "sBinaryInformation": oErrorReport.sHTMLBinaryInformation,
        "sCdbStdIO": sHTMLCdbStdIO,
      };
    return oErrorReport._sHTMLDetails;
  
  @classmethod
  def foCreate(cSelf, oCdbWrapper, uExceptionCode, sExceptionDescription):
    # Get current process details
    oProcess = cProcess.foCreate(oCdbWrapper);
    if not oCdbWrapper.bCdbRunning: return None;
    # Get exception details
    oException = cException.foCreate(oCdbWrapper, oProcess, uExceptionCode, sExceptionDescription);
    if not oCdbWrapper.bCdbRunning: return None;
    # Get registers. This information is not analyzed, but will end up in cdb output in the report, for potential
    # use by an analyst.
    oCdbWrapper.fasSendCommandAndReadOutput("r");
    if not oCdbWrapper.bCdbRunning: return None;
    # Similarly, try to get disassembly around code in which exception happened. This may not be possible if rip/eip
    # points to memeory that cannot be read.
    asDisassemblyOutput = oCdbWrapper.fasSendCommandAndReadOutput(".if ($vvalid(@$scopeip, 1)) { ub; }; .else { .echo Disassembly not possible };");
    if not oCdbWrapper.bCdbRunning: return None;
    if asDisassemblyOutput != ["Disassembly not possible"]:
      # rip/eip must be valid as disassembly before this address was returned: get disassembly after as well:
      oCdbWrapper.fasSendCommandAndReadOutput("u");
      if not oCdbWrapper.bCdbRunning: return None;
    # Get the stack
    oStack = oException.foGetStack(oCdbWrapper);
    if not oCdbWrapper.bCdbRunning: return None;
    # Compare stack with exception information
    if oException.sAddressSymbol:
      doModules_by_sCdbId = oCdbWrapper.fdoGetModulesByCdbIdForCurrentProcess();
      (
        uAddress,
        sUnloadedModuleFileName, oModule, uModuleOffset,
        oFunction, uFunctionOffset
      ) = oCdbWrapper.ftxSplitSymbolOrAddress(oException.sAddressSymbol, doModules_by_sCdbId);
      sCdbSource = oException.sAddressSymbol;
    else:
      sCdbSource = "%X" % oException.uAddress; # Kinda faking it here :)
      uAddress = oException.uAddress;
      sUnloadedModuleFileName, oModule, uModuleOffset = None, None, None;
      oFunction, uFunctionOffset = None, None;
    if not oStack.aoFrames:
      # Failed to get stack, use information from exception.
      uFrameNumber = 0;
      oStack.fCreateAndAddStackFrame(oCdbWrapper, uFrameNumber, sCdbSource, uAddress, sUnloadedModuleFileName, oModule, uModuleOffset, oFunction, uFunctionOffset);
    else:
      if oException.uCode in [STATUS_WX86_BREAKPOINT, STATUS_BREAKPOINT]:
        # A breakpoint happens at an int 3 instruction, and eip/rip may have been updated to the next instruction.
        # If the first stack frame is not the same as the exception address, fix this off-by-one:
        oFrame = oStack.aoFrames[0];
        if (
          oFrame.uAddress == uAddress
          and oFrame.sUnloadedModuleFileName == sUnloadedModuleFileName
          and oFrame.oModule == oModule
          and oFrame.uModuleOffset == uModuleOffset
          and oFrame.oFunction == oFunction
          and oFrame.uFunctionOffset == uFunctionOffset
        ):
          pass;
        else:
          if uAddress is not None:
            uAddress -= 1;
          elif uModuleOffset is not None:
            uModuleOffset -= 1;
          elif uFunctionOffset is not None:
            oFrame.uFunctionOffset -= 1;
          else:
            raise AssertionError("The first stack frame appears to have no address or offet to adjust.");
          assert (
            oFrame.uAddress == uAddress
            and oFrame.sUnloadedModuleFileName == sUnloadedModuleFileName
            and oFrame.oModule == oModule
            and oFrame.uModuleOffset == uModuleOffset
            and oFrame.oFunction == oFunction
            and oFrame.uFunctionOffset == uFunctionOffset
          ), "The first stack frame does not appear to match the exception address";
      else:
        # Check that the address where the exception happened is on the stack and hide any frames that appear above it,
        # as these are not interesting (e.g. ntdll!RaiseException).
        for oFrame in oStack.aoFrames:
          if (
            oFrame.uAddress == uAddress
            and oFrame.sUnloadedModuleFileName == sUnloadedModuleFileName
            and oFrame.oModule == oModule
            and oFrame.uModuleOffset == uModuleOffset
            and oFrame.oFunction == oFunction
            and oFrame.uFunctionOffset == uFunctionOffset
          ):
            break;
          oFrame.bIsHidden = True;
        else:
          raise AssertionError("The exception address %s was not found on the stack" % sCdbSource);
      
    # Hide some functions at the top of the stack that are merely helper functions and not relevant to the error:
    oStack.fHideTopFrames(asHiddenTopFrames);
    # Create a preliminary error report.
    oErrorReport = cSelf(
      oCdbWrapper = oCdbWrapper,
      sErrorTypeId = oException.sTypeId,
      sErrorDescription = oException.sDescription,
      sSecurityImpact = oException.sSecurityImpact,
      oException = oException,
      oStack = oStack,
      asImportantStdErrLines = oCdbWrapper.asImportantStdErrLines,
    );
    # Make exception specific changes to the error report:
    foSpecialErrorReport = dfoSpecialErrorReport_uExceptionCode.get(oException.uCode);
    if foSpecialErrorReport:
      oErrorReport = foSpecialErrorReport(oErrorReport, oCdbWrapper);
      if not oCdbWrapper.bCdbRunning: return None;
      if not oErrorReport:
        # This exception is not an error, continue the application.
        return None;
    
    # Find out which frame should be the "main" frame and get stack id.
    oTopmostRelevantFrame = None;          # topmost relevant frame
    oTopmostRelevantFunctionFrame = None;  # topmost relevant frame that has a function symbol
    oTopmostRelevantModuleFrame = None;    # topmost relevant frame that has no function symbol but a module
    uFramesHashed = 0;
    bStackShowsNoSignOfCorruption = True;
    asHTMLStack = [];
    sStackId = "";
    for oStackFrame in oStack.aoFrames:
      if oStackFrame.bIsHidden:
        # This frame is hidden (because it is irrelevant to the crash)
        asHTMLStack.append('<span class="StackIgnored">%s</span><br/>' % fsHTMLEncode(oStackFrame.sAddress));
      else:
        # Once a stack frame is encountered with no id, the stack can no longer be trusted to be correct.
        bStackShowsNoSignOfCorruption = bStackShowsNoSignOfCorruption and (oStackFrame.sId and True or False);
        oTopmostRelevantFrame = oTopmostRelevantFrame or oStackFrame;
        sHTMLAddress = fsHTMLEncode(oStackFrame.sAddress);
        # Make stack frames without a function symbol italic
        if not oStackFrame.oFunction:
          sHTMLAddress = '<span class="StackNoSymbol">%s</span>' % sHTMLAddress;
        # Hash frame address for id and output frame to html
        if not bStackShowsNoSignOfCorruption or uFramesHashed == oStack.uHashFramesCount:
          # no more hashing is needed: just output as is:
          asHTMLStack.append('<span class="Stack">%s</span><br/>' % sHTMLAddress);
        else:
          sStackId += oStackFrame.sId;
          # frame adds useful information to the id: add hash and output bold
          uFramesHashed += 1;
          asHTMLStack.append('<span class="StackHash">%s</span> (%s in id)<br/>' % (sHTMLAddress, oStackFrame.sId));
          # Determine the top frame for the id:
          if oStackFrame.oFunction:
            oTopmostRelevantFunctionFrame = oTopmostRelevantFunctionFrame or oStackFrame;
          elif oStackFrame.oModule:
            oTopmostRelevantModuleFrame = oTopmostRelevantModuleFrame or oStackFrame;
    # If there are not enouogh id-able stack frames, there may be many trailing "_"-s; remove these. Also, if there
    # was not id, or nothing is left after removing the "_"-s, use the id "##".
    oErrorReport.sStackId = sStackId.rstrip("_") or "##";
    if oStack.bPartialStack:
      asHTMLStack.append("... (rest of the stack was ignored)<br/>");
    oErrorReport.sHTMLStack = "".join(asHTMLStack);
    # Use a function for the id
    oCodeIdFrame = oTopmostRelevantFunctionFrame or oTopmostRelevantModuleFrame;
    oErrorReport.sCodeId = oCodeIdFrame and oCodeIdFrame.sSimplifiedAddress or "(unknown)";
    
    # Create the location description 
    oErrorReport.sCodeDescription = oTopmostRelevantFrame and oTopmostRelevantFrame.sAddress or "(unknown)";
    
    # Get the binary's cdb name for retreiving version information:
    asBinaryCdbNames = oCdbWrapper.fasGetCdbIdsForModuleFileNameInCurrentProcess(oErrorReport.sProcessBinaryName);
    if not oCdbWrapper.bCdbRunning: return None;
    assert len(asBinaryCdbNames) > 0, "Cannot find binary %s module" % oErrorReport.sProcessBinaryName;
    # If the binary is loaded as a module multiple times in the process, the first should be the binary that was
    # executed.
    # If this turns out to be wrong, this code should be switch to use "u @$exentry L1" to determine the cdb id of the
    # module in which the process's entry point is found.
    dsGetVersionCdbId_by_sBinaryName = {oErrorReport.sProcessBinaryName: asBinaryCdbNames[0]};
    # Get the id frame's module cdb name for retreiving version information:
    if oCodeIdFrame:
      dsGetVersionCdbId_by_sBinaryName[oCodeIdFrame.oModule.sBinaryName] = oCodeIdFrame.oModule.sCdbId;
    asHTMLBinaryInformation = [];
    for sBinaryName, sCdbId in dsGetVersionCdbId_by_sBinaryName.items():
      asModuleInformationOutput = oCdbWrapper.fasSendCommandAndReadOutput("lmv m *%s" % sCdbId);
      if not oCdbWrapper.bCdbRunning: return None;
      # Sample output:
      # |0:004> lmv M firefox.exe
      # |start             end                 module name
      # |00000000`011b0000 00000000`0120f000   firefox    (deferred)             
      # |    Image path: firefox.exe
      # |    Image name: firefox.exe
      # |    Timestamp:        Thu Aug 13 03:23:30 2015 (55CBF192)
      # |    CheckSum:         0006133B
      # |    ImageSize:        0005F000
      # |    File version:     40.0.2.5702
      # |    Product version:  40.0.2.0
      # |    File flags:       0 (Mask 3F)
      # |    File OS:          4 Unknown Win32
      # |    File type:        2.0 Dll
      # |    File date:        00000000.00000000
      # |    Translations:     0000.04b0
      # |    CompanyName:      Mozilla Corporation
      # |    ProductName:      Firefox
      # |    InternalName:     Firefox
      # |    OriginalFilename: firefox.exe
      # |    ProductVersion:   40.0.2
      # |    FileVersion:      40.0.2
      # |    FileDescription:  Firefox
      # |    LegalCopyright:   (c)Firefox and Mozilla Developers; available under the MPL 2 license.
      # |    LegalTrademarks:  Firefox is a Trademark of The Mozilla Foundation.
      # |    Comments:         Firefox is a Trademark of The Mozilla Foundation.
      # The first two lines can be skipped.
      asHTMLBinaryInformation.append(sHTMLBinaryInformationTemplate % {
        "sName": fsHTMLEncode(sBinaryName),
        "sInformation": "".join(["%s<br/>" % fsHTMLEncode(x) for x in asModuleInformationOutput[2:]]),
      });
    oErrorReport.sHTMLBinaryInformation = "".join(asHTMLBinaryInformation);
    # TODO: At some point the instruction that cause the exception could be added. Use "u @$eventip L1" to retreive it.
    
    return oErrorReport;
