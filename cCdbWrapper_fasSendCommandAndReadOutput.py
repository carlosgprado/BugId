import re;
from dxBugIdConfig import dxBugIdConfig;
from mHTML import fsHTMLEncode;

def cCdbWrapper_fasSendCommandAndReadOutput(oCdbWrapper, sCommand, bIsRelevantIO = True):
  if dxBugIdConfig["bOutputStdIn"]:
    print "cdb<%s" % repr(sCommand)[1:-1];
  try:
    oCdbWrapper.oCdbProcess.stdin.write("%s\r\n" % sCommand);
  except Exception, oException:
    oCdbWrapper.bCdbRunning = False;
    return None;
  if bIsRelevantIO:
    # Add the command to the current output block; this block should contain only one line that has the cdb prompt.
    oCdbWrapper.asHTMLCdbStdIOBlocks[-1] += "<span class=\"CDBCommand\">%s</span><br/>" % fsHTMLEncode(sCommand);
  else:
    # Remove the second to last output block: it contains the cdb prompt that is linked to this command and thus it
    # has become irrelevant.
    oCdbWrapper.asHTMLCdbStdIOBlocks.pop(-1);
  # The following command will always add a new output block with the new cdb prompt, regardless of bDoNotSaveIO.
  asOutput = oCdbWrapper.fasReadOutput(bIsRelevantIO = bIsRelevantIO);
  # Detect obvious errors executing the command. (this will not catch everything, but does help development)
  assert asOutput is None or len(asOutput) != 1 or not re.match(r"^(\s*\^ .*|Couldn't resolve error at .+)$", asOutput[0]), \
      "There was a problem executing the command %s:\r\n%s" % \
      (repr(sCommand), "\r\n".join([repr(sLine) for sLine in asOutput]));
  return asOutput;
