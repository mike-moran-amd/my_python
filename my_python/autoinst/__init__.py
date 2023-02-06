"""
REF: https://github.com/covertsh/ubuntu-autoinstall-generator


This page has a number of tips to make life easier for installing Ubuntu automagically
    https://www.golinuxcloud.com/customize-cloud-init-user-data-ubuntu/


# openssl passwd -6 -stdin <<< PASSWORD
$6$vNiKYMV/149WtcPg$kbIXH.fmh9F.Trmvq21EAxUR9/JDm.qPseETsjgZjkasd3AW0WRBp9RT3gbt/fSvvopRhJeZ21ThzbNdZwVLf1


python3 -c 'import crypt; print(crypt.crypt("ubuntu", crypt.mksalt(crypt.METHOD_SHA512)))'
$6$DgID3Ts5aNd5ps4E$Zus7WHKidEv0rkBvl6/kbeaOxCRXSBZB1.d30ez9drre1ku7nfJ7uD.ZN7eY7NMKWC8jQo/AGmk8CvxQAVOqV.


root@ubuntu:~# mkpasswd --method=SHA-512 --rounds=4096
Password:
$6$rounds=4096$c3PYnICGfjNb2$BwA2nUSowf2fc8xSxvbqX0MWAf0gEWs7MTcAU6tmiIEopNXFrOE4QzrGdazpSd3NdcwpTZXmeYsJISmls7C1f.


packages:
    - ubuntu-desktop

curl -o ubuntu-autoinstall-generator.sh https://raw.githubusercontent.com/covertsh/ubuntu-autoinstall-generator/main/ubuntu-autoinstall-generator.sh

"""