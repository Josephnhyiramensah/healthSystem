<!DOCTYPE html>
<html lang="en">
<head>
    <?php include('../includes/head.php'); ?>
</head>
<body>

<?php
session_start();
error_reporting(E_ALL);

// Establish a connection to your database
$conn = new mysqli("localhost", "username", "password", "database_name");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle file upload if an image is provided
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["image"])) {
    $targetDir = "upload/";
    $targetFile = $targetDir . basename($_FILES["image"]["name"]);

    // Check if the file is an image
    $imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));

    if (getimagesize($_FILES["image"]["tmp_name"])) {
        if (move_uploaded_file($_FILES["image"]["tmp_name"], $targetFile)) {
            // Image uploaded successfully
        } else {
            // Handle file upload error
        }
    } else {
        // Error handling for non-image file
    }
}

// Database configuration for patient data
$servername = "localhost";
$username = "admin";
$password = "J03@tech";
$patientDbName = "patient_data";

// Create a connection to the patient data database
$patientconn = new mysqli($servername, $username, $password, $patientDbName);

// Check the connection for patient data
if ($patientconn->connect_error) {
    die("Connection to patient data database failed: " . $patientconn->connect_error);
}

// Database configuration for medication data
$medicationServername = "localhost";
$medicationUsername = "medicals";
$medicationPassword = "J03@tech";
$medicationDbName = "medical_description";

// Create a connection to the medication data database
$medicationConn = new mysqli($medicationServername, $medicationUsername, $medicationPassword, $medicationDbName);

// Check the connection for medication data
if ($medicationConn->connect_error) {
    die("Connection to medication database failed: " . $medicationConn->connect_error);
}

// Retrieve the health issue description from the form
$healthIssue = $_POST['health_issue'];

// Handle the health issue and retrieve prescribed medication
$pythonScript = "python healthAssistance.py \"$healthIssue\"";
$suggestedMedication = exec($pythonScript);

if (!empty($suggestedMedication)) {
    echo "Suggested Medication: " . $suggestedMedication;
} else {
    echo "No suggested medication found.";
}

// Define critical health issues
$criticalHealthIssues = ["Critical Issue 1", "Critical Issue 2", "Critical Issue 3"];

// Check if the health issue is critical
if (in_array($healthIssue, $criticalHealthIssues)) {
    echo "Your health issue is critical. Please visit our health center or call for personal health service personnel immediately.";
} else {
    // Query for medication database based on the provided health issue
    $query = "SELECT prescribed_medication FROM medications WHERE health_issue = ?";
    $stmt = $medicationConn->prepare($query);
    $stmt->bind_param("s", $healthIssue);
    $stmt->execute();
    $stmt->bind_result($prescribedMedication);

    $prescriptions = [];

    while ($stmt->fetch()) {
        $prescriptions[] = $prescribedMedication;
    }

    $stmt->close();
    $medicationConn->close();

    if (empty($prescriptions)) {
        echo "No prescribed medication found. Please consider visiting our main hospital or call for a personal nurse/doctor for treatment.";
    } else {
        echo "Prescribed Medication: " . implode(", ", $prescriptions);
    }
}

// Insert registration data into the patient data database
$registrationDate = $_POST['registration_date'];
$registrationTime = $_POST['registration_time'];
$fullName = $_POST['fullname'];
$id = $_POST['id'];
$dateOfBirth = $_POST['date_of_birth'];
$phoneNumber = $_POST['phone_number'];
$maritalStatus = $_POST['marital_status'];
$gender = $_POST['gender'];
$email = $_POST['email'];
$password1 = $_POST['password1'];
$conPassword = $_POST['conpassword'];
$homeAddress = $_POST['home_address'];
$occupation = $_POST['occupation'];
$isUnder18 = $_POST['okay'] === 'Yes' ? 'Yes' : 'No';
$takingMedication = $_POST['yes-no'] === 'yes' ? 'yes' : 'no';
$nextOfKinsName = $_POST['next_of_kins_name'];
$nextOfKinsNumber = $_POST['next_of_kins_number'];
$healthInsuranceId = $_POST['health_insurance_id'];
$healthInsuranceNumber = $_POST['health_insurance_number'];

//  SQL query for inserting registration data
$sql = "INSERT INTO patient_data (registration_date, registration_time, fullname, id, date_of_birth, phone_number, marital_status, gender, email, password1, conpassword, home_address, occupation, is_under_18, taking_medication, health_issue, next_of_kins_name, next_of_kins_number, health_insurance_id, health_insurance_number, passport_image_path, suggested_medication)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = $patientconn->prepare($sql);
$stmt->bind_param("ssssssssssssssssssssss", $registrationDate, $registrationTime, $fullName, $id, $dateOfBirth, $phoneNumber, $maritalStatus, $gender, $email, $password1, $conPassword, $homeAddress, $occupation, $isUnder18, $takingMedication, $healthIssue, $nextOfKinsName, $nextOfKinsNumber, $healthInsuranceId, $healthInsuranceNumber, $targetFile);

if ($stmt->execute()) {
    echo "Data inserted successfully.";
} else {
    echo "Error: " . $sql . "<br>" . $patientconn->error;
}

$stmt->close();
$patientconn->close();
?>
</body>
</html>







