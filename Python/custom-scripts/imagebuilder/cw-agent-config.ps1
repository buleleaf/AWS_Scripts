Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
$Cmd = "${Env:ProgramFiles}\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1"
if (!(Test-Path -LiteralPath "${Cmd}")) {
    Write-Output 'CloudWatch Agent not installed.  Please install it using the AWS-ConfigureAWSPackage SSM Document.'"
    exit 1"
}
Get-ScheduledTask -TaskName "cw-memory" -ErrorAction SilentlyContinue -OutVariable task
if ($task) {
    C:\Windows\System32\schtasks.exe /Change /Disable /TN "cw-memory"
    if ($? -eq 'True') {
    Write-Host 'Memory metric task is disabled'
    } else {
    Write-Host 'Error while disabling Memory metric task'
    }
} else {
Write-Host 'Memory metric task is not installed'
}
$CWADirectory = "Amazon\AmazonCloudWatchAgent"
if ($Env:ProgramData) {
    $CWAProgramData = "${Env:ProgramData}\${CWADirectory}"
} else {
    $CWAProgramData = "${Env:ALLUSERSPROFILE}\Application Data\${CWADirectory}"
}
$TOML="${CWAProgramData}\amazon-cloudwatch-agent.toml"
    if ((Test-Path -LiteralPath "${TOML}")) {
        Write-Output "CloudWatch Agent already configured.  Skipping the rest of the SSM Document."
        exit 0
    }
$Params = @()
$Action = 'configure'
$Source = '{{configurationSource}}'
if ($Action -eq 'configure') {
    $Action = 'fetch-config'
    $Config = '{{windowsconfigurationLocation}}'
    if ($Source -ne 'default') {
        if (!("${Config}")) {
            Write-Output 'Config path is required when configuring from Parameter Store or file.'
            exit 1
        } else {
            $Config = "${Source}:${Config}"
        }
    } else {
        $Config = 'default'
    }
    $Params += '(''-c'', "${Config}")'
    $Params += '-s'
}
$Params += '(''-a'', "${Action}", ''-m'', ''{{mode}}'')'
Invoke-Expression '& ${Cmd} ${Params}'
Set-StrictMode -Off
exit $LASTEXITCODE