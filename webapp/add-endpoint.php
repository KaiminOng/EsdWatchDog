<?php

include "config.php";

define('BOT_USERNAME', $bot_username); // place username of your bot here

if (isset($_COOKIE['tg_user'])) {
	$user_info = json_decode($_COOKIE['tg_user'], true);
	$user_id = $user_info['id'];
	$first_name = $user_info['first_name'];
	$photo_url = isset($user_info['photo_url']) ? $user_info['photo_url'] : false;
}
// $hostname = "http://esdwatchdog.me:5001";
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
	<link href="src/checkbox.css" rel="stylesheet" type="text/css" media="all" />

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
				<h1 style="color:#2980b9"><?= $first_name ?></a></h1>
				<span>Welcome!</span>
			</div>
			<div id="menu">
				<ul>
					<li><a href="homepage.php" accesskey="1" title="">Homepage</a></li>
					<li class="current_page_item"><a href="add-endpoint.php" accesskey="2" title="">Add Endpoint</a></li>
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
				<p>Add a <strong>NEW</strong> website to monitor <strong>below</strong>!</p>
			</div>
			<div id="featured">
				<div class="title">
					<h3>New Website To Monitor!</h3>
				</div>
				<p>Note: If you wish to monitor the new website in a <strong>chat group, </strong></p>
				<p>
					Do remember to first add our bot<strong>@ESD_Telegram_Proj</strong> into the chat group!
				</p>
				<p>*Selection of <strong>multiple chats</strong> is possible</p>
				<p id="main-container"></p>

				<div class="limiter">
					<div class="container-table100">
						<div class="wrap-table100">
							<div class="table100 ver2 m-b-110">
								<form id='addEndpoint' name='addEndpoint'>
									<div class="table100-head">
										<table align="center">
											<thead>
												<tr class="row100 head">
													<th class="cell100 t2column1" style="width:15em">Website</th>
												</tr>
											</thead>
										</table>
									</div>

									<div class="table100-body js-pscroll">
										<table align="center" id='creationtable'>
											<tbody>
												<tr>
													<td class='cell100 t2column1'><input name='endpoint' type='text' id='endpoint' placeholder='Input Website URL'></td>
												</tr>
												<tr>
													<th class="cell100 t2column1" style="width:12em">Available Chat Groups</th>
												</tr>

											</tbody>
										</table>
									</div>
								</form>
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
		function showError(message) {
			// Hide the table and button in the event of error
			// $('#endpointTable').hide();

			// Display an error under the main container
			$('#main-container')
				.append("<label>" + message + "</label>");
		}

		function getCheckedValues() {
			var length = document.addEndpoint.chats.length;
			var chats_selected = [];
			$.each($("input[name='chats']:checked"), function(){
				chats_selected.push($(this).val());
			});

			return chats_selected;
		}

		// anonymous async function 

		$(async () => {
			var hostname_get = '<?php echo $hostname; ?>';

			var userid = '<?php echo $user_id; ?>';
			// Change serviceURL to your own
			var serviceURL = hostname_get + "/contact/get/" + userid;
			// var serviceURL = "http://esdwatchdog.com:5001/contact/get/" + userid;

			try {
				const response =
					await fetch(
						serviceURL, {
							method: 'GET',
						});

				const data = await response.json();
				var status = data.status;

				if (status != "success") {
					showError(data.message);
				} else {
					var contacts = data.result;
					// for loop to setup all table rows with obtained contacts data
					var row = "<tr class='row100 body'>" +
							"<td class='cell100 t2column2' style='text-align:left'>";

					for (const c of contacts) {
						row += "<label class='checkboxcontainer'>" + c.chat_title + "<input type='checkbox' name='chats' value='" + c.chat_id + "'><span class='checkmark'></span></label>";
						
					}

					row += "</td></tr>" +
						"<tr class='row100 body'><td class='cell100 t2column1'><input id='addBtn' class='btn btn-primary' type='submit' style='font-size:13px' value='Add'></td></tr>";


					// add all the rows to the table
					$('#creationtable tbody').append(row);
				}
			} catch (error) {
				// Errors when calling the service; such as network error, 
				// service offline, etc
				showError
					('There is a problem retrieving data, please try again later.<br />');

			} // error


			$('#addEndpoint')[0].addEventListener("submit", async (event) => {

				event.preventDefault();

				var userid = '<?php echo $user_id; ?>';

				var endpoint = $('#endpoint').val();
				// GET SELECTED CHAT GROUP'S CHAT ID
				var chats = getCheckedValues();

				// Change serviceURL to your own
				var serviceURL = hostname_get + "/watchlist/new";

				try {
					const response =
						await fetch(
							serviceURL, {
								method: 'POST',
								headers: {
									"Content-Type": "application/json"
								},
								body: JSON.stringify({
									id: userid,
									endpoint: endpoint,
									chat_id: chats
								})
							});

					const data = await response.json();
					// console.log(data);
					if (status != "success") {
						var message = "Error in input, please try again.";
						window.location.replace("homepage.php?status=error&message=" + message);
					} else {
						var message = "Endpoint successfully added."
						window.location.replace("homepage.php?status=success&message=" + message);
					}

				} catch (error) {
					// Errors when calling the service; such as network error, 
					// service offline, etc
					var message = "Error connecting to the service, please try again later.";
					window.location.replace("homepage.php?status=error&message=" + message);

				} // error

			});
			return false;
		});

		

	</script>
	<!-- 
	<script type="text/javascript">

	var checkList = document.getElementById('list1');
	checkList.getElementsByClassName('anchor')[0].onclick = function (evt) {
		if (checkList.classList.contains('visible'))
			checkList.classList.remove('visible');
		else
			checkList.classList.add('visible');
	}

	checkList.onblur = function(evt) {
		checkList.classList.remove('visible');
	}
	</script> -->
</body>

</html>