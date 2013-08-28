<!doctype html>
<html lang="fi">
<head>
<meta charset="utf-8"/>
<title>Mail</title>
<style>
label {font-weight: bold;}
</style>
</head>
<body>
<h1>Sähköpostihaku</h1>
<p>Etsii CSV-muodossa syötetyistä sähköpostin virheilmoituksista vastaanottajien osoitteet, ja kertoo, mistä koulusta he ovat.</p>

<h2>Tiedostot</h2>
<p>Tiedostojen tulee olla CSV-muotoisia.</p>

<form method="post" action="" enctype="multipart/form-data">
<p><label for="schools">Koulut:</label> <input type="file" name="schools" id="schools"/> (CSV, 3 saraketta puolipisteellä eroteltuna: id;koulun nimi;sähköposti)</p>
<p><label for="errors">Virheilmoitukset:</label> <input type="file" name="errors" id="errors"/> (CSV, ainakin kaksi saraketta, pilkulla eroteltuna, sarakkeet lainausmerkeissä ("), "Aihe","Leipäteksti")</p>

<p><input type="submit" value="Tarkista"/></p>
</form>
<hr/>
<h2>Tulokset</h2>
<?php
error_reporting(E_ALL);

$upload_dir = '../data';

if (isset($_FILES['schools']) && isset($_FILES['errors'])) {
	$schools = $_FILES['schools']['tmp_name'];
	$errors = $_FILES['errors']['tmp_name'];

	move_uploaded_file($schools, $upload_dir . $schools);
	move_uploaded_file($errors, $upload_dir . $errors);

$cmd = '../collect_errors.py -s ' . $upload_dir . $schools . ' -e ' . $upload_dir . $errors;

$output = shell_exec($cmd);
echo '<!-- Command: ' . $cmd . ' -->' . chr(10);
echo '<pre>' . $output . '</pre>' . chr(10);
}
?>
<hr/>
<p>&copy; 2013 Ylioppilastutkintolautakunta / Ville Korhonen</p>
</body>
</html>
