#!/bin/bash

#Copy Files USB to /mnt/nas2/raw_sequence_data/ftir
echo "Copying files from USB to /mnt/nas2/raw_sequence_data/ftir/working_dir"
cp -r /media/devon/SAMANTHA/FTIR/*.spc /mnt/nas2/raw_sequence_data/ftir/working_dir/
cp -r /media/devon/SAMANTHA/FTIR/*.XLSX /mnt/nas2/raw_sequence_data/ftir/working_dir/
sleep 10

#Run Renamer
echo "Running renamer.py"
renamer.py -s /mnt/nas2/raw_sequence_data/ftir/working_dir -f /mnt/nas2/raw_sequence_data/ftir/working_dir/FTIR.XLSX -o /mnt/nas2/raw_sequence_data/ftir/working_dir/renamedfiles
sleep 5

#Compress Files
echo "Compressing files"
zip -j /mnt/nas2/raw_sequence_data/ftir/working_dir/renamedfiles/FTIR.zip /mnt/nas2/raw_sequence_data/ftir/working_dir/renamedfiles/*.spc
sleep 5

#Move Zip to USB
echo "Moving archive to USB"
mv /mnt/nas2/raw_sequence_data/ftir/working_dir/renamedfiles/FTIR.zip /media/devon/SAMANTHA
sleep 2

echo "Moving raw files to storage"
# Move raw files from working_dir to raw_files
mv /mnt/nas2/raw_sequence_data/ftir/working_dir/*.spc /mnt/nas2/raw_sequence_data/ftir/raw_files/

echo "Moving renamed files to storage"
# Move renamed files from working_dir/renamed to renamedfiles
mv /mnt/nas2/raw_sequence_data/ftir/working_dir/renamedfiles/* /mnt/nas2/raw_sequence_data/ftir/renamedfiles/

#Delete Old FTIR
echo "Removing FTIR.XLSX from NAS"
rm /mnt/nas2/raw_sequence_data/ftir/working_dir/FTIR.XLSX

#Delete & Eject USB
echo "Removing original files from USB"
rm /media/devon/SAMANTHA/FTIR/*.spc
#udisksctl unmount -b /dev/sdb1 && udisksctl power-off -b /dev/sdb1

echo "Complete!"
