$Instances = (Get-EC2Instance).instances
$VPCS = Get-EC2Vpc
foreach ($VPC in $VPCS) {
     $Instances | Where-Object {$_.VpcId -eq $VPC.VpcId} | foreach {
        New-Object -TypeName PSObject -Property @{
            'VpcId' = $_.VpcId
            'VPCName' = ($VPC.Tags | Where-Object {$_.Key -eq 'Name'}).Value
            'InstanceId' = $_.InstanceId
            'InstanceName' = ($_.Tags | Where-Object {$_.Key -eq 'Name'}).Value
            'LaunchTime' = $_.LaunchTime
            'State' = $_.State.Name
            'KeyName' = $_.KeyName
        }
    }
}