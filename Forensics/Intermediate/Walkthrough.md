```
$ sudo veracrypt ./forensics_intermediate /media/veracrypt26 --password threerivers
```

```
sudo testdisk
TestDisk 7.1, Data Recovery Utility, July 2019                                                                      
Christophe GRENIER <grenier@cgsecurity.org>                                                                         
https://www.cgsecurity.org                                                                                          
                                                                                                                    
  TestDisk is free software, and                                                                                    
comes with ABSOLUTELY NO WARRANTY.                                                                                  
                                                                                                                    
Select a media (use Arrow keys, then press Enter):                                                                  
...  
>Disk /dev/mapper/veracrypt26 - 16 MB / 15 MiB
...
>[None   ] Non partitioned media        
>FAT16
"[ List ] List directories and files"
# Press the c button to copy flag.txt
# Press c again over . for the current directory
```

Flag: TRISS{everything_not_saved_will_be_lost}