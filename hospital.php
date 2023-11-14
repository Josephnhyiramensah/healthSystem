<?php

$servername="localhost";
$username= "root";
$password="";
$databaseame=" hospital base system";
 $con = mysqli_connect($servername, $username, $password, $databasename);

if($conn){
die("Connection failed".mysqli_connect_error());

}
$healthcare_provider=$_POST['healthcare_provider'];
$patient_health_issue=$POST['patient_health_issue'];
$suggested_medication='No medication suggested';

if($healthcare_provider==="doctor"){
$sql= "SELECT suggested_medication FROM medications WHERE health_issue LIKE '%$patient_health_issue%";
$result=mysqli_query($conn, $sql);
if(mysqli_num_rows($result)>0){
    $suggested_medication="";

while ($row = mysqli_fetch_assoc($result)){
    $suggested_medication.=$row['suggested_medication']. "\n";
}
}
}
mysqli_close($conn);
?>