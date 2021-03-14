Set-StrictMode -Version 2.0
$ErrorActionPreference = "stop" #halts script if error
$LocalFolder = "C:\AwsScripts\" #DO NOT CHANGE# location for files on local machine
$FolderExists = Test-Path $LocalFolder
$NetworkShare = "\\IRVINE834\AWS_MSPInstalls\AwsScripts\" #need network share to pull script
$NetworkExists = Test-Path $NetworkShare
$s3uri = "https://s3-us-west-2.amazonaws.com/onica-els-files/AwsScripts/"
$AllFiles = "*" #for copy command
$CLIFile = "AWSCLI.msi"
$XmlFile = "cw-memory.xml" #scheduled task XML
$SDKFile = "AWSToolsAndSDKForNet.msi"
$WinMemFile = "mon-put-metrics-mem.ps1"
$EC2ConfFile = "Ec2Install.exe"


# Write-Host "Checking for directory $NetworkShare..."
# If($NetworkExists)
#   {Write-Host "$NetworkShare Found!"}
# Else
#   {Write-Host "Unable to access $NetworkShare"}

Write-Host "Checking for directory $LocalFolder..."
if(!($FolderExists))
  {
  New-Item $LocalFolder -type directory
  Write-Host "Directoy $LocalFolder created"
  }
else
  {Write-Host "Directory found..."}

Write-Host "Copying files to local machine..."
Invoke-WebRequest -Uri $s3Uri$CLIFile -OutFile $LocalFolder$CLIFile
Invoke-WebRequest -Uri $s3Uri$XmlFile -OutFile $LocalFolder$XmlFile
Invoke-WebRequest -Uri $s3Uri$SDKFile -OutFile $LocalFolder$SDKFile
Invoke-WebRequest -Uri $s3Uri$WinMemFile -OutFile $LocalFolder$WinMemFile
Invoke-WebRequest -Uri $s3Uri$EC2ConfFile -OutFile $LocalFolder$EC2ConfFile

# Copy-Item $NetworkShare$AllFiles -Destination $LocalFolder -Exclude "*.txt" -Force -Recurse
# Write-Host "Installing .NET SDK..."
Write-Host "Installing SDK..."
Start-Process C:\Windows\System32\msiexec.exe "/i $LocalFolder$SDKFile /quiet /norestart" -Wait

Write-Host "Installing CLI..."
Start-Process C:\Windows\System32\msiexec.exe "/i $LocalFolder$CLIFile /quiet /norestart" -Wait

# if($SDKInstall)
#   {Write-Host "SDK Installed Successfully!"}
# else
#   {Write-Host "SDK Installation Failed!"}

Write-Host "Creating scheduled task"
schtasks.exe /create /RU "SYSTEM" /TN "cw-memory" /XML $LocalFolder$XmlFile
Set-StrictMode -Off
exit $LASTEXITCODE
