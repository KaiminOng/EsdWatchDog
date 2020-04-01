<?php
define('BOT_USERNAME', '@ESD_Proj_bot'); // place username of your bot here

if (isset($_COOKIE['tg_user'])) {
	$user_info = json_decode($_COOKIE['tg_user'], true);
	$user_id = $user_info['id'];
	$first_name = $user_info['first_name'];
	$photo_url = isset($user_info['photo_url']) ? $user_info['photo_url'] : false;
}

$hostname = "http://watchlist:5001";

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
	
</head>

<body>
	<div id="page" class="container">
		<div id="header">
			<div id="logo">
				<img width="100px" src="<?php echo $photo_url ? $photo_url : 'img/default_icon.png' ?>" alt="" />
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

				<?php 
				if(isset($_GET['status'])){
					$status = $_GET['status'];
					$message = $_GET['message'];

					if ($status === 'success'){
						echo "<ul class='list-group text-center font-weight-bold'>
						<li class='list-group-item list-group-item-success'>{$message}</li>
						</ul>";
					} else{
						echo "<ul class='list-group text-center font-weight-bold'>
						<li class='list-group-item list-group-item-danger'>{$message}</li>
						</ul>";
					}
				}
				?>
				<div class="limiter">
					<div class="container-table100">
						<div class="wrap-table100">
							<div class="table100 ver1 m-b-110">
								<div class="table100-head">
									<table>
										<thead>
											<tr class="row100 head">
												<th class="cell100 t1column1">Index</th>
												<th class="cell100 t1column2">Website</th>
												<th class="cell100 t1column3">Linked Chat</th>
												<th class="cell100 t1column4">Status</th>
												<th class="cell100 t1column5">Last Updated</th>
												<!-- <th class="cell100 t1column6">Graph</th> -->
												<th class="cell100 t1column7"></th>
											</tr>
										</thead>
									</table>
								</div>
								<div class="table100-body js-pscroll">
									<table id="displaytable">
										<tbody>
											
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
		const x = async () => {
			window.history.replaceState({}, document.title, "/webapp/homepage.php");
			var userid = '<?php echo $user_id; ?>';
			var hostname = '<?php echo $hostname; ?>';
			var serviceURL = hostname + ":5001/watchlist/get/" + userid;

			var ts = Math.round((new Date()).getTime() / 1000);
			// var test = Math.round((new Date()).getTime() / 1000) - 3598;
			while (true){
				try {
					const response =
					await fetch(
						serviceURL, {
						method: 'GET',
					});
					
					const data = await response.json();
					var status = data.status;
					console.log(data)

					if (status != "success") {
						showError(data.message);
					} else {
						var result = data.result;
						// for loop to setup all table rows with obtained book data
						var rows = "";
						var index = 1;
						for (var r of result) {
							var eachRow =
								"<td class='cell100 t1column1'>" + index + "</td>" +
								"<td class='cell100 t1column2'>" + r.endpoint + "</td>" +
								"<td class='cell100 t1column3'><ol>";
							for (var c of r.contacts){
								eachRow += "<li>" + c.chat_title + "</li>";
							}
							
							if (r.status === 'healthy') {
								var health = "<button class='btn btn-outline-success' style='font-size:12px'>Healthy</button>";
							} else if (r.status === 'unhealthy') {
								var health = "<button class='btn btn-outline-danger' style='font-size:12px'>Unhealthy</button>";
							} else{
								var health = "<button class='btn btn-outline-warning' style='font-size:12px'>Pending</button>";
							}
							
							if (r.last_checked === null){
								var timestamp = "<button class='btn btn-outline-warning' style='font-size:12px'>Pending</button>";
							} else{
								var last_checked = ts - r.last_checked;
								var hours = Math.floor(last_checked / 60 / 60);
								var minutes = Math.floor(last_checked / 60) - (hours * 60);
								var seconds = last_checked % 60;
								var timestamp = "<button class='btn btn-outline-info' style='font-size:12px'>" + hours + "h " + minutes + "m " + seconds + "s ago</button>";
							}
							

							eachRow += "</ol></td>" +
								"<td class='cell100 t1column4'>" + health + "</td>" +
								"<td class='cell100 t1column5'>" + timestamp + "</td>" +
								// "<td class='cell100 t1column6'><button type='button' class='btn btn-primary' href='graph.php?endpoint=" + r.endpoint + "&lastchecked=" + r.last_checked + "&events=" + r.events + "'>Graph</button></td>" +
								"<td class='cell100 t1column7'>" + 
								// "<button class='btn btn-primary' style='font-size:10px' id='updateBtn' >Update</button>" +
								// "<form method='GET' action='update.php'>" + "<input type='hidden' name='endpoint' value=" + r.endpoint + ">" +
								// "<input type='hidden' name='contacts[]' value=" + r.contacts + ">" +
								"<button id='updateBtn' type='submit' class='btn btn-primary' style='font-size:10px;'>Update</button>" +
								
								"<button id='deleteBtn' class='btn btn-danger' style='font-size:10px; margin:2px' data-dest='delete.php?endpoint=" + r.endpoint + "'>Delete</button></td>";

							rows += "<tr>" + eachRow + "</tr>";
							index += 1;
						}
						// add all the rows to the table
						$('#displaytable tbody').html(rows);

					}
				} catch (error) {
					// Errors when calling the service; such as network error, 
					// service offline, etc
					console.log(error)
					showError
						('There is a problem retrieving data, please try again later.<br />');
				} // error

				await new Promise(k=> setTimeout(k, 5000));
			}
		};

		x();



		

		// function updateURL(endpoint){
		// 	"<%Session['endpoint'] = " + endpoint + "; %>";
		// 	window.location.replace("update.php");
		// }

		// $('#updateBtn').click(async (event) => {

		// 	location.href = "update.php"
		// 	var userid = '<?php echo $user_id; ?>';

		// 	var endpoint = $('#endpoint').val();
		// 	// GET SELECTED CHAT GROUP'S CHAT ID
		// 	// var chatgroup = $('#chatgroup').val(); ???

		// 	// Change serviceURL to your own
		// 	var serviceURL = "http://esdwatchdog:5000/endpoint/edit";

		// 	try {
		// 		const response =
		// 			await fetch(
		// 				serviceURL, {
		// 					method: 'POST',
		// 					headers: {
		// 						"Content-Type": "application/json"
		// 					},
		// 					body: JSON.stringify({
		// 						userID: userid,
		// 						endpoint: endpoint,
		// 						chatID: chatid
		// 					})
		// 				});

		// 		const data = await response.json();
		// 		// console.log(data);
		// 		if (data[1] === 400) {
		// 			document.getElementById("message").innerHTML = data[0].message
		// 		} else if (data[1] === 201) {
		// 			document.getElementById("message").innerHTML = title + " has been succesfully added."
		// 		}

		// 	} catch (error) {
		// 		// Errors when calling the service; such as network error, 
		// 		// service offline, etc
		// 		showError
		// 			('There is a problem editing the endpoint, please try again later.<br />' + error);

		// 	} // error
		// });

		$('#deleteBtn').click(function() {
			var resp = confirm('Are you sure you want to stop monitoring this website?');
			if (resp == true) {
				// delete url if press ok
				var dest = $('#deleteBtn').data('dest');
				$("#deleteBtn").attr("href", dest);
			}
			else{
				return false;
			}
		});

	</script>
</body>

</html>