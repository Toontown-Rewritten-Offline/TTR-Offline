set pathtofolder=__pycache__

pushd "*" && (rd "%pathtofolder%" 2>nul & popd)

pause