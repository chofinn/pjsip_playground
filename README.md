# PJSIP recorder
testing the usage of pjsua
- player.py
    - play wav when call
    - no wav file in this repo, plz prepare ur own file
- recorder.py
    - recorder 10 sec wav when call
- myrecorder.py
    - a recorder
    - when oncall, input "a" to answer the call
    - it will play a wav to the caller, then start recording for 10 sec
    - after the recording is over, it will hangup the call
- Dockerfile
    - build docker image of myrecorder.py
## install PJSIP python API
- run `pjsip-install.sh`
