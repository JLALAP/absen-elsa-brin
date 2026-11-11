$pythonPath = "C:\Users\Jlalap78\AppData\Local\Programs\Python\Python313\python.exe"
$workingDir = "D:\absen-elsa-brin"

# 1. Jadwal Pagi (07:58 WIB, Hari Kerja)
$actionPagi = New-ScheduledTaskAction -Execute $pythonPath -Argument "absen.py --mode pagi" -WorkingDirectory $workingDir
$triggerPagi = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At 7:58am
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "Absen_ELSA_BRIN_Pagi" -Action $actionPagi -Trigger $triggerPagi -Settings $settings -Description "Otomasi Presensi Pagi ELSA BRIN (MBKM)" -Force

# 2. Jadwal Sore (16:00 WIB, Hari Kerja)
$actionSore = New-ScheduledTaskAction -Execute $pythonPath -Argument "absen.py --mode sore" -WorkingDirectory $workingDir
$triggerSore = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At 4:00pm

Register-ScheduledTask -TaskName "Absen_ELSA_BRIN_Sore" -Action $actionSore -Trigger $triggerSore -Settings $settings -Description "Otomasi Presensi Sore ELSA BRIN (MBKM)" -Force

Write-Host "[SUKSES] Jadwal Presensi Otomatis Windows berhasil dipasang!"
