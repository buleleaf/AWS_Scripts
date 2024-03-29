function Test-SqlConnection {
    param(
        [Parameter(Mandatory)]
        [string]$ServerName
    )

    try {
        $userName = 'lssadminuser'
        $password = 'dTueKxUFrKZkKRnsmN9BFDXCY'
        $connectionString = 'Data Source={0};database={1};User ID={2};Password={3}' -f $ServerName,$DatabaseName,$userName,$password
        $sqlConnection = New-Object System.Data.SqlClient.SqlConnection $ConnectionString
        $sqlConnection.Open()
        ## This will run if the Open() method does not throw an exception
        $true
    } catch {
       ## Only return $false if the excpeption was thrown because it can't connect for some reason. Otherwise
       ## throw the general exception
       if ($_.Exception.Message -match 'cannot open server') {
           $false
       } else {
           throw $_
       }
    } finally {
        ## Close the connection when we're done
        $sqlConnection.Close()
    }
}

Test-SqlConnection -ServerName 'dr-genius-prod.cripwf6ubgrw.us-west-2.rds.amazonaws.com'
