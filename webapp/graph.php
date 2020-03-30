<?php
define('BOT_USERNAME', '@ESD_Proj_bot'); // place username of your bot here

// var_dump($_COOKIE);

if (isset($_COOKIE['tg_user'])) {
	$user_info = json_decode($_COOKIE['tg_user'], true);
	// print_r($_COOKIE['tg_user']);
	$user_id = $user_info['id'];
	//   echo "USER ID:".$user_info['id'];
}

function getTelegramUserData()
{
	if (isset($_COOKIE['tg_user'])) {
		$auth_data_json = urldecode($_COOKIE['tg_user']);
		$auth_data = json_decode($auth_data_json, true);
		return $auth_data;
	}
	return false;
}

$tg_user = getTelegramUserData();
if ($tg_user !== false) {
	// var_dump($tg_user);
	$first_name = $tg_user['first_name'];

	if (isset($tg_user['last_name'])) {
		$last_name = " " . $tg_user['last_name'];
	} else {
		$last_name = "";
	}

	if (isset($tg_user['photo_url'])) {
		$photo_url = $tg_user['photo_url'];
	}
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--
Design by TEMPLATED
http://templated.co
Released for free under the Creative Commons Attribution License

Name       : Skeleton 
Description: A two-column, fixed-width design with dark color scheme.
Version    : 1.0
Released   : 20130902

-->
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>G5T6 Watchdog Application</title>
	<meta name="keywords" content="" />
	<meta name="description" content="" />

	<link rel="icon" type="image/png" href="images/icons/favicon.ico" />
	<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="src/tables/vendor/bootstrap/css/bootstrap.min.css">
	<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="src/tables/fonts/font-awesome-4.7.0/css/font-awesome.min.css">
	<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="src/tables/vendor/animate/animate.css">
	<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="src/tables/vendor/select2/select2.min.css">
	<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="src/tables/vendor/perfect-scrollbar/perfect-scrollbar.css">
	<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="src/tables/css/util.css">
	<link rel="stylesheet" type="text/css" href="src/tables/css/main.css">

	<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
	<link href="src/default.css" rel="stylesheet" type="text/css" media="all" />
	<link href="src/fonts.css" rel="stylesheet" type="text/css" media="all" />

	<!--[if IE 6]><link href="default_ie6.css" rel="stylesheet" type="text/css" /><![endif]-->

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>

	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
	<script src="../vendor/node_modules/chart.js/Chart.min.js"></script>
	<script src="../vendor/node_modules/angular-chart.js/dist/angular-chart.min.js"></script>
</head>

<body>
	<div id="page" class="container">
		<div id="header">
			<div id="logo">
				<img width="100px" src="<?= $photo_url ?>" alt="" />
				<h1 style="color:#6c7ae0"><?= $first_name ?></a></h1>
				<span>Welcome!</span>
			</div>
			<div id="menu">
				<ul>
					<li class="current_page_item"><a href="homepage.php" accesskey="1" title="">Homepage</a></li>
					<li><a href="add-endpoint.php" accesskey="2" title="">Add Endpoint</a></li>
					<li><a href="logout.php" accesskey="3" title="">Log Out</a></li>
				</ul>
			</div>
		</div>
		<div id="main">
			<div id="welcome">
				<div class="title">
					<h2>G5T6 Watchdog Application</h2>
					<span class="byline">Monitor your websites with ease</span>
				</div>
				<p>View your of list websites <strong>below!</strong></p>
			</div>
			<div id="featured">
				<div class="title">
					<h2>Monitoring</h2>
				</div>

				<p id="main-container"></p>

				<div class="limiter">
					<div class="container-table100">
						<div class="wrap-table100">
							<div class="table100 ver1 m-b-110">
								<div class="table100-head">
									<table align="center">
										<thead>
											<tr class="row100 head">
												<th class="cell100 t1column2">Website</th>
												<th class="cell100 t1column6">Graph</th>
												<th class="cell100 t1column7">Status</th>
											</tr>
										</thead>
									</table>
								</div>
								<div class="table100-body js-pscroll">
									<table id="displaytable">
										<tbody>
											<td class="cell100 t1column2">Website</td>
											<td class="cell100 t1column4">#</td>
											<td class="cell100 t1column5">4 hours ago</td>
											<!-- <td class="cell100 t1column6"><input id='graphBtn' class='btn btn-primary' style='font-size:12px;' type='button' value='Graph'></td>
											<td class="cell100 t1column7"><input id='editBtn' class='btn btn-primary' style='font-size:12px;' type='button' value='Edit'><input id='deleteBtn' style='font-size:12px;' class='btn btn-primary' type='button' value='Delete'> -->
											</td>
										</tbody>
									</table>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div id="copyright">
				<span>&copy; Untitled. All rights reserved. | Application By G5T6'2020</span>
				<span>Design by <a href="http://templated.co" rel="nofollow">TEMPLATED</a>.</span>
			</div>
		</div>
	</div>


	<script>
		// Helper function to display error message
		function showError(message) {
			// Hide the table and button in the event of error
			// $('#endpointTable').hide();

			// Display an error under the main container
			$('#main-container')
				.append("<label>" + message + "</label>");
		}

		// anonymous async function 
		// - using await requires the function that calls it to be async
		$(async () => {

			var userid = '<?php echo $user_id; ?>';
			// Change serviceURL to your own
			var serviceURL = "http://esdwatchdog:5000/account/" + userid;

			try {
				const response =
					await fetch(
						serviceURL, {
							method: 'GET'
						}
					);
				const data = await response.json();
				var status = data.status;

				if (status == 400) {
					showError(data.message);
				} else {
					var endpoints = data.result;
					// for loop to setup all table rows with obtained book data
					var rows = "";
					var index = 1;
					for (const endpoint of endpoints) {
						eachRow =
							"<td>" + endpoint.url + "</td>" +
							"<td>" + endpoint.timestamp + "</td>" +
							"<td>NOTHING FOR NOW</td>";

						rows += "<tr>" + eachRow + "</tr>";
					}
					// add all the rows to the table
					$('#displayTable tbody').append(rows);
				}
			} catch (error) {
				// Errors when calling the service; such as network error, 
				// service offline, etc
				showError
					('There is a problem retrieving data, please try again later.<br />');

			} // error
		});

	</script>
</body>

</html>